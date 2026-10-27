#!/usr/bin/env python3
"""What happens to unsaved edits when you switch projects?

Yamaha (User Guide 4.2): "Projects are saved automatically when SEQTRAK is
turned off or when switching projects." Never verified. This tests it.

Method, following 12-open-questions.md and the systematic-re-read rule in
14-song-mode.md:

  * write a DISTINCTIVE marker into a per-project setting (the tempo, which
    4.5 calls a project setting), plus a second marker in a zone with a
    verified write path (a user scale pad) to see whether the two scope alike;
  * snapshot the WHOLE state before and after, and diff it, rather than
    choosing a witness and hoping it is the one that speaks;
  * switch project away and back, confirming 01 10 15 at every step;
  * marker survived -> switching SAVES. Marker reverted -> switching DISCARDS.

Both outcomes are unambiguous, which is rare here.

The project switch is destructive if the guide is wrong, so it sits behind a
prompt. Nothing irreversible happens before you press Enter.
"""
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C

TEMPO = (0x30, 0x40, 0x76)
TEMPO_MARKER = [0x01, 0x47]          # 199 BPM, 7-bit big-endian
SCALE_PAD = (0x30, 0x4D, 0x00)
SCALE_MARKER = [0x43]                # note 67

# Everything worth re-reading. Not a chosen witness list: the point is breadth.
def state_plan():
    plan = [
        ('CurrentProject', 0x01, 0x10, 0x15),
        ('GeneralMode', 0x01, 0x10, 0x17),
        ('SequencerStatus', 0x01, 0x10, 0x20),
        ('CurrentPart', 0x01, 0x10, 0x27),
        ('Tempo', *TEMPO),
        ('PatternSelectMode', 0x30, 0x40, 0x79),
        ('ScalePad1', *SCALE_PAD),
        ('ScalePad2', 0x30, 0x4D, 0x01),
        ('SpeakerVolume', 0x00, 0x00, 0x00),
        ('Battery(drifts)', 0x01, 0x10, 0x02),
        ('SampleMemUsed', 0x01, 0x10, 0x11),
    ]
    for p in range(7):
        plan.append((f'PartAwmType p{p}', 0x01, 0x10 | p, 0x3C))
    for p in range(7):
        plan.append((f'PatternSelect p{p}', 0x30, 0x50 | p, 0x0F))
    for p in (0, 7, 10):
        plan.append((f'CurrentSound p{p}', 0x01, 0x10 | p, 0x33))
    return plan


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


class Link:
    def __init__(self, sub='SEQTRAK'):
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.mo.open_port(next(i for i, n in enumerate(self.mo.get_ports()) if sub in n))
        self.mi.open_port(next(i for i, n in enumerate(self.mi.get_ports()) if sub in n))
        self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.buf = []
        self.mi.set_callback(lambda m, d: self.buf.append(m[0]))
        time.sleep(0.2)
        self.buf.clear()

    def send(self, msg):
        self.mo.send_message(list(msg))
        time.sleep(0.002)            # the official app paces at 2 ms

    def req(self, ah, am, al, attempts=4, timeout=0.8):
        for _ in range(attempts):
            self.buf.clear()
            self.send([0xF0, MFR, 0x30, *GROUP, MODEL, ah, am, al, 0xF7])
            end = time.time() + timeout
            while time.time() < end:
                while self.buf:
                    m = self.buf.pop(0)
                    if len(m) >= 9 and m[0] == 0xF0 and m[1] == MFR \
                            and m[3:5] == list(GROUP) and m[5] == MODEL \
                            and (m[6], m[7], m[8]) == (ah, am, al):
                        return m[9:-1]
                time.sleep(0.004)
            time.sleep(0.04)
        return None

    def write(self, ah, am, al, data):
        self.send([0xF0, MFR, 0x10, *GROUP, MODEL, ah, am, al, *data, 0xF7])

    def select_project(self, n):
        """Bank MSB 64, LSB 0, Program n — 06-sounds-presets.md."""
        self.send([0xB0, 0x00, 64])
        self.send([0xB0, 0x20, 0])
        self.send([0xC0, n])

    def snapshot(self, label):
        print(f'\n--- full state: {label} ---')
        snap = {}
        for name, ah, am, al in state_plan():
            d = self.req(ah, am, al)
            snap[name] = hx(d) if d else 'NO REPLY'
        for name in snap:
            print(f'    {name:<22} {snap[name]}')
        return snap


def diff(a, b, label_a, label_b):
    print(f'\n=== diff: {label_a} -> {label_b} ===')
    moved = []
    for name in a:
        if a[name] != b[name]:
            moved.append(name)
            print(f'    MOVED  {name:<22} {a[name]}  ->  {b[name]}')
    if not moved:
        print('    nothing moved')
    return moved


def main():
    link = Link()

    rb = link.req(0x00, 0x00, 0x07)
    rp = link.req(0x00, 0x00, 0x08)
    print(f'Receive Bank Select  00 00 07 = {hx(rb) if rb else "?"}')
    print(f'Receive Prog Change  00 00 08 = {hx(rp) if rp else "?"}')
    if not rb or not rp or rb[0] != 1 or rp[0] != 1:
        sys.exit('REFUSING: the machine would ignore the project switch.')

    seq = link.req(0x01, 0x10, 0x20)
    if not seq or seq[0] != 0:
        sys.exit('REFUSING: stop the sequencer first.')

    cur = link.req(0x01, 0x10, 0x15)
    start_project = cur[0] if cur else None
    print(f'CurrentProject       01 10 15 = {start_project}')
    if start_project is None:
        sys.exit('REFUSING: cannot read CurrentProject.')

    orig_tempo = link.req(*TEMPO)
    orig_scale = link.req(*SCALE_PAD)
    print(f'Tempo now            {hx(orig_tempo) if orig_tempo else "?"}')
    print(f'ScalePad1 now        {hx(orig_scale) if orig_scale else "?"}')
    if not orig_tempo or not orig_scale:
        sys.exit('REFUSING: cannot read the markers back.')

    snap_a = link.snapshot('A, before any write')

    try:
        print(f'\n>>> writing markers: Tempo = 199 BPM, ScalePad1 = note 67')
        link.write(*TEMPO, TEMPO_MARKER)
        link.write(*SCALE_PAD, SCALE_MARKER)
        time.sleep(0.4)
        t = link.req(*TEMPO)
        s = link.req(*SCALE_PAD)
        print(f'    Tempo read-back     {hx(t) if t else "?"} '
              f'(wanted {hx(TEMPO_MARKER)})')
        print(f'    ScalePad1 read-back {hx(s) if s else "?"} '
              f'(wanted {hx(SCALE_MARKER)})')
        tempo_ok = t == TEMPO_MARKER
        scale_ok = s == SCALE_MARKER
        if not tempo_ok and not scale_ok:
            sys.exit('REFUSING: neither marker took. Nothing to test.')
        if not tempo_ok:
            print('    NOTE: the tempo write did not take; the scale pad carries the test.')

        snap_b = link.snapshot('B, markers written')
        diff(snap_a, snap_b, 'A', 'B')

        print('\n' + '=' * 70)
        print('THE DESTRUCTIVE STEP')
        print('=' * 70)
        print(f"""
Next I switch to project 7 and back to project {start_project}.

If Yamaha's User Guide 4.2 is right, switching SAVES project {start_project},
and the markers survive the round trip.

If it is wrong, switching DISCARDS uncommitted edits — and that includes the
1320-note song currently in project {start_project}, which would be lost.

The owner has said this song is expendable. Nothing is lost if that is still true.
""")
        try:
            input('>>> Enter to switch project, Ctrl-C to stop here: ')
        except (EOFError, KeyboardInterrupt):
            print('\nstopped before the switch; markers will be restored')
            raise

        print(f'\nswitching to project 7…')
        link.select_project(7)
        time.sleep(1.2)
        c = link.req(0x01, 0x10, 0x15)
        print(f'    CurrentProject = {c[0] if c else "NO REPLY"} (wanted 7)')
        if not c or c[0] != 7:
            print('    the switch did not take — the test is inconclusive, '
                  'restoring and stopping')
            return
        t7 = link.req(*TEMPO)
        s7 = link.req(*SCALE_PAD)
        print(f"    project 7's Tempo    {hx(t7) if t7 else '?'}")
        print(f'    ScalePad1 there      {hx(s7) if s7 else "?"} '
              f'(same value => the zone is global, not per-project)')

        print(f'\nswitching back to project {start_project}…')
        link.select_project(start_project)
        time.sleep(1.2)
        c = link.req(0x01, 0x10, 0x15)
        print(f'    CurrentProject = {c[0] if c else "NO REPLY"} '
              f'(wanted {start_project})')

        snap_c = link.snapshot('C, after the project round trip')
        diff(snap_b, snap_c, 'B', 'C')

        t_after = link.req(*TEMPO)
        s_after = link.req(*SCALE_PAD)
        print('\n' + '=' * 70)
        print('VERDICT')
        print('=' * 70)
        print(f'  Tempo     wrote {hx(TEMPO_MARKER)}, now {hx(t_after) if t_after else "?"}')
        print(f'  ScalePad1 wrote {hx(SCALE_MARKER)}, now {hx(s_after) if s_after else "?"}')
        if tempo_ok:
            if t_after == TEMPO_MARKER:
                print('\n  >>> The marker SURVIVED. Switching projects SAVED the')
                print('      outgoing project. Yamaha 4.2 is confirmed.')
            elif t_after == orig_tempo:
                print('\n  >>> The marker REVERTED to its pre-write value. Switching')
                print('      projects DISCARDED the uncommitted edit. Yamaha 4.2 is')
                print('      CONTRADICTED on this machine.')
            else:
                print('\n  >>> Neither the marker nor the original. Unexpected; do not')
                print('      interpret, record the raw values.')
    finally:
        print('\n' + '=' * 70)
        print('RESTORE')
        print('=' * 70)
        here = link.req(0x01, 0x10, 0x15)
        print(f'  CurrentProject = {here[0] if here else "?"} '
              f'(must be {start_project} before restoring)')
        if here and here[0] != start_project:
            print('  WRONG PROJECT — returning first')
            link.select_project(start_project)
            time.sleep(1.2)
        link.write(*TEMPO, list(orig_tempo))
        link.write(*SCALE_PAD, list(orig_scale))
        time.sleep(0.4)
        print(f'  Tempo     restored to {hx(link.req(*TEMPO) or [])}')
        print(f'  ScalePad1 restored to {hx(link.req(*SCALE_PAD) or [])}')


if __name__ == '__main__':
    sys.exit(main())
