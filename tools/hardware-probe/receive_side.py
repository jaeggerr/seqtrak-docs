#!/usr/bin/env python3
"""Receive-side checks: does the SEQTRAK act on `01 10 21`, and on a bare
Program Change?

Written to reproduce a third-party report (GitHub issue #2, 2026-11-14):

  1. writing `01 10 21` = 1 arms recording and = 0 stops it;
  2. a Program Change with no Bank Select before it does nothing, while
     CC 0 = 63, CC 32 = n, Program Change selects a sound.

Three stages, each optional:

    python3 receive_side.py --rec            # stage 1, reversible; the machine plays a few seconds
    python3 receive_side.py --panel          # stage 2, read-only, needs a hand on [REC]
    python3 receive_side.py --pc --part 9    # stage 3, REPLACES the part's sound

Stage 3 reloads a preset on the part and then reloads the original one. A
preset reload discards any edit made by hand to that sound; back the part up
first if it matters.

Every read is retried five times and the tempo (`30 40 76`) is read alongside
as a control, so a dropped reply is not mistaken for a behaviour.
"""
import argparse
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, [0x7F, 0x1C], 0x0C
SEQ = (0x01, 0x10, 0x20)        # SequencerStatus
REC = (0x01, 0x10, 0x21)        # RecordingStatus
TEMPO = (0x30, 0x40, 0x76)      # control


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
        self.mo, self.mi = mo, mi
        mo.open_port(oi)
        mi.open_port(ii)
        mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.log = []                       # (time, message), everything received
        self.t0 = time.time()
        mi.set_callback(lambda msg, data: self.log.append((time.time() - self.t0, msg[0])))
        time.sleep(0.2)

    def send(self, msg, note=''):
        print(f'    -> {hx(msg)}  {note}')
        self.mo.send_message(msg)
        time.sleep(0.002)

    def read(self, addr, tries=5, timeout=1.0):
        for _ in range(tries):
            mark = len(self.log)
            self.mo.send_message([0xF0, MFR, 0x30, *GROUP, MODEL, *addr, 0xF7])
            end = time.time() + timeout
            while time.time() < end:
                for _, m in self.log[mark:]:
                    if (len(m) >= 10 and m[0] == 0xF0 and m[1] == MFR and m[2] == 0x10
                            and m[3:5] == GROUP and m[5] == MODEL and tuple(m[6:9]) == addr):
                        v = 0
                        for b in m[9:-1]:
                            v = (v << 7) | b
                        return v
                time.sleep(0.01)
        return None

    def write(self, addr, value, note=''):
        self.send([0xF0, MFR, 0x10, *GROUP, MODEL, *addr, value & 0x7F, 0xF7], note)

    def since(self, mark):
        return [(t, m) for t, m in self.log[mark:]]


def show(link, mark, title):
    got = link.since(mark)
    print(f'    {title}: {len(got)} message(s) received')
    for t, m in got:
        print(f'      {t:8.3f}s  {hx(m)}')


def state(link, label):
    s, r, bpm = link.read(SEQ), link.read(REC), link.read(TEMPO)
    print(f'    {label}: SequencerStatus={s}  RecordingStatus={r}  tempo={bpm}')
    return s, r, bpm


def rec_cycle(link, label):
    mark = len(link.log)
    link.write(REC, 1, 'RecordingStatus = 1')
    time.sleep(1.5)
    echoes = [m for _, m in link.since(mark) if m[0] == 0xF0]
    s1, r1, bpm1 = state(link, f'{label}, after 1')
    mark = len(link.log)
    link.write(REC, 0, 'RecordingStatus = 0')
    time.sleep(1.5)
    echoes += [m for _, m in link.since(mark) if m[0] == 0xF0]
    s2, r2, bpm2 = state(link, f'{label}, after 0')
    print(f'    RESULT ({label})  write 1 -> RecordingStatus {r1}; write 0 -> {r2}; '
          f'SequencerStatus {s1}/{s2}; tempo {bpm1}/{bpm2}; '
          f'{len(echoes)} SysEx received besides the replies')
    for m in echoes:
        print(f'      {hx(m)}')


def stage_rec(link):
    """Write 01 10 21 with the sequencer stopped, then twice while it plays.

    The sequencer is started and stopped from here with FA / FC, so the machine
    plays for a few seconds. Nothing is recorded unless a key is pressed.
    """
    print('STAGE 1 — write 01 10 21')
    s0, r0, bpm0 = state(link, 'before')
    if None in (s0, r0, bpm0):
        sys.exit('    a read failed five times; writing nothing')
    if s0 != 0 or r0 != 0:
        sys.exit('    the sequencer is not stopped and idle; writing nothing')
    try:
        rec_cycle(link, 'stopped')
        link.send([0xFA], 'MIDI Start')
        time.sleep(1.0)
        if link.read(SEQ) != 1:
            sys.exit('    the sequencer did not start on FA; stopping here')
        rec_cycle(link, 'playing, 1st')
        rec_cycle(link, 'playing, 2nd')
    finally:
        link.write(REC, 0, 'restore: RecordingStatus = 0')
        time.sleep(0.3)
        link.send([0xFC], 'restore: MIDI Stop')
        time.sleep(0.8)
        state(link, 'restored')


def stage_panel(link):
    print('STAGE 2 — what [REC] emits (read-only)')
    input('    Appuie sur Entrée, puis une fois sur [REC] (la touche ronde rouge), '
          'attends deux secondes, et rappuie dessus pour arrêter. ')
    mark = len(link.log)
    time.sleep(12)
    show(link, mark, '12 s window')
    state(link, 'after  ')


def stage_pc(link, part):
    cur = (0x01, 0x10 | part, 0x33)     # CurrentSound = catalogue number - 1
    ch = part
    print(f'STAGE 3 — Program Change on part {part} (MIDI channel {part + 1})')
    if link.read(SEQ) != 0:
        sys.exit('    the sequencer is not stopped; sending nothing')
    n0 = link.read(cur)
    if n0 is None:
        sys.exit('    CurrentSound unreadable five times; sending nothing')
    lsb0, pc0 = divmod(n0, 128)
    # Three programs in the part's own bank, none of them the current one.
    a, b, c = [(pc0 + k) % 128 for k in (1, 2, 3)]
    print(f'    before: CurrentSound={n0}  (bank LSB {lsb0}, program {pc0})')
    try:
        link.send([0xC0 | ch, a], f'A. bare Program Change {a}, no Bank Select sent by this run')
        time.sleep(0.5)
        na = link.read(cur)
        print(f'    A. CurrentSound={na}  expected {n0} if a bare PC is ignored, '
              f'{lsb0 * 128 + a} if it uses the part\'s current bank')

        link.send([0xB0 | ch, 0x00, 63], 'B. Bank Select MSB 63')
        link.send([0xB0 | ch, 0x20, lsb0], f'B. Bank Select LSB {lsb0}')
        link.send([0xC0 | ch, b], f'B. Program Change {b}')
        time.sleep(0.5)
        nb = link.read(cur)
        print(f'    B. CurrentSound={nb}  expected {lsb0 * 128 + b}')

        link.send([0xC0 | ch, c], f'C. bare Program Change {c}, AFTER a Bank Select on this channel')
        time.sleep(0.5)
        nc = link.read(cur)
        print(f'    C. CurrentSound={nc}  {lsb0 * 128 + c} if the bank stays latched, {nb} if not')
        print(f'    RESULT  start {n0}; bare PC -> {na}; BS+PC -> {nb}; bare PC after BS -> {nc}; '
              f'tempo control {link.read(TEMPO)}')
    finally:
        link.send([0xB0 | ch, 0x00, 63], 'restore')
        link.send([0xB0 | ch, 0x20, lsb0], 'restore')
        link.send([0xC0 | ch, pc0], 'restore')
        time.sleep(0.5)
        back = link.read(cur)
        print(f'    restored: CurrentSound={back}' + ('' if back == n0 else f'  ⚠ should be {n0}'))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--rec', action='store_true')
    ap.add_argument('--panel', action='store_true')
    ap.add_argument('--pc', action='store_true')
    ap.add_argument('--part', type=int, default=9, help='0-9; 7-8 synth, 9 DX (default)')
    args = ap.parse_args()
    if not (args.rec or args.panel or args.pc):
        ap.error('pick at least one of --rec, --panel, --pc')
    if not 0 <= args.part <= 9:
        ap.error('--part is 0-9; the sampler (10) does not select sounds this way')
    link = Link()
    if args.rec:
        stage_rec(link)
    if args.panel:
        stage_panel(link)
    if args.pc:
        stage_pc(link, args.part)


if __name__ == '__main__':
    main()
