# seqtrak-docs — everything known about the Yamaha SEQTRAK protocol

A single, self-contained, English-language reference for the Yamaha SEQTRAK: its
MIDI and SysEx protocol, every parameter, its preset and waveform catalogues, its
effect system, its bulk and file transports, its firmware update channel, and
what the hardware has actually been observed doing.

**This repository is written to be read by an LLM.** Explicit tables over prose,
addresses in hex, one fact per row, machine-readable companions in
[`data/`](data/), and a confidence marker on every non-obvious claim. If you are
an agent, start with [AGENTS.md](AGENTS.md).

Nothing here requires opening a PDF. Every fact used by the documentation is
transcribed into Markdown or CSV. Yamaha's two PDFs are not redistributed;
[`reference/`](reference/README.md) says where to download them if you want to
re-run the extractors or check a transcription.

## What the SEQTRAK is

A battery-powered Yamaha groovebox: an 11-track sequencer with four sound
engines (AWM2 sample playback, a 4-operator FM engine, a sampler), a built-in
speaker and microphone, in a 343 × 97 × 38 mm box. 2424 factory presets, 2024
preset waveforms, 8 projects, 6 patterns per track, up to 128 steps per pattern.

**It has no screen.** Its whole display surface is about twenty silkscreened
words with one LED each, plus a column of eight LEDs that renders every numeric
value as "how many dots are lit" — and it never shows the name of anything. That
is why this protocol matters: it is the only way to see what the machine is
doing, and the only way to reach the large parts of it the front panel cannot.

Yamaha has effectively stopped developing the product. This repository is the
community-side reference that fills the gap.

## Source and confidence legend

Every non-obvious claim carries one of four markers. They are deliberately
greppable and deliberately never blurred together.

| Marker | Meaning |
|---|---|
| `verified on hardware` | observed on a real SEQTRAK. The strongest claim in this repository. |
| `from Yamaha Data List` | published by Yamaha in the *SEQTRAK Data List* (OS V2.00) or the *User Guide*. Authoritative, but covers only part of the real surface. |
| `reverse-engineered from app traffic` | derived by watching MIDI traffic between the official app and the hardware, or read out of a working third-party implementation. Behaviourally grounded; structure partly inferred. |
| `from the official app, untested` | recovered from the official macOS app's own parameter definitions. Addresses are highly reliable, semantics come from the app's own names, and nothing was sent to a machine. |
| `from firmware image (static analysis)` | recovered from the official firmware update file. Checked byte for byte against the artefact and reproducible, which makes it strong — but it describes a **file**, not runtime behaviour, so it can never establish what the hardware does with it. Used only in [docs/09-firmware.md](docs/09-firmware.md). |

```bash
grep -rn "verified on hardware" docs/            # what is certain
grep -rn "untested" docs/                        # what is not
```

### Why the unverified parts are credible

The two large sources — Yamaha's published table and the static extraction from
the official app — were produced completely independently, and they overlap on
the System zone (`00 00 xx`).

**All 37 System-zone parameters recovered from the official app match the Data
List exactly**, addresses and value ranges alike, with zero mismatches.

Across the whole table: **1753 addresses**, of which 257 appear in both sources,
118 only in the official app (the genuinely undocumented zones) and 1378 only in
the Data List. Of the 216 overlapping rows with a comparable value range,
**212 agree exactly**, and the four that do not are each explained in
[docs/12-open-questions.md](docs/12-open-questions.md#4-four-value-ranges-where-the-two-sources-disagreed--all-explained):
one per-engine restriction, one case of the app being permissive, one rendering
artefact, and one app-side artefact disproved on hardware. **No disagreement
between the two parameter sources is left open.**

Reproduce the comparison:

```bash
python3 tools/cross_check.py
```

That agreement is the reason the app-only zones — live state, user
scales, step record, song mode, Wi-Fi, firmware — are worth trusting as a
starting point.

And the hardware then confirmed it: **33 of 33 probed addresses answered**,
including every zone known only from the official app — and two undocumented
zones have since been **written** to and restored, among them the step
sequencer, which means patterns can be composed from outside the machine. See
[docs/10-verified-behaviour.md](docs/10-verified-behaviour.md).

## Where to look for what

### Start here

| File | Contents |
|---|---|
| [AGENTS.md](AGENTS.md) | how an agent should use this repository: which file answers which kind of question |
| [docs/01-overview.md](docs/01-overview.md) | the hardware: tracks, parts, MIDI channels, pads, scales, memory, power limits |
| [docs/02-sysex-format.md](docs/02-sysex-format.md) | **the one to read first for protocol work** — framing, the five message forms, the address map, encodings, checksum, bulk variants, worked examples, reference code |

### Parameter reference

One row per address, with both sources and a confidence marker on each.

| File | Zone |
|---|---|
| [docs/03a-parameters-system.md](docs/03a-parameters-system.md) | System settings and Wi-Fi (`00 xx xx`) |
| [docs/03b-parameters-live-state.md](docs/03b-parameters-live-state.md) | live app and editing state (`01 xx xx`, `18 xx xx`) |
| [docs/03c-parameters-project.md](docs/03c-parameters-project.md) | project, send and master effects, master EQ, A/D, scales, chords, tracks (`30 xx xx`) |
| [docs/03d-parameters-sound.md](docs/03d-parameters-sound.md) | per-track sound: name, general, insertion A/B, LFO, arpeggiator (`31 xx xx`) |
| [docs/03e-parameters-element.md](docs/03e-parameters-element.md) | AWM elements and sampler samples (`41`, `42`, `50`) |
| [docs/03f-parameters-fm.md](docs/03f-parameters-fm.md) | the FM engine (`48`, `49`) |
| [docs/03g-parameters-sequencer.md](docs/03g-parameters-sequencer.md) | bulk control, step record, song mode (`11`, `12`, `70`, `71`) |

### Subsystems

| File | Contents |
|---|---|
| [docs/04-sequencer-editing.md](docs/04-sequencer-editing.md) | writing notes into patterns: step record and both piano rolls |
| [docs/05-live-state.md](docs/05-live-state.md) | the `01` zone: what the machine broadcasts as the user plays, and how to follow a knob |
| [docs/06-sounds-presets.md](docs/06-sounds-presets.md) | preset numbering, Bank Select / Program Change, and how to resolve a preset *name* |
| [docs/07-transports.md](docs/07-transports.md) | USB MIDI, BLE MIDI (with UUIDs and framing), MIDI TRS, Wi-Fi over SysEx |
| [docs/08-bulk-and-files.md](docs/08-bulk-and-files.md) | bulk dumps, project list, rename, content management, result codes, file transfer, XML |
| [docs/09-firmware.md](docs/09-firmware.md) | the firmware update protocol, and an honest custom-firmware assessment |
| [docs/10-verified-behaviour.md](docs/10-verified-behaviour.md) | **what was actually observed on a real machine** |
| [docs/11-controllers.md](docs/11-controllers.md) | the CC map, RPN, and a worked Arturia MiniLab 3 mapping |
| [docs/12-open-questions.md](docs/12-open-questions.md) | conflicts kept open, semantics still unproven, what to test next |
| [docs/13-track-types.md](docs/13-track-types.md) | re-typing a drum track as DRUM / DRUMKIT / SYNTH — the only way past two synth voices |
| [docs/14-song-mode.md](docs/14-song-mode.md) | scenes, and the practical route for getting a whole composition into a project |
| [docs/15-front-panel.md](docs/15-front-panel.md) | the front panel itself: what each printed control is called, and every button combination the User Guide documents |

### Appendices — full transcribed tables

| File | Contents |
|---|---|
| [docs/appendix-a-effect-types.md](docs/appendix-a-effect-types.md) | 95 effect types with their MSB/LSB codes and which slots accept them |
| [docs/appendix-b-effect-parameters.md](docs/appendix-b-effect-parameters.md) | every effect type's 16 parameters, with offsets, ranges and data-assign tables |
| [docs/appendix-c-sound-list.md](docs/appendix-c-sound-list.md) | all 2424 presets with bank and program numbers |
| [docs/appendix-d-wave-list.md](docs/appendix-d-wave-list.md) | all 2024 AWM waveforms |
| [docs/appendix-e-effect-presets.md](docs/appendix-e-effect-presets.md) | the 144 effect presets and their slider assignments |
| [docs/appendix-f-arpeggio-presets.md](docs/appendix-f-arpeggio-presets.md) | the 16 arpeggio presets |
| [docs/appendix-g-lfo-destinations.md](docs/appendix-g-lfo-destinations.md) | the 69 LFO destination numbers |
| [docs/appendix-h-sound-design-parameters.md](docs/appendix-h-sound-design-parameters.md) | what each hardware knob page edits, and what can be parameter-locked |
| [docs/appendix-i-midi-implementation-chart.md](docs/appendix-i-midi-implementation-chart.md) | Yamaha's MIDI implementation chart |
| [docs/appendix-j-value-conversion-tables.md](docs/appendix-j-value-conversion-tables.md) | index of the 63 effect data-assign tables and the 2 EQ frequency tables |

### Machine-readable

| File | Rows | Contents |
|---|---|---|
| [data/parameters.csv](data/parameters.csv) | 1753 | **the merged parameter table** — both sources, one row per address, plus what hardware established |
| [data/hardware-verified.csv](data/hardware-verified.csv) | 91 | **hand-maintained**: per address, what a real unit did and which document writes it up. The only input that is not an extraction |
| [data/parameters-datalist.csv](data/parameters-datalist.csv) | 1518 | the Data List's parameter table, as published |
| [data/presets.csv](data/presets.csv) | 2424 | presets with engine, category, bank and program. Engine, number, name and category are extracted; **bank and program are computed** from the number, so they are not evidence about banks |
| [data/waves.csv](data/waves.csv) | 2024 | AWM waveforms with categories |
| [data/cc-map.csv](data/cc-map.csv) | 53 | every Control Change the SEQTRAK sends or receives, with what hardware established |
| [data/effect-types.csv](data/effect-types.csv) | 95 | effect types with MSB/LSB and assignability |
| [data/effect-parameters.csv](data/effect-parameters.csv) | 1445 | per-type effect parameters |
| [data/effect-presets.csv](data/effect-presets.csv) | 144 | effect presets |
| [data/effect-data-assign-tables.csv](data/effect-data-assign-tables.csv) | 7330 | the 63 value-conversion tables effect parameters use |
| [data/eq-frequency-tables.csv](data/eq-frequency-tables.csv) | 512 | 3-band and 2-band EQ frequency tables |

### Provenance and tools

| Path | Contents |
|---|---|
| [reference/](reference/README.md) | where to download the two official Yamaha PDFs (not redistributed) |

The firmware-file facts in [docs/09-firmware.md](docs/09-firmware.md) come from
a static analysis of the official OS 2.00 updater (`8Z33OS_.PGM`, sha256
`1a87fb5a…13bcf63`), carried out in the sibling `seqtrak-firmware-analysis`
project. That file is not redistributed here and no part of it is reproduced;
what is documented is its structure.

| [tools/pdf-extract/](tools/pdf-extract/) | the extractors that turn those PDFs into the CSVs and appendices |
| [tools/build_docs.py](tools/build_docs.py) | regenerates every generated document from `data/` |
| [tools/cross_check.py](tools/cross_check.py) | compares the two parameter sources where they overlap |
| [tools/hardware-probe/](tools/hardware-probe/) | the read-only prober, the reversible write tests, and the write sweep used to settle value ranges |

## Answering the obvious questions

**How do I set the tempo?** Two-byte parameter at `30 40 76`, range 5-300:
`F0 43 10 7F 1C 0C 30 40 76 00 78 F7` sets 120 BPM. See
[docs/02-sysex-format.md](docs/02-sysex-format.md#multi-byte-integers-7-bits-per-byte-big-endian).

**How do I write a note into step 3 of the kick track?** KICK is part 0, steps
are 0-indexed, so step 3 with middle C at velocity 100 and a one-step gate is
`F0 43 10 7F 1C 0C 70 00 00 03 3C 64 00 78 F7`. Delete it again with
`F0 43 10 7F 1C 0C 70 20 00 03 F7`. Both are `verified on hardware`, and the
sequencer must be stopped. See
[docs/04-sequencer-editing.md](docs/04-sequencer-editing.md#the-verified-round-trip).

**What does address `01 1p 53` mean?** `SingleSlider1Assign` for part `p`,
range 0-24 — which parameter the first single-effect slider is assigned to. See
[docs/05-live-state.md](docs/05-live-state.md#01-1p-xx--per-part-editing-state),
and read the warning there: this is *not* how to follow a knob.

**Which preset is loaded on a track?** The machine sends Bank Select MSB, LSB
and then a Program Change whenever the sound changes, so look the triplet up in
[data/presets.csv](data/presets.csv). For user sounds or the exact stored name,
bulk-dump `11 02 pp` and read the `31 0p 00` block. See
[docs/06-sounds-presets.md](docs/06-sounds-presets.md#reading-back-which-sound-is-loaded).

**Is custom firmware feasible?** The official OS 2.00 file has **no
cryptographic signature** — its only integrity check is a 32-bit additive sum
per block, and the `Program` image is a flat ARMv7-A image in the clear. That is
a *necessary* condition, not a sufficient one: the component that validates and
writes is not in the file, and the resident loader has never been inspected. See
[docs/09-firmware.md](docs/09-firmware.md#is-custom-firmware-feasible), and read
[what the signature search could not have detected](docs/09-firmware.md#what-the-signature-search-could-not-have-detected)
before quoting the verdict.

## Reproducing everything

```bash
# Needs poppler (pdftotext, pdftoppm) and python3.
python3 tools/pdf-extract/param_table.py          > data/parameters-datalist.csv
python3 tools/pdf-extract/sound_list.py           > data/presets.csv
python3 tools/pdf-extract/wave_list.py            > data/waves.csv
python3 tools/pdf-extract/effect_types.py --csv   > data/effect-types.csv
python3 tools/pdf-extract/effect_params.py        > data/effect-parameters.csv
python3 tools/pdf-extract/effect_presets.py       > data/effect-presets.csv
python3 tools/pdf-extract/effect_assign_tables.py > data/effect-data-assign-tables.csv
python3 tools/pdf-extract/misc_tables.py eq-tables > data/eq-frequency-tables.csv
python3 tools/build_docs.py
```

`data/parameters.csv` and `data/cc-map.csv` are inputs here, not generated:
the first is the merged parameter table, maintained upstream, and the second is
transcribed by hand from the Data List's MIDI Data Format section.

## Scope and legality

This is interoperability documentation, assembled from a legitimately published
PDF, a legitimately installed application, and observation of a legitimately
owned machine. No Yamaha code is redistributed here — only names, addresses and
value ranges, which are facts about a protocol. Yamaha's PDFs are
not redistributed: they are Yamaha's copyright, and Yamaha publishes them for
free download (see [`reference/`](reference/README.md)).

## License

Everything in this repository — the documentation, the CSVs in `data/` and the
tools — is released under the [MIT License](LICENSE): use it in any client,
commercial or not, and keep the copyright notice. Yamaha's PDFs are not covered
by it, since they are Yamaha's and are not part of what is licensed.
