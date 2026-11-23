#!/usr/bin/env python3
"""Dit quel son est charge sur chaque piste, y compris les sons utilisateur.

Lecture seule : une Parameter Request par piste sur 01 1p 35
(CurrentSoundName), 100 octets empaquetes 7-dans-8. Quatre tentatives par
adresse, tempo lu en controle avant et apres, port garde ouvert.

    ./which_sound.py            toutes les pistes
    ./which_sound.py 8          une seule (0 = KICK ... 10 = SAMPLER)

01 1p 33 (CurrentSound) ne sert a rien ici : il lit 00 00 des qu'un son
utilisateur est charge, et il n'est pas ecrivable.
"""
import sys, time, rtmidi

TRACKS = ['KICK', 'SNARE', 'CLAP', 'HAT 1', 'HAT 2', 'PERC 1', 'PERC 2',
          'SYNTH 1', 'SYNTH 2', 'DX', 'SAMPLER']

out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
out.open_port(next(i for i, n in enumerate(out.get_ports()) if 'SEQTRAK' in n))
inp.open_port(next(i for i, n in enumerate(inp.get_ports()) if 'SEQTRAK' in n))
inp.ignore_types(sysex=False, timing=True, active_sense=True)


def unpack7(d):
    """7-dans-8, MSB d'abord ; le dernier groupe partiel porte de vraies donnees."""
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
    """Une Parameter Request, reessayee : une absence de reponse n'est pas une information."""
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
print('tempo (controle) :', req([0x30, 0x40, 0x76]))
for p in parts:
    nm = sound_name(p)
    print(f'{p:2d} {TRACKS[p]:8s} {nm if nm is not None else "(pas de reponse)"}')
print('tempo (controle) :', req([0x30, 0x40, 0x76]))
