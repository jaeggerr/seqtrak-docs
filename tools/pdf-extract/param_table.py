#!/usr/bin/env python3
"""Rebuild the Data List's Parameter Change Table (pp. 122-154) as CSV.

Every row of the official table becomes one CSV line with the full three-byte
address restated, so the result is greppable and needs no column carrying.

Usage: python3 tools/pdf-extract/param_table.py > data/parameters-datalist.csv
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from boxes import (Word, banded_column, column, find, page_words,  # noqa: E402
                   rows, text_of)

PDF = Path(__file__).resolve().parents[2] / "reference" / "SEQTRAK_data_list_En_D0.pdf"
FIRST, LAST = 122, 154
SIZE = re.compile(r"^\d+$")
ADDR = re.compile(r"^[0-9A-Fnmpeo]{2}$")


def geometry(words: list[Word]) -> dict[str, float]:
    size = find(words, "size")
    hexes = sorted((w for w in words if w.text == "(HEX)"), key=lambda w: w.x0)
    default = hexes[-1]
    return {
        "high": size.x0 - 60, "mid": size.x0 - 42, "low": size.x0 - 25,
        "size": size.x0 - 6, "range": size.x0 + 24, "name": 155.0,
        "desc": 305.0, "default": default.x0 - 6, "notes": 497.0, "end": 600.0,
    }


BASE_ADDRESS_PAGE = 119


def base_address_blocks() -> dict[tuple[str, str], str]:
    """(high, mid) -> block name, read from the Parameter Base Address page."""
    words = page_words(PDF, BASE_ADDRESS_PAGE)
    out: dict[tuple[str, str], str] = {}
    group = ""
    for line in rows(words):
        cells = [w.text for w in line]
        hexes = [w for w in line if ADDR.match(w.text) and 165 <= w.cx < 212]
        if len(hexes) != 3:
            continue
        prefix = " ".join(w.text for w in line if w.cx < hexes[0].x0 - 2)
        name = " ".join(w.text for w in line if w.cx > hexes[-1].x1)
        group = prefix or group
        name = re.sub(r"\s*\[.*", "", name).strip()
        out[(hexes[0].text, hexes[1].text)] = f"{group} / {name}" if name else group
    return out


def block_title(words: list[Word], top: float) -> str:
    head = [w for w in words if w.cy < top - 6 and w.cy > 50 and w.x0 < 440]
    return " / ".join(text_of(line) for line in rows(head)) if head else ""


def parse_page(page: int) -> tuple[list[dict], str]:
    words = page_words(PDF, page)
    geo = geometry(words)
    header = find(words, "Address")
    title = block_title(words, header.cy)

    body = [w for w in words if w.cy > header.cy + 8 and w.cy < 800]
    lines = rows(body)
    anchors = []
    for line in lines:
        sizes = [w for w in line if SIZE.match(w.text) and geo["size"] <= w.cx < geo["range"]]
        if sizes:
            anchors.append((line[0].cy, sizes[0].text))

    ys = [a[0] for a in anchors]
    # Address, size, Range and Default are top-aligned on the row's own line;
    # Parameter Name, Description and Notes are centred in the row.
    cols = {
        key: banded_column(lines, ys, geo[key], geo[nxt])
        for key, nxt in [("high", "mid"), ("mid", "low"), ("low", "size"),
                         ("range", "name"), ("default", "notes")]
    }
    cols.update({
        key: column(lines, ys, geo[key], geo[nxt])
        for key, nxt in [("name", "desc"), ("desc", "default"), ("notes", "end")]
    })
    out = []
    for i, (_, size) in enumerate(anchors):
        out.append({
            "high": _addr(cols["high"][i]),
            "mid": _addr(cols["mid"][i]),
            "low": _addr(cols["low"][i]),
            "size": size,
            "range_hex": cols["range"][i],
            "default_hex": cols["default"][i],
            "name": _unheader("name", cols["name"][i]),
            "description": _unheader("description", cols["desc"][i]),
            "notes": _unheader("notes", cols["notes"][i]),
            "block": title,
            "page": str(page),
        })
    return out, title


def _addr(text: str) -> str:
    """Keep only address-shaped tokens; block headings can overlap the column."""
    return " ".join(t for t in text.split() if ADDR.match(t))


# The three centred columns are banded by y, and on a page where the column
# labels sit within 8 points of the word "Address" they fall inside the first
# row's band instead of above it. The label then prefixes the real cell:
# `49 o9 00` came out named "Parameter Name ON/OFF". No parameter is called
# after its own column, so stripping the label is unambiguous.
HEADERS = {"name": "Parameter Name", "description": "Description", "notes": "Notes"}


def _unheader(key: str, text: str) -> str:
    label = HEADERS[key]
    return text[len(label):].strip() if text.strip().startswith(label) else text


def main() -> None:
    rows_out: list[dict] = []
    blocks = base_address_blocks()
    carried = ""
    high = mid = ""
    for page in range(FIRST, LAST + 1):
        page_rows, title = parse_page(page)
        carried = title or carried
        for row in page_rows:
            if not row["low"] or row["name"] == "(HEX)":
                continue  # "TOTAL SIZE =" footer line
            high = row["high"] or high
            mid = row["mid"] or mid
            row["high"], row["mid"] = high, mid
            row["block"] = blocks.get((high, mid)) or row["block"] or carried
            rows_out.append(row)

    fields = ["block", "high", "mid", "low", "size", "range_hex", "default_hex",
              "name", "description", "notes", "page"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows_out)
    print(f"{len(rows_out)} parameter rows", file=sys.stderr)


if __name__ == "__main__":
    main()
