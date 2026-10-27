"""Where is the index in the 76 reply?

Run 2 asked for the note at index 0 and got back
    76 01 00 | 00 00 00 3C 00 00 00 00
The trailing 00 00 could be the index, or padding. Asking for the note at
index 1 separates the two: a 00 01 there settles it, anything else does not.

Also asks for a note that is NOT in the list, which is the control: a lookup
that answers the same way for a note that is absent is not reporting an index.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]
LOCAL = 0


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

    def lookup(self, payload, attempts=4, window=0.7):
        for _ in range(attempts):
            self.drain()
            self.out.send_message(SET + [0x76, 0x00, LOCAL, *payload, 0xF7])
            deadline = time.time() + window
            while time.time() < deadline:
                m = self.inp.get_message()
                if m and m[0] and m[0][0] == 0xF0 and len(m[0]) >= 8 and m[0][6] == 0x76:
                    return m[0]
                if not m:
                    time.sleep(0.002)
        return None


def ev(d):
    if d is None:
        return "no reply"
    return "(empty)" if not d else " ".join(f"{x:02X}" for x in d)


def payload(ticks, note, vel=100, gate=12):
    return [ticks >> 7, ticks & 0x7F, 0x00, note, vel, 0x00, gate >> 7, gate & 0x7F]


link = Link()
if (link.ask(0x01, 0x10, 0x20) or [1])[0] != 0 or link.ask(0x75, LOCAL << 4, 0x00):
    print("ABORT: sequencer running, or SYNTH 1 not empty")
    raise SystemExit(1)

notes = [(0, 0x3C), (12, 0x43), (24, 0x48)]   # three, so index 2 exists too
added = 0
try:
    for t, n in notes:
        link.put(0x72, LOCAL << 4, 0x00, payload(t, n))
        added += 1
        time.sleep(0.18)
    print(f"wrote {added} notes at ticks {[t for t, _ in notes]}\n")

    for want_idx, (t, n) in enumerate(notes):
        reply = link.lookup([t >> 7, t & 0x7F, 0x00, n, 0x00, 0x00])
        if reply is None:
            print(f"  looking for idx {want_idx} (tick {t}, note {n}): no reply")
            continue
        body = reply[9:-1]
        tail = (body[-2] << 7) | body[-1] if len(body) >= 2 else None
        print(f"  looking for idx {want_idx} (tick {t:>2}, note {n}): "
              f"addr {reply[6]:02X} {reply[7]:02X} {reply[8]:02X} | data {ev(body)} "
              f"| trailing pair = {tail}  {'MATCHES' if tail == want_idx else 'does not match'}")

    absent = link.lookup([0x00, 0x60, 0x00, 0x7F, 0x00, 0x00])   # tick 96, note 127
    print(f"\n  control — a note that is NOT in the list: "
          f"{'no reply' if absent is None else ev(absent[6:-1])}")

finally:
    print(f"\ndeleting {added}:")
    for idx in reversed(range(added)):
        link.put(0x74, (LOCAL << 4) | (idx >> 7), idx & 0x7F)
        time.sleep(0.18)
    final = link.ask(0x75, LOCAL << 4, 0x00)
    print(f"  SYNTH 1 idx0 = {ev(final)} | control {ev(link.ask(0x30, 0x40, 0x76))}")
    print("RESTORED" if final == [] else "*** NOT RESTORED ***")
