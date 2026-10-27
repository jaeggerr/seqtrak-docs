"""Are 30 41 33..41 one-byte slots at a two-byte stride, or two-byte fields?

The reference lists them every two addresses with size 2; the machine answers
one byte. If they are one-byte slots, the addresses the table skips (34, 36, …)
should answer too. If they are two-byte fields the table got right and the
reply is truncated, those skipped addresses should be silent, like every other
continuation byte measured today.
"""
import sys, time
import rtmidi

HEAD = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]


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
ok = checks = 0
print("documented (odd) and skipped (even) addresses in 30 41 33..42:")
for low in range(0x33, 0x43):
    if (low - 0x33) % 4 == 0:
        checks += 1
        ok += link.ask(0x30, 0x40, 0x76) is not None
    d = link.ask(0x30, 0x41, low)
    listed = "listed" if (low - 0x33) % 2 == 0 else "skipped"
    shown = " ".join(f"{b:02X}" for b in d) if d is not None else "no reply"
    print(f"  30 41 {low:02X}  {listed:<8} {shown}")

print()
print("a control pair: a genuine two-byte field and the address inside it")
for base in (0x31,):
    d0 = link.ask(0x30, 0x41, base)
    d1 = link.ask(0x30, 0x41, base + 1)
    f = lambda d: " ".join(f"{b:02X}" for b in d) if d is not None else "no reply"
    print(f"  30 41 {base:02X} = {f(d0)}   |   30 41 {base + 1:02X} = {f(d1)}")

print(f"\ncontrol 30 40 76: {ok}/{checks}")
