#!/usr/bin/env python3
"""Reversible write test on a user scale (30 4D xx).

Reads the value, writes a different one, reads it back, then restores it. The
restore is in a finally block, so it happens even if a step fails.
"""
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C
TARGET = (0x30, 0x4D, 0x00)      # Scale1NoteOfPad1
WITNESS = (0x30, 0x4D, 0x01)     # Scale1NoteOfPad2 — must not move
NEW_VALUE = 67                   # G, against an expected C (60); range 36..96


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


class Link:
    def __init__(self, sub='SEQTRAK'):
        mo, mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        outs, ins = mo.get_ports(), mi.get_ports()
        oi = next((i for i, n in enumerate(outs) if sub.lower() in n.lower()), None)
        ii = next((i for i, n in enumerate(ins) if sub.lower() in n.lower()), None)
        if oi is None or ii is None:
            sys.exit(f'no port matching "{sub}" — OUT={outs} IN={ins}')
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.mo.open_port(oi)
        self.mi.open_port(ii)
        self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.buf = []
        self.mi.set_callback(lambda msg, data: self.buf.append(msg[0]))
        time.sleep(0.2)
        self.buf.clear()

    def read(self, addr, tries=5, timeout=1.5):
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
                        data = m[9:-1]
                        v = 0
                        for b in data:
                            v = (v << 7) | (b & 0x7F)
                        return v, data
                time.sleep(0.01)
        return None, None

    def write(self, addr, value):
        ah, am, al = addr
        msg = [0xF0, MFR, 0x10, *GROUP, MODEL, ah, am, al, value & 0x7F, 0xF7]
        print(f'    -> write: {hx(msg)}')
        self.mo.send_message(msg)
        time.sleep(0.25)


def label(addr):
    return f'{addr[0]:02X} {addr[1]:02X} {addr[2]:02X}'


link = Link()
original = None
try:
    print('STEP 1 — read before')
    original, raw = link.read(TARGET)
    w0, _ = link.read(WITNESS)
    if original is None:
        sys.exit('    target unreadable, writing nothing')
    print(f'    target   {label(TARGET)} = {original}  (raw {hx(raw)})')
    print(f'    witness  {label(WITNESS)} = {w0}')

    if original == NEW_VALUE:
        sys.exit(f'    the target already holds {NEW_VALUE}, pick another value')

    print(f'\nSTEP 2 — write {NEW_VALUE} (replacing {original})')
    link.write(TARGET, NEW_VALUE)

    print('\nSTEP 3 — read back')
    after, raw2 = link.read(TARGET)
    w1, _ = link.read(WITNESS)
    print(f'    target   {label(TARGET)} = {after}  (raw {hx(raw2) if raw2 else "-"})')
    print(f'    witness  {label(WITNESS)} = {w1}')
    if after == NEW_VALUE:
        print(f'    ✓ WRITE CONFIRMED: {original} -> {after}')
    else:
        print(f'    ✗ expected {NEW_VALUE}, read {after}')
    if w1 != w0:
        print(f'    ⚠ the witness moved ({w0} -> {w1}) — the write is not localised!')
    else:
        print('    ✓ witness unchanged, the write is localised')
finally:
    if original is not None:
        print(f'\nSTEP 4 — restore {original}')
        link.write(TARGET, original)
        back, _ = link.read(TARGET)
        print(f'    target   {label(TARGET)} = {back}')
        print('    ✓ back to the initial state' if back == original
              else f'    ⚠ FAILED: holds {back}, should hold {original}')
