"""Assemble five zones as live elements on SYNTH 2 (part 8).

Writes Element Assign, Wave Select/Number, Note Limit and the envelope of
elements 0 to 4, then reads everything back. SYNTH 1 is the witness and the
tempo the control. Nothing is persisted: loading a sound wipes it all."""
import time, rtmidi
PART=8; CH=8
ZONES=[(432,0,41,36),(433,42,53,48),(434,54,65,60),(435,66,77,72),(436,78,127,84)]
ENV={0x33:0, 0x37:0, 0x3B:116, 0x39:127, 0x3A:119}
out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i,n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i,n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)
def unpack7(d):
    o=bytearray()
    for i in range(0,len(d),8):
        g=d[i:i+8]
        if not g: break
        h=g[0]
        for k,v in enumerate(g[1:]): o.append(v|(((h>>(6-k))&1)<<7))
    return bytes(o)
def req(aa,n=4,wait=1.2):
    pre=[0xF0,0x43,0x10,0x7F,0x1C,0x0C]+aa
    for _ in range(n):
        while inp.get_message(): pass
        out.send_message([0xF0,0x43,0x30,0x7F,0x1C,0x0C]+aa+[0xF7])
        t0=time.time()
        while time.time()-t0<wait:
            m=inp.get_message()
            if m:
                d=list(m[0])
                if d[:9]==pre: return d[9:-1]
                if d[0]==0xF0 and d[1]==0x43 and (d[2]&0xF0)==0x00 and d[8:11]==aa: return d[11:-2]
            else: time.sleep(0.002)
        time.sleep(0.04)
    return None
def w(aa, *vals):
    out.send_message([0xF0,0x43,0x10,0x7F,0x1C,0x0C]+aa+list(vals)+[0xF7]); time.sleep(0.05)
def name(p=PART):
    v=req([0x01,0x10|p,0x35])
    return unpack7(bytes(v)).split(b'\0')[0].decode('utf8','replace') if v and len(v)>8 else None
def load(prog):
    out.send_message([0xB0|CH,0x00,63]); time.sleep(0.03)
    out.send_message([0xB0|CH,0x20,32]); time.sleep(0.03)
    out.send_message([0xC0|CH,prog]);    time.sleep(0.8)
load(31)
print('SYNTH 2:', name(), '| witness SYNTH 1:', name(7))
for e,(wave,lo,hi,root) in enumerate(ZONES):
    m = (e<<4) | PART
    w([0x41,m,0x00], 1)                                  # Element Assign
    w([0x41,m,0x01], 1)                                  # Wave Select: user wave
    w([0x41,m,0x03], (wave>>7)&0x7F, wave&0x7F)          # Wave Number
    w([0x41,m,0x10], lo); w([0x41,m,0x11], hi)           # Note Limit
    w([0x41,m,0x12], 1);  w([0x41,m,0x13], 127)          # Velocity Limit
    w([0x41,m,0x2E], 100)                                # Element Level
    for off,v in ENV.items(): w([0x41,m,off], v)
print('\nread back:')
for e,(wave,lo,hi,root) in enumerate(ZONES):
    m=(e<<4)|PART
    wn=req([0x41,m,0x03]); got = (wn[0]<<7|wn[1]) if wn and len(wn)==2 else None
    print('  el%d  assign=%s select=%s wave=%s (want %d)  notes %s-%s (want %d-%d)  3B=%s'
          % (e, req([0x41,m,0x00]), req([0x41,m,0x01]), got, wave,
             req([0x41,m,0x10]), req([0x41,m,0x11]), lo, hi, req([0x41,m,0x3B])))
print('\nwitness SYNTH 1 el0 wave:', req([0x41,0x07,0x03]), '| tempo:', req([0x30,0x40,0x76]))
