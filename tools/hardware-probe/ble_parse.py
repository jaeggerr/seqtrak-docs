#!/usr/bin/env python3
"""Parse a raw BLE-MIDI packet dump properly, and answer the F7 question.

A naive scan of a BLE-MIDI packet cannot answer "does the machine send an
un-timestamped F7", because a timestamp byte is 0x80 | (time & 0x7F) and so
takes the values 0xF1, 0xF3, 0xF5, 0xF7, 0xF9, 0xFB, 0xFD, 0xFF among others.
Counting every byte >= 0xF0 reports those as status bytes. This parser tracks
position in the packet and SysEx state across packets instead, which is the
only way the question can be answered.

  python3 ble_parse.py <dumpfile>
"""
import collections
import sys

STATUS_LEN = {0x8: 3, 0x9: 3, 0xA: 3, 0xB: 3, 0xC: 2, 0xD: 2, 0xE: 3}
REALTIME = {0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF}


def hx(bs):
    return ' '.join(f'{b:02X}' for b in bs)


def main(path):
    packets = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            t, _, rest = line.partition(' ')
            packets.append((float(t), [int(x, 16) for x in rest.split()]))

    status_counts = collections.Counter()
    sysex_msgs = []
    f7_timestamped = 0
    f7_untimestamped = 0
    f7_examples = []
    in_sysex = False
    sysex_buf = []
    max_len = 0
    bad_header = 0

    for t, b in packets:
        max_len = max(max_len, len(b))
        if not b:
            continue
        if not (b[0] & 0x80):
            bad_header += 1
            continue

        i = 1
        while i < len(b):
            by = b[i]

            if in_sysex:
                # Inside a SysEx body. A byte with bit 7 set here is either a
                # timestamp (introducing F7 or a real-time byte) or F7 itself.
                if by == 0xF7:
                    # F7 with no timestamp in front of it.
                    f7_untimestamped += 1
                    if len(f7_examples) < 8:
                        f7_examples.append(
                            f'untimestamped: {hx(b)}  (F7 at index {i}/{len(b)})')
                    sysex_buf.append(0xF7)
                    sysex_msgs.append(list(sysex_buf))
                    sysex_buf, in_sysex = [], False
                    i += 1
                elif by & 0x80:
                    # A timestamp. What follows decides.
                    nxt = b[i + 1] if i + 1 < len(b) else None
                    if nxt == 0xF7:
                        f7_timestamped += 1
                        if len(f7_examples) < 8:
                            f7_examples.append(
                                f'timestamped:   {hx(b)}  (ts {by:02X} then F7 '
                                f'at index {i+1}/{len(b)})')
                        sysex_buf.append(0xF7)
                        sysex_msgs.append(list(sysex_buf))
                        sysex_buf, in_sysex = [], False
                        i += 2
                    elif nxt is not None and nxt in REALTIME:
                        status_counts[nxt] += 1
                        i += 2
                    else:
                        # Trailing timestamp with nothing after it: the spec
                        # forbids it, so treat the byte as data and move on.
                        sysex_buf.append(by)
                        i += 1
                else:
                    sysex_buf.append(by)
                    i += 1
                continue

            # Not in a SysEx: expect timestamp, then status.
            if by & 0x80:
                nxt = b[i + 1] if i + 1 < len(b) else None
                if nxt is None:
                    break
                if nxt & 0x80:
                    st = nxt
                    status_counts[st] += 1
                    if st == 0xF0:
                        in_sysex = True
                        sysex_buf = [0xF0]
                        i += 2
                    elif st in REALTIME or st in (0xF6,):
                        i += 2
                    elif st == 0xF2:
                        i += 4
                    elif st == 0xF3:
                        i += 3
                    else:
                        i += 1 + STATUS_LEN.get(st >> 4, 1)
                else:
                    i += 1
            else:
                i += 1

    print(f'packets            : {len(packets)}')
    print(f'largest packet     : {max_len} bytes')
    print(f'headers malformed  : {bad_header}')
    print('\n=== STATUS BYTES, properly parsed ===')
    for k in sorted(status_counts):
        print(f'  {k:02X}  x{status_counts[k]}')
    print('\n=== F7 FRAMING (the actual question) ===')
    print(f'  F7 preceded by a timestamp     : {f7_timestamped}')
    print(f'  F7 NOT preceded by a timestamp : {f7_untimestamped}')
    for e in f7_examples:
        print(f'    {e}')
    if f7_timestamped == 0 and f7_untimestamped == 0:
        print('    no SysEx terminator seen at all — no SysEx crossed the link,')
        print('    so this run says NOTHING about F7 framing.')
    print(f'\n=== SYSEX REASSEMBLED: {len(sysex_msgs)} ===')
    addrs = collections.Counter()
    for m in sysex_msgs[:40]:
        print(f'  [{len(m):3d}]  {hx(m[:14])}{" …" if len(m) > 14 else ""}')
    for m in sysex_msgs:
        if len(m) >= 9 and m[1] == 0x43:
            addrs[(m[6], m[7], m[8])] += 1
    if addrs:
        print('\n  by address:')
        for a, n in sorted(addrs.items()):
            print(f'    {hx(a)}  x{n}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'ble_dump.txt')
