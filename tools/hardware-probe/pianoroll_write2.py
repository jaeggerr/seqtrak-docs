"""Confirm the melodic write, and chase the index lookup (76).

Run 1 showed the add works and that the READ reply is 8 bytes — the same shape
as the write payload — not the 9 the reference describes. This run:
  * writes two notes and checks both indices;
  * tries 76 with retries, logging every SysEx that arrives, because "no reply"
    after one attempt is not information;
  * deletes both, highest index first, in a finally.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]
LOCAL, OTHER = 0, 2


class Link:
    def __init__(self):
        self.out, self.inp = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.inp.ignore_types(sysex=False, timing=True, active_sense=True)
        self.out.open_port([i for i, n in enumerate(self.out.get_ports()) if "SEQTRAK" in n][0])
        self.inp.open_port([i for i, n in enumerate(self.inp.get_ports()) if "SEQTRAK" in n][0])
        time.sleep(0.2)

    def drain(self):
        while self.inp.get_message():
            pass

    def ask(self, a, b, c, attempts=4, timeout=0.5):
        for _ in range(attempts):
            self.drain()
            self.out.send_message(REQ + [a, b, c, 0xF7])
            deadline = time.time() + timeout
            while time.time() < deadline:
                m = self.inp.get_message()
                if m and m[0] and m[0][0] == 0xF0 and len(m[0]) >= 9 and m[0][6] == a:
                    return m[0][9:-1]
                if not m:
                    time.sleep(0.002)
            time.sleep(0.03)
        return None

    def put(self, a, b, c, data=()):
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        time.sleep(0.06)

    def put_collect(self, a, b, c, data, attempts=4, window=0.8):
        """Send, then collect EVERY SysEx that arrives in the window."""
        seen = []
        for _ in range(attempts):
            self.drain()
            self.out.send_message(SET + [a, b, c, *data, 0xF7])
            deadline = time.time() + window
            while time.time() < deadline:
                m = self.inp.get_message()
                if m and m[0] and m[0][0] == 0xF0:
                    seen.append(m[0])
                elif not m:
                    time.sleep(0.002)
            if seen:
                return seen
        return seen


def ev(d):
    if d is None:
        return "no reply"
    return "(empty)" if not d else " ".join(f"{x:02X}" for x in d)


def note_payload(ticks, note, vel=100, offvel=0, gate=12):
    return [ticks >> 7, ticks & 0x7F, 0x00, note, vel, offvel, gate >> 7, gate & 0x7F]


link = Link()
if (link.ask(0x01, 0x10, 0x20) or [1])[0] != 0:
    print("ABORT: sequencer not stopped")
    raise SystemExit(1)
if link.ask(0x75, LOCAL << 4, 0x00):
    print("ABORT: SYNTH 1 is not empty")
    raise SystemExit(1)
print("sequencer stopped, SYNTH 1 empty, DX empty:", not link.ask(0x75, OTHER << 4, 0x00))

notes = [(0, 0x3C), (12, 0x43)]   # C3 at tick 0, G3 at tick 12
added = 0
try:
    for ticks, n in notes:
        link.put(0x72, LOCAL << 4, 0x00, note_payload(ticks, n))
        added += 1
        time.sleep(0.2)

    print(f"\nwrote {added} notes; reading the list back:")
    for idx in range(4):
        d = link.ask(0x75, (LOCAL << 4) | (idx >> 7), idx & 0x7F)
        if d:
            t = (d[0] << 7) | d[1]
            gate = (d[6] << 7) | d[7]
            print(f"  idx {idx}: time {t:>4} type {d[2]} note {d[3]:>3} "
                  f"vel {d[4]:>3}/{d[5]:>3} gate {gate:>4}   [{ev(d)}]")
        else:
            print(f"  idx {idx}: {ev(d)}")

    print("\n76 index lookup for the C3 at tick 0, four attempts, logging every SysEx:")
    seen = link.put_collect(0x76, 0x00, LOCAL, [0x00, 0x00, 0x00, 0x3C, 0x00, 0x00])
    if not seen:
        print("  nothing came back in 4 x 0.8 s")
    for m in seen[:6]:
        print("  <-", " ".join(f"{x:02X}" for x in m))

finally:
    print(f"\ndeleting {added} event(s), highest index first:")
    for idx in reversed(range(added)):
        link.put(0x74, (LOCAL << 4) | (idx >> 7), idx & 0x7F)
        time.sleep(0.2)
    final = link.ask(0x75, LOCAL << 4, 0x00)
    otherf = link.ask(0x75, OTHER << 4, 0x00)
    print(f"  SYNTH 1 idx0 = {ev(final)} | DX idx0 = {ev(otherf)} "
          f"| control {ev(link.ask(0x30, 0x40, 0x76))}")
    print("RESTORED" if final == [] else "*** NOT RESTORED ***")
