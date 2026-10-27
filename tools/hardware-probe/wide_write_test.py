"""Does the SEQTRAK accept a two-byte Parameter Change?

Every effect parameter is a 14-bit field. The encoding is documented but a
two-byte write has never been sent to this machine, so the whole effect surface
is read-only to any honest client.

Target: 30 41 0B — Reverb Parameter 5, which on the loaded REV-X HALL is LPF
Cutoff Frequency with a documented range of 34-60. Audible, reversible, and
far from anything destructive.

Discipline, from seqtrak-docs/CLAUDE.md:
  * read -> write -> read back -> restore, restore in a finally;
  * a witness address that must not move (30 41 09, Parameter 4);
  * the control address 30 40 76 in the same loop;
  * four attempts per read, because a missing reply is never information;
  * the sequencer must be stopped — checked before anything is sent.
"""
import sys, time
import rtmidi

REQ = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
SET = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C]

TARGET = (0x30, 0x41, 0x0B)   # Reverb Parameter 5
WITNESS = (0x30, 0x41, 0x09)  # Reverb Parameter 4 — must not move
CONTROL = (0x30, 0x40, 0x76)  # tempo


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
                msg = self.inp.get_message()
                if msg and msg[0] and msg[0][0] == 0xF0:
                    d = msg[0]
                    if len(d) >= 10 and d[6:9] == [a, b, c]:
                        return d[9:-1]
                elif not msg:
                    time.sleep(0.002)
            time.sleep(0.05)
        return None

    def put(self, a, b, c, data):
        self.out.send_message(SET + [a, b, c, *data, 0xF7])
        time.sleep(0.05)   # the official app paces at 2 ms; this is generous


def fmt(d):
    return " ".join(f"{x:02X}" for x in d) if d is not None else "no reply"


link = Link()

seq = link.ask(0x01, 0x10, 0x20)
if seq is None or seq[0] != 0:
    print(f"ABORT: sequencer state {fmt(seq)} — must read 00 before any write")
    raise SystemExit(1)
print("sequencer stopped (01 10 20 = 00)")

original = link.ask(*TARGET)
witness0 = link.ask(*WITNESS)
control0 = link.ask(*CONTROL)
print(f"before:  target {TARGET[0]:02X} {TARGET[1]:02X} {TARGET[2]:02X} = {fmt(original)}"
      f" | witness = {fmt(witness0)} | control = {fmt(control0)}")

if original is None or len(original) != 2:
    print("ABORT: target did not answer with two bytes; nothing was written")
    raise SystemExit(1)

try:
    # --- 1. the two-byte write -------------------------------------------
    wide = [0x00, 0x32]          # 50, inside the documented 34-60
    print(f"\n[1] two-byte write {fmt(wide)} (value 50)")
    link.put(*TARGET, wide)
    time.sleep(0.2)
    after = link.ask(*TARGET)
    w1 = link.ask(*WITNESS)
    c1 = link.ask(*CONTROL)
    print(f"    read back {fmt(after)} | witness {fmt(w1)} | control {fmt(c1)}")
    if after == wide:
        print("    RESULT: the machine accepted a two-byte Parameter Change")
    elif after == original:
        print("    RESULT: refused — the value did not change")
    else:
        print("    RESULT: changed, but not to what was sent")
    print(f"    witness moved: {w1 != witness0}")

    # restore before the second experiment so they do not confound
    link.put(*TARGET, original)
    time.sleep(0.2)
    mid = link.ask(*TARGET)
    print(f"    restored to {fmt(mid)}")

    # --- 2. the one-byte write to the same two-byte address ---------------
    narrow = [0x28]              # 40, also inside 34-60
    print(f"\n[2] one-byte write {fmt(narrow)} (value 40) to the same address")
    link.put(*TARGET, narrow)
    time.sleep(0.2)
    after2 = link.ask(*TARGET)
    w2 = link.ask(*WITNESS)
    print(f"    read back {fmt(after2)} | witness {fmt(w2)}")
    if after2 == original:
        print("    RESULT: ignored — a one-byte write to a two-byte field does nothing")
    elif after2 is not None and len(after2) == 2 and after2[0] == narrow[0]:
        print("    RESULT: the byte landed in the MSB — a one-byte write is DANGEROUS here")
    elif after2 is not None and len(after2) == 2 and after2[1] == narrow[0]:
        print("    RESULT: the byte landed in the LSB")
    else:
        print("    RESULT: something else happened")
    print(f"    witness moved: {w2 != witness0}")

finally:
    link.put(*TARGET, original)
    time.sleep(0.25)
    final = link.ask(*TARGET)
    wf = link.ask(*WITNESS)
    cf = link.ask(*CONTROL)
    print(f"\nrestore: target {fmt(final)} (was {fmt(original)})"
          f" | witness {fmt(wf)} | control {fmt(cf)}")
    print("RESTORED" if final == original else "*** RESTORE FAILED — CHECK THE MACHINE ***")
