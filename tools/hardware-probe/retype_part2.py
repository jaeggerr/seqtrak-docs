#!/usr/bin/env python3
"""Points 2, 3 and 4 — the track-type round trip on part 2 (HATO).

DESTRUCTIVE: re-typing a track deletes its patterns. Part 2 is the agreed
sacrifice; the song it belongs to is regenerable from song.trk.

Three questions in one sitting, because they all need the same destruction:

  point 2  does `01 33 01` arrive spontaneously when the FRONT PANEL re-types
           a track, with nothing sent from here?
  point 3  is `01 33 00` echoed back by the machine?
  point 4  do types 01 (DRUM) and 03 (DRUMKIT) work on the wire? Only 02 has
           ever been sent.

Everything inbound is captured the whole time by one cumulative counter, so a
spontaneous message cannot be missed between phases.
"""
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C
PART = 2
TYPE_NAME = {0: '(0)', 1: 'DRUM', 2: 'SYNTH', 3: 'DRUMKIT', 4: '(4)', 5: '(5)'}


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


class Link:
    def __init__(self, sub='SEQTRAK'):
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.mo.open_port(next(i for i, n in enumerate(self.mo.get_ports()) if sub in n))
        self.mi.open_port(next(i for i, n in enumerate(self.mi.get_ports()) if sub in n))
        self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.all = []          # every SysEx seen, with a timestamp. Never pruned.
        self.t0 = time.time()
        self.mi.set_callback(self._cb)
        time.sleep(0.2)

    def _cb(self, msg, data):
        m = msg[0]
        if m and m[0] == 0xF0:
            self.all.append((time.time() - self.t0, list(m)))

    def matching(self, ah, am, al, since=0.0):
        out = []
        for t, m in self.all:
            if t < since or len(m) < 9:
                continue
            if m[1] == MFR and m[3:5] == list(GROUP) and m[5] == MODEL \
                    and (m[6], m[7], m[8]) == (ah, am, al):
                out.append((t, m))
        return out

    def send_raw(self, msg):
        self.mo.send_message(list(msg))

    def req(self, ah, am, al, attempts=4, timeout=0.8):
        for _ in range(attempts):
            mark = time.time() - self.t0
            self.send_raw([0xF0, MFR, 0x30, *GROUP, MODEL, ah, am, al, 0xF7])
            end = time.time() + timeout
            while time.time() < end:
                hits = self.matching(ah, am, al, since=mark)
                if hits:
                    return hits[0][1][9:-1]
                time.sleep(0.005)
            time.sleep(0.05)
        return None


def read_type(link, part):
    d = link.req(0x01, 0x10 | part, 0x3C)
    return d[0] if d else None


def show_type(link, part, label):
    v = read_type(link, part)
    print(f'  {label}: 01 {0x10|part:02X} 3C = {v} ({TYPE_NAME.get(v, "?")})')
    return v


def main():
    link = Link()

    seq = link.req(0x01, 0x10, 0x20)
    print(f'SequencerStatus 01 10 20 = {hx(seq) if seq else "NO REPLY"}')
    if not seq or seq[0] != 0:
        sys.exit('REFUSING: the sequencer must be stopped before a type change.')
    gm = link.req(0x01, 0x10, 0x17)
    print(f'GeneralMode     01 10 17 = {hx(gm) if gm else "NO REPLY"} '
          f'(must not be Song mode)')

    print('\nInitial types, all parts (witnesses — only part 2 may move):')
    before = {}
    for p in range(7):
        before[p] = read_type(link, p)
    print('  ' + '  '.join(f'p{p}={before[p]}' for p in range(7)))
    if before[PART] != 1:
        print(f'NOTE: part {PART} is not DRUM, it is {before[PART]}.')

    # ---------------- PHASE 1: front panel, nothing sent from here ----------
    print('\n' + '=' * 70)
    print('PHASE 1 — FRONT PANEL. I send NOTHING for the next 60 s.')
    print('=' * 70)
    print(f"""
Re-type part {PART} (HATO, the third drum track) to DrumKit, from the machine:

  1. Press and hold that track's Drum Track knob.
     Drum keys 9-11 light up: 9 = Drum, 10 = DrumKit, 11 = Synth.
  2. Still holding, press and hold Drum key 10 (DrumKit) for FIVE seconds.
  3. The key turns purple when it is done.

This deletes that track's patterns. That is expected and agreed.
""")
    quiet_start = time.time() - link.t0
    for remaining in range(60, 0, -10):
        print(f'   listening, {remaining} s left…', flush=True)
        time.sleep(10)

    spontaneous_ack = link.matching(0x01, 0x33, 0x01, since=quiet_start)
    spontaneous_cmd = link.matching(0x01, 0x33, 0x00, since=quiet_start)
    others = [(t, m) for t, m in link.all if t >= quiet_start]

    print(f'\nPHASE 1 RESULT — nothing was sent from the host in this window.')
    print(f'  SysEx messages received      : {len(others)}')
    print(f'  `01 33 01` (acknowledge)     : {len(spontaneous_ack)}')
    for t, m in spontaneous_ack:
        print(f'      t={t:6.2f}  {hx(m)}   part={m[9]} result={m[10]}')
    print(f'  `01 33 00` (command, echoed) : {len(spontaneous_cmd)}')
    for t, m in spontaneous_cmd:
        print(f'      t={t:6.2f}  {hx(m)}')
    print('  other addresses seen in the window:')
    seen = {}
    for t, m in others:
        if len(m) >= 9:
            seen[(m[6], m[7], m[8])] = seen.get((m[6], m[7], m[8]), 0) + 1
    for a, n in sorted(seen.items()):
        print(f'      {hx(a)}  x{n}')

    after_panel = show_type(link, PART, 'part 2 after the front-panel change')

    # ---------------- PHASE 2: host-sent type 01 and 03 ---------------------
    print('\n' + '=' * 70)
    print('PHASE 2 — host-sent type changes (types 01 and 03, never sent before)')
    print('=' * 70)

    original = before[PART]
    try:
        for wanted in (0x03, 0x01):
            cur = read_type(link, PART)
            if cur == wanted:
                print(f'\npart {PART} already reads {wanted}; '
                      f'skipping to keep the test meaningful')
                continue
            print(f'\n--- sending type {wanted:02X} ({TYPE_NAME[wanted]}) ---')
            mark = time.time() - link.t0
            msg = [0xF0, MFR, 0x10, *GROUP, MODEL, 0x01, 0x33, 0x00, PART, wanted, 0xF7]
            print(f'  sent     {hx(msg)}')
            link.send_raw(msg)

            deadline = time.time() + 8
            ack = []
            while time.time() < deadline and not ack:
                ack = link.matching(0x01, 0x33, 0x01, since=mark)
                time.sleep(0.02)
            if ack:
                t, m = ack[0]
                print(f'  ack      {hx(m)}   part={m[9]} result={m[10]} '
                      f'after {t - mark:.2f} s')
            else:
                print('  ack      NONE in 8 s — a missing reply is not information; '
                      'the read-back below decides')
            echo = link.matching(0x01, 0x33, 0x00, since=mark)
            print(f'  echo of `01 33 00` from the machine: {len(echo)}')

            time.sleep(1.0)
            got = show_type(link, PART, f'read-back after asking for {wanted:02X}')
            print(f'  VERDICT: {"OK" if got == wanted else "MISMATCH"} '
                  f'(asked {wanted}, read {got})')

            wit = {p: read_type(link, p) for p in range(7) if p != PART}
            moved = [p for p in wit if wit[p] != before[p]]
            print(f'  witnesses (other parts) moved: {moved if moved else "none"}')
    finally:
        print('\n' + '=' * 70)
        print(f'RESTORE — returning part {PART} to its original type {original}')
        print('=' * 70)
        cur = read_type(link, PART)
        if cur == original:
            print(f'  already {original}, nothing to do')
        elif original is None:
            print('  original type unknown — NOT restoring blindly')
        else:
            msg = [0xF0, MFR, 0x10, *GROUP, MODEL, 0x01, 0x33, 0x00, PART, original, 0xF7]
            link.send_raw(msg)
            print(f'  sent {hx(msg)}')
            time.sleep(1.5)
            show_type(link, PART, 'part 2 after restore')
        print('\nNOTE: the restore brings the TYPE back. The patterns that the '
              'type change deleted are NOT restored — re-run write_song.py.')


if __name__ == '__main__':
    sys.exit(main())
