"""Does the machine accept a FOUR-byte Parameter Change?

The last untested write width. The sampler's trim points are the only four-byte
fields: Loop Length 50 eA 60, Start Point 50 eA 66, End Point 50 eA 6A.

Target: slot 7 ("Bongo3 High 3", the shortest at ~49 ms), Start Point, which
reads 0 on all seven factory slots. Writing a small value and restoring 0 is
exactly reversible, and 0 is not a guess — it is what was read.

Witness: the End Point of the same slot, which must not move, plus the tempo as
the control address. Restore in a finally, verified.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]

ELEMENT = 6                     # slot 7, zero-based
MID = (ELEMENT << 4) | 0x0A     # 50 6A
START, END = 0x66, 0x6A


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
            self.out.send_message(REQ + [a, b, c, 0xF7])
            deadline = time.time() + timeout
            while time.time() < deadline:
                m = self.inp.get_message()
                if m and m[0] and m[0][0] == 0xF0 and len(m[0]) >= 10 and m[0][6:9] == [a, b, c]:
                    return m[0][9:-1]
                if not m:
                    time.sleep(0.002)
            time.sleep(0.05)
        return None

    def put(self, a, b, c, data):
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        time.sleep(0.06)


def ev(d):
    return "no reply" if d is None else (" ".join(f"{x:02X}" for x in d) or "(empty)")


def val(d):
    out = 0
    for b in d or []:
        out = (out << 7) | (b & 0x7F)
    return out


link = Link()
seq = link.ask(0x01, 0x10, 0x20)
if seq is None or seq[0] != 0:
    print(f"ABORT: sequencer {ev(seq)}")
    raise SystemExit(1)
print(f"sequencer stopped; control 30 40 76 = {ev(link.ask(0x30, 0x40, 0x76))}")

original = link.ask(0x50, MID, START)
witness0 = link.ask(0x50, MID, END)
print(f"before: start {ev(original)} = {val(original)} | end (witness) {ev(witness0)} = {val(witness0)}")

if original is None or len(original) != 4:
    print("ABORT: the start point did not answer with four bytes")
    raise SystemExit(1)
if val(original) != 0:
    print("ABORT: this run only writes a start point that reads 0")
    raise SystemExit(1)

try:
    target = 128                       # 00 00 01 00 — exercises a carry
    packed = [(target >> 21) & 0x7F, (target >> 14) & 0x7F,
              (target >> 7) & 0x7F, target & 0x7F]
    print(f"\nwriting {target} as {ev(packed)}")
    link.put(0x50, MID, START, packed)
    time.sleep(0.3)
    after = link.ask(0x50, MID, START)
    w1 = link.ask(0x50, MID, END)
    print(f"  read back {ev(after)} = {val(after)}")
    if after == packed:
        print("  RESULT: the machine accepted a four-byte Parameter Change")
    elif after == original:
        print("  RESULT: ignored — the value did not change")
    else:
        print("  RESULT: changed, but not to what was sent")
    print(f"  witness moved: {w1 != witness0}  ({ev(w1)})")

finally:
    link.put(0x50, MID, START, original)
    time.sleep(0.35)
    final = link.ask(0x50, MID, START)
    wf = link.ask(0x50, MID, END)
    ctrl = link.ask(0x30, 0x40, 0x76)
    print(f"\nrestore: start {ev(final)} (was {ev(original)}) | end {ev(wf)} | control {ev(ctrl)}")
    print("RESTORED" if final == original else "*** RESTORE FAILED — CHECK SLOT 7 ***")
