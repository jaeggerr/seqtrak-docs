#!/usr/bin/env python3
"""Installe un .Y3S multi-echantillons : N samples lies a N keybanks.

Deux differences avec content_push.py, toutes deux a verifier sur le fil :
  - l'en-tete declare le nombre de samples et la taille totale ;
  - chaque flux de sample est prefixe de deux octets ; l'hypothese ici est que
    ce sont le numero de keybank (ils valaient 00 00 pour l'unique keybank).
01 10 01 remis a 0 dans un finally.
"""
import sys, time, zipfile, struct, uuid, rtmidi

Y3S = sys.argv[1]
SOUND_CN = int(sys.argv[2]) if len(sys.argv) > 2 else 4103
WAVE_CN  = int(sys.argv[3]) if len(sys.argv) > 3 else 8598

out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i, n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i, n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)
MODE = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C, 0x01, 0x10, 0x01]

def flush():
    while inp.get_message(): pass
def cks(b):
    s = sum(b[7:len(b)-2]) & 0x7F
    return 0 if s == 0 else (0x80 - s) & 0x7F
def b4(v): return [(v>>21)&0x7F, (v>>14)&0x7F, (v>>7)&0x7F, v&0x7F]
def b2(v): return [(v>>7)&0x7F, v&0x7F]
def addr(n): return ((n>>7)&0x7F, n&0x7F)
def pack7(raw):
    o = bytearray()
    for i in range(0, len(raw), 7):
        g = raw[i:i+7]; h = 0
        for k, b in enumerate(g):
            if b & 0x80: h |= 1 << (6-k)
        o.append(h); o.extend(x & 0x7F for x in g)
    return bytes(o)
def send(ah, num, body):
    am, al = addr(num)
    cnt = 1 + 3 + len(body)
    m = [0xF0,0x43,0x00,0x7F,0x1C,(cnt>>7)&0x7F,cnt&0x7F,0x0C,ah,am,al]+list(body)+[0,0xF7]
    m[-2] = cks(m); out.send_message(m)
def ack(timeout=8.0):
    t0 = time.time()
    while time.time()-t0 < timeout:
        m = inp.get_message()
        if m:
            d = list(m[0])
            if d and d[0] == 0xF0 and len(d) >= 17 and d[8] == 0x01 and d[9] in (0x20,0x21,0x22):
                return d
        else: time.sleep(0.0005)
    return None
def step(label, ah, num, body):
    send(ah, num, body)
    a = ack()
    if a is None: raise SystemExit("  %-22s -> AUCUN acquittement" % label)
    print("  %-22s -> ack 01 %02X 00 result=%d" % (label, a[9], a[11]))
    if a[11] != 0: raise SystemExit("    refus, arret")
    return a

z = zipfile.ZipFile(Y3S); root = z.namelist()[0].split('/')[0]
names = z.namelist()
nsmp = len([n for n in names if n.endswith('.bin') and '/sample' in n])
pcms = [z.read('%s/sample%d.bin' % (root, i)) for i in range(nsmp)]
rec  = z.read(root + '/waveform0.bin')
snd  = bytearray(z.read(root + '/sound.bin'))
struct.pack_into('<H', snd, 0x1E8, WAVE_CN - 8192)
snd = bytes(snd)
su, wu = uuid.uuid4().bytes, uuid.uuid4().bytes
kb = struct.unpack_from('<I', rec, 0)[0]
print("source : %s" % Y3S)
print("  %d keybanks, %d samples, %d o. de PCM, record %d o., sound.bin %d o."
      % (kb, nsmp, sum(len(p) for p in pcms), len(rec), len(snd)))
for i in range(kb):
    o = 4 + 64*i
    print("    kb%d touches %3d-%3d note %3d loop=%02X depart %d n %d"
          % (i, rec[o], rec[o+1], rec[o+8], rec[o+0x0F],
             struct.unpack_from('<I', rec, o+0x2C)[0]*16,
             struct.unpack_from('<I', rec, o+0x3C)[0]))
assert kb == nsmp, "un sample par keybank attendu"

try:
    out.send_message(MODE + [0x01, 0xF7]); time.sleep(0.4); flush()
    blob = b''.join(pcms)
    hdr = [0,1,0,0, 0,0, 0,0] + b2(1) + b4(1) + b4(len(blob))
    step("en-tete blob", 0x03, SOUND_CN, hdr)
    stream = bytes(b2(0)) + pack7(blob)
    pk = [stream[i:i+3000] for i in range(0, len(stream), 3000)]
    print("  blob de %d o. : %d paquets" % (len(blob), len(pk)))
    for i, enc in enumerate(pk):
        body = b2(len(pk)) + b2(i) + list(enc)
        send(0x0A, WAVE_CN, body)
        a = ack()
        if a is None or a[11] != 0:
            raise SystemExit("  paquet %d/%d -> %s"
                             % (i, len(pk), "aucun ack" if a is None else "result=%d" % a[11]))
        if i % 40 == 0 or i == len(pk)-1: print("    paquet %d/%d ok" % (i, len(pk)))
    body = [0,1,0,0]+list(pack7(wu))[:19]+[0,0,0,0]+[0]*50+[0]*50+[3,1,0]+list(pack7(rec))
    step("corps waveform (09)", 0x09, WAVE_CN, body)
    body = [0,1,0,0]+list(pack7(su))[:19]+[0,0,0,0]+[0]*50+[0]*50+[0,1]+list(pack7(snd))
    step("corps son (07)", 0x07, SOUND_CN, body)
    print("\ntransfert complet accepte")
finally:
    out.send_message(MODE + [0x00, 0xF7]); time.sleep(0.3)
    print("mode gestion de contenu remis a 0")
