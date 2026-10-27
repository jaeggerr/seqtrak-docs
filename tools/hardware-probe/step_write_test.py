#!/usr/bin/env python3
"""Reversible write test for a note in a step (step record, 70 xx xx).

Scans the track, picks an EMPTY step, writes a note into it, reads it back, then
deletes it. The delete is in a finally block, so it runs even if the read-back
fails. An empty step replies with zero data bytes — that is the reference
marker this test relies on.
"""
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C
TRACK = 0          # KICK
NSTEPS = 16
NOTE, VELOCITY, GATE = 60, 100, 120

A_ADD = lambda t: (0x70, t, 0x00)              # ajouter un evenement
A_DEL = lambda t: (0x70, 0x20 | t, 0x00)       # supprimer
A_INFO = lambda t, s: (0x70, 0x40 | t, s)      # read a step's note info


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs) if bs else '(vide)'


class Link:
    def __init__(self, sub='SEQTRAK'):
        probe = rtmidi.MidiOut()
        outs = probe.get_ports()
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
        self.mi.set_callback(lambda msg, data: self.buf.append(msg[0]))
        time.sleep(0.2)
        self.buf.clear()

    def read(self, addr, tries=5, timeout=1.2):
        """-> (True, data) if the address replied, (False, None) otherwise."""
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
                        return True, m[9:-1]
                time.sleep(0.01)
        return False, None

    def write(self, addr, data, quiet=False):
        ah, am, al = addr
        msg = [0xF0, MFR, 0x10, *GROUP, MODEL, ah, am, al, *data, 0xF7]
        if not quiet:
            print(f'    -> {hx(msg)}')
        self.mo.send_message(msg)
        time.sleep(0.3)


def show(data):
    if not data:
        return '(empty step — 0 bytes)'
    names = ['note', 'vel', 'retrig', 'uTiming', 'gateMsb', 'gateLsb']
    return hx(data) + '   ' + ', '.join(
        f'{n}={v}' for n, v in zip(names, data))


link = Link()

ok, st = link.read((0x01, 0x10, 0x20))
if ok and st and st[0] == 1:
    sys.exit('the sequencer is running — stop it before this test')
print('sequencer stopped, good to go\n')

print(f'STEP 1 — scan the first {NSTEPS} steps of part {TRACK}')
occupancy = {}
for s in range(NSTEPS):
    ok, d = link.read(A_INFO(TRACK, s))
    occupancy[s] = (ok, d)
    flag = '?' if not ok else ('.' if not d else '#')
    print(f'    step {s:2d}  {flag}  {show(d) if ok else "no reply"}')

empty = [s for s, (ok, d) in occupancy.items() if ok and not d]
if not empty:
    sys.exit('no empty step in the first 16 — writing nothing')
target = empty[0]
witness = next((s for s in empty if s != target), None)
print(f'\n    target chosen : step {target} (empty)')
print(f'    witness       : step {witness} (empty, must not change)')

wrote = False
try:
    print(f'\nSTEP 2 — write note={NOTE} vel={VELOCITY} gate={GATE} into step {target}')
    gh, gl = (GATE >> 7) & 0x7F, GATE & 0x7F
    link.write(A_ADD(TRACK), [target, NOTE, VELOCITY, gh, gl])
    wrote = True

    print(f'\nETAPE 3 — relecture')
    ok, d = link.read(A_INFO(TRACK, target))
    print(f'    step {target}  {show(d) if ok else "no reply"}')
    okw, dw = link.read(A_INFO(TRACK, witness))
    print(f'    witness {witness}  {show(dw) if okw else "no reply"}')

    if ok and d and d[0] == NOTE and d[1] == VELOCITY:
        print(f'    ✓ WRITE CONFIRMED: step {target} holds note={d[0]} vel={d[1]}')
        if len(d) >= 6:
            print(f'      gate read back = {(d[4] << 7) | d[5]} (wrote {GATE})'
                  f'   retrigger={d[2]}  microTiming={d[3]}')
    elif ok and not d:
        print('    ✗ the step is still empty — the write did not take')
    else:
        print(f'    ✗ contenu inattendu : {hx(d)}')
    if okw and dw:
        print(f'    ⚠ the witness was modified! ({hx(dw)})')
    elif okw:
        print('    ✓ witness still empty, the write is localised')
finally:
    if wrote:
        print(f'\nSTEP 4 — delete step {target}')
        link.write(A_DEL(TRACK), [target])
        ok, d = link.read(A_INFO(TRACK, target))
        if ok and not d:
            print(f'    step {target}  (empty)   ✓ back to the initial state')
        else:
            print(f'    step {target}  {show(d) if ok else "no reply"}')
            print(f'    ⚠ FAILED: step {target} of part {TRACK} still holds a note '
                  f'— clear it by hand on the machine')
