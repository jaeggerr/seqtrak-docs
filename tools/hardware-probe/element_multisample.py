#!/usr/bin/env python3
"""Reassemble un instrument multi-echantillons sur une piste, en une passe.

Les ondes utilisateur restent sur la machine, mais l'affectation des elements
est de l'etat vivant : elle est perdue des qu'un son est charge sur la piste
(et Sound Save est une adresse non resolue, voir docs/08-bulk-and-files.md).
Ce script la refait. Il ecrit TOUT ce qu'un element allume a la main n'herite
pas, dans les DEUX blocs -- c'est la lecon de la session du 2026-11-24 :

    41 ep 54  Pitch Key Follow Sensitivity  64 -> 96   sinon la hauteur ne suit pas
    42 ep 0C  Filter Gain                  102 -> 127  sinon les zones sont plus douces
    42 ep 1D  FEG Depth                    104 -> 64   sinon un balayage de filtre en trop

    ./element_multisample.py                 valeurs par defaut ci-dessous
    ./element_multisample.py 44 445          premier programme, premiere onde

Les numeros par defaut sont ceux d'une machine particuliere : lisez-les avec
which_sound.py et 41 08 03 avant de vous y fier.
"""
import sys, time, rtmidi

PART = 8                      # SYNTH 2
CH   = 8                      # canal MIDI de la partie 8
PROG0 = int(sys.argv[1]) if len(sys.argv) > 1 else 44    # programme du 1er son, banque 63/32
WAVE0 = int(sys.argv[2]) if len(sys.argv) > 2 else 445   # numero de la 1re onde utilisateur

# (note de reference, note basse, note haute) -- une racine tous les 3 demi-tons,
# les deux elements extremes elargis pour que rien ne soit muet
ZONES = [(48, 0, 49), (51, 50, 52), (54, 53, 55), (57, 56, 58),
         (60, 59, 61), (63, 62, 64), (66, 65, 67), (69, 68, 127)]

BLOCK41 = {0x00: 1,    # Element Assign
           0x01: 1,    # Wave Select : onde utilisateur
           0x12: 1, 0x13: 127,          # limites de velocite
           0x2E: 100,  # Element Level
           0x2F: 84,   # Level Velocity Sensitivity
           0x33: 0,    # AEG Attack Time
           0x34: 97, 0x35: 64,          # AEG Decay 1/2 Time
           0x37: 0,    # AEG Release Time
           0x39: 127, 0x3A: 119, 0x3B: 116,   # niveaux AEG
           0x54: 96,   # Pitch Key Follow Sensitivity
           0x55: 60}   # note centrale du suivi
BLOCK42_PAIR = (0x0C, (1, 127))          # Filter Gain, 2 octets
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


# charger le premier son met l'element 0 dans un etat configure
out.send_message([0xB0 | CH, 0x00, 63]); time.sleep(0.03)
out.send_message([0xB0 | CH, 0x20, 32]); time.sleep(0.03)
out.send_message([0xC0 | CH, PROG0]);    time.sleep(0.8)
print('piste %d : %s   (temoin, piste 7 : %s)' % (PART, sound_name(), sound_name(7)))

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

print('relecture :')
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
    print('  el%d  onde %s (ref %3d)  notes %3d-%3d  54=%s  gain=%s  feg=%s  %s'
          % (e, got, root, lo, hi, kf, gain, feg, 'ok' if good else '<<< ECART'))
print('\ntout conforme :', ok)
print('temoin piste 7 onde :', req([0x41, 0x07, 0x03]), ' tempo :', req([0x30, 0x40, 0x76]))
