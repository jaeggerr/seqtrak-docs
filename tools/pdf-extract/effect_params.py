#!/usr/bin/env python3
"""Rebuild the Effect Parameter List (Data List pp. 64-88) as CSV.

The pages hold one or two panels side by side. Each panel is headed by the
effect type names it applies to, then lists parameters 1-16 with their display
range, the transmitted value range, the Data Assign Table that converts between
them, and which of the three hardware sliders defaults to that parameter.

Usage: python3 tools/pdf-extract/effect_params.py > data/effect-parameters.csv
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import Word, column, page_words, rows, text_of  # noqa: E402

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
PAGES = range(64, 89)
# No. | Parameter | Range | Value | Data Assign Table No. | Default Slider No.
LEFT = [52.0, 68.0, 120.0, 172.0, 215.0, 252.0, 300.0]
RIGHT = [309.0, 325.0, 377.0, 428.0, 472.0, 509.0, 557.0]
NUMBERED = re.compile(r"^\d+(\s*-\s*\d+)?$")
BLOCKS = {64: "Single / Master Effect Block", 84: "Single EQ Block", 85: "Send Effect Block"}


def panels(page: int):
    """Yield (title, bounds, top, bottom, lines) for each parameter panel.

    Left and right halves are tracked independently: a page can hold three
    panels on the left and two on the right.
    """
    lines = rows(page_words(PDF, page))
    for bounds in (LEFT, RIGHT):
        tops = sorted(l[0].cy for l in lines
                      if any(w.text == "No." and bounds[0] <= w.cx < bounds[1] + 12
                             for w in l))
        titles = {t: [l for l in lines if t - 26 < l[0].cy < t - 9] for t in tops}
        title_ys = {round(l[0].cy, 1) for ls in titles.values() for l in ls}
        for i, top in enumerate(tops):
            bottom = tops[i + 1] - 30 if i + 1 < len(tops) else 800.0
            title = " ".join(
                text_of([w for w in l if bounds[0] - 4 <= w.cx < bounds[-1]])
                for l in titles[top]
            ).strip()
            # Block headings ("Single EQ Block", "Master EQ Block") sit inside a
            # panel's vertical span rather than in a title slot, so drop them too.
            body = [l for l in lines
                    if top + 8 < l[0].cy < bottom
                    and round(l[0].cy, 1) not in title_ys
                    and not any(w.text == "Block" for w in l)]
            yield title, bounds, body


def main() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["block", "effect_types", "parameter_number", "parameter",
                     "display_range", "value_range", "data_assign_table",
                     "default_slider", "panel_note", "page"])
    block, count = BLOCKS[64], 0
    for page in PAGES:
        block = BLOCKS.get(page, block)
        for title, bounds, body in panels(page):
            ys = [l[0].cy for l in body
                  if any(bounds[0] <= w.cx < bounds[1] for w in l)]
            cols = [column(body, ys, bounds[i], bounds[i + 1])
                    for i in range(len(bounds) - 1)]
            table = [[c[i] for c in cols] for i in range(len(ys))]
            notes = " ".join(" ".join(r).strip() for r in table if not NUMBERED.match(r[0]))
            for row in table:
                if not NUMBERED.match(row[0]):
                    continue
                writer.writerow([block, title] + row + [notes, str(page)])
                count += 1
    print(f"{count} effect parameter rows", file=sys.stderr)


if __name__ == "__main__":
    main()
