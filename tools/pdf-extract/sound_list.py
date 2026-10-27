#!/usr/bin/env python3
"""Rebuild the Sound List (Data List pp. 4-33) as CSV.

Each page carries two halves of the same No./Name/Category table. The engine is
taken from the page heading (Drum / Synth / DX / SAMPLER Sound), and the Bank
Select / Program Change triplet is derived from the sound number.

Usage: python3 tools/pdf-extract/sound_list.py > data/presets.csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import grid, page_words, rows, text_of  # noqa: E402

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
PAGES = range(4, 34)
HALVES = [  # No. | Name | Category
    [52.0, 74.0, 200.0, 300.0],
    [309.0, 331.0, 457.0, 560.0],
]
# Drum, Synth and DX share one numbering space under bank MSB 63 (the Data List
# already numbers them 1-2032 continuously); SAMPLER elements are numbered
# separately from 1 under MSB 62.
#
# NOTE: bank_msb, bank_lsb and program are **computed below**, not read from the
# PDF — this extractor only reads No. | Name | Category. So those three columns
# of presets.csv carry no independent evidence about banks, and comparing any
# client's bank arithmetic against them compares the formula to itself. Two
# separate attempts to "validate" the formula that way have already returned a
# meaningless zero divergence.
MSB = {"Drum": 63, "Synth": 63, "DX": 63, "SAMPLER": 62}


def main() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["engine", "number", "name", "category",
                     "bank_msb", "bank_lsb", "program"])
    engine, count = "", 0
    for page in PAGES:
        lines = rows(page_words(PDF, page))
        heading = text_of(lines[1]) if len(lines) > 1 else ""
        if heading.endswith("Sound"):
            engine = heading[: -len(" Sound")].strip()
        top = max((l[0].cy for l in lines if any(w.text == "No." for w in l)), default=95.0)
        for bounds in HALVES:
            for number, name, category in grid(
                lines, (bounds[0], bounds[1]), bounds, top=top + 4
            ):
                if not number.isdigit():
                    continue
                n = int(number)
                writer.writerow([engine, n, name, category,
                                 MSB[engine], (n - 1) // 128, (n - 1) % 128])
                count += 1
    print(f"{count} sounds", file=sys.stderr)


if __name__ == "__main__":
    main()
