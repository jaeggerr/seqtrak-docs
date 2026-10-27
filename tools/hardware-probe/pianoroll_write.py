"""Can a melodic step be written? Add one note, read it, find it, delete it.

The last large gap in this project: the drum grid writes steps on drum-typed
parts (70, verified), but the synth blocks 72-76 had only ever been read.

All four melodic tracks read EMPTY before this ran, so nothing of the owner's
is at risk — and that emptiness is itself the witness: anything left behind is
ours.

Discipline: sequencer checked stopped; the control address in the same loop; a
second track that must stay empty; delete in a finally.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]

LOCAL = 0          # SYNTH 1
OTHER = 2          # DX — must stay empty
NOTE, VEL, OFFVEL = 0x3C, 100, 0     # C3
TIME_TICKS, GATE_TICKS = 0, 12


class Link:
    def __init__(self):
        self.out, self.inp = rtmidi.MidiOut(), rtmidi.MidiIn()
        self.inp.ignore_types(sysex=False, timing=True, active_sense=True)
        self.out.open_port([i for i, n in enumerate(self.out.get_ports()) if "SEQTRAK" in n][0])
        self.inp.open_port([i for i, n in enumerate(self.inp.get_ports()) if "SEQTRAK" in n][0])
        time.sleep(0.2)

    def ask(self, a, b, c, attempts=4, timeout=0.5, expect=None):
        for _ in range(attempts):
            while self.inp.get_message():
                pass
            self.out.send_message(REQ + [a, b, c, 0xF7])
            deadline = time.time() + timeout
            while time.time() < deadline:
                m = self.inp.get_message()
                if m and m[0] and m[0][0] == 0xF0:
                    d = m[0]
                    if len(d) >= 9 and d[6] == (expect if expect is not None else a):
                        return d[9:-1]
                elif not m:
                    time.sleep(0.002)
            time.sleep(0.03)
        return None

    def put(self, a, b, c, data=()):
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        time.sleep(0.06)

    def put_and_listen(self, a, b, c, data, want, timeout=0.6):
        """Send a Parameter Change and collect whatever comes back at `want`."""
        while self.inp.get_message():
            pass
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        deadline = time.time() + timeout
        while time.time() < deadline:
            m = self.inp.get_message()
            if m and m[0] and m[0][0] == 0xF0 and len(m[0]) >= 9 and m[0][6] == want:
                return m[0][6:-1]
            if not m:
                time.sleep(0.002)
        return None


def ev(d):
    if d is None:
        return "no reply"
    return "(empty)" if not d else " ".join(f"{x:02X}" for x in d)


link = Link()

seq = link.ask(0x01, 0x10, 0x20)
if seq is None or seq[0] != 0:
    print(f"ABORT: sequencer {ev(seq)} — must be 00")
    raise SystemExit(1)
print(f"sequencer stopped; control 30 40 76 = {ev(link.ask(0x30, 0x40, 0x76))}")

before = link.ask(0x75, LOCAL << 4, 0x00)
other0 = link.ask(0x75, OTHER << 4, 0x00)
print(f"before:  SYNTH 1 idx0 = {ev(before)} | DX idx0 = {ev(other0)}")
if before:
    print("ABORT: SYNTH 1 is not empty; this script only runs on an empty list")
    raise SystemExit(1)

payload = [TIME_TICKS >> 7, TIME_TICKS & 0x7F, 0x00, NOTE, VEL, OFFVEL,
           GATE_TICKS >> 7, GATE_TICKS & 0x7F]
wrote = False
try:
    print(f"\n[1] add  72 {LOCAL << 4:02X} 00  {' '.join(f'{b:02X}' for b in payload)}")
    link.put(0x72, LOCAL << 4, 0x00, payload)
    wrote = True
    time.sleep(0.25)

    after = link.ask(0x75, LOCAL << 4, 0x00)
    other1 = link.ask(0x75, OTHER << 4, 0x00)
    print(f"    read back idx0 = {ev(after)}")
    print(f"    DX still empty: {not after is None and not other1}")
    if after and len(after) >= 9:
        t = (after[2] << 8) | after[3]
        gate = (after[7] << 8) | after[8]
        print(f"    parsed: type {after[0]} part {after[1]} time {t} "
              f"note {after[4]} vel {after[5]}/{after[6]} gate {gate}")
        ok = after[4] == NOTE and after[5] == VEL
        print(f"    RESULT: {'the note is there' if ok else 'something landed, but not ours'}")
    else:
        print("    RESULT: the write did nothing — the list is still empty")

    # --- the index lookup, 76 00 part ------------------------------------
    print(f"\n[2] find 76 00 {LOCAL:02X}  {TIME_TICKS >> 7:02X} {TIME_TICKS & 0x7F:02X} "
          f"00 {NOTE:02X} 00 00   (reply expected on 77)")
    reply = link.put_and_listen(
        0x76, 0x00, LOCAL,
        [TIME_TICKS >> 7, TIME_TICKS & 0x7F, 0x00, NOTE, 0x00, 0x00],
        want=0x77,
    )
    print(f"    reply: {ev(reply)}")

finally:
    if wrote:
        print(f"\n[3] delete 74 {LOCAL << 4:02X} 00")
        link.put(0x74, LOCAL << 4, 0x00)
        time.sleep(0.3)
        final = link.ask(0x75, LOCAL << 4, 0x00)
        otherf = link.ask(0x75, OTHER << 4, 0x00)
        ctrl = link.ask(0x30, 0x40, 0x76)
        print(f"    SYNTH 1 idx0 = {ev(final)} | DX idx0 = {ev(otherf)} | control {ev(ctrl)}")
        print("RESTORED (list empty again)" if final == [] else
              "*** NOT RESTORED — SYNTH 1 still holds an event ***")
