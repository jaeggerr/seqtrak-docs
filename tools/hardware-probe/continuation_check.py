"""Does the base-address rule hold on a second block?

The element blocks showed that a Parameter Request is answered at a field's
base address and is silent inside it. 31 1p holds seven two-byte fields whose
continuation addresses have no row of their own in the reference. Ask for each
base and each continuation, four attempts, control address interleaved.
"""
import sys, time
import rtmidi

HEAD = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
BASES = [0x17, 0x24, 0x39, 0x3D, 0x41, 0x46, 0x4B]   # the seven 2-byte fields
PART = 7


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


link = Link()
mid = 0x10 | PART
ok = 0
for low in BASES:
    ok += link.ask(0x30, 0x40, 0x76) is not None
    base = link.ask(0x31, mid, low)
    cont = link.ask(0x31, mid, low + 1)
    fb = " ".join(f"{b:02X}" for b in base) if base is not None else "no reply"
    fc = " ".join(f"{b:02X}" for b in cont) if cont is not None else "no reply"
    print(f"31 {mid:02X} {low:02X} = {fb:<10} | 31 {mid:02X} {low + 1:02X} = {fc}")
print(f"\ncontrol 30 40 76: {ok}/{len(BASES)}")
