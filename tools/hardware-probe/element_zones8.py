"""Huit zones tous les 3 demi-tons sur la partie 8, elements 0 a 7.
Ecrit tout ce qu'un element frais ne porte pas, 41 ep 54 compris."""
import time, rtmidi
PART=8; CH=8; PROG0=36
# (onde, note basse, note haute, note de reference)
Z=[(437,  0, 49, 48), (438, 50, 52, 51), (439, 53, 55, 54), (440, 56, 58, 57),
   (441, 59, 61, 60), (442, 62, 64, 63), (443, 65, 67, 66), (444, 68,127, 69)]
SET={0x00:1, 0x01:1, 0x10:None, 0x11:None, 0x12:1, 0x13:127, 0x2E:100, 0x2F:84,
     0x33:0, 0x34:97, 0x35:64, 0x37:0, 0x39:127, 0x3A:119, 0x3B:116,
     0x54:96, 0x55:60}
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
def w(aa,*v):
    out.send_message([0xF0,0x43,0x10,0x7F,0x1C,0x0C]+aa+list(v)+[0xF7]); time.sleep(0.045)
def name(p=PART):
    v=req([0x01,0x10|p,0x35])
    return unpack7(bytes(v)).split(b'\0')[0].decode('utf8','replace') if v and len(v)>8 else None
out.send_message([0xB0|CH,0x00,63]); time.sleep(0.03)
out.send_message([0xB0|CH,0x20,32]); time.sleep(0.03)
out.send_message([0xC0|CH,PROG0]);   time.sleep(0.8)
print('SYNTH 2 :', name(), '| temoin SYNTH 1 :', name(7))
for e,(wave,lo,hi,root) in enumerate(Z):
    m=(e<<4)|PART
    for off,v in SET.items():
        if off==0x10: v=lo
        elif off==0x11: v=hi
        w([0x41,m,off], v)
    w([0x41,m,0x03], (wave>>7)&0x7F, wave&0x7F)
print('\nrelecture :')
ok=True
for e,(wave,lo,hi,root) in enumerate(Z):
    m=(e<<4)|PART
    wn=req([0x41,m,0x03]); got=(wn[0]<<7|wn[1]) if wn and len(wn)==2 else None
    a,l,h,kf=req([0x41,m,0x00]),req([0x41,m,0x10]),req([0x41,m,0x11]),req([0x41,m,0x54])
    good = got==wave and l==[lo] and h==[hi] and kf==[96] and a==[1]
    ok &= good
    print('  el%d  onde %s (ref %d)  notes %s-%s  54=%s  assign=%s  %s'
          % (e, got, root, l, h, kf, a, 'ok' if good else '<<< ECART'))
print('\ntout conforme :', ok)
print('temoin SYNTH1 41 07 03 :', req([0x41,0x07,0x03]), '| tempo :', req([0x30,0x40,0x76]))
