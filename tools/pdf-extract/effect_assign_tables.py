#!/usr/bin/env python3
"""Rebuild the Effect Data Assign Tables (Data List pp. 89-103) as CSV.

These convert a transmitted effect-parameter byte into the value the hardware
shows. The Effect Parameter List names which table each parameter uses.

A page is laid out as up to five fixed columns; within a column the tables are
stacked, so a short table is followed further down the same column by the next
one while its neighbours keep going. Tables are therefore located per column,
each running from its own "Table #n" heading to the next heading below it.

Usage: python3 tools/pdf-extract/effect_assign_tables.py > data/effect-data-assign-tables.csv
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import Word, page_words, rows, text_of  # noqa: E402

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
PAGES = range(89, 104)
TABLE_NO = re.compile(r"^#(\d+)$")


def tables_on(lines: list[list[Word]]):
    """Yield (table_no, x0, x1, top, bottom) for every table on the page."""
    heads: list[tuple[float, float, str]] = []
    for line in lines:
        for i, word in enumerate(line):
            if word.text == "Table" and i + 1 < len(line) and TABLE_NO.match(line[i + 1].text):
                heads.append((word.x0, word.cy, TABLE_NO.match(line[i + 1].text).group(1)))

    xs = sorted({x for x, _, _ in heads})
    xs = [x for i, x in enumerate(xs) if i == 0 or x - xs[i - 1] > 20]
    for i, x0 in enumerate(xs):
        x1 = xs[i + 1] if i + 1 < len(xs) else 600.0
        in_column = sorted((cy, no) for x, cy, no in heads if x0 - 4 <= x < x1 - 4)
        for j, (top, no) in enumerate(in_column):
            bottom = in_column[j + 1][0] - 4 if j + 1 < len(in_column) else 800.0
            yield no, x0, x1, top, bottom


def main() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["table", "quantity", "data", "value"])
    count, tables = 0, set()
    for page in PAGES:
        lines = rows(page_words(PDF, page))
        for no, x0, x1, top, bottom in tables_on(lines):
            header_y = min((l[0].cy for l in lines
                            if top < l[0].cy < bottom
                            and any(w.text == "Data" and x0 - 4 <= w.cx < x1 - 4 for w in l)),
                           default=None)
            if header_y is None:
                continue
            quantity = " ".join(
                text_of([w for w in l if x0 - 4 <= w.cx < x1 - 4])
                for l in lines if top + 4 < l[0].cy < header_y - 2
            ).strip()
            pairs = sorted(w.cx for l in lines if abs(l[0].cy - header_y) < 1
                           for w in l if w.text == "Data" and x0 - 4 <= w.cx < x1 - 4)
            for pair_x in pairs:
                limit = min((p for p in pairs if p > pair_x), default=x1 - 4)
                for line in lines:
                    if not (header_y + 2 < line[0].cy < bottom):
                        continue
                    cells = [w for w in line if pair_x - 7 <= w.cx < limit - 7]
                    if len(cells) < 2 or not cells[0].text.lstrip("-").isdigit():
                        continue
                    writer.writerow([no, quantity, cells[0].text,
                                     " ".join(w.text for w in cells[1:])])
                    count += 1
                    tables.add(no)
    print(f"{count} rows across {len(tables)} assign tables", file=sys.stderr)


if __name__ == "__main__":
    main()
