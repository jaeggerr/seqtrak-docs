#!/usr/bin/env python3
"""Generic reversible write sweep: try a list of values and record which ones
the machine actually accepts. The restore runs in a finally block.

  probe_write.py AH AM AL v1 v2 v3 ...
"""
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs) if bs else '(vide)'


class Link:
    def __init__(self, sub='SEQTRAK'):
        outs = rtmidi.MidiOut().get_ports()
        ins = rtmidi.MidiIn().get_ports()
        oi = next((i for i, n in enumerate(outs) if sub.lower() in n.lower()), None)
        ii = next((i for i, n in enumerate(ins) if sub.lower() in n.lower()), None)
        if oi is None or ii is None:
            sys.exit(f'port « {sub} » introuvable — OUT={outs} IN={ins}')
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.mo.open_port(oi)
        self.mi.open_port(ii)
        self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.buf = []
        self.mi.set_callback(lambda m, d: self.buf.append(m[0]))
        time.sleep(0.2)
        self.buf.clear()

    def read(self, addr, tries=5, timeout=1.2):
        ah, am, al = addr
        for _ in range(tries):
            self.buf.clear()
            self.mo.send_message([0xF0, MFR, 0x30, *GROUP, MODEL, ah, am, al, 0xF7])
            end = time.time() + timeout
            while time.time() < end:
                while self.buf:
                    m = self.buf.pop(0)
                    if (len(m) >= 10 and m[0] == 0xF0 and m[1] == MFR
                            and m[3:5] == list(GROUP) and m[5] == MODEL
                            and (m[6], m[7], m[8]) == addr):
                        d = m[9:-1]
                        v = 0
                        for b in d:
                            v = (v << 7) | (b & 0x7F)
                        return v, d
                time.sleep(0.01)
        return None, None

    def write(self, addr, value, nbytes=1):
        ah, am, al = addr
        data = [(value >> (7 * (nbytes - 1 - i))) & 0x7F for i in range(nbytes)]
        self.mo.send_message([0xF0, MFR, 0x10, *GROUP, MODEL, ah, am, al, *data, 0xF7])
        time.sleep(0.3)


ah, am, al = (int(x, 16) for x in sys.argv[1:4])
values = [int(x) for x in sys.argv[4:]]
addr = (ah, am, al)
link = Link()

original, raw = link.read(addr)
if original is None:
    sys.exit(f'{ah:02X} {am:02X} {al:02X} does not answer — writing nothing')
print(f'adresse  {ah:02X} {am:02X} {al:02X}')
print(f'original value = {original}  (raw {hx(raw)})\n')
print(f'{"wrote":>8s} {"read":>8s}   verdict')

try:
    for v in values:
        link.write(addr, v)
        back, _ = link.read(addr)
        if back == v:
            verdict = 'accepted as written'
        elif back is None:
            verdict = 'no reply'
        elif back == original:
            verdict = 'refused (unchanged)'
        else:
            verdict = f'clamped to {back}'
        print(f'{v:>8d} {str(back):>8s}   {verdict}')
finally:
    link.write(addr, original)
    back, _ = link.read(addr)
    print(f'\nrestauration -> {back}  '
          f'{"✓ etat initial retrouve" if back == original else "⚠ ECHEC"}')
