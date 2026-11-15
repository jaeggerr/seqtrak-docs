# 06 — Sounds and presets

How sounds are numbered, how to select one, and — the hard part — how to find
out which one is currently loaded.

The preset catalogue itself is
[appendix-c-sound-list.md](appendix-c-sound-list.md) (2424 entries) and
[`../data/presets.csv`](../data/presets.csv). The waveforms an AWM element can
point at are [appendix-d-wave-list.md](appendix-d-wave-list.md) (2024 entries).

## The four engines and their categories

Every engine has its own set of 15 categories. Categories are a browsing concept
used by the app and the hardware's category-jump; they are not part of an
address.

| No. | Drum | Synth | DX | SAMPLER |
|---|---|---|---|---|
| 1 | Kick | Bass | Bass | Vocal Count |
| 2 | Snare | Synth Lead | Synth Lead | Vocal Phrase / Chant |
| 3 | Rim | Piano | Piano | Singing Vocal |
| 4 | Clap | Keyboard | Keyboard | Robotic Vocal / Effect |
| 5 | Snap | Organ | Organ | Riser |
| 6 | Closed HiHat | Pad | Pad | Laser / Sci-Fi |
| 7 | Open HiHat | Strings | Strings | Impact |
| 8 | Shaker / Tambourine | Brass | Brass | Noise / Distorted Sound |
| 9 | Ride | Woodwind | Woodwind | Ambient / Soundscape |
| 10 | Crash | Guitar | Guitar | SFX |
| 11 | Tom | World | World | Scratch |
| 12 | Bell | Mallet | Mallet | Nature / Animals |
| 13 | Conga / Bongo | Bell | Bell | Hit / Stab / Musical Instrument Sound |
| 14 | World | Rhythmic | Rhythmic | Percussion |
| 15 | SFX | SFX | SFX | Recorded Sound |

Preset counts: **Drum 855**, **Synth 1077**, **DX 100**, **SAMPLER 392** —
2424 in total. Drum, Synth and DX share one continuous numbering space of 2032
(Drum 1-855, Synth 856-1932, DX 1933-2032); SAMPLER elements are numbered 1-392
in a space of their own.

`from Yamaha Data List`. The counts and every name were extracted twice,
independently — once by this repository's own PDF extractor and once by hand in
an earlier project — and agree on all 2424 entries, differing only in the
spacing around eight hyphens.

For laying out a display: the **longest preset name is 33 characters**,
`Singing - Female - La la la la la` (SAMPLER 79), followed by
`Punchy Kick + Electronic Ping 1` at 31. The longest waveform name is the same
33-character string. The on-wire name field holds 77 bytes of UTF-8, so no
factory name comes close to filling it.

## Bank Select and Program Change

| Bank MSB | Bank LSB | Program | Target | Memory |
|---|---|---|---|---|
| 64 | 0 | 0-8 | Project (8 = temporary) | user — **`verified on hardware`** for programs 0 and 7 |
| 63 | 0-31 | 0-127 | Sound (Drum / Synth / DX) | preset banks 1-32 |
| 63 | 32-47 | 0-127 | Sound | user banks 1-16 |
| 62 | 0-3 | 0-127 | Sampler element | preset 1-4 |
| 62 | 4-11 | 0-127 | Sampler element | user 1-8 |
| 32-38 | 0-47 | 0-127 | DrumKit sound, MSB = 32 + part (part 0-6) | preset / user |

From a sound number *n* in the shared space:

```
bank LSB = (n - 1) // 128
program  = (n - 1) %  128
```

> The bank size of 128 is `from Yamaha Data List` and nothing contradicts it,
> but it has never been isolated by a measurement, and `presets.csv`'s bank
> columns are **computed with this formula** rather than extracted — so they
> cannot be used to check it. See
> [12-open-questions.md](12-open-questions.md#the-bank-arithmetic-is-documented-and-used-but-never-pinned-by-measurement)
> for what the wire captures do and do not establish, and for the test that
> would settle it.

Three details worth knowing, all `from Yamaha Data List`:

- **Bank Select only takes effect when the Program Change arrives.** Send MSB,
  LSB, then PC.
- Unsupported bank or program numbers are **silently ignored**.
- Under bank MSB 62 the SEQTRAK **reads the MIDI channel number as the element
  number**, and programs 72 and above are temporary areas the sampler uses
  (project 1 elements 1-7, project 2 elements 1-7, and so on).

**A Program Change with no Bank Select before it is ignored**, and the bank is
**not latched**: a bare Program Change sent right after a full triplet on the
same channel is ignored too. `verified on hardware` on part 9 (DX), by reading
`01 19 33` after each message
([10-verified-behaviour.md](10-verified-behaviour.md#2026-11-15-a-program-change-needs-its-own-bank-select-every-time)); first reported by a
third party. So send all three, every time. Whether LSB + Program Change
without the MSB is enough has not been tried.

Two System switches can block reception, both on by default: `00 00 07`
(Receive/Transmit Bank Select) and `00 00 08` (Receive/Transmit Program Change).
On the transmit side the per-interface bitmasks `00 00 0B` (TRS), `00 00 0F`
(USB) and `00 00 13` (Bluetooth) gate CC, Bank Select and Program Change
independently — bit 6, bit 5 and bit 4. All three read back as `0x70`, every bit
set, on a real unit (`verified on hardware`).

### Example: load Synth preset 858 ("Acid3") on SYNTH 1

SYNTH 1 is part 7, MIDI channel 8 (status nibble `n = 7`).
`(858 - 1) // 128 = 6`, `(858 - 1) % 128 = 89`.

```
B7 00 3F     Bank Select MSB = 63
B7 20 06     Bank Select LSB = 6
C7 59        Program Change 89
```

## Reading back which sound is loaded

### The machine tells you, bank and all

When the sound changes, the SEQTRAK transmits **Bank Select MSB, Bank Select
LSB and then a Program Change** on the track's MIDI channel. `verified on
hardware`: turning the sound-select knob produced ten preset changes and ten
complete triplets — `CC 0 = 63`, `CC 32 = 7`, then the Program Change —
systematically, not only at bank boundaries.

So **bank plus program resolves a preset name from the local catalogue**, with no
round trip:

```python
def preset_name(engine_rows, bank_lsb, program):
    # Look a received Bank Select + Program Change up in data/presets.csv.
    number = bank_lsb * 128 + program + 1
    return next((r["name"] for r in engine_rows if int(r["number"]) == number), None)
```

> **This reverses an earlier conclusion.** Two sessions in 2026 reported that
> Bank Select was *never* transmitted, and this document used to say a Program
> Change could not identify a preset. That was wrong — both sessions shared an
> instrument, a nine-line scrolling log too small to see a burst of ~30
> messages, so neither could support a negative claim. The transmit
> bitmasks (`00 00 0B`, `00 00 0F`, `00 00 13`) read back with every bit set and
> are **not** cosmetic. See
> [10-verified-behaviour.md](10-verified-behaviour.md#bank-select-is-transmitted--a-documented-conclusion-reversed).

### When you still want the bulk dump

The catalogue route covers factory presets. It cannot cover:

- **user sounds**, which are not in any local table;
- the **exact** name as the machine stores it, including anything renamed.

For those, use a **single-track bulk dump** and read the name out of the Sound
Common Name block:

```
F0 43 20 7F 1C 0C 11 02 pp F7        request the sound edit buffer of part pp
```

The reply is a **burst of roughly thirty bulk-dump blocks** — the name, then the
sound settings, then the eight elements. Filter on the address or the later
blocks will overwrite whatever you just parsed. The name is in the block at
`31 0p 00`: 88 bytes, 7-bit packed, 11 groups of 8. `verified on hardware`.

This is correct for **user** sounds as well as presets, and it is fast enough
that scrolling presets with the knob shows no perceptible lag.
`verified on hardware`.

### Sound Common Name block layout

106 bytes per part, at `31 0p 00`. Structure `reverse-engineered from app
traffic` out of a project edit-buffer dump; the 88-byte name field and the block
size are `from Yamaha Data List`.

| Offset | Size | Field | Values |
|---|---|---|---|
| `00`-`57` | 88 | Sound name | UTF-8, 7-bit packed (see [02-sysex-format.md](02-sysex-format.md#strings-and-blobs-7-into-8-packing)) |
| `58`-`64` | 13 | reserved | zero |
| `65` | 1 | Engine type | `01` Drum, `02` Synth, `04` DX, `05` Sampler |
| `66` | 1 | Sub-type | `00` Drum/Sampler, `01` Synth, `02` DX — tentative |
| `67` | 1 | Category index | 0-14, into that engine's category table |
| `68`-`69` | 2 | reserved | zero |

Sound names read out of a factory project, part by part:

| Part | Track | Example name |
|---|---|---|
| 0 | KICK | Tight Punchy Kick 1 |
| 1 | SNARE | Tight Snare 1 |
| 2 | CLAP | Hand Clap 1 |
| 3 | HAT 1 | Tight Closed Hat 1 |
| 4 | HAT 2 | Bright Open Hat 1 |
| 5 | PERC 1 | Acoustic High Tom 1 |
| 6 | PERC 2 | Shaker 1 |
| 7 | SYNTH 1 | Prec Flat Wound |
| 8 | SYNTH 2 | Pedal Steel |
| 9 | DX | Square |
| 10 | SAMPLER | *(empty — user sample)* |

### The cheaper, less certain route

`01 1p 33` (`CurrentSound`, 2 bytes) holds the current sound number for a part
and can be read with a single Parameter Request. It is **not broadcast** when
the sound changes, so it is a poll, not a notification — but its numbering is
now established.

**It does not answer on the SAMPLER part.** `01 1A 33` went unanswered in eight
attempts across two independent clients on 2026-10-23, while `01 17 33` (SYNTH
1) answered immediately before and after, and `01 1A 3C` had answered on the
same part in an earlier session. So the part nibble and the address family are
both fine; it is this parameter on this part that is silent. A plausible reason
is that the sampler's loaded thing is an **element**, not a sound — under bank
MSB 62 the MIDI channel number is read as the element number — but that is
inference, not measurement. [12-open-questions.md](12-open-questions.md).

**The mapping is the catalogue number minus one.** `verified on hardware`:

```
CurrentSound = bank_lsb × 128 + program = catalogue number − 1
```

Measured twice over, by two different routes.

*Reading.* The seven drum parts of a factory project 0 read 2, 112, 248, 311,
384, 553 and 456. Decoded with the formula above they are Tight Punchy Kick 3,
Tight Snare 1, Hand Clap 1, Tight Closed Hat 1, Bright Open Hat 1, Acoustic Mid
Tom 4 and Shaker 1 — kick, snare, clap, closed hat, open hat, tom, shaker, in
that order, which is the factory layout of the machine. Seven simultaneous
matches do not happen by chance, but on its own this is still inference.

*Writing.* Ten presets were then loaded by Bank Select + Program Change on each
part's own channel and `01 1p 33` read back. All ten returned the predicted
number, across four different bank LSBs and the Drum, Synth and DX spaces.
That closes it: a known input produced the predicted output.

This upgrades what this section previously said — that the mapping "has not
been checked". It has.

`01 1p 35` (`CurrentSoundName`, 87 bytes) is still untested.

One part answered nothing at all: **part 10 (SAMPLER) gave no reply** to
`01 1A 33` on a factory project, where its sound slot is empty. Consistent
with the table above, but it means a missing reply on that part is not
by itself evidence about the address.

## Waveforms

An AWM element points at a waveform rather than at a "sound":

| Parameter | Address | Meaning |
|---|---|---|
| `Wave Select` | `41 ep 01` | 0 = preset, 1 = user |
| `Wave Number` | `41 ep 03` | 2 bytes, 1-4096 preset (2024 populated), 1-2048 user |

The 2024 preset waveforms are listed in
[appendix-d-wave-list.md](appendix-d-wave-list.md) with their main and sub
categories. Preset wave memory is 800 MB as 16-bit linear; user wave memory is
500 MB.

## Favourites and the sound browser — `0C xx xx` and `10 01 xx`

`reverse-engineered from app traffic`. This zone is how the official app drives
the hardware's category browsing and favourites list. It is not in the Data
List and not in the app's address-high enumeration either, so it is the least
certain part of this document.

### Toggling a favourite

A Bulk Dump at `10 01 xx`:

```
F0 43 00 7F 1C 00 07 0C 10 01 [engine] [LSB] [program] [flag] cc F7
```

| Field | Values |
|---|---|
| engine | `01` Drum, `02` Synth, `04` DX, `05` Sampler |
| LSB | Bank Select LSB for the sound |
| program | Program Change number |
| flag | `01` add to favourites, `00` remove |
| cc | standard Yamaha checksum |

Adding DX sound "FM Metallic Lead" (LSB `0F`, program `1F`) to favourites:

```
F0 43 00 7F 1C 00 07 0C 10 01 04 0F 1F 01 cc F7
```

### Requesting a category list

A Bulk Dump Request at `0C [mode] [param]`:

```
F0 43 20 7F 1C 0C 0C [mode] [param] F7
```

The encoding of `mode` and `param` is **not fully decoded**. Known-good
examples:

- `0C 12 01` — DX Synth Lead, the full category list
- `0C 02 0F` — the DX favourites list

### The reply

A bulk dump carrying a 4-byte count header followed by *N* entries of 228 bytes
each, so the payload is `4 + N × 228` bytes.

Count header:

| Offset | Size | Field |
|---|---|---|
| 0-1 | 2 | entry count, big-endian 16-bit |
| 2-3 | 2 | padding, `00 00` |

An empty list is a 4-byte all-zero payload. A one-entry list is 232 bytes
starting `00 01 00 00`.

Entry structure, offsets relative to the entry:

| Offset | Size | Field |
|---|---|---|
| 0-18 | 19 | sound parameters / header |
| 19-20 | 2 | sound ID: `[LSB] [program]` |
| 21-24 | 4 | padding / flags (observed `00 00 00 01`) |
| 25-124 | 100 | sound name, 7-bit packed |
| 125-224 | 100 | secondary name — e.g. "Modulation", a knob assignment |
| 225-227 | 3 | trailer (observed `00 00 01`, purpose unknown) |

The 228-byte entry size matches `SoundInfoSize = 228` read out of `MIDI.Bulk`
(`from the official app, untested`) — independent corroboration of
the slot size.

Only single-entry replies have been observed. The app sends acknowledgements
between pages, so larger categories presumably stream several responses.

### Detecting whether a sound is a favourite

Favourites are **not** a per-entry flag. The hardware keeps a separate
favourites list per engine. To decide whether a sound is a favourite:

1. request the favourites list for the engine (for example `0C 02 0F` for DX);
2. parse the `[LSB][program]` pair out of each entry;
3. compare against the category list you are displaying.

Adding or removing a favourite makes that list grow or shrink.
