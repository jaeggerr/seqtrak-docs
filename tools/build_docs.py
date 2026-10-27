#!/usr/bin/env python3
"""Render the generated reference documents under docs/ from the CSVs in data/.

The hand-written documents (01-12) explain the protocol; everything this script
writes is a straight rendering of a table, so it can be regenerated whenever an
extractor improves. Run it from the repository root:

    python3 tools/build_docs.py
"""
from __future__ import annotations

import csv
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
DOCS = REPO / "docs"
EXTRACT = REPO / "tools" / "pdf-extract"

LEGEND = (
    "> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from "
    "`reference/SEQTRAK_data_list_En_D0.pdf` by {script}.\n"
    "> Confidence: `from Yamaha Data List`.\n"
)

# Which address-high regions get their own parameter document.
ZONES: list[tuple[str, str, list[str]]] = [
    ("03a-parameters-system", "System and Wi-Fi (`00 xx xx`)", ["00"]),
    ("03b-parameters-live-state", "Live app state (`01 xx xx`, `18 xx xx`)", ["01", "18"]),
    ("03c-parameters-project", "Project, tracks and master effects (`30 xx xx`)", ["30"]),
    ("03d-parameters-sound", "Sound, per track (`31 xx xx`)", ["31"]),
    ("03e-parameters-element", "AWM elements and sampler (`41`, `42`, `50`)",
     ["41", "42", "50"]),
    ("03f-parameters-fm", "FM engine (`48`, `49`)", ["48", "49"]),
    ("03g-parameters-sequencer", "Sequencer and song (`11`, `12`, `70`, `71`)",
     ["11", "12", "70", "71"]),
]


def read(name: str) -> list[dict]:
    with open(DATA / name, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def cell(text: str) -> str:
    return text.replace("|", "\\|").strip()


def write(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(REPO)}")


def run(script: str, *args: str) -> str:
    return subprocess.run(
        ["python3", str(EXTRACT / script), *args],
        check=True, capture_output=True, text=True, cwd=REPO,
    ).stdout


def source_marker(source: str, hardware: str = "", document: str = "") -> str:
    """The confidence marker for one row.

    `source` is the provenance of the *definition*. It cannot say whether the
    behaviour has been exercised, so an address with a hardware result is
    rendered as `verified on hardware` instead — otherwise the generated tables
    would call a measured address untested, which is the opposite of this
    repository's evidence discipline.
    """
    base = {
        "Yamaha Data List": "from Yamaha Data List",
        "Yamaha Data List + official app": "from Yamaha Data List",
        "official app": "from the official app, untested",
    }[source]
    if not hardware:
        return base
    # Keep the provenance alongside the measurement. Dropping it would lose the
    # fact that Yamaha documented the row, and a parameter that is both
    # published and measured is the strongest standing in this repository.
    where = f" ([{document}]({document}))" if document else ""
    provenance = "" if source == "official app" else \
        " — also `from Yamaha Data List`"
    return f"`verified on hardware`{where} — {hardware}{provenance}"


def parameters() -> None:
    rows = read("parameters.csv")
    for slug, title, highs in ZONES:
        selected = [r for r in rows if r["address_high"] in highs]
        lines = [
            f"# {title}",
            "",
            "One row per address. `p` is a part number, `e` an element number, "
            "`o` an FM operator number, `n` a master-effect number and `nn`/`mm` a "
            "bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how "
            "those nibbles are filled in.",
            "",
            "The **Source** column is the confidence marker. "
            "`from Yamaha Data List` means the row is in Yamaha's published table. "
            "`from the official app, untested` means it was recovered "
            "from the official app and has no Yamaha documentation. "
            "`verified on hardware` means the behaviour was established on a real "
            "unit, and the cell says what was established and where it is written "
            "up — that comes from "
            "[`../data/hardware-verified.csv`](../data/hardware-verified.csv), the "
            "one input to this table that is not an extraction. A marker there is "
            "an assertion about **that** address, never about its block or its "
            "neighbours.",
            "",
            "Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).",
            "",
            f"{len(selected)} addresses.",
            "",
            "| Address | Block | Parameter | Size | Value range (hex) | Default (hex) "
            "| Display / meaning | App name | Notes | Source |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for r in selected:
            address = f"`{r['address_high']} {r['address_mid']} {r['address_low']}`"
            name = r["parameter"] or r["app_name"]
            if name.startswith("<key="):
                # The official app stores the parameter's name as a dictionary key
                # read from an enum; a handful could not be resolved.
                name = "*(name unresolved)*"
            size = r["size_bytes"] or r["app_size"]
            value = r["value_range"] or (
                f"{r['app_min']} - {r['app_max']} (decimal)"
                if r["app_min"] else "")
            display = r["display_range"] or r["app_display"]
            lines.append(
                f"| {address} | {cell(r['block'])} | {cell(name)} | {size} | "
                f"{cell(value)} | {cell(r['default'])} | {cell(display)} | "
                f"`{r['app_name']}` | {cell(r['notes'])} | "
                f"{source_marker(r['source'], r.get('hardware', ''), r.get('hardware_document', ''))} |"
            )
        write(DOCS / f"{slug}.md", lines)


def effect_types() -> None:
    table = run("effect_types.py")
    write(DOCS / "appendix-a-effect-types.md", [
        "# Appendix A — Effect type list",
        "",
        LEGEND.format(script="`tools/pdf-extract/effect_types.py`"),
        "",
        "The **MSB** and **LSB** columns are the two bytes written to an effect "
        "block's type parameter (offset `00`-`01` of a Send Reverb, Send Delay, "
        "Master Effect or Insertion Effect block). **Assignable to** lists the "
        "effect slots that accept the type.",
        "",
        "The check marks in the source table are Wingdings glyphs; they are read "
        "back by column position, and the columns are calibrated against the "
        "header labels, so a mark can only land in the column it was drawn in.",
        "",
        table.rstrip(),
    ])


def effect_parameters() -> None:
    rows = read("effect-parameters.csv")
    lines = [
        "# Appendix B — Effect parameter list",
        "",
        LEGEND.format(script="`tools/pdf-extract/effect_params.py`"),
        "",
        "Each effect type exposes up to 16 parameters. Parameter *k* is written at "
        "offset `al = 0x01 | (k << 1)` inside its effect block — two bytes, MSB "
        "first — so parameter 1 is at `03`, parameter 2 at `05`, and so on. That "
        "formula came out of the official app and has been confirmed twice against "
        "live traffic (`verified on hardware`, see "
        "[10-verified-behaviour.md](10-verified-behaviour.md)).",
        "",
        "**Value range** is what goes on the wire; **display range** is what the "
        "hardware and app show. **Data assign table** names the conversion table "
        "between them, in "
        "[`../data/effect-data-assign-tables.csv`](../data/effect-data-assign-tables.csv). "
        "**Default slider** is which of the three hardware sliders picks that "
        "parameter up by default.",
        "",
        f"{len(rows)} rows. Machine-readable: "
        "[`../data/effect-parameters.csv`](../data/effect-parameters.csv).",
        "",
    ]
    current = None
    for r in rows:
        key = (r["block"], r["effect_types"])
        if key != current:
            current = key
            lines += ["", f"## {r['effect_types']} — {r['block']}", ""]
            if r["panel_note"]:
                lines += [f"> {r['panel_note']}", ""]
            lines += [
                "| No. | Offset | Parameter | Display range | Value range | "
                "Data assign table | Default slider |",
                "|---|---|---|---|---|---|---|",
            ]
        number = r["parameter_number"]
        offset = ""
        if number.isdigit() and 1 <= int(number) <= 16:
            offset = f"`{0x01 | (int(number) << 1):02X}`"
        lines.append(
            f"| {number} | {offset} | {cell(r['parameter'])} | "
            f"{cell(r['display_range'])} | {cell(r['value_range'])} | "
            f"{cell(r['data_assign_table'])} | {cell(r['default_slider'])} |"
        )
    write(DOCS / "appendix-b-effect-parameters.md", lines)


def sound_list() -> None:
    rows = read("presets.csv")
    lines = [
        "# Appendix C — Preset sound list",
        "",
        LEGEND.format(script="`tools/pdf-extract/sound_list.py`"),
        "",
        f"All {len(rows)} factory presets. Drum, Synth and DX share one numbering "
        "space (1-2032) under bank MSB 63; SAMPLER elements are numbered from 1 "
        "under bank MSB 62. **LSB** = `(number - 1) / 128`, **PC** = "
        "`(number - 1) % 128`.",
        "",
        "The SEQTRAK transmits Bank Select MSB, Bank Select LSB and then a "
        "Program Change whenever the sound changes (`verified on hardware`), so a "
        "received triplet resolves to a row of this table directly. For **user** "
        "sounds, which are not listed here, and for the exact stored name, dump "
        "`31 0p 00` instead — see "
        "[06-sounds-presets.md](06-sounds-presets.md).",
        "",
        "Machine-readable: [`../data/presets.csv`](../data/presets.csv).",
        "",
    ]
    engine = category = None
    for r in rows:
        if r["engine"] != engine:
            engine = r["engine"]
            category = None
            count = sum(1 for x in rows if x["engine"] == engine)
            lines += ["", f"## {engine} sounds ({count})", ""]
        if r["category"] != category:
            category = r["category"]
            count = sum(1 for x in rows
                        if x["engine"] == engine and x["category"] == category)
            lines += ["", f"### {category} ({count})", "",
                      "| No. | Name | Bank MSB | Bank LSB | Program |",
                      "|---|---|---|---|---|"]
        lines.append(f"| {r['number']} | {cell(r['name'])} | {r['bank_msb']} | "
                     f"{r['bank_lsb']} | {r['program']} |")
    write(DOCS / "appendix-c-sound-list.md", lines)


def wave_list() -> None:
    rows = read("waves.csv")
    lines = [
        "# Appendix D — AWM wave list",
        "",
        LEGEND.format(script="`tools/pdf-extract/wave_list.py`"),
        "",
        f"The {len(rows)} preset waveforms an AWM element can point at. The number "
        "goes into **Wave Number**, the 14-bit parameter at `41 ep 03` "
        "(`Wave Select` at `41 ep 01` chooses preset or user memory). The "
        "parameter accepts 1-4096 while only these are populated.",
        "",
        "Machine-readable: [`../data/waves.csv`](../data/waves.csv).",
        "",
    ]
    main = None
    for r in rows:
        if r["main_category"] != main:
            main = r["main_category"]
            count = sum(1 for x in rows if x["main_category"] == main)
            lines += ["", f"## {main} ({count})", "",
                      "| No. | Name | Sub category |", "|---|---|---|"]
        lines.append(f"| {r['number']} | {cell(r['name'])} | "
                     f"{cell(r['sub_category'])} |")
    write(DOCS / "appendix-d-wave-list.md", lines)


def effect_presets() -> None:
    rows = read("effect-presets.csv")
    lines = [
        "# Appendix E — Effect preset list",
        "",
        LEGEND.format(script="`tools/pdf-extract/effect_presets.py`"),
        "",
        "The eight-per-category presets the hardware's effect selection steps "
        "through. A preset sets the effect type plus a template number "
        "(offset `02` of the effect block) and decides which parameters the three "
        "sliders control.",
        "",
        "Machine-readable: [`../data/effect-presets.csv`](../data/effect-presets.csv).",
        "",
    ]
    section = category = None
    for r in rows:
        if (r["section"], r["category"]) != (section, category):
            section, category = r["section"], r["category"]
            lines += ["", f"## {section.capitalize()} effect — {category}", "",
                      "| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |",
                      "|---|---|---|---|---|---|"]
        lines.append(
            f"| {r['preset_number']} | {cell(r['preset_name'])} | "
            f"{cell(r['effect_type'])} | {cell(r['slider_parameter_1'])} | "
            f"{cell(r['slider_parameter_2'])} | {cell(r['slider_parameter_3'])} |"
        )
    write(DOCS / "appendix-e-effect-presets.md", lines)


def value_tables() -> None:
    """Index the two families of pure value-conversion tables."""
    assign = read("effect-data-assign-tables.csv")
    eq = read("eq-frequency-tables.csv")
    index: dict[str, tuple[str, int, str, str]] = {}
    for row in assign:
        key = row["table"]
        if key not in index:
            index[key] = (row["quantity"], 0, row["data"], row["data"])
        name, count, lo, hi = index[key]
        index[key] = (name, count + 1, lo, row["data"])

    lines = [
        "# Appendix J — Value conversion tables",
        "",
        LEGEND.format(script="`tools/pdf-extract/effect_assign_tables.py` and "
                             "`tools/pdf-extract/misc_tables.py`"),
        "",
        "Two families of lookup tables turn a transmitted byte into the value the "
        "hardware shows. They are long and purely numeric, so the rows live in CSV "
        "rather than in Markdown; this page is the index.",
        "",
        "## Effect data assign tables",
        "",
        "Referenced by number from the **Data assign table** column of "
        "[appendix-b-effect-parameters.md](appendix-b-effect-parameters.md). Rows: "
        "[`../data/effect-data-assign-tables.csv`](../data/effect-data-assign-tables.csv) "
        f"({len(assign)} rows across {len(index)} tables).",
        "",
        "```bash",
        "# every entry of table 41 (short delay times)",
        "awk -F, '$1==41' data/effect-data-assign-tables.csv",
        "```",
        "",
        "| Table | Quantity | Entries | Data range |",
        "|---|---|---|---|",
    ]
    for key in sorted(index, key=int):
        name, count, lo, hi = index[key]
        lines.append(f"| {key} | {name} | {count} | {lo} - {hi} |")

    eq_tables = sorted({row["table"] for row in eq})
    lines += [
        "",
        "Table numbers are Yamaha's own and are not contiguous — there is no "
        "table 40.",
        "",
        "## EQ frequency tables",
        "",
        "Used by the 3-band and 2-band EQ frequency parameters, which are "
        "two-byte values. Each row gives the decimal data value, the two "
        "transmitted bytes in hex, and the resulting frequency in Hz. Rows: "
        "[`../data/eq-frequency-tables.csv`](../data/eq-frequency-tables.csv) "
        f"({len(eq)} rows).",
        "",
        "| Table | Entries | Data range |",
        "|---|---|---|",
    ]
    for name in eq_tables:
        values = [int(r["data_dec"]) for r in eq if r["table"] == name]
        lines.append(f"| {name} | {len(values)} | {min(values)} - {max(values)} |")
    write(DOCS / "appendix-j-value-conversion-tables.md", lines)


def simple(script: str, args: list[str], path: str, title: str, intro: list[str]) -> None:
    table = run(script, *args)
    write(DOCS / path, [f"# {title}", "",
                        LEGEND.format(script=f"`tools/pdf-extract/{script}`"), "",
                        *intro, "", table.rstrip()])


def main() -> None:
    parameters()
    effect_types()
    effect_parameters()
    sound_list()
    wave_list()
    effect_presets()
    simple("arpeggio_presets.py", [], "appendix-f-arpeggio-presets.md",
           "Appendix F — Arpeggio preset list",
           ["`ARP Template` (`31 5p 00`, and CC 27) selects one of these 16 "
            "presets. Each sets the arpeggiator's type, key mode and octave "
            "range; `ARP Type` (`31 5p 1E`) can also be set directly."])
    simple("misc_tables.py", ["lfo-destination"], "appendix-g-lfo-destinations.md",
           "Appendix G — LFO destination numbers",
           ["The value written to `LFO Box1/2/3 Destination` "
            "(`31 4p 0B`, `0E`, `11`). Destinations 0-23 and 32-55 reach the two "
            "insertion effects' parameters; 64-68 reach element-level controls. "
            "The last two columns say which engines accept the destination."])
    simple("misc_tables.py", ["sound-design"], "appendix-h-sound-design-parameters.md",
           "Appendix H — Sound design parameter list",
           ["What each hardware knob page edits, per engine, and which of those "
            "parameters can be parameter-locked or motion-recorded. This is the "
            "bridge between a physical control and the SysEx address that backs "
            "it: look the detailed parameter name up in the parameter documents "
            "(`03a`-`03g`)."])
    simple("misc_tables.py", ["midi-chart"], "appendix-i-midi-implementation-chart.md",
           "Appendix I — MIDI implementation chart",
           ["Yamaha's standard chart, dated 26 September 2023, version 1.0. "
            "`O` means supported, `X` not supported."])
    value_tables()


if __name__ == "__main__":
    main()
