"""ChangeLength (71 10 00) — the last untested song message, and its unit.

The official app's composite bound 245903 = 15 x 16384 + 143 says the data is a
scene number and a 14-bit length, 0-143. Nothing has ever sent one, and no
conversion for that 143 appears in the app.

Method, fully reversible because the scene is created for the test:
  * find the first scene index that does NOT exist (Scene Info answers with
    zero data bytes — that is an answer, not a timeout);
  * AddScene it (verified reversible on hardware);
  * read its Scene Info as the baseline;
  * send ChangeLength with a distinctive value, re-read, diff byte by byte;
  * repeat with a second value, so a byte that merely changed is told from a
    byte that TRACKS the value;
  * RemoveScene in a finally, and verify it is gone.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]


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
                if m and m[0] and m[0][0] == 0xF0 and len(m[0]) >= 9 and m[0][6] == a:
                    return m[0][9:-1]
                if not m:
                    time.sleep(0.002)
            time.sleep(0.04)
        return None

    def put(self, a, b, c, data=()):
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        time.sleep(0.08)


def ev(d):
    return "no reply" if d is None else (" ".join(f"{x:02X}" for x in d) or "(empty)")


link = Link()
ctrl = link.ask(0x30, 0x40, 0x76)
print(f"control 30 40 76 = {ev(ctrl)}")

scratch = None
for index in range(16):
    info = link.ask(0x71, 0x40, index)
    if info is None:
        print(f"scene {index}: no reply — stopping rather than guessing")
        raise SystemExit(1)
    if not info:
        scratch = index
        break
if scratch is None:
    print("ABORT: all sixteen scenes exist; this run needs a free slot")
    raise SystemExit(1)
print(f"scene {scratch} does not exist — using it as the scratch scene")

created = False
try:
    link.put(0x71, 0x00, 0x00, [scratch])
    created = True
    time.sleep(0.25)
    base = link.ask(0x71, 0x40, scratch)
    print(f"\nafter AddScene, Scene Info is {len(base or [])} bytes:\n  {ev(base)}")
    if not base:
        print("ABORT: the scene was not created")
        raise SystemExit(1)

    for length in (64, 100):
        packed = [scratch, (length >> 7) & 0x7F, length & 0x7F]
        print(f"\nChangeLength 71 10 00 {' '.join(f'{b:02X}' for b in packed)}  (length {length})")
        link.put(0x71, 0x10, 0x00, packed)
        time.sleep(0.3)
        after = link.ask(0x71, 0x40, scratch)
        if after is None:
            print("  no reply to Scene Info")
            continue
        if len(after) != len(base):
            print(f"  reply length changed: {len(base)} -> {len(after)}")
        diffs = [(i, b, a) for i, (b, a) in enumerate(zip(base, after)) if b != a]
        if not diffs:
            print("  no byte of Scene Info changed")
        for i, b, a in diffs:
            print(f"  byte {i:>2}: {b:02X} -> {a:02X}  ({b} -> {a})")
        base = after

finally:
    if created:
        link.put(0x71, 0x20, 0x00, [scratch])
        time.sleep(0.3)
        gone = link.ask(0x71, 0x40, scratch)
        print(f"\nRemoveScene: scene {scratch} now {len(gone or [])} bytes"
              f"  — {'REMOVED' if gone == [] else '*** STILL THERE ***'}")
        print(f"control {ev(link.ask(0x30, 0x40, 0x76))}")
