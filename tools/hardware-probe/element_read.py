"""Read-only survey of the AWM element blocks 41 ep / 42 ep.

Nothing is written. The tempo at 30 40 76 is interleaved every eight requests
as the control address, so a run of no-replies can be told from a device that
stopped answering. Four attempts per address, per 10-verified-behaviour.md.
"""
import sys, time
import rtmidi

HEAD = [0xF0, 0x43, 0x30, 0x7F, 0x1C, 0x0C]   # Parameter Request, SEQTRAK


def request(a, b, c):
    return HEAD + [a, b, c, 0xF7]


class Link:
    def __init__(self):
        self.out = rtmidi.MidiOut()
        self.inp = rtmidi.MidiIn()
        self.inp.ignore_types(sysex=False, timing=True, active_sense=True)
        oi = [i for i, n in enumerate(self.out.get_ports()) if "SEQTRAK" in n][0]
        ii = [i for i, n in enumerate(self.inp.get_ports()) if "SEQTRAK" in n][0]
        self.out.open_port(oi)
        self.inp.open_port(ii)
        time.sleep(0.2)

    def ask(self, a, b, c, attempts=4, timeout=0.6):
        for _ in range(attempts):
            while self.inp.get_message():
                pass
            self.out.send_message(request(a, b, c))
            deadline = time.time() + timeout
            while time.time() < deadline:
                msg = self.inp.get_message()
                if msg and msg[0] and msg[0][0] == 0xF0:
                    data = msg[0]
                    if len(data) >= 10 and data[6:9] == [a, b, c]:
                        return data[9:-1]
                elif not msg:
                    time.sleep(0.002)
            time.sleep(0.05)
        return None


link = Link()
control_ok = control_fail = 0
answered = missing = 0
PART = 7           # SYNTH 1
rows = []
for high, lows in ((0x41, range(0x00, 0x20)), (0x42, range(0x00, 0x20))):
    for element in (0, 1):
        mid = (element << 4) | PART
        for i, low in enumerate(lows):
            if i % 8 == 0:
                control_ok += link.ask(0x30, 0x40, 0x76, attempts=4) is not None
            data = link.ask(high, mid, low)
            if data is None:
                missing += 1
                rows.append((high, mid, low, None))
            else:
                answered += 1
                rows.append((high, mid, low, data))

print(f"control address 30 40 76 answered {control_ok} of {len(rows)//8 + 1} interleaved checks")
print(f"{answered} answered, {missing} silent, out of {len(rows)}")
for high, mid, low, data in rows:
    shown = " ".join(f"{b:02X}" for b in data) if data is not None else "-- no reply"
    print(f"{high:02X} {mid:02X} {low:02X} = {shown}")
