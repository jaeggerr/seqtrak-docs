#!/usr/bin/env python3
"""Trouve la boucle la plus silencieuse par APPARIEMENT DE FORME D'ONDE.

Un nombre entier de periodes de la fondamentale ne suffit pas : le timbre porte
des partiels desaccordes, donc rien ne se raccorde a cette periode-la. On
cherche la longueur qui fait coincider la forme d'onde avant le depart et la
forme d'onde avant la fin -- ce que l'oreille juge au bouclage.

Seul le DEPART doit etre un multiple de 16 (il est stocke divise par 16). La
longueur est libre : la contrainte que je m'etais imposee coutait jusqu'a huit
echantillons de desalignement.
"""
import numpy as np, wave, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RATE = 44100
NOTES = [int(x) for x in sys.argv[1:]] or [48, 51, 54, 57, 60, 63, 66, 69]
LMIN, LMAX = int(0.20*RATE), int(1.40*RATE)
WC, WF = 512, 4096          # fenetres de correlation, grossiere puis fine

def mono(note):
    w = wave.open(os.path.join(HERE, 'long%d.wav' % note))
    ch, nf = w.getnchannels(), w.getnframes()
    a = np.frombuffer(w.readframes(nf), dtype='<i2').astype(np.float64)
    return a[0::ch] if ch > 1 else a

def corr(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na*nb)) if na and nb else -1.0

out = {}
print('%-5s %-8s %-9s %-8s %-9s %s' % ('note','depart','longueur','duree','corr','saut'))
for note in NOTES:
    d = mono(note)
    best = None
    for start in range(int(0.45*RATE)//16*16, int(0.95*RATE), 16*16):
        ref_c = d[start-WC:start]
        ref_f = d[start-WF:start]
        # passe grossiere
        cands = []
        for L in range(LMIN, LMAX, 8):
            e = start + L
            if e + 8 > len(d): break
            cands.append((corr(ref_c, d[e-WC:e]), L))
        cands.sort(reverse=True)
        # passe fine autour des meilleures
        for _, L0 in cands[:12]:
            for L in range(L0-16, L0+17):
                e = start + L
                if e > len(d) or e-WF < start: continue
                c = corr(ref_f, d[e-WF:e])
                jump = abs(d[start] - d[e-1])
                score = c - jump/32768.0*0.15
                if best is None or score > best[0]:
                    best = (score, c, start, L, jump)
    score, c, start, L, jump = best
    out[str(note)] = [int(start), int(L)]
    print('%-5d %-8d %-9d %.3f s  %.4f    %5d' % (note, start, L, L/RATE, c, jump))
json.dump(out, open(os.path.join(HERE, 'loops2.json'), 'w'))
