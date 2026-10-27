"""Is a two-byte value really 7-bit big-endian on the wire?

Every two-byte write so far has had an MSB of 00, so the packing has never
been exercised. The tempo is documented 5-300 and is a known-good write, so
130 -> 01 02 tests the MSB directly: if the halves were swapped or the second
byte were 8-bit, the machine would land somewhere else.

read -> write -> read back -> restore, restore in a finally, witness in the
same loop, sequencer checked stopped first.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]
TEMPO = (0x30, 0x40, 0x76)
WITNESS = (0x30, 0x40, 0x7C)   # swing offset — must not move


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
                if m and m[0] and m[0][0] == 0xF0:
                    d = m[0]
                    if len(d) >= 10 and d[6:9] == [a, b, c]:
                        return d[9:-1]
                elif not m:
                    time.sleep(0.002)
            time.sleep(0.05)
        return None

    def put(self, a, b, c, data):
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        time.sleep(0.05)


def fmt(d):
    return " ".join(f"{x:02X}" for x in d) if d is not None else "no reply"


link = Link()
seq = link.ask(0x01, 0x10, 0x20)
if seq is None or seq[0] != 0:
    print(f"ABORT: sequencer {fmt(seq)}")
    raise SystemExit(1)

original = link.ask(*TEMPO)
w0 = link.ask(*WITNESS)
print(f"before: tempo {fmt(original)} = {(original[0] << 7) | original[1]} | witness {fmt(w0)}")

try:
    for target in (130, 200, 61):
        packed = [target >> 7, target & 0x7F]
        link.put(*TEMPO, packed)
        time.sleep(0.25)
        back = link.ask(*TEMPO)
        w = link.ask(*WITNESS)
        decoded = (back[0] << 7) | back[1] if back and len(back) == 2 else None
        ok = "MATCH" if decoded == target else "MISMATCH"
        print(f"  wrote {target:>3} as {fmt(packed)} -> read {fmt(back)} = {decoded}  {ok}"
              f" | witness moved: {w != w0}")
finally:
    link.put(*TEMPO, original)
    time.sleep(0.3)
    final = link.ask(*TEMPO)
    wf = link.ask(*WITNESS)
    print(f"\nrestore: tempo {fmt(final)} (was {fmt(original)}) | witness {fmt(wf)}")
    print("RESTORED" if final == original else "*** RESTORE FAILED ***")
