#!/usr/bin/env python3
"""Rebuild the Arpeggio Preset List (Data List p. 59) as Markdown."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import grid, page_words, rows  # noqa: E402

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
BOUNDS = [70.0, 110.0, 220.0, 328.0, 436.0, 540.0]


def main() -> None:
    lines = rows(page_words(PDF, 59))
    print("| No. | Preset Name | Type | Mode | Octave |")
    print("|---|---|---|---|---|")
    count = 0
    for no, name, type_, mode, octave in grid(lines, (BOUNDS[0], BOUNDS[1]), BOUNDS, top=125):
        if not no.isdigit():
            continue
        print(f"| {no} | {name} | {type_} | {mode} | {octave} |")
        count += 1
    print(f"{count} arpeggio presets", file=sys.stderr)


if __name__ == "__main__":
    main()
