#!/usr/bin/env python3
"""Find the quietest loop in a rendered note by WAVEFORM MATCHING.

An integer number of periods of the fundamental is not enough: the tone carries
detuned partials, so nothing lines up at that period and the loop clicks. What
is wanted is the length that makes the waveform before the loop start coincide
with the waveform before the end -- which is what the ear judges at the join.

Only the START has to be a multiple of 16 (it is stored divided by 16). The
LENGTH is free: constraining it to 16 as well, as this repository once did,
costs up to eight samples of misalignment at the join.
"""
import numpy as np, wave, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RATE = 44100
NOTES = [int(x) for x in sys.argv[1:]] or [48, 51, 54, 57, 60, 63, 66, 69]
LMIN, LMAX = int(0.20*RATE), int(1.40*RATE)
WC, WF = 512, 4096          # correlation windows, coarse then fine

def mono(note):
    w = wave.open(os.path.join(HERE, 'long%d.wav' % note))
    ch, nf = w.getnchannels(), w.getnframes()
    a = np.frombuffer(w.readframes(nf), dtype='<i2').astype(np.float64)
    return a[0::ch] if ch > 1 else a

def corr(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na*nb)) if na and nb else -1.0

out = {}
print('%-5s %-8s %-9s %-8s %-9s %s' % ('note','start','length','secs','corr','jump'))
for note in NOTES:
    d = mono(note)
    best = None
    for start in range(int(0.45*RATE)//16*16, int(0.95*RATE), 16*16):
        ref_c = d[start-WC:start]
        ref_f = d[start-WF:start]
        # coarse pass
        cands = []
        for L in range(LMIN, LMAX, 8):
            e = start + L
            if e + 8 > len(d): break
            cands.append((corr(ref_c, d[e-WC:e]), L))
        cands.sort(reverse=True)
        # fine pass around the best candidates
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
