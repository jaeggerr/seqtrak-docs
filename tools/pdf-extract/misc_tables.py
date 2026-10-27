#!/usr/bin/env python3
"""Rebuild the Data List's remaining tables as Markdown or CSV.

  lfo-destination   pp. 155-156  LFO destination numbers (Markdown)
  eq-tables         pp. 157-160  3bandEQ / 2bandEQ frequency tables (CSV)
  midi-chart        p.  162      MIDI Implementation Chart (Markdown)
  sound-design      pp. 108-110  Sound Design Parameter List (Markdown)

Usage: python3 tools/pdf-extract/misc_tables.py <name>
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import (TICK, assign_spanning, column, label_groups,  # noqa: E402
                   page_words, rows, text_of)

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"


def lfo_destination() -> None:
    print("| No. | No. (HEX) | No. (BIN) | Parameter | Drum/Synth/SAMPLER part | DX part |")
    print("|---|---|---|---|---|---|")
    count = 0
    for page in (155, 156):
        lines = rows(page_words(PDF, page))
        top = max(l[0].cy for l in lines if any(w.text == "Parameter" for w in l)
                  and any(w.text.startswith("No.") for w in l))
        # "Common Parameter" and "Drum/Synth/SAMPLER Parameter" are sub-headings
        # spanning the number columns; they are not rows.
        body = [l for l in lines
                if top + 4 < l[0].cy < 800
                and not (all(w.x0 < 135 for w in l) and any(w.text == "Parameter" for w in l))]
        ys = [l[0].cy for l in body if any(60 <= w.cx < 100 and w.text.isdigit() for w in l)]
        bounds = [60.0, 100.0, 155.0, 200.0, 350.0, 470.0, 540.0]
        cols = [column(body, ys, bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
        marks = [[any(w.text == TICK and lo <= w.cx < hi for w in l)
                  for lo, hi in ((350.0, 470.0), (470.0, 540.0))]
                 for l in body if l[0].cy in ys]
        for i in range(len(ys)):
            drum = "yes" if marks[i][0] else ""
            dx = "yes" if marks[i][1] else ""
            print(f"| {cols[0][i]} | `{cols[1][i]}` | `{cols[2][i]}` | {cols[3][i]} | {drum} | {dx} |")
            count += 1
    print(f"{count} LFO destinations", file=sys.stderr)


def eq_tables() -> None:
    writer = csv.writer(sys.stdout)
    writer.writerow(["table", "data_dec", "data1_hex", "data2_hex", "frequency_hz"])
    count, table = 0, ""
    halves = [[70.0, 130.0, 189.0, 240.0, 310.0], [326.0, 388.0, 447.0, 500.0, 570.0]]
    for page in range(157, 161):
        lines = rows(page_words(PDF, page))
        for line in lines:
            text = text_of(line)
            if text.startswith("Table ") and ":" in text:
                table = text.split(":", 1)[1].strip()
        # Table 1 heads its columns DATA(DEC), table 2 MIDI(DEC).
        top = max(l[0].cy for l in lines
                  if any(w.text.startswith(("DATA(DEC)", "MIDI(DEC)")) for w in l))
        body = [l for l in lines if top + 4 < l[0].cy < 800]
        for bounds in halves:
            ys = [l[0].cy for l in body
                  if any(bounds[0] <= w.cx < bounds[1] for w in l)]
            cols = [column(body, ys, bounds[i], bounds[i + 1])
                    for i in range(len(bounds) - 1)]
            for i in range(len(ys)):
                if not cols[0][i].isdigit():
                    continue
                writer.writerow([table] + [c[i] for c in cols])
                count += 1
    print(f"{count} EQ frequency rows", file=sys.stderr)


def midi_chart() -> None:
    lines = rows(page_words(PDF, 162))
    bounds = [40.0, 135.0, 195.0, 315.0, 430.0, 580.0]
    top = next(l[0].cy for l in lines if any(w.text == "Function..." for w in l))
    body = [l for l in lines if top + 4 < l[0].cy < 760]
    ys = [l[0].cy for l in body]
    cols = [column(body, ys, bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    print("| Function | | Transmitted | Recognized | Remarks |")
    print("|---|---|---|---|---|")
    for i in range(len(ys)):
        cells = [c[i].replace("|", "\\|") for c in cols]
        if not any(cells):
            continue
        print("| " + " | ".join(cells) + " |")
    print(f"{len(ys)} chart lines", file=sys.stderr)




def sound_design() -> None:
    """Sound Design Parameter List (pp. 108-110): hardware knob -> parameter.

    Each page carries several "<engine> Sound Design" sub-tables, each with its
    own column header, so sections are located by their headings.
    """
    bounds = [55.0, 85.0, 167.0, 252.0, 316.0, 445.0, 479.0, 560.0]
    print("| Engine | Page | Adjustment item | Index display | Scope | "
          "Detailed parameter name | Parameter lock / motion recording | Note |")
    print("|---|---|---|---|---|---|---|---|")
    count = 0
    for page in (108, 109, 110):
        lines = rows(page_words(PDF, page))
        sections = [(l[0].cy, text_of(l).replace(" Sound Design", ""))
                    for l in lines if text_of(l).endswith("Sound Design")]
        header_ys = {round(l[0].cy, 1) for l in lines
                     if any(w.text == "Page" for w in l)
                     or (all(w.cx > 400 for w in l)
                         and any(w.text in ("*Parameter", "Motion", "Parameter", "Lock")
                                 for w in l))
                     or text_of(l).endswith("Sound Design")}
        body = [l for l in lines
                if sections[0][0] < l[0].cy < 800
                and round(l[0].cy, 1) not in header_ys]
        ys = [l[0].cy for l in body if any(bounds[1] <= w.cx < bounds[2] for w in l)]
        cols = [column(body, ys, bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
        # The Page number is printed once, centred over the four rows it covers.
        pages_col = assign_spanning(
            ys, label_groups([w for l in body for w in l], bounds[0], bounds[1], gap=8)
        )
        locks = [any(w.text == TICK and bounds[5] <= w.cx < bounds[6] for w in l)
                 for l in body if l[0].cy in ys]
        for i in range(len(ys)):
            engine = [name for y, name in sections if y <= ys[i]][-1]
            cells = [pages_col[i], cols[1][i], cols[2][i], cols[3][i], cols[4][i],
                     "yes" if locks[i] else "", cols[6][i]]
            print("| " + engine + " | " + " | ".join(cells) + " |")
            count += 1
    print(f"{count} sound design parameters", file=sys.stderr)


if __name__ == "__main__":
    {"lfo-destination": lfo_destination, "eq-tables": eq_tables,
     "midi-chart": midi_chart, "sound-design": sound_design}[sys.argv[1]]()
