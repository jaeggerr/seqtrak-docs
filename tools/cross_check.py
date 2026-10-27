#!/usr/bin/env python3
"""Compare the two independent parameter sources where they overlap.

The Yamaha Data List and the static extraction from the official app were
produced completely independently. Wherever they describe the same address,
they are expected to agree; this script prints every place they do not, which
is the evidence behind the confidence claims in README.md.

Usage: python3 tools/cross_check.py
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

MERGED = Path(__file__).resolve().parents[1] / "data" / "parameters.csv"


def datalist_range(text: str) -> tuple[int, int] | None:
    """Parse a Data List hex range. Multi-byte rows list one range per byte."""
    parts = text.replace(" ", "").split("-")
    if len(parts) != 2:
        return None
    try:
        return int(parts[0], 16), int(parts[1], 16)
    except ValueError:
        return None


def main() -> None:
    rows = list(csv.DictReader(open(MERGED, newline="", encoding="utf-8")))
    both = [r for r in rows if "+" in r["source"]]
    system = [r for r in both if (r["address_high"], r["address_mid"]) == ("00", "00")]

    mismatches = []
    compared = 0
    for row in both:
        expected = datalist_range(row["value_range"])
        if not expected or not row["app_min"]:
            continue
        compared += 1
        actual = (int(row["app_min"]), int(row["app_max"]))
        if expected != actual:
            mismatches.append(row)

    print(f"{len(rows)} addresses in total")
    for source, count in Counter(r["source"] for r in rows).most_common():
        print(f"  {count:5d}  {source}")
    print()
    print(f"{len(both)} addresses described by both sources, "
          f"{compared} with a comparable value range")
    print(f"{len(system)} of them in the System zone (00 00 xx)")

    system_bad = [r for r in mismatches
                  if (r["address_high"], r["address_mid"]) == ("00", "00")]
    print(f"\nSystem zone range mismatches: {len(system_bad)}")
    print(f"Range mismatches overall:     {len(mismatches)}")
    for row in mismatches:
        print(f"  {row['address_high']} {row['address_mid']} {row['address_low']}  "
              f"{row['parameter'][:34]:34s} "
              f"Data List {row['value_range']:12s} "
              f"app {row['app_min']}-{row['app_max']} "
              f"(shown {row['app_display']})")
    if mismatches:
        print("\nEach of these is accounted for in "
              "docs/12-open-questions.md section 4 — they are not open work.")


if __name__ == "__main__":
    main()
