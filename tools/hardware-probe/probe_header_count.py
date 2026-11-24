#!/usr/bin/env python3
"""Send a content transfer header ALONE and read the result code.

Nothing is installed: the header opens the transfer, the acknowledgement is
read, and ContentsManagementMode is restored in a finally without a single
packet or body being sent. docs/08 records three header fields measured this
same way.

The question it answers: result 127 for a sample count of 2 or 5 -- was it the
count, or the message length? The header carries ONE 4-BYTE SIZE ENTRY PER
SAMPLE from offset 0x19, so a count of n needs a 14 + 4n byte payload.

    probe_header_count.py file.Y3S              correct length, n entries
    probe_header_count.py file.Y3S --bad        n declared, ONE entry (the
                                                shape the earlier runs sent)

Expected if the diagnosis holds: correct -> result 0, --bad -> result 127.
"""
import sys, time, zipfile, struct, rtmidi

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BAD = "--bad" in sys.argv
Y3S = args[0]
SOUND_CN = int(args[1]) if len(args) > 1 else 4103

z = zipfile.ZipFile(Y3S)
root = z.namelist()[0].split("/")[0]
nsmp = len([n for n in z.namelist() if "/sample" in n and n.endswith(".bin")])
sizes = [len(z.read("%s/sample%d.bin" % (root, i))) for i in range(nsmp)]
kb = struct.unpack_from("<I", z.read(root + "/waveform0.bin"), 0)[0]

out, inp = rtmidi.MidiOut(), rtmidi.MidiIn()
try:
    oi = next(i for i, n in enumerate(out.get_ports()) if "SEQTRAK" in n)
    ii = next(i for i, n in enumerate(inp.get_ports()) if "SEQTRAK" in n)
except StopIteration:
    raise SystemExit("no SEQTRAK port -- is it plugged in over USB-C and on?")
out.open_port(oi)
inp.open_port(ii)
inp.ignore_types(sysex=False, timing=True, active_sense=True)
MODE = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C, 0x01, 0x10, 0x01]


def flush():
    while inp.get_message():
        pass


def cks(b):
    s = sum(b[7:len(b) - 2]) & 0x7F
    return 0 if s == 0 else (0x80 - s) & 0x7F


def b4(v):
    return [(v >> 21) & 0x7F, (v >> 14) & 0x7F, (v >> 7) & 0x7F, v & 0x7F]


def b2(v):
    return [(v >> 7) & 0x7F, v & 0x7F]


def send(ah, num, body):
    cnt = 1 + 3 + len(body)
    m = ([0xF0, 0x43, 0x00, 0x7F, 0x1C, (cnt >> 7) & 0x7F, cnt & 0x7F, 0x0C,
          ah, (num >> 7) & 0x7F, num & 0x7F] + list(body) + [0, 0xF7])
    m[-2] = cks(m)
    out.send_message(m)
    return cnt


def ack(timeout=10.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        m = inp.get_message()
        if m:
            d = list(m[0])
            if (d and d[0] == 0xF0 and len(d) >= 17 and d[8] == 0x01
                    and d[9] in (0x20, 0x21, 0x22)):
                return d
        else:
            time.sleep(0.0005)
    return None


print("source: %s" % Y3S)
print("  %d keybanks, %d samples, sizes %s" % (kb, nsmp, sizes))

hdr = [0, 1, 0, 0] + b2(0) + b2(0) + b2(1) + b4(nsmp)
entries = sizes[:1] if BAD else sizes
for s in entries:
    hdr += b4(s)
print("  header: count=%d, %d size entr%s, payload %d B, Yamaha count 0x%02X%s"
      % (nsmp, len(entries), "y" if len(entries) == 1 else "ies", len(hdr),
         1 + 3 + len(hdr), "   <-- DELIBERATELY MALFORMED" if BAD else ""))

try:
    out.send_message(MODE + [0x01, 0xF7])
    time.sleep(0.4)
    flush()
    send(0x03, SOUND_CN, hdr)
    a = ack()
    if a is None:
        print("  -> NO acknowledgement (a missing reply is never information:"
              " run it again)")
    else:
        print("  -> ack 01 %02X 00  result=%d" % (a[9], a[11]))
finally:
    out.send_message(MODE + [0x00, 0xF7])
    time.sleep(0.3)
    print("ContentsManagementMode restored to 0; nothing was installed")
