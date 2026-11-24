#!/usr/bin/env python3
"""Push a multi-keybank .Y3S with a CORRECTLY SIZED header.

docs/08-bulk-and-files.md, "The header's payload", already said it and it was
missed: the header carries ONE 4-BYTE ENTRY PER SAMPLE from offset 0x19, and a
stereo import's header carried two. Declaring a count of n with a single size
entry is a malformed message, which is what result 127 was answering.

    0x0B  4      00 01 00 00
    0x0F  2      sound count    (0 when the kind sent is Sound)
    0x11  2      element count  (0)
    0x13  2      waveform count (1)
    0x15  4      sample count   n
    0x19  4 x n  each sample's byte size
"""
import sys, time, zipfile, struct, uuid, rtmidi

Y3S = sys.argv[1]
SOUND_CN = int(sys.argv[2]) if len(sys.argv) > 2 else 4103
WAVE_CN = int(sys.argv[3]) if len(sys.argv) > 3 else 8598

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
def pack7(raw):
    o = bytearray()
    for i in range(0, len(raw), 7):
        g = raw[i:i+7]; h = 0
        for k, b in enumerate(g):
            if b & 0x80: h |= 1 << (6-k)
        o.append(h); o.extend(x & 0x7F for x in g)
    return bytes(o)
def send(ah, num, body):
    cnt = 1 + 3 + len(body)
    m = ([0xF0,0x43,0x00,0x7F,0x1C,(cnt>>7)&0x7F,cnt&0x7F,0x0C,ah,
          (num>>7)&0x7F, num&0x7F] + list(body) + [0, 0xF7])
    m[-2] = cks(m); out.send_message(m)
def ack(timeout=10.0):
    t0 = time.time()
    while time.time()-t0 < timeout:
        m = inp.get_message()
        if m:
            d = list(m[0])
            if (d and d[0] == 0xF0 and len(d) >= 17 and d[8] == 0x01
                    and d[9] in (0x20, 0x21, 0x22)):
                return d
        else: time.sleep(0.0005)
    return None
def step(label, ah, num, body):
    send(ah, num, body); a = ack()
    if a is None: raise SystemExit("  %-24s -> NO acknowledgement" % label)
    print("  %-24s -> ack 01 %02X 00 result=%d" % (label, a[9], a[11]))
    if a[11] != 0: raise SystemExit("    refused, stopping")
    return a

z = zipfile.ZipFile(Y3S); root = z.namelist()[0].split('/')[0]
nsmp = len([n for n in z.namelist() if '/sample' in n and n.endswith('.bin')])
pcms = [z.read('%s/sample%d.bin' % (root, i)) for i in range(nsmp)]
rec = z.read(root + '/waveform0.bin')
snd = bytearray(z.read(root + '/sound.bin'))
struct.pack_into('<H', snd, 0x1E8, WAVE_CN - 8192); snd = bytes(snd)
su, wu = uuid.uuid4().bytes, uuid.uuid4().bytes
kb = struct.unpack_from('<I', rec, 0)[0]
print("source: %s\n  %d keybanks, %d samples, %d B of PCM"
      % (Y3S, kb, nsmp, sum(len(p) for p in pcms)))
assert kb == nsmp

try:
    out.send_message(MODE + [0x01, 0xF7]); time.sleep(0.4); flush()
    hdr = [0,1,0,0] + b2(0) + b2(0) + b2(1) + b4(nsmp)
    for p in pcms:
        hdr += b4(len(p))                       # one entry per sample
    print("  header: %d bytes of payload, Yamaha count %d" % (len(hdr), 0x12 + 4*nsmp))
    step("kind 03 header", 0x03, SOUND_CN, hdr)
    for si, pcm in enumerate(pcms):
        stream = bytes(b2(si)) + pack7(pcm)
        pk = [stream[k:k+3000] for k in range(0, len(stream), 3000)]
        for i, enc in enumerate(pk):
            send(0x0A, WAVE_CN, b2(len(pk)) + b2(i) + list(enc))
            a = ack()
            if a is None or a[11] != 0:
                raise SystemExit("  stream %d packet %d/%d -> %s"
                                 % (si, i, len(pk), "no ack" if a is None
                                    else "result=%d" % a[11]))
        print("  stream %d (kb%d): %d packets accepted" % (si, si, len(pk)))
    body = ([0,1,0,0] + list(pack7(wu))[:19] + [0,0,0,0] + [0]*50 + [0]*50
            + [3,1,0] + list(pack7(rec)))
    step("waveform body (09)", 0x09, WAVE_CN, body)
    body = ([0,1,0,0] + list(pack7(su))[:19] + [0,0,0,0] + [0]*50 + [0]*50
            + [0,1] + list(pack7(snd)))
    step("sound body (07)", 0x07, SOUND_CN, body)
    print("\nwhole transfer accepted")
finally:
    out.send_message(MODE + [0x00, 0xF7]); time.sleep(0.3)
    print("ContentsManagementMode restored to 0")
