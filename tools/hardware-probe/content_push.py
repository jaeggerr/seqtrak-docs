#!/usr/bin/env python3
"""Installe un .Y3S sur le SEQTRAK par le canal de contenu, comme l'app officielle.

Chaine observee sur le fil : en-tete kind 03 (SON) -> paquets de sample (0A)
-> corps de la waveform (09) -> corps du son (07). Chaque message attendu.
01 10 01 remis a 0 dans un finally.
"""
import sys, time, zipfile, struct, uuid, rtmidi

Y3S = sys.argv[1] if len(sys.argv) > 1 else 'sound.Y3S'
SOUND_CN = 4103          # numeros libres ; la machine reattribue de toute facon
WAVE_CN  = 8598

out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i,n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i,n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)
MODE=[0xF0,0x43,0x10,0x7F,0x1C,0x0C,0x01,0x10,0x01]

def flush():
    while inp.get_message(): pass
def cks(b):
    s=sum(b[7:len(b)-2])&0x7F
    return 0 if s==0 else (0x80-s)&0x7F
def b4(v): return [(v>>21)&0x7F,(v>>14)&0x7F,(v>>7)&0x7F,v&0x7F]
def addr(n): return ((n>>7)&0x7F, n&0x7F)   # PAS de |0x40 : l'app envoie 03 20 07 pour 4103
def pack7(raw):
    o=bytearray()
    for i in range(0,len(raw),7):
        g=raw[i:i+7]; h=0
        for k,b in enumerate(g):
            if b & 0x80: h |= 1<<(6-k)
        o.append(h); o.extend(x & 0x7F for x in g)
    return bytes(o)
def send(ah, num, body):
    am,al = addr(num)
    cnt = 1+3+len(body)
    m=[0xF0,0x43,0x00,0x7F,0x1C,(cnt>>7)&0x7F,cnt&0x7F,0x0C,ah,am,al]+list(body)+[0,0xF7]
    m[-2]=cks(m); out.send_message(m); return m
def ack(timeout=8.0):
    t0=time.time()
    while time.time()-t0<timeout:
        m=inp.get_message()
        if m:
            d=list(m[0])
            if d and d[0]==0xF0 and len(d)>=17 and d[8]==0x01 and d[9] in (0x20,0x21,0x22):
                return d
        else: time.sleep(0.0005)
    return None
def step(label, ah, num, body):
    send(ah, num, body)
    a=ack()
    if a is None: raise SystemExit("  %-22s -> AUCUN acquittement" % label)
    res=a[11]
    extra=" assigne=%d" % ((a[16]<<7)|a[17]) if len(a)>17 and (a[16] or a[17]) else ""
    print("  %-22s -> ack 01 %02X 00 result=%d%s" % (label, a[9], res, extra))
    if res!=0: raise SystemExit("    refus, arret")
    return a

z=zipfile.ZipFile(Y3S); root=z.namelist()[0].split('/')[0]
pcm=z.read(root+'/sample0.bin'); rec=z.read(root+'/waveform0.bin'); snd=bytearray(z.read(root+'/sound.bin'))
struct.pack_into('<H', snd, 0x1E8, WAVE_CN-8192)        # coherence du pointeur de wave
snd=bytes(snd)
su=uuid.uuid4().bytes; wu=uuid.uuid4().bytes
print("source : %s" % Y3S)
print("  pcm %d o., record %d o., sound.bin %d o." % (len(pcm), len(rec), len(snd)))
print("  loop=%02X start=%d n=%d" % (rec[4+0x0F], struct.unpack_from('<I',rec,4+0x2C)[0], struct.unpack_from('<I',rec,4+0x3C)[0]))

try:
    out.send_message(MODE+[0x01,0xF7]); time.sleep(0.4); flush()
    # 1. en-tete : kind 03 (SON). Le type envoye est exclu de son propre compte.
    sz=len(pcm)
    hdr=[0,1,0,0] + [0,0] + [0,0] + b4(1)[2:] + b4(1) + b4(sz)
    hdr=[0,1,0,0, 0,0, 0,0, 0,1] + b4(1) + b4(sz)   # sound=0, element=0, waveform=1, sample=1
    step("en-tete kind 03", 0x03, SOUND_CN, hdr)
    # 2. les samples, adresses sur la WAVEFORM
    stream=b'\x00\x00'+pack7(pcm)
    pk=[stream[i:i+3000] for i in range(0,len(stream),3000)]
    print("  %d paquets de sample" % len(pk))
    for i,enc in enumerate(pk):
        body=[(len(pk)>>7)&0x7F,len(pk)&0x7F,(i>>7)&0x7F,i&0x7F]+list(enc)
        send(0x0A, WAVE_CN, body)
        a=ack()
        if a is None or a[11]!=0: raise SystemExit("  paquet %d -> %s" % (i,"aucun ack" if a is None else "result=%d"%a[11]))
        if i%20==0 or i==len(pk)-1: print("    paquet %d/%d ok" % (i,len(pk)))
    # 3. corps de la waveform : UUID, order, 2 chaines de 50, 3 octets, le fichier
    body=[0,1,0,0]+list(pack7(wu))[:19]+[0,0,0,0]+[0]*50+[0]*50+[3,1,0]+list(pack7(rec))
    step("corps waveform (09)", 0x09, WAVE_CN, body)
    # 4. corps du son : idem mais 2 octets de queue (Commercial, Favorite)
    body=[0,1,0,0]+list(pack7(su))[:19]+[0,0,0,0]+[0]*50+[0]*50+[0,1]+list(pack7(snd))
    step("corps son (07)", 0x07, SOUND_CN, body)
    print("\ntransfert complet accepte")
finally:
    out.send_message(MODE+[0x00,0xF7]); time.sleep(0.3)
    print("mode gestion de contenu remis a 0")
