#!/usr/bin/env python3
"""Does a normal power-off save the project? (User Guide 4.2, second half)

The test spans a power cycle, so it cannot be one run: the USB MIDI port goes
away with the machine. Two phases, with the snapshot kept on disk between them.

  python3 test_power_off.py 1     before powering off
  python3 test_power_off.py 2     after powering back on

Phase 1 writes a distinctive marker and records 28 addresses. Phase 2 re-reads
them and diffs. Marker present -> a normal power-off saves. Marker gone -> it
discards, and Yamaha 4.2 is wrong about this machine.

IMPORTANT, from the guide:
  3.2.1 normal power off      hold [power/PLAY] 2 s or longer     4.2 says saves
  3.2.2 forced termination    hold [power/PLAY] + [PROJECT up]    explicitly does NOT save
  3.2.3 auto power off        30 min idle                         says it saves
This tests 3.2.1 only. Do NOT use the forced termination for this test, and do
NOT take the 4.6 temporary snapshot — either would void it.
"""
import json
import pathlib
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C
STORE = pathlib.Path(__file__).with_name('power_off_snapshot.json')

TEMPO = (0x30, 0x40, 0x76)
TEMPO_MARKER = [0x01, 0x35]          # 181 BPM — distinct from every earlier test
SCALE_PAD = (0x30, 0x4D, 0x00)
SCALE_MARKER = [0x47]                # note 71


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
        ('SampleMemUsed', 0x01, 0x10, 0x11),
        ('FirmwareVersion', 0x01, 0x00, 0x00),
    ]
    for p in range(7):
        plan.append((f'PartAwmType p{p}', 0x01, 0x10 | p, 0x3C))
    for p in range(7):
        plan.append((f'PatternSelect p{p}', 0x30, 0x50 | p, 0x0F))
    for p in (0, 7):
        plan.append((f'CurrentSound p{p}', 0x01, 0x10 | p, 0x33))
    return plan


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


class Link:
    def __init__(self, sub='SEQTRAK'):
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        oi = next((i for i, n in enumerate(self.mo.get_ports()) if sub in n), None)
        ii = next((i for i, n in enumerate(self.mi.get_ports()) if sub in n), None)
        if oi is None or ii is None:
            sys.exit('no SEQTRAK port — is the machine on and plugged in?')
        self.mo.open_port(oi)
        self.mi.open_port(ii)
        self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.buf = []
        self.mi.set_callback(lambda m, d: self.buf.append(m[0]))
        time.sleep(0.2)
        self.buf.clear()

    def send(self, msg):
        self.mo.send_message(list(msg))
        time.sleep(0.002)

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

    def snapshot(self):
        snap = {}
        for name, ah, am, al in state_plan():
            d = self.req(ah, am, al)
            snap[name] = hx(d) if d else 'NO REPLY'
        return snap


def show(snap, title):
    print(f'\n--- {title} ---')
    for k, v in snap.items():
        print(f'    {k:<22} {v}')


def phase1():
    link = Link()
    seq = link.req(0x01, 0x10, 0x20)
    if not seq or seq[0] != 0:
        sys.exit('REFUSING: stop the sequencer first.')
    proj = link.req(0x01, 0x10, 0x15)
    if not proj:
        sys.exit('REFUSING: cannot read CurrentProject.')
    print(f'CurrentProject = {proj[0]}, sequencer stopped. Good.')

    orig = {'tempo': hx(link.req(*TEMPO) or []),
            'scale': hx(link.req(*SCALE_PAD) or [])}
    print(f"Tempo before     {orig['tempo']}")
    print(f"ScalePad1 before {orig['scale']}")

    print(f'\n>>> writing markers: Tempo = 181 BPM ({hx(TEMPO_MARKER)}), '
          f'ScalePad1 = note 71 ({hx(SCALE_MARKER)})')
    link.write(*TEMPO, TEMPO_MARKER)
    link.write(*SCALE_PAD, SCALE_MARKER)
    time.sleep(0.4)
    t = link.req(*TEMPO)
    s = link.req(*SCALE_PAD)
    print(f'    Tempo read-back     {hx(t) if t else "?"}')
    print(f'    ScalePad1 read-back {hx(s) if s else "?"}')
    if t != TEMPO_MARKER or s != SCALE_MARKER:
        sys.exit('REFUSING: a marker did not take; nothing to test.')

    snap = link.snapshot()
    show(snap, 'snapshot before power-off')
    STORE.write_text(json.dumps({'snapshot': snap, 'original': orig,
                                 'project': proj[0]}, indent=2))
    print(f'\nsnapshot saved to {STORE}')

    print(f"""
{'=' * 70}
NOW, ON THE MACHINE
{'=' * 70}

  1. Press and HOLD the [power/PLAY] button for 2 SECONDS or longer,
     until it switches off. That is the normal power-off of guide 3.2.1.

     Do NOT hold [power/PLAY] + [PROJECT up] together — that is the forced
     termination, which the guide says does not save, and it would answer a
     different question.

     Do NOT take a temporary snapshot ([PROJECT up] + the lit Drum key).

  2. Wait a few seconds with it off.

  3. Press and HOLD [power/PLAY] again for 2 seconds to switch it back on.
     Wait for it to finish starting up.

  4. Then run phase 2.
""")


def phase2():
    if not STORE.exists():
        sys.exit(f'no snapshot at {STORE} — run phase 1 first.')
    saved = json.loads(STORE.read_text())
    before, orig = saved['snapshot'], saved['original']

    link = Link()
    fw = link.req(0x01, 0x00, 0x00)
    if not fw:
        sys.exit('no reply — is the machine finished starting up?')
    print(f'machine answering, firmware {hx(fw)}')

    after = link.snapshot()
    show(after, 'snapshot after power-on')

    print('\n=== diff: before power-off -> after power-on ===')
    moved = []
    for k in before:
        if before[k] != after.get(k):
            moved.append(k)
            print(f'    MOVED  {k:<22} {before[k]}  ->  {after.get(k)}')
    if not moved:
        print('    nothing moved')

    print('\n' + '=' * 70)
    print('VERDICT')
    print('=' * 70)
    t_after, s_after = after['Tempo'], after['ScalePad1']
    print(f'  Tempo     wrote {hx(TEMPO_MARKER)}, now {t_after} '
          f'(was {orig["tempo"]} before the write)')
    print(f'  ScalePad1 wrote {hx(SCALE_MARKER)}, now {s_after} '
          f'(was {orig["scale"]} before the write)')

    if t_after == hx(TEMPO_MARKER) and s_after == hx(SCALE_MARKER):
        print('\n  >>> BOTH MARKERS SURVIVED the power cycle.')
        print('      A normal power-off SAVES. Guide 4.2 confirmed on both')
        print('      of the two moments it names.')
    elif t_after == orig['tempo'] and s_after == orig['scale']:
        print('\n  >>> BOTH MARKERS REVERTED to their pre-write values.')
        print('      A normal power-off DISCARDED the uncommitted edits.')
        print('      Guide 4.2 is CONTRADICTED on this machine.')
    else:
        print('\n  >>> MIXED or unexpected. Do not interpret; record the raw')
        print('      values and treat the two zones as scoping differently.')

    print(f'\nrestoring: Tempo -> {orig["tempo"]}, ScalePad1 -> {orig["scale"]}')
    try:
        link.write(*TEMPO, [int(x, 16) for x in orig['tempo'].split()])
        link.write(*SCALE_PAD, [int(x, 16) for x in orig['scale'].split()])
        time.sleep(0.4)
        print(f'  Tempo     now {hx(link.req(*TEMPO) or [])}')
        print(f'  ScalePad1 now {hx(link.req(*SCALE_PAD) or [])}')
    finally:
        STORE.unlink(missing_ok=True)


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else ''
    if arg == '1':
        phase1()
    elif arg == '2':
        phase2()
    else:
        sys.exit(__doc__)
