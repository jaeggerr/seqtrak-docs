# CLAUDE.md — how to use this repository

*(Identical to [AGENTS.md](AGENTS.md); edit both together.)*

This repository is a reference, not a codebase. It documents the Yamaha SEQTRAK
groovebox's MIDI/SysEx protocol. Nothing in it runs against hardware except the
scripts in [`tools/hardware-probe/`](tools/hardware-probe/).

If you are answering a question about the SEQTRAK, the answer is almost
certainly already written down here. Find it rather than deriving it.

## Which file answers which question

| The question | Read |
|---|---|
| How do I build a SysEx message at all? | [docs/02-sysex-format.md](docs/02-sysex-format.md) — read this before anything else |
| What is at address `ah am al`? | `grep` [data/parameters.csv](data/parameters.csv), then the matching `docs/03x-parameters-*.md` |
| Has *this address* been tried on hardware, and what happened? | `grep` [data/hardware-verified.csv](data/hardware-verified.csv) — or the `hardware` column of `parameters.csv` |
| What address is parameter *X* at? | `grep -i` [data/parameters.csv](data/parameters.csv) by name |
| How many tracks / what MIDI channel / how much power on USB? | [docs/01-overview.md](docs/01-overview.md) |
| How do I put a note in a pattern? | [docs/04-sequencer-editing.md](docs/04-sequencer-editing.md) |
| What does the machine send when the user turns a knob? | [docs/05-live-state.md](docs/05-live-state.md) |
| Which preset is loaded? What is it called? | [docs/06-sounds-presets.md](docs/06-sounds-presets.md) |
| What is the BLE service UUID / how is a BLE packet framed? | [docs/07-transports.md](docs/07-transports.md) |
| How do I dump or rename a project? | [docs/08-bulk-and-files.md](docs/08-bulk-and-files.md) |
| Can I flash my own firmware? | [docs/09-firmware.md](docs/09-firmware.md) |
| Is this actually true? Has anyone tested it? | [docs/10-verified-behaviour.md](docs/10-verified-behaviour.md) |
| What CC does what? | [data/cc-map.csv](data/cc-map.csv), [docs/11-controllers.md](docs/11-controllers.md) — its `hardware` column says which eight have been seen on a real unit |
| What is still unknown or contradictory? | [docs/12-open-questions.md](docs/12-open-questions.md) |
| How do I turn a drum track into a synth track? | [docs/13-track-types.md](docs/13-track-types.md) |
| How do I write a whole song, or chain patterns into scenes? | [docs/14-song-mode.md](docs/14-song-mode.md) |
| What button combination does *X* on the machine itself? What is that control called? | [docs/15-front-panel.md](docs/15-front-panel.md) — the front panel, not the wire |
| What effect types exist and what is their code? | [docs/appendix-a-effect-types.md](docs/appendix-a-effect-types.md) |
| What does effect parameter 5 of CROSS DELAY do? | [docs/appendix-b-effect-parameters.md](docs/appendix-b-effect-parameters.md) |
| What is preset 1432 called? | `grep` [data/presets.csv](data/presets.csv) |
| What hardware knob maps to which parameter? | [docs/appendix-h-sound-design-parameters.md](docs/appendix-h-sound-design-parameters.md) |
| What value does effect byte 73 of data-assign table 41 mean? | [docs/appendix-j-value-conversion-tables.md](docs/appendix-j-value-conversion-tables.md), then [data/effect-data-assign-tables.csv](data/effect-data-assign-tables.csv) |

For anything numeric and bulky — parameters, presets, waveforms, effect
parameters, value-conversion tables — **prefer the CSV in `data/` over the
Markdown**. The Markdown appendices are the same data, rendered; the CSVs are
smaller to search and easier to join.

**Two columns, two different facts.** `source` is the provenance of the
parameter's **definition** — its address, name and range. `hardware` is what a
real unit did when it was asked, and `hardware_document` points at the write-up.
A measurement does not change where a definition came from, so the two never
overwrite each other, and a row can legitimately read "official app" in one and a verified result in the other.

That split exists because the `source` vocabulary has only three values —
`Yamaha Data List`, `Yamaha Data List + official app`, `official app` — and **none of them can express a hardware verification**. Before
`hardware` existed, every measurement was lost the moment the CSV was rebuilt,
and the generated tables called 53 measured addresses "untested". That is the
opposite of the evidence discipline below, in the one file meant to be read
without human judgement.

`data/hardware-verified.csv` is where a verification is recorded, and it is the
**only input to `parameters.csv` that is not an extraction** — so it is the only
one a human maintains and the only one that can go wrong by carelessness:

- one row per address, naming **what** was established and **which document**
  writes it up. "It answered" is not a result; "read `46` = 70, battery
  percentage" is;
- a marker there asserts something about **that address**, never about its block
  or its neighbours. An over-marked row is worse than an unmarked one, because
  it manufactures a confidence nobody can later tell from a real measurement;
- addresses that are verified but are not parameter rows — `01 33 00`,
  `01 33 01`, the `70 4x xx` step-record reads — stay in the file and
  the merge reports them as prose-only. They are not
  silently dropped.

## The four confidence markers — never blur them

Every non-obvious claim in this repository carries exactly one of these strings.
They are stable and greppable, and they mean different things. The last one is
used only in [docs/09-firmware.md](docs/09-firmware.md).

| Marker | What it licenses |
|---|---|
| `verified on hardware` | state it as fact |
| `from Yamaha Data List` | state it as documented; it is authoritative but incomplete |
| `reverse-engineered from app traffic` | state it as observed behaviour whose structure is partly inferred |
| `from the official app, untested` | **always say it is untested** when relaying it. Check the `hardware` column first: 53 addresses carry a measurement that overrides this marker |
| `from firmware image (static analysis)` | state it as a fact about the update **file**; never let it imply what the hardware does with the file |

```bash
grep -rn "verified on hardware" docs/
grep -rn "from the official app, untested" docs/
```

### Evidence discipline — four rules that have each caught a real error

This repository has had **two** `verified on hardware` claims overturned, and
both failed the same way. Bank Select was documented as "never transmitted" and
the FX sliders as "no SysEx". Both were negative claims, and both were read off
the same instrument: a **nine-line scrolling log**, while the machine sent
bursts of ~105 messages in ~1.2 seconds. The receiving code was fine; the
window was too small to see what was there.

1. **Two agreeing observations are not two independent observations when they
   share an instrument.** "Verified twice" meant "verified once, twice over".
   The measurement chain is part of the claim — when you record a verification,
   say what measured it, not just what was measured.
2. **A consumer of this repository is not a source for it.** Several sibling
   projects were written *from* this documentation. When one of them agrees with
   it, that may be inheritance rather than confirmation, and citing it as
   independent corroboration launders a guess into a fact. This happened: a
   reading of the piano-roll address was credited to "a working third-party iOS
   app" when it was the user's own code, built from the same lineage. Before
   citing an implementation, ask what *it* was written from.
3. **A table's bytes are not the table's behaviour.** Code may mask, gate or
   bypass a lookup before it happens. The official plug-in's MIDI length table
   reads `1` for four undefined status bytes, but a bitmask ahead of the lookup
   sends those to a path returning `0` — so transcribing the bytes gives you
   four wrong answers *while you believe you are verifying them*. When you cite
   a table, cite what reads it.
4. **A negative claim needs an instrument that can establish absence.** "The
   machine does not send X" is a much stronger assertion than it looks, and a
   live scrolling view cannot support it: you are sampling a window, not
   surveying the stream. Use a cumulative counter, or capture everything and
   analyse it afterwards. Both failures above would have been caught by a
   counter that was already available and simply not consulted.

Rules when you write into this repository:

- Never promote a marker without evidence of that strength. "It looks right" is
  not hardware verification.
- When something *is* verified, change the marker **and** say what was done to
  verify it — which address, which gesture, what the reply was. A verified claim
  with no method is a rumour with a better label.
- When two sources disagree, keep both, attribute each, and add it to
  [docs/12-open-questions.md](docs/12-open-questions.md). Do not silently pick a
  winner.
- Addresses in hex, uppercase, in backticks: `30 40 76`. Part/element/operator
  nibbles as `p`, `e`, `o`, `n`, matching Yamaha's own notation.

## Conventions

- **Everything is in English**, including file names, headings, table headers and
  code comments. This is non-negotiable for this repository.
- One fact per table row. Explicit tables over prose.
- Addresses are always written high, mid, low, space-separated, hex.
- Values are written in hex when the source gives hex, in decimal when it gives
  decimal, and the unit is named. Where a parameter is multi-byte, the encoding
  is named (7-bit big-endian, nibble-packed, or 7-into-8 packed).
- Part numbers are **0-based** (0-10). MIDI channels are **1-based** (1-11).
  Channel = part + 1. Getting this wrong is the most common error with this
  machine.
- Steps are 0-based. Patterns are 0-based on the wire (`30 5p 0F` = 0-5) and
  1-based in the UI (pattern 1-6).

## Regenerating the generated files

The documents under `docs/` numbered `03a`-`03g` and every `appendix-*` are
**generated** from `data/`. Do not hand-edit them; change the extractor or the
CSV and re-run:

```bash
python3 tools/build_docs.py
```

The hand-written documents are `01`, `02`, `04`-`15`, this file, `CLAUDE.md` and
`README.md`.

To rebuild the CSVs from the PDFs, see the command list at the end of
[README.md](README.md). The extractors need `pdftotext` and `pdftoppm` from
poppler; they read word bounding boxes, so they recover columns correctly even
where a cell wraps.

## Talking to real hardware

[`tools/hardware-probe/seqtrak_probe.py`](tools/hardware-probe/seqtrak_probe.py)
is read-only by default and needs `rtmidi`:

```bash
python3 tools/hardware-probe/seqtrak_probe.py --list
python3 tools/hardware-probe/seqtrak_probe.py --identity
python3 tools/hardware-probe/seqtrak_probe.py --req 30 40 76 --size 2
python3 tools/hardware-probe/seqtrak_probe.py --watch 90 --timeline
```

Three rules learned the hard way, all from
[docs/10-verified-behaviour.md](docs/10-verified-behaviour.md):

1. **A missing reply is never information.** Isolated Parameter Requests are
   dropped roughly 1 in 10. Retry four times before concluding anything.
2. **Always keep a known-good control address in the same loop** (the tempo at
   `30 40 76` is ideal). Without one, a dropped reply looks like a device
   behaviour, and a false fact gets documented.
3. **Use witnesses.** To prove what an address *means*, change one thing
   physically and re-read the target plus two or three addresses that must not
   move. Reaching an address only proves it exists.
4. **To prove a negative, build the instrument for it first.** The machine sends
   in bursts — about 105 messages in 1.2 seconds for one FX slider — so a live
   scrolling view shows you the tail and nothing else. Before writing "the
   machine never sends X", make sure you are counting cumulatively or capturing
   the whole stream. Two claims in this repository were overturned for exactly
   this reason, and in both cases a counter was already available and simply not
   consulted.

### The hardware-probe tools

| Script | What it is for |
|---|---|
| `seqtrak_probe.py` | general read-only prober: `--identity`, `--req`, `--watch`, `--plan` |
| `probe_awmtype.py` | reads `01 1p 3C` on all eleven parts, four attempts, control address interleaved |
| `listen_counter.py` | **cumulative** counter per status byte, with a self-test that injects `F2` through a virtual port first. Use this, not `--watch`, for any negative claim about what the machine sends |
| `retype_part2.py` | the full track-type cycle, witnesses on the other parts, restore in a `finally` |
| `point2_facade.py` | a self-paced silent window for capturing what a **front-panel** gesture emits |
| `element_read.py` | read-only survey of the AWM element blocks `41 ep` / `42 ep`, control address interleaved; the run that showed a multi-byte field answers only at its base address |
| `sound_common_read.py` | read-only survey of `31 1p` and `31 4p` from the reference's own CSV, checking each reply's **width** against the documented size |
| `continuation_check.py` | asks a two-byte field at its base and at the address inside it, to tell a structural silence from a dropped reply |
| `sampler_read.py` | reads all seven SAMPLER slots at `50 eA`, decoding the 88-byte packed name and reporting each reply's width |
| `block_read.py` | **the general one**: reads any named block from the CSV — `block_read.py "Project Common / Send Reverb"`, `--part`/`--element` for placeholder mid bytes — and checks every reply's width against the documented size |
| `reserved_stride.py` | the run that showed `30 41 33`-`41` are one-byte slots at a two-byte stride, and that the size column is wrong for them |
| `write_test.py`, `step_write_test.py`, `probe_write.py` | the reversible write cycles and a value sweep |
| `ble_trace.swift` + `ble_parse.py` | CoreBluetooth central reading the negotiated MTU and dumping raw packets, plus the only parser that can answer a framing question about them |

Two practical warnings:

- **`ble_trace` must be launched from a real terminal**, not from a sandboxed
  tool call: macOS TCC aborts a CoreBluetooth process it cannot attribute a
  Bluetooth usage description to, even a compiled binary with an embedded
  `__info_plist`, ad-hoc signed.
- **Never scan a BLE-MIDI packet byte by byte for status bytes.** A timestamp
  is `0x80 | (time & 0x7F)`, so it routinely *is* `F7`, `F1`, `F9`, `FF`. That
  mistake produced a confident, entirely false "42 un-timestamped `F7`" in this
  repository's own measurements before `ble_parse.py` was written.

Reads are safe. Writes are not: prefer a read → write → read-back → restore
cycle with the restore in a `finally`, which is what
[`tools/hardware-probe/write_test.py`](tools/hardware-probe/write_test.py) and
[`tools/hardware-probe/step_write_test.py`](tools/hardware-probe/step_write_test.py)
both do. Two zones have verified writes — a user scale pad (`30 4D 00`) and a
sequencer step (`70 tt 00`, undone by `70 (20|tt) 00`) — so those are known-good
paths rather than guesses. **The sequencer must be stopped** before writing to a
pattern: check `01 10 20` reads `0`.

To settle what range an address really accepts, use
[`tools/hardware-probe/probe_write.py`](tools/hardware-probe/probe_write.py): it
sweeps a list of values and reports each as accepted, clamped or refused, then
restores the original. That is how the last disagreement between the two
parameter sources was closed.
Never send `01 34 00` (factory reset), `01 40 00` / `01 41 00` / `01 42 00`
(remove project / sound / element) or `01 31 xx` (defragmentation)
speculatively.

## Traps worth knowing before you write any client

1. **Bank Select *is* transmitted** — MSB, LSB, then the Program Change, on
   every sound change. So a received triplet resolves a preset name straight
   out of `data/presets.csv`. (This repository said the opposite until it was
   measured properly; the bulk dump of `31 0p 00` is still the route for **user**
   sounds and exact names.)
2. **The `01 1p 5x` slider mirror is not broadcast.** To follow a knob, decode
   the SysEx Parameter Change the machine sends at the *real* parameter address.
3. **Bluetooth transmit flags are all off by default.** Over BLE a fresh machine
   sends nothing: write `00 00 11`, `00 00 13` and `00 00 14` first.
4. **About 95 % of USB MIDI traffic is null-packet padding.** Filter code index
   number `0x0` or it drowns everything. A SysEx message also arrives fragmented
   across several 4-byte packets (code index numbers `0x4` start/continue, then
   `0x5`, `0x6` or `0x7` to end), so a reassembly buffer is required; a Control
   Change fits in one packet.
5. **An FX slider's CC does not report everything it did.** One slider can drive
   several parameters; the CC gives the slider position, the SysEx gives each
   parameter that moved, and some parameters have no CC at all. Master Effect
   CCs arrive on channel 1, Single/Insertion Effect CCs on the track's channel.
6. **A single-track bulk dump returns ~30 blocks.** Filter by address or the
   later blocks overwrite what you parsed.
7. **An empty step replies with zero data bytes** — that is a valid answer, not
   a timeout.
8. **Each track has its own pattern length.** A single global playhead is only
   correct when every track shares the master length.
9. **Read the settings; do not assume the defaults.** Several apparent device
   limitations are switches, and the published defaults do not match a machine
   that has been used.
10. **The checksum covers Model ID through data, not the byte count** — the Data
   List's wording is loose on this. Arithmetic in
   [docs/02-sysex-format.md](docs/02-sysex-format.md#bulk-dump).
11. **`01 10` is two blocks.** `al < 0x30` is global session state; `al >= 0x30`
    is part 0's per-part state.
12. **Re-typing a track deletes its pattern**, and the UI order (DRUM, DRUMKIT,
    SYNTH) is not the wire order (DRUM, SYNTH, DRUMKIT). Sending the UI index
    gives a drum kit where a synth was meant.
    [docs/13-track-types.md](docs/13-track-types.md).
13. **Pace writes at 2 ms.** The official app sleeps 2 ms after every message,
    on every transport. A burst write with no pacing is untested territory.
14. **In Song mode the scene number is in the *data*, not the address.**
    `71 1p 01` + `<scene> <pattern>`. The parameter table's "range 0-1925" is a
    composite (`scene × 128 + pattern`), not a scalar bound.
## Relationship to the sibling projects

This repository is the documentation. The implementations live beside it, in
separate folders that are **not** part of this repository and must not be
modified from here: an ESP32 external display, an iOS/macOS app, a Swift BLE
library, UI mockups, a MiniLab 3 mapping and a WAV exporter.

Facts flow **into** this repository from those projects, not out of it. If you
learn something new while working in one of them, write it here, with the right
confidence marker.
