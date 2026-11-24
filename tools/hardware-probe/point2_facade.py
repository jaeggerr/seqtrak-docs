#!/usr/bin/env python3
"""Point 2 — does `01 33 01` arrive on its own when the FRONT PANEL re-types
a track, with nothing sent from the host?

Self-paced: one instruction at a time, and it waits for you to press Enter.
Take as long as you like — the capture runs the whole time in the background.

Part 2's patterns were already destroyed by the earlier SysEx round trip, so
this costs nothing more.
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
        self.all = []
        self.t0 = time.time()
        self.mi.set_callback(self._cb)
        time.sleep(0.2)

    def _cb(self, msg, data):
        m = msg[0]
        if m and m[0] == 0xF0:
            self.all.append((time.time() - self.t0, list(m)))

    def matching(self, ah, am, al, since=0.0):
        return [(t, m) for t, m in self.all
                if t >= since and len(m) >= 9 and m[1] == MFR
                and m[3:5] == list(GROUP) and m[5] == MODEL
                and (m[6], m[7], m[8]) == (ah, am, al)]

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


def ask(prompt):
    print('\n' + '-' * 68)
    print(prompt)
    print('-' * 68)
    try:
        input('>>> Enter when it is done (Ctrl-C to give up): ')
    except EOFError:
        pass


def main():
    link = Link()

    seq = link.req(0x01, 0x10, 0x20)
    gm = link.req(0x01, 0x10, 0x17)
    print(f'SequencerStatus = {hx(seq) if seq else "?"}   '
          f'GeneralMode = {hx(gm) if gm else "?"}')
    if not seq or seq[0] != 0:
        sys.exit('REFUSING: stop the sequencer first.')
    if gm and gm[0] != 0:
        sys.exit('REFUSING: leave Song mode first (GeneralMode must be 0).')

    start = link.req(0x01, 0x10 | PART, 0x3C)
    start_type = start[0] if start else None
    print(f'part {PART} currently reads type {start_type} '
          f'({TYPE_NAME.get(start_type, "?")})')

    target_key, target_name, target_wire = 11, 'Synth', 2
    if start_type == 2:
        target_key, target_name, target_wire = 9, 'Drum', 1

    ask(f"""STEP 1 of 2 — read this calmly, then press Enter.

You are going to change the TYPE of a single drum track, from the machine's
own front panel. While you do, I send absolutely nothing: I only listen.

THE TRACK: the 3rd drum track, the one printed **CLAP** on the machine.
(The 7 tracks are, in order: KICK, SNARE, CLAP, HAT 1, HAT 2, PERC 1,
 PERC 2. It is the third one, CLAP.)
Its patterns are already cleared, so nothing more of yours is destroyed.

THE GESTURE (Yamaha guide 6.7):

  a. Press the CLAP track knob and HOLD IT DOWN.
     -> Drum keys 9, 10 and 11 light up.
          key  9 = Drum
          key 10 = DrumKit
          key 11 = Synth
  b. STILL holding the knob, press key {target_key} ({target_name})
     and HOLD IT FOR FIVE SECONDS.
     The global meter flashes to show the progress.
  c. The key turns PURPLE: that means it is done.

Do nothing yet. Press Enter first.""")

    quiet = time.time() - link.t0
    print('\n*** I am now SILENT. Nothing goes out until you press Enter. ***')

    ask(f"""STEP 2 of 2 — do the gesture NOW, then press Enter.

  Hold the CLAP knob  ->  hold key {target_key} ({target_name})
  for 5 seconds  ->  wait for PURPLE  ->  let go
  ->  come back here and press Enter.

Take all the time you need, I am listening throughout.
If you cannot manage it, press Enter anyway and say so: the attempt will be
recorded honestly rather than guessed at.""")

    window = [(t, m) for t, m in link.all if t >= quiet]
    acks = link.matching(0x01, 0x33, 0x01, since=quiet)
    cmds = link.matching(0x01, 0x33, 0x00, since=quiet)

    print('\n' + '=' * 68)
    print('RESULT — host sent nothing during this window')
    print('=' * 68)
    print(f'  SysEx messages received     : {len(window)}')
    print(f'  `01 33 01` acknowledgements : {len(acks)}')
    for t, m in acks:
        print(f'      {hx(m)}   part={m[9]} result={m[10]}')
    print(f'  `01 33 00` commands echoed  : {len(cmds)}')
    for t, m in cmds:
        print(f'      {hx(m)}')
    if window:
        print('  every address seen in the window:')
        seen = {}
        for t, m in window:
            if len(m) >= 9:
                k = (m[6], m[7], m[8])
                seen.setdefault(k, []).append(hx(m[9:-1]))
        for a, vals in sorted(seen.items()):
            print(f'      {hx(a)}  x{len(vals)}  {sorted(set(vals))[:6]}')

    end = link.req(0x01, 0x10 | PART, 0x3C)
    end_type = end[0] if end else None
    print(f'\n  part {PART} now reads type {end_type} '
          f'({TYPE_NAME.get(end_type, "?")}), was {start_type}')
    if end_type == start_type:
        print('  >>> THE TYPE DID NOT CHANGE — the gesture did not take effect.')
        print('  >>> This window therefore says NOTHING about point 2.')
    else:
        print('  >>> The type changed from the front panel.')
        print(f'  >>> So the {len(acks)} acknowledgement(s) above are the answer '
              f'to point 2.')

    if end_type is not None and start_type is not None and end_type != start_type:
        print(f'\nrestoring part {PART} to type {start_type} by SysEx…')
        link.send_raw([0xF0, MFR, 0x10, *GROUP, MODEL,
                       0x01, 0x33, 0x00, PART, start_type, 0xF7])
        time.sleep(1.5)
        back = link.req(0x01, 0x10 | PART, 0x3C)
        print(f'  part {PART} now reads {back[0] if back else "?"}')


if __name__ == '__main__':
    sys.exit(main())
