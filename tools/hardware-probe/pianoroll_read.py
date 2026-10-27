"""Read the synth piano roll, read-only, to see what is already there.

75 ((t<<4)|(idx>>7)) (idx&7F) — the synth block counts its own four tracks
from zero: SYNTH 1 = 0, SYNTH 2 = 1, DX = 2, SAMPLER = 3.
Nothing is written.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]


class Link:
    def __init__(self):
        self.out, self.inp = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.inp.ignore_types(sysex=False, timing=True, active_sense=True)
        self.out.open_port([i for i, n in enumerate(self.out.get_ports()) if "SEQTRAK" in n][0])
        self.inp.open_port([i for i, n in enumerate(self.inp.get_ports()) if "SEQTRAK" in n][0])
        time.sleep(0.2)

    def ask(self, a, b, c, attempts=4, timeout=0.5):
        for _ in range(attempts):
            while self.inp.get_message():
                pass
            self.out.send_message(REQ + [a, b, c, 0xF7])
            deadline = time.time() + timeout
            while time.time() < deadline:
                m = self.inp.get_message()
                if m and m[0] and m[0][0] == 0xF0:
                    d = m[0]
                    if len(d) >= 9 and d[6] == a:
                        return d[9:-1]
                elif not m:
                    time.sleep(0.002)
            time.sleep(0.03)
        return None


def ev(d):
    if d is None:
        return "no reply"
    if not d:
        return "(empty)"
    return " ".join(f"{x:02X}" for x in d)


link = Link()
print("control 30 40 76:", ev(link.ask(0x30, 0x40, 0x76)))
for local, name in ((0, "SYNTH 1"), (1, "SYNTH 2"), (2, "DX"), (3, "SAMPLER")):
    print(f"\n=== {name} (local {local}) ===")
    found = 0
    for idx in range(24):
        mid = (local << 4) | (idx >> 7)
        data = link.ask(0x75, mid, idx & 0x7F)
        if data is None:
            print(f"  idx {idx:>2}: no reply")
            break
        if not data:
            print(f"  idx {idx:>2}: empty — end of list")
            break
        found += 1
        if len(data) >= 9:
            etype, part = data[0], data[1]
            t = (data[2] << 8) | data[3]
            note, onv, offv = data[4], data[5], data[6]
            gate = (data[7] << 8) | data[8]
            print(f"  idx {idx:>2}: type {etype} part {part} time {t:>5} "
                  f"note {note:>3} vel {onv:>3}/{offv:>3} gate {gate:>5}   [{ev(data)}]")
        else:
            print(f"  idx {idx:>2}: {ev(data)}")
    print(f"  -> {found} event(s) read")
