#!/usr/bin/env python3
"""Pull one content off the SEQTRAK through the content channel.

Read-only as far as content goes: the only thing written is 01 10 01
(ContentsManagementMode), and it is restored in a `finally`.

    content_pull.py --kind waveform --number 8593 --out ./pulled

The protocol is documented in docs/08-bulk-and-files.md; this script is the
run that verified it (docs/10-verified-behaviour.md, 2026-11-23).
"""
import argparse, pathlib, sys, time

try:
    import rtmidi
except ImportError:
    sys.exit("needs python-rtmidi:  pip install python-rtmidi")

KINDS = {"project": 0x02, "sound": 0x03, "element": 0x04, "waveform": 0x05}
MODE = [0xF0, 0x43, 0x10, 0x7F, 0x1C, 0x0C, 0x01, 0x10, 0x01]


def checksum(buf, size):
    s = sum(buf[7:size - 2]) & 0x7F
    return 0 if s == 0 else (0x80 - s) & 0x7F


def unpack7(enc):
    """7-into-8, most-significant-first: raw[k] = enc[k+1] | bit(6-k) of enc[0]."""
    out = bytearray()
    for i in range(0, len(enc) - 7, 8):
        g = enc[i:i + 8]
        h = g[0]
        for k, b in enumerate(g[1:]):
            out.append(b | (((h >> (6 - k)) & 1) << 7))
    return bytes(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=sorted(KINDS), default="waveform")
    ap.add_argument("--number", type=int, required=True, help="content number")
    ap.add_argument("--out", default="pulled", help="directory for the .bin files")
    ap.add_argument("--max-messages", type=int, default=4000)
    a = ap.parse_args()

    out_dir = pathlib.Path(a.out); out_dir.mkdir(parents=True, exist_ok=True)
    mo, mi = rtmidi.MidiOut(), rtmidi.MidiIn()
    try:
        oi = next(i for i, n in enumerate(mo.get_ports()) if "SEQTRAK" in n)
        ii = next(i for i, n in enumerate(mi.get_ports()) if "SEQTRAK" in n)
    except StopIteration:
        sys.exit("SEQTRAK not found among the MIDI ports")
    mo.open_port(oi); mi.open_port(ii)
    mi.ignore_types(sysex=False, timing=True, active_sense=True)

    def flush():
        while mi.get_message():
            pass

    def get(timeout=4.0):
        t0 = time.time()
        while time.time() - t0 < timeout:
            m = mi.get_message()
            if m:
                d = list(m[0])
                if d and d[0] == 0xF0:
                    return d
            else:
                time.sleep(0.0005)
        return None

    def ack(msg, result=0):
        b = [0xF0, 0x43, 0x00, 0x7F, 0x1C, 0x00, 0x0C, 0x0C, 0x01, 0x21, 0x00,
             result, msg[8], msg[9], msg[10], msg[0x0D], msg[0x0E], 0, 0, 0, 0xF7]
        b[19] = checksum(b, 21)
        mo.send_message(b)

    n = a.number
    am = ((n >> 7) | 0x40) & 0x7F
    al = n & 0x7F
    parts, headers = {}, []
    try:
        mo.send_message(MODE + [0x01, 0xF7]); time.sleep(0.3); flush()
        req = [0xF0, 0x43, 0x20, 0x7F, 0x1C, 0x0C, KINDS[a.kind], am, al, 0xF7]
        print("request:", " ".join("%02X" % b for b in req))
        mo.send_message(req)
        for _ in range(a.max_messages):
            d = get()
            if d is None:
                print("no more messages"); break
            if len(d) < 17:
                continue
            if d[9] == 0x22:
                print("refused, result = %d (see the result-code table)" % d[11]); break
            ah = d[8]
            if ah in (0x02, 0x03, 0x04, 0x05):
                headers.append(d); ack(d); continue
            # Two framings, and they must not be mixed: a body (07/08/09)
            # carries 00 01 00 00 at 0x0B and its data from 0x0F; a packet
            # path (06/0A) carries the count at 0x0B and the index at 0x0D.
            if ah in (0x06, 0x0A):
                index = (d[0x0D] << 7) | d[0x0E]
            else:
                index = 0
            parts.setdefault(ah, {})[index] = bytes(d[0x0F:len(d) - 2])
            ack(d)
    finally:
        mo.send_message(MODE + [0x00, 0xF7]); time.sleep(0.2)
        print("ContentsManagementMode restored to 0")

    print("%d header(s)" % len(headers))
    for ah, pk in sorted(parts.items()):
        enc = b"".join(pk[i] for i in sorted(pk))
        # A packet path's data starts two bytes into the first packet's
        # payload; those two bytes are unexplained. A body starts at once.
        raw = unpack7(enc[2:] if ah in (0x06, 0x0A) else enc)
        p = out_dir / ("content_%02X.bin" % ah)
        p.write_bytes(raw)
        print("ah=%02X: %d packets, %d encoded -> %d raw  ->  %s"
              % (ah, len(pk), len(enc), len(raw), p))


if __name__ == "__main__":
    main()
