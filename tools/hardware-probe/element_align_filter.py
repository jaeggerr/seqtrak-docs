"""Aligne le bloc 42 ep (filtre/EQ) des elements 1-7 sur l'element 0.
Filter Gain (42 ep 0C, 2 octets) et FEG Depth (42 ep 1D) : un element allume a
la main garde les valeurs par defaut, plus douces, d'ou une marche de volume
des qu'on quitte la zone de l'element 0."""
import time, rtmidi
PART=8
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
def w(aa,*v):
    out.send_message([0xF0,0x43,0x10,0x7F,0x1C,0x0C]+aa+list(v)+[0xF7]); time.sleep(0.05)
gain0 = req([0x42,0x08,0x0C]); feg0 = req([0x42,0x08,0x1D])
print('el0 : Filter Gain =', gain0, ' FEG Depth =', feg0)
for e in range(1,8):
    m=(e<<4)|PART
    w([0x42,m,0x0C], gain0[0], gain0[1])
    w([0x42,m,0x1D], feg0[0])
print('relecture :')
for e in range(8):
    m=(e<<4)|PART
    print('  el%d  Filter Gain %-9s FEG Depth %s' % (e, req([0x42,m,0x0C]), req([0x42,m,0x1D])))
print('temoin SYNTH1 42 07 0C :', req([0x42,0x07,0x0C]), '| tempo :', req([0x30,0x40,0x76]))
