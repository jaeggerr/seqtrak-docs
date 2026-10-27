"""Read-only survey of the Sound Common blocks 31 1p and 31 4p.

Nothing is written. Four attempts per address, control address 30 40 76
interleaved every eight requests. Addresses come from the reference's own CSV,
so only documented rows are asked for — a silence here is about the machine,
not about an address nobody claims exists.
"""
import csv, pathlib, sys, time
import rtmidi

HEAD = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
CSV = str(pathlib.Path(__file__).resolve().parents[2] / "data" / "parameters.csv")


class Link:
    def __init__(self):
        self.out, self.inp = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.inp.ignore_types(sysex=False, timing=True, active_sense=True)
        self.out.open_port([i for i, n in enumerate(self.out.get_ports()) if "SEQTRAK" in n][0])
        self.inp.open_port([i for i, n in enumerate(self.inp.get_ports()) if "SEQTRAK" in n][0])
        time.sleep(0.2)

    def ask(self, a, b, c, attempts=4, timeout=0.6):
        for _ in range(attempts):
            while self.inp.get_message():
                pass
            self.out.send_message(HEAD + [a, b, c, 0xF7])
            deadline = time.time() + timeout
            while time.time() < deadline:
                msg = self.inp.get_message()
                if msg and msg[0] and msg[0][0] == 0xF0:
                    d = msg[0]
                    if len(d) >= 10 and d[6:9] == [a, b, c]:
                        return d[9:-1]
                elif not msg:
                    time.sleep(0.002)
            time.sleep(0.05)
        return None


wanted = {"Sound Common / General": "1p", "Sound Common / LFO": "4p"}
rows = []
for r in csv.DictReader(open(CSV)):
    if r["address_mid"] in wanted.values() and r["block"] in wanted:
        rows.append((r["block"], int(r["address_mid"][0], 16), int(r["address_low"], 16),
                     r["parameter"][:38], int(r["size_bytes"] or 1)))

PART = 7        # SYNTH 1
link = Link()
control = 0
checks = 0
out = []
for i, (block, hi_nibble, low, name, size) in enumerate(rows):
    if i % 8 == 0:
        checks += 1
        control += link.ask(0x30, 0x40, 0x76) is not None
    mid = (hi_nibble << 4) | PART
    data = link.ask(0x31, mid, low)
    out.append((block, mid, low, name, size, data))

answered = sum(1 for *_, d in out if d is not None)
print(f"control 30 40 76: {control}/{checks}")
print(f"{answered} of {len(out)} documented addresses answered")
wrong = [(m, l, n, s, d) for _, m, l, n, s, d in out if d is not None and len(d) != s]
print(f"{len(wrong)} replies whose width is not the documented size")
for m, l, n, s, d in wrong[:12]:
    print(f"  31 {m:02X} {l:02X} {n}: size {s}, got {len(d)} bytes")
print()
for block, mid, low, name, size, data in out:
    shown = " ".join(f"{b:02X}" for b in data) if data is not None else "-- no reply"
    print(f"31 {mid:02X} {low:02X} [{size}] {name:<40} {shown}")
