#!/usr/bin/env python3
"""SEQTRAK SysEx probe — read-only by default.

  --list                         list MIDI ports
  --identity                     Universal Identity Request
  --req AH AM AL [--size N]      Parameter Request (hex bytes)
  --plan NAME                    run a named batch of read-only requests
  --watch SECONDS                passively log everything the machine emits
  --set AH AM AL VALUE [--size N]   Parameter Change  (WRITES — asks first)
"""
import argparse
import sys
import time

import rtmidi

MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


def find_ports(sub):
    mo, mi = rtmidi.MidiOut(), rtmidi.MidiIn()
    outs, ins = mo.get_ports(), mi.get_ports()
    if sub is None:
        return outs, ins, None, None
    oi = next((i for i, n in enumerate(outs) if sub.lower() in n.lower()), None)
    ii = next((i for i, n in enumerate(ins) if sub.lower() in n.lower()), None)
    return outs, ins, oi, ii


class Link:
    def __init__(self, sub):
        outs, ins, oi, ii = find_ports(sub)
        if oi is None or ii is None:
            print('ports OUT:', outs)
            print('ports IN :', ins)
            sys.exit(f'no port matching "{sub}"')
        self.name_out, self.name_in = outs[oi], ins[ii]
        self.mo, self.mi = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.mo.open_port(oi)
        self.mi.open_port(ii)
        self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.buf = []
        self.mi.set_callback(lambda msg, data: self.buf.append(msg[0]))
        time.sleep(0.2)
        self.buf.clear()

    def send(self, msg):
        self.mo.send_message(list(msg))

    def collect(self, timeout=1.5, want=1):
        end = time.time() + timeout
        got = []
        while time.time() < end:
            while self.buf:
                m = self.buf.pop(0)
                if m and m[0] == 0xF0:
                    got.append(m)
            if len(got) >= want:
                break
            time.sleep(0.01)
        return got


def param_request(ah, am, al):
    return [0xF0, MFR, 0x30, *GROUP, MODEL, ah, am, al, 0xF7]


def param_change(ah, am, al, data):
    return [0xF0, MFR, 0x10, *GROUP, MODEL, ah, am, al, *data, 0xF7]


def decode_reply(msg):
    """Return (ah, am, al, data) for a SEQTRAK parameter-change style reply."""
    if len(msg) < 10 or msg[1] != MFR:
        return None
    if msg[3:5] != list(GROUP):
        return None
    if msg[5] != MODEL:
        return None
    return msg[6], msg[7], msg[8], msg[9:-1]


def value_of(data):
    v = 0
    for b in data:
        v = (v << 7) | (b & 0x7F)
    return v


# name, ah, am, al, how to interpret, why it is worth checking
PLANS = {
    'sanity': [
        ('SpeakerMasterVolume', 0x00, 0x00, 0x00, 'int', 'known from the Data List — validates the plumbing'),
        ('HeadphoneMasterVolume', 0x00, 0x00, 0x01, 'int', 'known'),
        ('Tempo', 0x30, 0x40, 0x76, 'int', 'known, 2 bytes — validates the multi-byte encoding'),
        ('MidiClockOut', 0x00, 0x00, 0x2D, 'int', 'explains a missing F8 clock'),
        ('UsbMidiTxSysEx', 0x00, 0x00, 0x10, 'int', 'must be 1 to receive SysEx'),
    ],
    # Three targets whose behaviour is predicted, and three witnesses that must
    # NOT move: if the witnesses change too, the reading is wrong.
    'semantics': [
        ('>> HeadphonePlugStatus', 0x01, 0x10, 0x07, 'int', 'TARGET: 0 unplugged -> 1 plugged in'),
        ('>> SequencerStatus', 0x01, 0x10, 0x20, 'int', 'TARGET: 0 stopped -> 1 playing'),
        ('>> CurrentPart', 0x01, 0x10, 0x27, 'int', 'TARGET: = index of the selected track'),
        ('   witness Battery', 0x01, 0x10, 0x02, 'int', 'WITNESS: must stay stable'),
        ('   witness CurrentProject', 0x01, 0x10, 0x15, 'int', 'WITNESS: must stay at 0'),
        ('   witness Tempo', 0x30, 0x40, 0x76, 'int', 'WITNESS: must stay at 119'),
    ],
    'livestate': [
        ('FirmwareVersion', 0x01, 0x00, 0x00, 'int', 'CHECKABLE: compare with the displayed version'),
        ('CompatibleVersion', 0x01, 0x00, 0x04, 'int', 'new'),
        ('SystemStatus', 0x01, 0x10, 0x00, 'int', 'new'),
        ('Battery', 0x01, 0x10, 0x02, 'int', 'CHECKABLE: 0-100, compare with the LEDs'),
        ('HeadphonePlugStatus', 0x01, 0x10, 0x07, 'int', 'CHECKABLE: plug and unplug the headphones'),
        ('SampleMemoryUsedSize', 0x01, 0x10, 0x11, 'int', 'new'),
        ('SampleMemoryTotalSize', 0x01, 0x10, 0x13, 'int', 'new'),
        ('CurrentProject', 0x01, 0x10, 0x15, 'int', 'already known from traffic sniffing — cross-check'),
        ('GeneralMode', 0x01, 0x10, 0x17, 'int', 'new'),
        ('SequencerStatus', 0x01, 0x10, 0x20, 'int', 'CHECKABLE: press play'),
        ('CurrentPart', 0x01, 0x10, 0x27, 'int', 'CHECKABLE: change track'),
        ('MasterKnobMode', 0x01, 0x10, 0x2D, 'int', 'primary use case: see what a knob is doing'),
        ('ParameterLedMode', 0x01, 0x10, 0x2E, 'int', 'primary use case: see what a knob is doing'),
    ],
    'track0': [
        ('SoundDesignPage', 0x01, 0x10, 0x30, 'int', 'per part (p=0)'),
        ('CurrentSound', 0x01, 0x10, 0x33, 'int', 'new'),
        ('PatternKnobMode', 0x01, 0x10, 0x39, 'int', 'primary use case: see what a knob is doing'),
        ('MasterSlider1Assign', 0x01, 0x10, 0x50, 'int', 'primary use case: see what a knob is doing'),
        ('SingleSlider1Assign', 0x01, 0x10, 0x53, 'int', 'primary use case: see what a knob is doing'),
        ('SingleSlider1ControlValue', 0x01, 0x10, 0x5C, 'int', 'primary use case: see what a knob is doing'),
    ],
    'scales': [
        ('Scale1NoteOfPad1', 0x30, 0x4D, 0x00, 'int', 'user scale 1, pad 1'),
        ('Scale1NoteOfPad2', 0x30, 0x4D, 0x01, 'int', 'scale 1, pad 2'),
        ('Scale2NoteOfPad1', 0x30, 0x4D, 0x10, 'int', 'scale 2, pad 1'),
        ('Scale8NoteOfPad7', 0x30, 0x4D, 0x76, 'int', 'last entry'),
    ],
    'steprec': [
        ('StepNoteInfo t0 s0', 0x70, 0x40, 0x00, 'raw', 'note info for step 0, part 0'),
        ('StepNoteInfo t0 s1', 0x70, 0x40, 0x01, 'raw', 'step 1'),
        ('StepParamInfo t0 s0', 0x70, 0x50, 0x00, 'raw', 'parameter info for step 0'),
        ('StepCondLock t0 s0', 0x70, 0x60, 0x00, 'raw', 'conditional lock for step 0'),
    ],
    'wifi': [
        ('WiFiMode', 0x00, 0x60, 0x00, 'int', 'new'),
        ('WiFiReady', 0x00, 0x60, 0x01, 'int', 'new'),
        ('WirelessLAN', 0x00, 0x00, 0x16, 'int', 'known from the Data List'),
    ],
    'song': [
        ('Song CurrentScene', 0x71, 0x10, 0x04, 'raw', 'song mode, new'),
        ('Song PlayMode', 0x71, 0x10, 0x06, 'raw', 'new'),
        ('Song SceneMode', 0x71, 0x50, 0x00, 'raw', 'new'),
    ],
}


def run_plan(link, name, timeout):
    rows = PLANS[name]
    print(f'\n=== plan "{name}" — {len(rows)} READ-ONLY requests ===')
    print(f'{"parameter":28s} {"address":10s} {"reply":30s} {"value":>10s}  note')
    ok = 0
    for label, ah, am, al, kind, why in rows:
        # An isolated request is occasionally lost (observed on hardware): retry.
        hit, got = None, []
        for _ in range(4):
            link.buf.clear()
            link.send(param_request(ah, am, al))
            got = link.collect(timeout)
            for m in got:
                d = decode_reply(m)
                if d and (d[0], d[1], d[2]) == (ah, am, al):
                    hit = d
                    break
            if hit:
                break
        addr = f'{ah:02X} {am:02X} {al:02X}'
        if hit:
            ok += 1
            data = hit[3]
            val = value_of(data) if kind == 'int' else ''
            print(f'{label:28s} {addr:10s} {hx(data):30s} {str(val):>10s}  {why}')
        else:
            extra = f'  (recu: {len(got)} autre(s) SysEx)' if got else ''
            print(f'{label:28s} {addr:10s} {"— aucune reponse —":30s} {"":>10s}  {why}{extra}')
    print(f'\n{ok}/{len(rows)} adresses ont repondu')
    return ok, len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--port', default='SEQTRAK')
    ap.add_argument('--identity', action='store_true')
    ap.add_argument('--req', nargs=3)
    ap.add_argument('--plan')
    ap.add_argument('--all-plans', action='store_true')
    ap.add_argument('--watch', type=float)
    ap.add_argument('--timeline', action='store_true')
    ap.add_argument('--set', nargs=4)
    ap.add_argument('--size', type=int, default=1)
    ap.add_argument('--timeout', type=float, default=1.5)
    a = ap.parse_args()

    if a.list:
        outs, ins, _, _ = find_ports(None)
        print('ports MIDI OUT :')
        for i, n in enumerate(outs):
            print(f'  [{i}] {n}')
        print('ports MIDI IN  :')
        for i, n in enumerate(ins):
            print(f'  [{i}] {n}')
        if not outs and not ins:
            print('  (none)')
        return

    link = Link(a.port)
    print(f'OUT → {link.name_out}\nIN  ← {link.name_in}')

    if a.identity:
        expected = '[F0 7E 7F 06 02 43 00 41 64 06 xx 00 yy 7F F7]'
        link.buf.clear()
        link.send([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7])
        got = link.collect(a.timeout)
        print(f'\nIdentity Request envoye : F0 7E 7F 06 01 F7')
        print(f'expected pattern (read from the official app): {expected}')
        if not got:
            print('aucune reponse')
        for m in got:
            print(f'recu ({len(m)} o.) : {hx(m)}')
            if len(m) == 15 and m[:10] == [0xF0, 0x7E, 0x7F, 0x06, 0x02, 0x43, 0x00, 0x41, 0x64, 0x06]:
                print(f'  ✓ matches the pattern; byte 10 = {m[10]:#02x}, '
                      f'byte 12 = {m[12]:#02x}, tail = {m[13]:02X} {m[14]:02X}')
            else:
                print('  ✗ does not match the expected pattern')
        return

    if a.watch:
        print(f'\npassive listen for {a.watch} s — go and play with the machine...')
        link.buf.clear()
        t0 = time.time()
        end = t0 + a.watch
        seen, chan, events = {}, {}, []
        n = 0
        while time.time() < end:
            while link.buf:
                m = link.buf.pop(0)
                if not m:
                    continue
                n += 1
                t = time.time() - t0
                if m[0] == 0xF0:
                    d = decode_reply(m)
                    if d:
                        k = (d[0], d[1], d[2])
                        seen.setdefault(k, []).append(hx(d[3]))
                        events.append((t, 'SYSEX', f'{k[0]:02X} {k[1]:02X} {k[2]:02X}',
                                       hx(d[3])))
                    else:
                        seen.setdefault(('?',), []).append(hx(m))
                        events.append((t, 'SYSEX?', '-', hx(m)[:40]))
                else:
                    st = m[0] & 0xF0
                    ch = (m[0] & 0x0F) + 1
                    kind = {0x80: 'NoteOff', 0x90: 'NoteOn', 0xA0: 'AfterTouch',
                            0xB0: 'CC', 0xC0: 'ProgramChange', 0xD0: 'ChanPressure',
                            0xE0: 'PitchBend'}.get(st)
                    if kind is None:
                        kind = {0xFA: 'Start', 0xFB: 'Continue', 0xFC: 'Stop',
                                0xF8: 'Clock', 0xFE: 'ActiveSense'}.get(m[0], f'{m[0]:02X}')
                        chan.setdefault((kind, None), 0)
                        chan[(kind, None)] += 1
                        events.append((t, kind, '-', hx(m)))
                    else:
                        if kind == 'NoteOn' and len(m) > 2 and m[2] == 0:
                            kind = 'NoteOff'
                        key = (kind, ch)
                        chan.setdefault(key, 0)
                        chan[key] += 1
                        events.append((t, kind, f'ch{ch}', hx(m[1:])))
            time.sleep(0.005)

        print(f'\n{n} messages in total\n')
        print(f'--- SysEx : {len(seen)} adresses distinctes ---')
        for k, vals in sorted(seen.items(), key=lambda kv: str(kv[0])):
            if k == ('?',):
                print(f'  non SEQTRAK            x{len(vals):<4d} ex. {vals[0][:60]}')
            else:
                uniq = list(dict.fromkeys(vals))
                print(f'  {k[0]:02X} {k[1]:02X} {k[2]:02X}  x{len(vals):<4d} '
                      f'{len(uniq)} distinct value(s): '
                      f'{", ".join(uniq[:8])}{" …" if len(uniq) > 8 else ""}')
        print(f'\n--- canaux / temps reel ---')
        for (kind, ch), c in sorted(chan.items(), key=lambda kv: -kv[1]):
            print(f'  {kind:14s} {("ch" + str(ch)) if ch else "":6s} x{c}')

        if a.timeline:
            print(f'\n--- chronologie ({len(events)} evenements) ---')
            last = None
            for t, kind, where, data in events:
                gap = '' if last is None or t - last < 0.8 else '   <<< pause'
                print(f'  {t:6.2f}s  {kind:14s} {where:10s} {data}{gap}')
                last = t
        return

    if a.req:
        ah, am, al = (int(x, 16) for x in a.req)
        link.buf.clear()
        link.send(param_request(ah, am, al))
        got = link.collect(a.timeout)
        print(f'\nrequete {ah:02X} {am:02X} {al:02X}')
        if not got:
            print('aucune reponse')
        for m in got:
            d = decode_reply(m)
            print(f'  {hx(m)}')
            if d:
                print(f'  → address {d[0]:02X} {d[1]:02X} {d[2]:02X}  '
                      f'data [{hx(d[3])}]  value {value_of(d[3])}')
        return

    if a.all_plans:
        tot_ok = tot = 0
        for name in PLANS:
            o, t = run_plan(link, name, a.timeout)
            tot_ok += o
            tot += t
        print(f'\n########  TOTAL : {tot_ok}/{tot}  ########')
        return

    if a.plan:
        run_plan(link, a.plan, a.timeout)
        return

    if a.set:
        ah, am, al = (int(x, 16) for x in a.set[:3])
        val = int(a.set[3], 0)
        data = [(val >> (7 * (a.size - 1 - i))) & 0x7F for i in range(a.size)]
        msg = param_change(ah, am, al, data)
        print(f'\nECRITURE : {hx(msg)}')
        link.send(msg)
        print('envoye')
        return

    ap.print_help()


main()
