"""Aligne les elements 1-4 sur l'element 0 : suivi de clavier en hauteur et les
trois autres ecarts releves au dump. SYNTH 1 temoin, tempo en controle."""
import time, rtmidi
PART=8
FIX={0x54:96,   # Pitch Key Follow Sensitivity : 64 = ne suit pas, 96 = suit
     0x55:60,   # note centrale du suivi
     0x2F:84,   # Level Velocity Sensitivity
     0x34:97,   # AEG Decay 1 Time
     0x35:64}   # AEG Decay 2 Time
out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i,n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i,n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)
def req(aa,n=4,wait=1.2):
    pre=[0xF0,0x43,0x10,0x7F,0x1C,0x0C]+aa
    for _ in range(n):
        while inp.get_message(): pass
        out.send_message([0xF0,0x43,0x30,0x7F,0x1C,0x0C]+aa+[0xF7])
        t0=time.time()
        while time.time()-t0<wait:
            m=inp.get_message()
            if m and list(m[0])[:9]==pre: return list(m[0])[9:-1]
            if not m: time.sleep(0.002)
        time.sleep(0.04)
    return None
def w(aa,v):
    out.send_message([0xF0,0x43,0x10,0x7F,0x1C,0x0C]+aa+[v,0xF7]); time.sleep(0.05)
print('el0 (reference) 54=%s 55=%s' % (req([0x41,0x08,0x54]), req([0x41,0x08,0x55])))
for e in range(1,5):
    m=(e<<4)|PART
    for off,v in FIX.items(): w([0x41,m,off], v)
print('relecture :')
for e in range(5):
    m=(e<<4)|PART
    print('  el%d  54=%-5s 55=%-5s 2F=%-5s 34=%-5s 35=%-5s  wave=%s notes %s-%s'
      % (e, req([0x41,m,0x54]), req([0x41,m,0x55]), req([0x41,m,0x2F]),
         req([0x41,m,0x34]), req([0x41,m,0x35]),
         (lambda v: (v[0]<<7|v[1]) if v and len(v)==2 else None)(req([0x41,m,0x03])),
         req([0x41,m,0x10]), req([0x41,m,0x11])))
print('temoin SYNTH1 41 07 54 :', req([0x41,0x07,0x54]), '| tempo :', req([0x30,0x40,0x76]))
