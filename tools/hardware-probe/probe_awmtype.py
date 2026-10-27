#!/usr/bin/env python3
"""Point 1 — does 01 1p 3C (PartAwmType) answer a Parameter Request?

Read-only. Four attempts per address (the repository's standing rule: an
isolated Parameter Request is dropped roughly 1 in 10), and a known-good
control address read in the same loop so that a silent machine cannot be
mistaken for a silent address.
"""
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C
ATTEMPTS = 4


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


class Link:
    def __init__(self, sub='SEQTRAK'):
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        oi = next(i for i, n in enumerate(self.mo.get_ports()) if sub in n)
        ii = next(i for i, n in enumerate(self.mi.get_ports()) if sub in n)
        self.mo.open_port(oi)
        self.mi.open_port(ii)
        # Nothing ignored: we want to see exactly what arrives.
        self.mi.ignore_types(sysex=False, timing=False, active_sense=False)
        self.buf = []
        self.mi.set_callback(lambda msg, data: self.buf.append(msg[0]))
        time.sleep(0.2)
        self.buf.clear()

    def request(self, ah, am, al, timeout=1.0):
        """Send one Parameter Request; return the matching reply or None."""
        self.buf.clear()
        self.mo.send_message([0xF0, MFR, 0x30, *GROUP, MODEL, ah, am, al, 0xF7])
        end = time.time() + timeout
        while time.time() < end:
            while self.buf:
                m = self.buf.pop(0)
                if len(m) >= 10 and m[0] == 0xF0 and m[1] == MFR \
                        and m[3:5] == list(GROUP) and m[5] == MODEL \
                        and (m[6], m[7], m[8]) == (ah, am, al):
                    return m
            time.sleep(0.005)
        return None

    def try_hard(self, ah, am, al):
        """ATTEMPTS attempts; return (n_replies, first reply)."""
        hits, first = 0, None
        for _ in range(ATTEMPTS):
            r = self.request(ah, am, al)
            if r is not None:
                hits += 1
                if first is None:
                    first = r
            time.sleep(0.05)
        return hits, first


CONTROL = (0x30, 0x40, 0x76, 'Tempo (control)')

TARGETS = [(0x01, 0x10 | p, 0x3C, f'PartAwmType part {p}') for p in range(7)]
# Two parts beyond the app's 0-6 window, to see whether the address exists there.
TARGETS += [(0x01, 0x10 | p, 0x3C, f'PartAwmType part {p} (beyond app range)')
            for p in (7, 8, 9, 10)]


def main():
    link = Link()
    print(f'{"address":<10} {"what":<40} {"replies":>8}  value')
    print('-' * 78)
    rows = []
    for ah, am, al, name in TARGETS:
        hits, reply = link.try_hard(ah, am, al)
        data = reply[9:-1] if reply else []
        val = hx(data) if data else ('(zero data bytes)' if reply else '—')
        print(f'{hx((ah, am, al)):<10} {name:<40} {hits}/{ATTEMPTS:<6}  {val}')
        rows.append((name, hits, val))

        # Control address in the same loop, after every target.
        cah, cam, cal, cname = CONTROL
        chits, creply = link.try_hard(cah, cam, cal)
        cdata = creply[9:-1] if creply else []
        cval = hx(cdata) if cdata else '—'
        flag = '' if chits else '   <<< CONTROL SILENT — machine or link at fault'
        print(f'{hx((cah, cam, cal)):<10} {cname:<40} {chits}/{ATTEMPTS:<6}  {cval}{flag}')
    print('-' * 78)
    answered = [r for r in rows if r[1] > 0]
    print(f'{len(answered)}/{len(rows)} target addresses answered at least once '
          f'in {ATTEMPTS} attempts')


if __name__ == '__main__':
    sys.exit(main())
