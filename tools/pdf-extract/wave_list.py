#!/usr/bin/env python3
"""Rebuild the AWM Wave List (Data List pp. 34-58) as CSV.

Each page carries two side-by-side halves of the same No./Name/Main/Sub table.

Usage: python3 tools/pdf-extract/wave_list.py > data/waves.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import grid, page_words, rows  # noqa: E402

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
PAGES = range(34, 59)
HALVES = [  # No. | Name | Main category | Sub category
    [55.0, 80.0, 180.0, 235.0, 300.0],
    [312.0, 337.0, 438.0, 493.0, 560.0],
]


def main() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["number", "name", "main_category", "sub_category"])
    count = 0
    for page in PAGES:
        lines = rows(page_words(PDF, page))
        top = max((l[0].cy for l in lines if any(w.text == "Category" for w in l)), default=110.0)
        for bounds in HALVES:
            for number, name, main, sub in grid(
                lines, (bounds[0], bounds[1]), bounds, top=top + 4, bottom=800.0
            ):
                if not number.isdigit():
                    continue
                writer.writerow([number, name, main, sub])
                count += 1
    print(f"{count} waves", file=sys.stderr)


if __name__ == "__main__":
    main()
