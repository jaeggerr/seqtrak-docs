#!/usr/bin/env python3
"""Reassemble un instrument multi-echantillons sur une piste, en une passe.

The user waveforms stay on the machine, but the element assignment is live
state: it is lost the moment a sound is loaded onto the part (and Sound Save is
an unresolved address, see docs/08-bulk-and-files.md). This script redoes it.

It writes EVERYTHING an element switched on by hand does not inherit, in BOTH
blocks -- the lesson of the 2026-11-24 session:

    41 ep 54  Pitch Key Follow Sensitivity  64 -> 96   or the pitch will not track
    42 ep 0C  Filter Gain                  102 -> 127  or the zones are quieter
    42 ep 1D  FEG Depth                    104 -> 64   or you get an extra filter sweep

    ./element_multisample.py                 the defaults below
    ./element_multisample.py 44 445          first program, first wave

The default numbers are one particular machine's: read yours with
which_sound.py and 41 08 03 before relying on them.
"""
import sys, time, rtmidi

PART = 8                      # SYNTH 2
CH   = 8                      # canal MIDI de la partie 8
PROG0 = int(sys.argv[1]) if len(sys.argv) > 1 else 52    # program of the first sound, bank 63/32
WAVE0 = int(sys.argv[2]) if len(sys.argv) > 2 else 453   # number of the first user wave

# (root note, low note, high note) -- a root every 3 semitones, with the two
# outer elements widened so that nothing is silent
ZONES = [(48, 0, 49), (51, 50, 52), (54, 53, 55), (57, 56, 58),
         (60, 59, 61), (63, 62, 64), (66, 65, 67), (69, 68, 127)]

BLOCK41 = {0x00: 1,    # Element Assign
           0x01: 1,    # Wave Select: user wave
           0x12: 1, 0x13: 127,          # velocity limits
           0x2E: 100,  # Element Level
           0x2F: 84,   # Level Velocity Sensitivity
           0x33: 0,    # AEG Attack Time
           0x34: 97, 0x35: 64,          # AEG Decay 1/2 Time
           0x37: 0,    # AEG Release Time
           0x39: 127, 0x3A: 119, 0x3B: 116,   # AEG levels
           0x54: 96,   # Pitch Key Follow Sensitivity
           0x55: 60}   # centre note of the tracking
BLOCK42_PAIR = (0x0C, (1, 127))          # Filter Gain, 2 bytes
BLOCK42 = {0x1D: 64}                     # FEG Depth

out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i, n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i, n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)


def unpack7(d):
    o = bytearray()
    for i in range(0, len(d), 8):
        g = d[i:i+8]
        if not g:
            break
        h = g[0]
        for k, v in enumerate(g[1:]):
            o.append(v | (((h >> (6-k)) & 1) << 7))
    return bytes(o)


def req(addr, tries=4, wait=1.2):
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


def write(addr, *vals):
    out.send_message([0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C] + addr + list(vals) + [0xF7])
    time.sleep(0.045)


def sound_name(part=PART):
    v = req([0x01, 0x10 | part, 0x35])
    return unpack7(bytes(v)).split(b'\0')[0].decode('utf8', 'replace') if v and len(v) > 8 else None


# loading the first sound puts element 0 into a configured state
out.send_message([0xB0 | CH, 0x00, 63]); time.sleep(0.03)
out.send_message([0xB0 | CH, 0x20, 32]); time.sleep(0.03)
out.send_message([0xC0 | CH, PROG0]);    time.sleep(0.8)
print('part %d: %s   (witness, part 7: %s)' % (PART, sound_name(), sound_name(7)))

for e, (root, lo, hi) in enumerate(ZONES):
    m41 = (e << 4) | PART
    for off, v in BLOCK41.items():
        write([0x41, m41, off], v)
    write([0x41, m41, 0x10], lo)
    write([0x41, m41, 0x11], hi)
    wave = WAVE0 + e
    write([0x41, m41, 0x03], (wave >> 7) & 0x7F, wave & 0x7F)
    off, vals = BLOCK42_PAIR
    write([0x42, m41, off], *vals)
    for off, v in BLOCK42.items():
        write([0x42, m41, off], v)

print('read back:')
ok = True
for e, (root, lo, hi) in enumerate(ZONES):
    m = (e << 4) | PART
    wn = req([0x41, m, 0x03])
    got = (wn[0] << 7 | wn[1]) if wn and len(wn) == 2 else None
    want = WAVE0 + e
    kf, gain, feg = req([0x41, m, 0x54]), req([0x42, m, 0x0C]), req([0x42, m, 0x1D])
    good = (got == want and kf == [96] and gain == [1, 127] and feg == [64]
            and req([0x41, m, 0x10]) == [lo] and req([0x41, m, 0x11]) == [hi])
    ok &= good
    print('  el%d  wave %s (root %3d)  notes %3d-%3d  54=%s  gain=%s  feg=%s  %s'
          % (e, got, root, lo, hi, kf, gain, feg, 'ok' if good else '<<< MISMATCH'))
print('\nall as written:', ok)
print('witness part 7 wave:', req([0x41, 0x07, 0x03]), ' tempo:', req([0x30, 0x40, 0x76]))
