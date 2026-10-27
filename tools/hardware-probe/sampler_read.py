"""Read-only survey of the SAMPLER Sample block 50 eA.

103 documented addresses, never queried on hardware before. Nothing is written.
Four attempts per address, control address 30 40 76 interleaved.

The first 88 addresses are the sample name, packed 7-into-8 (02-sysex-format),
so they are read as a block and decoded rather than listed one by one.
"""
import sys, time
import rtmidi

HEAD = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]
NAME_BYTES = 88
TAIL = [(0x5F, 1, "Loop On/Off"), (0x60, 4, "Loop Length"),
        (0x66, 4, "Start Point"), (0x6A, 4, "End Point")]


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


def decode7into8(packed):
    """7 data bytes per group of 8; the group's first byte holds their bit 7."""
    out = []
    for i in range(0, len(packed) - 6, 8):
        high = packed[i]
        for j in range(7):
            out.append(packed[i + 1 + j] | (((high >> j) & 1) << 7))
    return bytes(out)


link = Link()
control = checks = 0
for element in range(7):
    mid = (element << 4) | 0x0A
    checks += 1
    control += link.ask(0x30, 0x40, 0x76) is not None

    name_bytes, silent = [], 0
    for low in range(NAME_BYTES):
        data = link.ask(0x50, mid, low)
        if data is None:
            silent += 1
            name_bytes.append(0)
        else:
            name_bytes.extend(data)
    raw = decode7into8(name_bytes).split(b"\x00")[0]
    try:
        name = raw.decode("utf-8")
    except UnicodeDecodeError:
        name = repr(raw)

    print(f"\n=== element {element + 1} (50 {mid:02X}) ===")
    print(f"  name: {name!r}  ({silent} of {NAME_BYTES} name bytes silent)")
    for low, size, label in TAIL:
        data = link.ask(0x50, mid, low)
        if data is None:
            print(f"  50 {mid:02X} {low:02X} {label:<12} no reply")
        else:
            shown = " ".join(f"{b:02X}" for b in data)
            flag = "" if len(data) == size else f"  << documented size {size}"
            print(f"  50 {mid:02X} {low:02X} {label:<12} [{len(data)}] {shown}{flag}")

print(f"\ncontrol 30 40 76: {control}/{checks}")
