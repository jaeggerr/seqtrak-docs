#!/usr/bin/env python3
"""Lit plusieurs adresses en gardant le port ouvert et en filtrant l'horloge.
Controle (tempo) interleave, 4 tentatives par adresse."""
import time, sys, rtmidi
PLAN = [
    ("30 40 76", 2, "CONTROLE tempo"),
    ("01 10 20", 1, "SequencerRunning"),
    ("01 10 01", 1, "ContentsManagementMode"),
    ("01 10 15", 1, "CurrentProject"),
    ("01 18 33", 2, "CurrentSound SYNTH 2"),
    ("41 08 01", 1, "SYNTH2 el0 Wave Select"),
    ("41 08 03", 2, "SYNTH2 el0 Wave Number"),
    ("41 07 01", 1, "SYNTH1 el0 Wave Select  [temoin]"),
    ("41 07 03", 2, "SYNTH1 el0 Wave Number  [temoin]"),
    ("41 00 01", 1, "KICK el0 Wave Select    [temoin]"),
    ("30 40 76", 2, "CONTROLE tempo"),
]
out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i,n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i,n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)

def read(addr):
    a = [int(x,16) for x in addr.split()]
    pre = [0xF0,0x43,0x10,0x7F,0x1C,0x0C]+a
    while inp.get_message(): pass
    out.send_message([0xF0,0x43,0x30,0x7F,0x1C,0x0C]+a+[0xF7])
    t0=time.time()
    while time.time()-t0 < 1.2:
        m=inp.get_message()
        if m:
            d=list(m[0])
            if d[:9]==pre: return d[9:-1]
        else: time.sleep(0.002)
    return None

for addr, size, label in PLAN:
    got=[]
    for _ in range(4):
        r=read(addr); got.append(r); time.sleep(0.04)
    ok=[g for g in got if g is not None]
    vals={" ".join("%02X"%b for b in g) for g in ok}
    print("%-34s %s  %d/4  %s" % (label, addr, len(ok), " | ".join(sorted(vals)) if vals else "muet"))
