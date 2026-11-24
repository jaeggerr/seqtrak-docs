#!/usr/bin/env python3
"""Say which sound is loaded on each track, user sounds included.

Read-only: one Parameter Request per track on 01 1p 35 (CurrentSoundName),
100 bytes packed 7-into-8. Four attempts per address, the tempo read as a
control before and after, one port held open.

    ./which_sound.py            every track
    ./which_sound.py 8          one of them (0 = KICK ... 10 = SAMPLER)

01 1p 33 (CurrentSound) is no use here: it reads 00 00 as soon as a user sound
is loaded, and it is not writable.
"""
import sys, time, rtmidi

TRACKS = ['KICK', 'SNARE', 'CLAP', 'HAT 1', 'HAT 2', 'PERC 1', 'PERC 2',
          'SYNTH 1', 'SYNTH 2', 'DX', 'SAMPLER']

out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i, n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i, n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)


def unpack7(d):
    """7-into-8, MSB first; the final partial group carries real data."""
    o = bytearray()
    for i in range(0, len(d), 8):
        g = d[i:i + 8]
        if not g:
            break
        h = g[0]
        for k, v in enumerate(g[1:]):
            o.append(v | (((h >> (6 - k)) & 1) << 7))
    return bytes(o)


def req(addr, tries=4, wait=1.2):
    """One Parameter Request, retried: a missing reply is never information."""
    pre = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C] + addr
    for _ in range(tries):
        while inp.get_message():
            pass
        out.send_message([0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C] + addr + [0xF7])
        t0 = time.time()
        while time.time() - t0 < wait:
            m = inp.get_message()
            if m:
                d = list(m[0])
                if d[:9] == pre:
                    return d[9:-1]
                if d[0] == 0xF0 and d[1] == 0x43 and (d[2] & 0xF0) == 0x00 and d[8:11] == addr:
                    return d[11:-2]
            else:
                time.sleep(0.002)
        time.sleep(0.04)
    return None


def sound_name(part):
    v = req([0x01, 0x10 | part, 0x35])
    if not v or len(v) < 9:
        return None
    return unpack7(bytes(v)).split(b'\0')[0].decode('utf8', 'replace')


parts = [int(sys.argv[1])] if len(sys.argv) > 1 else range(11)
print('tempo (control):', req([0x30, 0x40, 0x76]))
for p in parts:
    nm = sound_name(p)
    print(f'{p:2d} {TRACKS[p]:8s} {nm if nm is not None else "(no reply)"}')
print('tempo (control):', req([0x30, 0x40, 0x76]))
