#!/usr/bin/env python3
"""Build a .Y3S with ONE KEYBANK PER SEMITONE over a note range.

Generalises build_kb.py, which had its eight zones written out by hand. Each
root covers exactly its own semitone; the lowest root is widened down to key 0
and the highest up to key 127 so nothing is silent.

    build_hq.py <lo> <hi> <name>

One common gain across the whole set, never a per-sample normalisation: the
engine's level falls with pitch and normalising each sample inverts that
contour into a rising ramp (docs/10, "Normalising each zone to the same peak
is a mistake").
"""
import zipfile, struct, wave, uuid, array, os, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LO = int(sys.argv[1]) if len(sys.argv) > 1 else 21
HI = int(sys.argv[2]) if len(sys.argv) > 2 else 87
NAME = sys.argv[3] if len(sys.argv) > 3 else "clavi-hq"
TEMPLATE = os.path.expanduser("~/Downloads/clavioline-sustain.Y3S")
OUT = os.path.expanduser("~/Downloads/%s.Y3S" % NAME)
RATE, PEAK, EBASE = 44100, 27000, 0x14A
# 0x37 is AEGReleaseTime. build_kb.py wrote 0; 83 is what a working user sound
# carries, so 83 is used here. A release of 0 was briefly blamed for a silent
# package and that was WRONG -- the silence survives 83 (docs/10, "a
# 52-keybank waveform does not play"). This value is alignment with a known
# good sound, not a fix for anything.
ENV = {0x33: 0, 0x34: 97, 0x35: 64, 0x37: 83, 0x38: 0, 0x39: 127, 0x3A: 119,
       0x3B: 116}
SOUND_CN, WAVE_CN = 4100, 8593
LOOPS = json.load(open(os.path.join(HERE, "loops2.json")))

roots = [n for n in range(LO, HI + 1) if str(n) in LOOPS]
if len(roots) != HI - LO + 1:
    missing = [n for n in range(LO, HI + 1) if str(n) not in LOOPS]
    raise SystemExit("no loop for notes %s -- run find_loop.py for them" % missing)
ZONES = []
for i, r in enumerate(roots):
    lo = 0 if i == 0 else r
    hi = 127 if i == len(roots) - 1 else r
    ZONES.append((r, lo, hi))

_tz = zipfile.ZipFile(TEMPLATE)
TREC = _tz.read([n for n in _tz.namelist() if n.endswith("waveform0.bin")][0])[4:68]
TSND = _tz.read([n for n in _tz.namelist() if n.endswith("sound.bin")][0])


def mono(note):
    w = wave.open(os.path.join(HERE, "long%d.wav" % note))
    ch, nf = w.getnchannels(), w.getnframes()
    a = array.array("h")
    a.frombytes(w.readframes(nf))
    return a[0::ch] if ch > 1 else a


cuts = []
for root, lo, hi in ZONES:
    d = mono(root)
    start, L = LOOPS[str(root)]
    cuts.append((root, lo, hi, start, L, d[:start + L]))

gmax = max(max(max(c[5]), -min(c[5])) for c in cuts)
gain = PEAK / gmax
print("%d zones, roots %d-%d, one common gain %.4f" % (len(ZONES), LO, HI, gain))

records, samples = bytearray(), []
for root, lo, hi, start, L, cut in cuts:
    pcm = array.array("h", [max(-32768, min(32767, int(round(v * gain))))
                            for v in cut]).tobytes()
    n = start + L
    r = bytearray(TREC)
    r[0x00], r[0x01] = lo, hi
    r[0x02], r[0x03] = 0x01, 0x7F
    r[0x08] = root
    r[0x0B] = 1                      # the machine overwrites this with the count
    r[0x0F] = 0x00                   # loop, not one-shot
    struct.pack_into("<I", r, 0x24, RATE)
    struct.pack_into("<I", r, 0x2C, start // 16)
    struct.pack_into("<I", r, 0x30, n - 1)
    struct.pack_into("<I", r, 0x3C, n)
    records += r
    samples.append(pcm)
rec = struct.pack("<I", len(ZONES)) + bytes(records)

sb = bytearray(TSND)
for off, v in ENV.items():
    sb[EBASE + off] = v
sb[0x88] = 0x02                      # stop at key release
nm = NAME.encode("ascii")[:28].ljust(28, b"\x00")
for g in range(4):
    sb[8 + g * 8] = 0x00
    sb[9 + g * 8:16 + g * 8] = nm[g * 7:(g + 1) * 7]
struct.pack_into("<H", sb, 0x1E8, WAVE_CN - 8192)

su, wu = str(uuid.uuid4()), str(uuid.uuid4())
SX = ('﻿<?xml version="1.0" encoding="utf-8"?>\n<SoundData>\n'
      '  <ContentNumber>%d</ContentNumber>\n  <UUID>%s</UUID>\n  <Order>0</Order>\n'
      '  <Tag1></Tag1>\n  <Tag2></Tag2>\n  <Commercial>false</Commercial>\n'
      '  <Favorite>true</Favorite>\n</SoundData>\n') % (SOUND_CN, su)
WX = ('<?xml version="1.0" encoding="utf-8"?>\n<WaveformData>\n'
      '  <ContentNumber>%d</ContentNumber>\n  <UUID>%s</UUID>\n  <Order>0</Order>\n'
      '  <Tag1></Tag1>\n  <Tag2></Tag2>\n  <MainCategory>3</MainCategory>\n'
      '  <SubCategory>1</SubCategory>\n  <Commercial>false</Commercial>\n'
      '</WaveformData>\n') % (WAVE_CN, wu)
ent = [("sound.bin", bytes(sb)), ("sound.xml", SX.encode()),
       ("waveform0.bin", rec), ("waveform0.xml", WX.encode())]
for i, p in enumerate(samples):
    ent.append(("sample%d.bin" % i, p))
    ent.append(("sample%d.xml" % i,
                ('<?xml version="1.0" encoding="UTF-8"?>\n<SampleData>\n'
                 '  <WaveformNumber>%d</WaveformNumber>\n'
                 '  <KeybankNumber>%d</KeybankNumber>\n'
                 '  <DataSize>%d</DataSize>\n</SampleData>\n'
                 % (WAVE_CN, i, len(p))).encode()))
if os.path.exists(OUT):
    os.remove(OUT)
zo = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
for fn, data in ent:
    zo.writestr("%s/%s" % (su, fn), data)
zo.close()
total = sum(len(s) for s in samples)
print("wrote %s" % OUT)
print("  %d keybanks, %d B of PCM (%.2f MB), record table %d B"
      % (len(ZONES), total, total / 1e6, len(rec)))
