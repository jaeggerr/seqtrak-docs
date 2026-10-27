"""Read any named parameter block, read-only, and check each reply's width.

    python3 block_read.py "Project Common / Send Reverb" ["another block" ...]
    python3 block_read.py --part 7 "Sound Common / General"

Addresses come from the reference's own CSV, so only rows the reference claims
exist are asked for: a silence here is about the machine, not about an address
nobody documents. Four attempts each, control address 30 40 76 interleaved
every eight requests. Nothing is written.
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


def resolve_mid(text, part, element):
    """A mid byte that may carry a part, element or operator placeholder."""
    if all(ch in "0123456789ABCDEF" for ch in text):
        return int(text, 16)
    hi, lo = text[0], text[1]
    high = int(hi, 16) if hi in "0123456789ABCDEF" else {"e": element}.get(hi)
    low = int(lo, 16) if lo in "0123456789ABCDEF" else {"p": part, "e": element}.get(lo)
    if high is None or low is None:
        return None
    return (high << 4) | low


def main():
    args = sys.argv[1:]
    part = element = 0
    while args and args[0].startswith("--"):
        flag, value, args = args[0], args[1], args[2:]
        if flag == "--part":
            part = int(value)
        elif flag == "--element":
            element = int(value)
    if not args:
        print(__doc__)
        return

    rows = []
    for r in csv.DictReader(open(CSV)):
        if r["block"] in args:
            mid = resolve_mid(r["address_mid"], part, element)
            if mid is None:
                continue
            rows.append((r["block"], int(r["address_high"], 16), mid,
                         int(r["address_low"], 16), r["parameter"][:40],
                         int(r["size_bytes"] or 1)))
    if not rows:
        print(f"no rows for {args}")
        return

    link = Link()
    control = checks = 0
    out = []
    for i, (block, high, mid, low, name, size) in enumerate(rows):
        if i % 8 == 0:
            checks += 1
            control += link.ask(0x30, 0x40, 0x76) is not None
        out.append((block, high, mid, low, name, size, link.ask(high, mid, low)))

    answered = sum(1 for *_, d in out if d is not None)
    wrong = [x for x in out if x[6] is not None and len(x[6]) != x[5]]
    print(f"control 30 40 76: {control}/{checks}")
    print(f"{answered} of {len(out)} documented addresses answered")
    print(f"{len(wrong)} replies whose width is not the documented size")
    for block, high, mid, low, name, size, data in wrong[:12]:
        print(f"  {high:02X} {mid:02X} {low:02X} {name}: size {size}, got {len(data)}")
    print()
    for block, high, mid, low, name, size, data in out:
        shown = " ".join(f"{b:02X}" for b in data) if data is not None else "-- no reply"
        print(f"{high:02X} {mid:02X} {low:02X} [{size}] {name:<42} {shown}")


main()
