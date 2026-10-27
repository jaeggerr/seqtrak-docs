#!/usr/bin/env python3
"""Rebuild the Effect Type List (Data List pp. 61-63) as Markdown.

Usage: python3 tools/pdf-extract/effect_types.py [--csv]
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import (TICK, Word, assign_spanning, column, find, label_groups,  # noqa: E402
                   page_words, partition, rows, text_of)

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
PAGES = (61, 62, 63)
SLOTS = ["Chain", "Single", "Send", "Master 1", "Master 2", "Master 3", "Master 4"]
HEX = re.compile(r"^[0-9A-F]{2}$")


def slot_columns(words: list[Word]) -> list[float]:
    """Centre of each assignability column, read off the header labels."""
    masters = sorted((w for w in words if w.text == "Master"), key=lambda w: w.x0)
    digits = [next(d for d in words if d.text == str(i + 1) and abs(d.cy - m.cy) < 2)
              for i, m in enumerate(masters)]
    return [find(words, "Chain").cx, find(words, "Single").cx, find(words, "Send").cx] + \
           [(m.x0 + d.x1) / 2 for m, d in zip(masters, digits)]


def parse_page(page: int, carried: str) -> tuple[list[list[str]], str]:
    words = page_words(PDF, page)
    msb, lsb = find(words, "MSB"), find(words, "LSB")
    chain = find(words, "Chain")
    x_name, x_msb, x_desc, x_end = msb.x0 - 75, msb.x0 - 6, lsb.x1 + 4, chain.x0 - 6

    body = [w for w in words if w.cy > chain.cy + 4 and w.cy < 800]
    anchors = []
    for line in rows(body):
        hexes = [w for w in line if HEX.match(w.text) and x_msb <= w.cx < x_desc]
        if len(hexes) == 2:
            anchors.append((line[0].cy, hexes[0].text, hexes[1].text))

    lines = rows(body)
    ys = [a[0] for a in anchors]
    names = column(lines, ys, x_name, x_msb)
    descs = column(lines, ys, x_desc, x_end)
    marks = partition(ys, [(l[0].cy, [w for w in l if w.text == TICK and w.cx >= x_end])
                           for l in lines if any(w.text == TICK for w in l)])
    slot_x = slot_columns(words)

    cats = assign_spanning(ys, label_groups(body, 0, x_name, gap=8))

    out, last = [], carried
    for i, (y, hi, lo) in enumerate(anchors):
        cat = cats[i] or last
        last = cat
        flat = [w for part in marks[i] for w in part]
        slots = [s for s, x in zip(SLOTS, slot_x) if any(abs(w.cx - x) <= 6 for w in flat)]
        out.append([cat, names[i], hi, lo, descs[i], ", ".join(slots)])
    return out, last


def main() -> None:
    table, carried = [], ""
    for page in PAGES:
        rows_, carried = parse_page(page, carried)
        table += rows_
    if "--csv" in sys.argv:
        writer = csv.writer(sys.stdout)
        writer.writerow(["category", "type_name", "msb", "lsb", "description",
                         "assignable_to"])
        writer.writerows(table)
    else:
        print("| Category | Type Name | MSB | LSB | Description | Assignable to |")
        print("|---|---|---|---|---|---|")
        for cat, name, hi, lo, desc, slots in table:
            print(f"| {cat} | {name} | `{hi}` | `{lo}` | {desc} | {slots} |")
    print(f"{len(table)} effect types", file=sys.stderr)


if __name__ == "__main__":
    main()
