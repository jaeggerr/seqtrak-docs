#!/usr/bin/env python3
"""Build a one-zone .Y3S from a mono 16-bit 44.1 kHz WAV.

The missing link between find_loop.py, which picks a loop that does not click,
and content_push.py, which installs it. It starts from a real app export as a
template: the PCM, the keybank record, element 0's envelope and the name are
replaced, and +0x38 is left as it is -- the machine overwrites it on import
(verified on hardware, docs/10-verified-behaviour.md).

    ./build_y3s.py --template export.Y3S --wav note.wav --root 60 \
                   --start 22400 --length 58900 --out my-sound.Y3S

--start and --length come from find_loop.py. The start must be a multiple of 16
(it is stored divided by 16); the length is free -- do not constrain it, which
is a mistake this repository made and which cost up to eight samples of
misalignment at the join.

Without --start/--length the loop is switched off (one-shot).
"""
import argparse, array, os, struct, uuid, wave, zipfile

RATE = 44100
EBASE = 0x14A                 # base of element 0's block inside sound.bin
# attack and release at zero, sustain level held
ENV = {0x33: 0, 0x34: 97, 0x35: 64, 0x37: 0, 0x38: 0, 0x39: 127, 0x3A: 119, 0x3B: 116}
SOUND_CN, WAVE_CN = 4100, 8593        # reassigned on import anyway


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--template', required=True, help='a .Y3S exported by the official app')
    ap.add_argument('--wav', required=True, help='mono WAV (or stereo: the left channel is taken), 16-bit, 44100 Hz')
    ap.add_argument('--root', type=int, default=60, help='MIDI root key (default 60)')
    ap.add_argument('--low', type=int, default=0, help="the record's lowest key")
    ap.add_argument('--high', type=int, default=127, help="the record's highest key")
    ap.add_argument('--start', type=int, help='loop start, a multiple of 16')
    ap.add_argument('--length', type=int, help='loop length, unconstrained')
    ap.add_argument('--gain', type=float, default=1.0, help='gain applied; use ONE gain for a whole set of zones')
    ap.add_argument('--name', default='user sound')
    ap.add_argument('--release-on-key-off', dest='rel', action='store_true', default=True,
                    help='31 1p 0D = 02, the note stops at key release (default)')
    ap.add_argument('--ignore-key-off', dest='rel', action='store_false',
                    help='31 1p 0D = 00, Trigger: the note loops for ever')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    w = wave.open(a.wav)
    if w.getsampwidth() != 2 or w.getframerate() != RATE:
        raise SystemExit('16-bit at %d Hz is required' % RATE)
    ch, nf = w.getnchannels(), w.getnframes()
    d = array.array('h'); d.frombytes(w.readframes(nf))
    if ch > 1:
        d = d[0::ch]

    if a.start is not None:
        if a.start % 16:
            raise SystemExit('--start must be a multiple of 16')
        if a.length is None:
            raise SystemExit('--length is required with --start')
        n = a.start + a.length
        if n > len(d):
            raise SystemExit('the WAV is too short: %d asked for, %d available' % (n, len(d)))
    else:
        n = len(d)

    cut = d[:n]
    if a.gain != 1.0:
        cut = array.array('h', [max(-32768, min(32767, int(round(v * a.gain)))) for v in cut])
    pcm = cut.tobytes()

    z = zipfile.ZipFile(a.template)
    root_dir = z.namelist()[0].split('/')[0]
    trec = bytearray(z.read(root_dir + '/waveform0.bin')[4:68])
    sb = bytearray(z.read(root_dir + '/sound.bin'))

    trec[0x00], trec[0x01] = a.low, a.high
    trec[0x02], trec[0x03] = 0x01, 0x7F
    trec[0x08] = a.root
    trec[0x0B] = 1                                   # mono
    trec[0x0F] = 0x00 if a.start is not None else 0x01
    struct.pack_into('<I', trec, 0x24, RATE)
    struct.pack_into('<I', trec, 0x2C, (a.start // 16) if a.start is not None else 0)
    struct.pack_into('<I', trec, 0x30, n - 1)
    struct.pack_into('<I', trec, 0x3C, n)
    rec = struct.pack('<I', 1) + bytes(trec)

    for off, v in ENV.items():
        sb[EBASE + off] = v
    sb[0x88] = 0x02 if a.rel else 0x00               # 31 1p 0D Trigger/Gate Mode
    nm = a.name.encode('ascii', 'replace')[:28].ljust(28, b'\x00')
    for g in range(4):                               # the name is packed 7-into-8 in place
        sb[8 + g * 8] = 0x00
        sb[9 + g * 8:16 + g * 8] = nm[g * 7:(g + 1) * 7]
    struct.pack_into('<H', sb, 0x1E8, WAVE_CN - 8192)

    su, wu = str(uuid.uuid4()), str(uuid.uuid4())
    xml = lambda s: s.encode('utf-8')
    entries = [
        ('sound.bin', bytes(sb)),
        ('sound.xml', xml('﻿<?xml version="1.0" encoding="utf-8"?>\n<SoundData>\n'
            '  <ContentNumber>%d</ContentNumber>\n  <UUID>%s</UUID>\n  <Order>0</Order>\n'
            '  <Tag1></Tag1>\n  <Tag2></Tag2>\n  <Commercial>false</Commercial>\n'
            '  <Favorite>true</Favorite>\n</SoundData>\n' % (SOUND_CN, su))),
        ('waveform0.bin', rec),
        ('waveform0.xml', xml('<?xml version="1.0" encoding="utf-8"?>\n<WaveformData>\n'
            '  <ContentNumber>%d</ContentNumber>\n  <UUID>%s</UUID>\n  <Order>0</Order>\n'
            '  <Tag1></Tag1>\n  <Tag2></Tag2>\n  <MainCategory>3</MainCategory>\n'
            '  <SubCategory>1</SubCategory>\n  <Commercial>false</Commercial>\n</WaveformData>\n'
            % (WAVE_CN, wu))),
        ('sample0.bin', pcm),
        ('sample0.xml', xml('<?xml version="1.0" encoding="UTF-8"?>\n<SampleData>\n'
            '  <WaveformNumber>%d</WaveformNumber>\n  <KeybankNumber>0</KeybankNumber>\n'
            '  <DataSize>%d</DataSize>\n</SampleData>\n' % (WAVE_CN, len(pcm)))),
    ]
    if os.path.exists(a.out):
        os.remove(a.out)
    zo = zipfile.ZipFile(a.out, 'w', zipfile.ZIP_DEFLATED)
    for fn, data in entries:
        zo.writestr('%s/%s' % (su, fn), data)
    zo.close()
    print('wrote %s' % a.out)
    print('  %d samples, root key %d, keys %d-%d'
          % (n, a.root, a.low, a.high))
    print('  loop: %s' % ('start %d, length %d (%.3f s)'
          % (a.start, a.length, a.length / RATE) if a.start is not None else 'switched off'))
    print('  key release: %s' % ('the note stops (31 1p 0D = 02)' if a.rel
                                 else 'loops for ever (31 1p 0D = 00)'))


if __name__ == '__main__':
    main()
