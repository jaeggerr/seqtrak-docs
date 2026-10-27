#!/usr/bin/env python3
"""Points 2, 3, 5 — a cumulative counter over the whole inbound stream.

The repository has had two negative claims overturned because they were read
off a scrolling log. This instrument never scrolls: it counts every byte that
arrives, per status and per SysEx address, and prints totals at the end. It
also carries its own positive control for F2 (Song Position Pointer): before
listening to the machine, it pushes an F2 through a virtual CoreMIDI port into
the same capture code, so that a count of zero afterwards means "absent from
the stream" and not "invisible to the instrument".

Read-only: nothing is ever sent to the SEQTRAK.
"""
import argparse
import collections
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C

STATUS_NAMES = {
    0xF0: 'SysEx start', 0xF1: 'MTC quarter frame', 0xF2: 'Song Position Pointer',
    0xF3: 'Song Select', 0xF6: 'Tune Request', 0xF7: 'SysEx end / EOX',
    0xF8: 'Timing Clock', 0xFA: 'Start', 0xFB: 'Continue', 0xFC: 'Stop',
    0xFE: 'Active Sensing', 0xFF: 'System Reset',
}
CHANNEL_NAMES = {
    0x80: 'Note Off', 0x90: 'Note On', 0xA0: 'Poly Aftertouch',
    0xB0: 'Control Change', 0xC0: 'Program Change', 0xD0: 'Channel Aftertouch',
    0xE0: 'Pitch Bend',
}


class Counter:
    """Cumulative tallies. Never discards, never overwrites."""

    def __init__(self):
        self.status = collections.Counter()
        self.sysex_addr = collections.Counter()
        self.sysex_values = collections.defaultdict(list)
        self.total = 0
        self.events = []          # (t, status, detail) for the timeline
        self.f2_payloads = []

    def feed(self, msg, t):
        if not msg:
            return
        self.total += 1
        st = msg[0]
        key = st if st >= 0xF0 else (st & 0xF0)
        self.status[key] += 1

        if st == 0xF2:
            # 14-bit, LSB first: position in MIDI beats (6 clocks = 1/16 note)
            pos = (msg[2] << 7) | msg[1] if len(msg) >= 3 else None
            self.f2_payloads.append((t, list(msg), pos))
            self.events.append((t, 'F2', f'SPP position={pos} raw={hx(msg)}'))
        elif st == 0xF0 and len(msg) >= 10 and msg[1] == MFR \
                and msg[3:5] == list(GROUP) and msg[5] == MODEL:
            addr = (msg[6], msg[7], msg[8])
            data = msg[9:-1]
            self.sysex_addr[addr] += 1
            self.sysex_values[addr].append(hx(data))
            self.events.append((t, 'SysEx', f'{hx(addr)} = {hx(data)}'))
        elif st in (0xFA, 0xFB, 0xFC):
            self.events.append((t, STATUS_NAMES[st], ''))
        elif (st & 0xF0) == 0xC0:
            self.events.append((t, 'ProgramChange', f'ch{(st & 0x0F) + 1} pc={msg[1]}'))

    def report(self, label, duration):
        print()
        print('=' * 72)
        print(f'{label} — {duration:.1f} s, {self.total} messages counted')
        print('=' * 72)
        print('\nPer status byte (cumulative, nothing dropped):')
        for k in sorted(self.status):
            name = STATUS_NAMES.get(k) or CHANNEL_NAMES.get(k) or '?'
            print(f'  {k:02X}  {name:<24} {self.status[k]:>7}')
        for probe in (0xF2, 0xF3, 0xF1):
            n = self.status.get(probe, 0)
            print(f'\n  >>> {probe:02X} {STATUS_NAMES[probe]}: {n} occurrence(s)')
        if self.sysex_addr:
            print('\nPer SysEx address:')
            for addr, n in sorted(self.sysex_addr.items()):
                vals = self.sysex_values[addr]
                uniq = sorted(set(vals))
                shown = ', '.join(uniq[:6]) + (' …' if len(uniq) > 6 else '')
                print(f'  {hx(addr)}  x{n:<5}  values: {shown}')


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


def positive_control():
    """Prove the capture chain counts F2 before claiming the machine sends none."""
    print('Positive control: pushing F2 through a virtual port into the same counter…')
    out = rtmidi.MidiOut()
    out.open_virtual_port('seqtrak-probe-control')
    time.sleep(0.4)

    mi = rtmidi.MidiIn()
    idx = next((i for i, n in enumerate(mi.get_ports())
                if 'seqtrak-probe-control' in n), None)
    if idx is None:
        print('  !! virtual port not visible — control INCONCLUSIVE')
        return False
    mi.open_port(idx)
    mi.ignore_types(sysex=False, timing=False, active_sense=False)
    c = Counter()
    t0 = time.time()
    mi.set_callback(lambda m, d: c.feed(m[0], time.time() - t0))
    time.sleep(0.3)

    for pos in (0, 1, 384, 16383):
        out.send_message([0xF2, pos & 0x7F, (pos >> 7) & 0x7F])
        time.sleep(0.05)
    out.send_message([0xF8])          # a timing clock too, to check nothing is filtered
    time.sleep(0.5)

    seen = c.status.get(0xF2, 0)
    clk = c.status.get(0xF8, 0)
    print(f'  F2 injected: 4, F2 counted: {seen}   |   F8 injected: 1, counted: {clk}')
    for t, raw, pos in c.f2_payloads:
        print(f'    decoded SPP position={pos} from {hx(raw)}')
    mi.close_port()
    out.close_port()
    ok = (seen == 4 and clk == 1)
    print('  control PASSED — the instrument can see F2 and F8\n' if ok
          else '  control FAILED — do not draw a negative conclusion from this run\n')
    return ok


# (seconds to hold on this cue, what the operator should do)
# There is no separate stop control: [P] is one play/stop toggle.
#
# NOTE: --cues is TIMED, and the owner found it unreadable in practice ("I do
# not even have time to read"). It is kept because it is what produced the
# documented F2 measurement and must stay reproducible. For a new experiment
# that needs gestures, prefer the self-paced pattern in point2_facade.py: print
# one step, block on input(), and let the capture run in the background. A cue
# nobody managed to follow yields an empty window that looks like a result.
CUES = [
    (6,  'IDLE — do nothing, this is the baseline'),
    (10, 'Press [P] to START. Let it run.'),
    (6,  'Press [P] again to STOP.'),
    (8,  'Press [P] START, wait ~4 s, press [P] STOP.'),
    (8,  'Press [P] START, wait ~4 s, press [P] STOP. (third time)'),
    (10, 'STOPPED: change PATTERN — 1, then 3, then 5.'),
    (10, 'Press [P] START, then change PATTERN while it plays.'),
    (6,  'Press [P] to STOP.'),
    (10, 'Enter SONG MODE.'),
    (10, 'In SONG MODE: change SCENE a few times.'),
    (10, 'Press [P] START in SONG MODE — let a scene change happen by itself.'),
    (8,  'Press [P] to STOP, then LEAVE Song mode.'),
    (6,  'IDLE again — do nothing.'),
]


def run_cues(counter, cues):
    for hold, text in cues:
        before = counter.status.get(0xF2, 0)
        print(f'>>> {text}', flush=True)
        time.sleep(hold)
        after = counter.status.get(0xF2, 0)
        mark = f'   [F2 +{after - before}]' if after > before else ''
        print(f'    …{counter.total} messages so far, F2 total {after}{mark}',
              flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=60)
    ap.add_argument('--label', default='listen')
    ap.add_argument('--timeline', action='store_true')
    ap.add_argument('--no-control', action='store_true')
    ap.add_argument('--cues', action='store_true')
    args = ap.parse_args()

    control_ok = True if args.no_control else positive_control()

    mi = rtmidi.MidiIn()
    idx = next((i for i, n in enumerate(mi.get_ports()) if 'SEQTRAK' in n), None)
    if idx is None:
        sys.exit('no SEQTRAK input port')
    mi.open_port(idx)
    mi.ignore_types(sysex=False, timing=False, active_sense=False)

    c = Counter()
    t0 = time.time()
    mi.set_callback(lambda m, d: c.feed(m[0], time.time() - t0))

    planned = sum(h for h, _ in CUES) if args.cues else args.seconds
    print(f'Listening {planned:.0f} s on "{mi.get_ports()[idx]}".')
    if args.cues:
        print('Follow the cues below. [P] is the single [power/PLAY] toggle.\n')
        run_cues(c, CUES)
    else:
        print('Manipulate the machine now.')
        for remaining in range(int(args.seconds), 0, -5):
            time.sleep(min(5, remaining))
            print(f'  {remaining:>4} s left — {c.total} messages, '
                  f'F2 so far: {c.status.get(0xF2, 0)}', flush=True)
    duration = time.time() - t0
    mi.close_port()

    c.report(args.label, duration)
    if args.timeline:
        print('\nTimeline (non-clock events):')
        for t, kind, detail in c.events:
            print(f'  {t:7.2f}  {kind:<14} {detail}')
    print(f'\npositive control for F2: {"PASSED" if control_ok else "NOT ESTABLISHED"}')


if __name__ == '__main__':
    sys.exit(main())
