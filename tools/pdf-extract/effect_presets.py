#!/usr/bin/env python3
"""Rebuild the Effect Preset List (Data List pp. 104-107) as CSV.

Three sections run across the four pages: Single Effect, Send Effect and Master
Effect presets. Every category holds exactly eight presets numbered 1-8, so the
rows are grouped on the preset number resetting to 1 and the category labels are
consumed in document order.

Usage: python3 tools/pdf-extract/effect_presets.py > data/effect-presets.csv
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import column, label_groups, page_words, rows, text_of  # noqa: E402

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
PAGES = range(104, 108)
BOUNDS = [100.0, 130.0, 215.0, 300.0, 370.0, 440.0, 540.0]
SECTION = re.compile(r"^(Single|Send|Master) Effect Preset$")
SKIP = {"Category", "Effect", "Preset", "List"}


def main() -> None:
    entries: list[tuple[float, str, list]] = []  # (order, kind, payload)
    order = 0.0
    for page in PAGES:
        words = page_words(PDF, page)
        lines = rows(words)
        for line in lines:
            if SECTION.match(text_of(line)):
                entries.append((order + line[0].cy / 1000, "section", text_of(line)))
        for y, label in label_groups(words, 0, BOUNDS[0], gap=8):
            if label in SKIP or SECTION.match(label) or label in ("Single", "Send", "Master"):
                continue
            entries.append((order + y / 1000, "category", label))
        # A page can carry two sections, so drop every header line, not just the
        # first one: anything holding "Category", "Preset" or "Slider" labels.
        headers = [l for l in lines
                   if any(w.text in ("Category", "Slider") for w in l)
                   or {w.text for w in l} <= {"Preset", "No."}]
        header_ys = {round(l[0].cy, 1) for l in headers}
        body = [l for l in lines
                if round(l[0].cy, 1) not in header_ys
                and not SECTION.match(text_of(l))
                and l[0].cy > min(header_ys) and l[0].cy < 800]
        ys = [l[0].cy for l in body
              if any(BOUNDS[0] <= w.cx < BOUNDS[1] and w.text.isdigit() for w in l)]
        cols = [column(body, ys, BOUNDS[i], BOUNDS[i + 1]) for i in range(len(BOUNDS) - 1)]
        for i, y in enumerate(ys):
            entries.append((order + y / 1000, "row", [c[i] for c in cols]))
        order += 1

    entries.sort(key=lambda e: e[0])
    writer = csv.writer(sys.stdout)
    writer.writerow(["section", "category", "preset_number", "preset_name", "effect_type",
                     "slider_parameter_1", "slider_parameter_2", "slider_parameter_3"])

    # Every category holds exactly eight presets, so the stream of rows splits
    # into fixed chunks of eight and lines up with the category labels in order.
    section, pending, collected = "", [], []
    for _, kind, payload in entries:
        if kind == "section":
            section = payload.split()[0].lower()
        elif kind == "category":
            pending.append(payload)
        else:
            collected.append((section, payload))

    count = 0
    for n, category in enumerate(pending):
        chunk = collected[n * 8:(n + 1) * 8]
        numbers = [row[0] for _, row in chunk]
        if numbers != [str(i) for i in range(1, 9)]:
            print(f"WARNING: {category} numbering {numbers}", file=sys.stderr)
        for section, row in chunk:
            writer.writerow([section, category] + row)
            count += 1
    print(f"{count} effect presets in {len(pending)} categories", file=sys.stderr)


if __name__ == "__main__":
    main()
