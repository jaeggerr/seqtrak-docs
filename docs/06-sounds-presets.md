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
| 63 | 32-47 | 0-127 | Sound | user banks 1-16 — **`verified on hardware`** for LSB 32, see below |
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

### The user bank, measured

`verified on hardware`. Sweeping MSB 63, LSB 32, programs 0-31 on SYNTH 2's
channel and reading the loaded name back from
[`01 1p 35`](#reading-back-which-sound-is-loaded) after each one enumerated the
whole user bank: **programs 0-27 loaded 28 distinct user sounds, in the order
they were created**, the most recent last. Programs 28 and above left the name
unchanged, which is the documented "unsupported program numbers are silently
ignored".

Three programs in the middle of the range (15, 16, 17) also left the name
unchanged while their neighbours loaded — so the bank is **not densely packed**,
and a program that loads nothing is indistinguishable from one that reloads what
is already there. Read the name back rather than assuming a program took.

This settles the user side of the bank arithmetic for the first user bank: user
sound *k*, counting from zero, is LSB `32 + k // 128`, program `k % 128`. It
says nothing about the 128-per-bank size itself, since only 28 sounds existed —
that part of
[the open question](12-open-questions.md#the-bank-arithmetic-is-documented-and-used-but-never-pinned-by-measurement)
stands.

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

### One message for the name, including user sounds

`01 1p 35` `CurrentSoundName` answers an ordinary Parameter Request with the
loaded sound's name — 100 bytes, 7-bit packed, the same encoding as the Sound
Common Name block. One message instead of a thirty-block burst, and it is
correct for **user** sounds: it returned the names of sounds installed by
[`content_push.py`](../tools/hardware-probe/content_push.py) on all eleven
parts. `verified on hardware`.

This is the cheapest way to find out what is loaded on a track, and the only
practical way to tell which user sound a Program Change actually landed on.

### The cheaper, less certain route

`01 1p 33` (`CurrentSound`, 2 bytes) holds the current sound number for a part
and can be read with a single Parameter Request. It is **not broadcast** when
the sound changes, so it is a poll, not a notification — but its numbering is
now established.

Two limits, both `verified on hardware`:

- ~~With a **user** sound loaded it reads `00 00`, not the sound's number, so it
  cannot identify one.~~ **Contradicted, 2026-11-24.** Parts 7 and 8, both
  holding user sounds, read `20 1A` = **4122** (`clavi-B2op`) and `20 34` =
  **4148** (`fn0`), 4/4 attempts, raw bytes logged. That agrees with the note in
  [03b](03b-parameters-live-state.md) where part 8 read 4100 for a user sound
  and it matched that sound's exported `<ContentNumber>`. Three readings now say
  the address **does** report a user sound's content number. `01 1p 35` is still
  the way to get a name.
- **An anomaly in the same sweep, unexplained.** On the eleven parts of the
  current project, parts 0, 4, 5 and 6 read `0` while holding *factory* sounds,
  and parts 1, 2 and 3 read **10597**, **15205** and **14690** — above the
  documented maximum of 6143 — while their names are ordinary factory drum
  names. Raw reply for part 1: `F0 43 10 7F 1C 0C 01 11 33 52 65 F7`, 4/4
  attempts. The earlier survey of a factory project read small numbers (2, 112,
  248, …) on these same parts. **No reading is proposed**; the mapping below is
  left exactly as it was, since it was closed by a known-input test and this
  sweep does not touch that. Recorded so the next person does not take the
  formula as covering every part in every project.
- It is **not writable**. Written `858` on part 8 with four confirming reads
  around it, the loaded sound did not change and the address still read `00 00`,
  with the neighbouring part's name unmoved as witness. Loading a sound is Bank
  Select plus Program Change; this address only reports.

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

**The block is shared by parts 0-8 and 10**, so on paper a *drum* element can
be pointed at a user wave — a recorded or imported sample — just as a synth
element can. The Data List says only that the **SAMPLER track is fixed to 1
(User)**, which constrains part 10 and says nothing about the rest.
**`verified on hardware` for a synth part.** SYNTH 2 element 0 read
`41 08 01` = `01` (User) after a WAV import, with SYNTH 1 and KICK reading `00`
as witnesses in the same loop, and its `41 08 03` read **401** — the very number
the exported `.Y3S` carries as `ContentNumber − 8192`
([10-verified-behaviour.md](10-verified-behaviour.md#2026-11-23-hardware-session--an-awm-element-really-does-play-a-user-wave)).
For a **drum** part (0-6) it is still untested, and nothing on the front panel
exposes it: Yamaha's copy/paste matrix keeps samples inside the SAMPLER track
([15-front-panel.md](15-front-panel.md)). The experiment is in
[12-open-questions.md](12-open-questions.md).

**By another route it is settled.** A `.Y3S` package's element wave field
references a user waveform directly, and sounds built that way play on synth
tracks — so a non-sampler element really does reach user wave memory. Reported
by a third party, not reproduced here:
[the `.Y3S` section below](#the-y3s-content-package--how-a-sound-of-your-own-gets-in).

## The `.Y3S` content package — how a sound of your own gets in

**This is the route a host actually has.** A `.Y3S` is a sound package the
machine imports: a zip holding one folder named by the sound's UUID, with
`sound.bin`, per-waveform keybank records and one raw PCM file per keybank. It
carries both the sound *and* its user waveforms, so it is the only known way to
put your own audio into user wave memory — the SysEx bulk selectors reach a
sampler element's metadata only ([08-bulk-and-files.md](08-bulk-and-files.md)).

### Two independent third-party sources, and who found what

The format has been reverse-engineered twice, by different people, and the two
accounts cover different ground. Keeping them apart matters: one is the
container, the other is the loop.

| Source | What it establishes | When |
|---|---|---|
| [`FORMAT.md`](https://github.com/rechandler/seqtrak_sampler/blob/main/FORMAT.md) in `rechandler/seqtrak_sampler`, a **reader** for the official app's `.Y3S` exports | the package layout, the keybank table (u32 count + 64-byte records) and the record fields `+0x00`-`+0x03` (key and velocity ranges, marked uncertain), `+0x05` pan, `+0x08` root note, `+0x24` sample rate, `+0x30` last frame, `+0x3C` frame count, `+0x38` unknown. Also a sampler export's 512-byte `element.bin`, whose start and end points match what `50 eA` reports over MIDI | published first |
| [`Research/docs/10-Y3S-spec.md`](https://github.com/rexendevar/SLOPTRAK/blob/main/Research/docs/10-Y3S-spec.md) in SLOPTRAK, by `rexendevar`/`giddycadet` — the same analyst as the firmware patches in [09-firmware.md](09-firmware.md) | **the loop**: `+0x0F` and `+0x2C`, tested by import. Plus `sound.bin`'s element blocks and the wave reference, and the factory wave table's addresses in the `Program` image | 2026-11-18 |

So the container was already public when the sustain was found. **What is new is
the loop switch**, and that is the part the owner community had been missing.

One caution on reading them as two independent observations: both rule out the
same candidate list for `+0x38` (byte and word sums, CRC-16, CRC-32 halves,
Adler-32) in nearly the same words. That may be two people reaching for the
obvious list, or it may be inheritance. It is not two confirmations.

`rechandler`'s notes also carry two things worth having here:

- the official app **exports** a resampled sound as `.Y3S` but will not import
  that file into a synth track — which is why a converter exists at all;
- for a **one-shot** sampler pad, `Loop Length` over MIDI holds the sample's
  last frame, not a loop length. Their reading of the bulk checksum (Model ID
  through data, byte count excluded) agrees with
  [02-sysex-format.md](02-sysex-format.md#bulk-dump) — an outside agreement,
  though they may have read this repository, so not independent corroboration.

> **The loop switch itself is now `verified on hardware`** — a patched waveform
> sustains indefinitely on this project's unit, once its envelope is allowed to
> ([10-verified-behaviour.md](10-verified-behaviour.md#2026-11-23--the-loop-switch-works-and-the-envelope-is-why-nobody-noticed)).
>
> **The rest of this section is *reported by a third party, not reproduced here*** —
> their own notes grade each claim, and their strongest tag means *they*
> imported a patch on *their* unit and listened.
>
> **Three things have since been measured here**, and they are marked where they
> appear: the keybank record's own fields, read off a real unit through the
> content channel; the rule that an element refers to a user waveform as
> `ContentNumber − 8192`; and that a non-SAMPLER element really does play a user
> wave. See
> [10-verified-behaviour.md](10-verified-behaviour.md#2026-11-23-hardware-session--an-awm-element-really-does-play-a-user-wave).
>
> **Rule 2 applies, hard.** The SLOPTRAK spec cites this repository for the
> parameter table and the wave list, and its element-block layout is read
> *against* it. Where it agrees with us about `41 ep`, that is inheritance, not
> corroboration. What is genuinely theirs is the loop.

### Package layout

```
<sound UUID>/
    sound.bin          1792 bytes        the sound itself
    sound.xml                            ContentNumber, UUID, Order, Favorite
    waveform0.bin      4 + 64 × keybanks keybank records
    waveform0.xml                        ContentNumber (user waves are ≥ 8192)
    sample0.bin        2 × n bytes       raw signed 16-bit LE PCM, mono, no header
    sample0.xml                          WaveformNumber + KeybankNumber + DataSize
```

A sound that references only factory waves ships `sound.bin` and `sound.xml`
alone. A stereo waveform is **two keybanks**: left is `sample0.bin`, right is
`sample1.bin`.

The audio file is **raw PCM, not a WAV**. A patch that stored whole `.wav`
files played its 112-byte header as audio.

### Infinite sustain is a loop switch in the keybank record

This is the answer to a question the owner community had open since release:
why every user patch is a one-shot while factory pads hold forever. It is not
an engine difference and not a firmware limit — it is **two fields in the
64-byte keybank record**, and nothing else changes.

| Record offset | Size | One-shot | Looping |
|---|---|---|---|
| `+0x0F` | u8 | `01` | **`00`** — loop switch, 1 = one-shot, 0 = loop |
| `+0x2C` | u32 | `0` | **loop start ÷ 16** — in 16-sample blocks |
| `+0x30` | u32 | `n − 1` | `n − 1` — index of the last sample |
| `+0x3C` | u32 | `n` | `n` — sample count, `n` = file size ÷ 2 |
| `+0x34` | u32 | `0` | `0` — **leave it**; the variants that put a loop start here did not loop |

The loop runs from the start point **to the end of the data**; no loop end is
stored, and whether shortening `+0x30` moves it is untested even by them. Loop
start has **16-sample granularity** — floor it to a multiple of 16. The loop
**length** has none: `+0x3C` is a plain u32 sample count, and a real device-made
file carries 110,235, an odd number. On a stereo waveform, set both records
identically.

> **Choosing the loop length: match the waveform, do not count periods.**
> An integer number of periods of the note's fundamental is the obvious
> objective and it is the wrong one — a tone with detuned partials is not
> periodic at its fundamental, it is periodic at the much longer beat period, so
> counting f0 periods lines up nothing and the loop clicks. Measured over eight
> zones built that way, the join correlation ran from 0.81 down to **−0.49**,
> with sample jumps up to 31,221. Searching instead for the length that
> maximises the correlation between the window before the loop start and the
> window before the end gives 0.9999 or better on all eight, with jumps of 4 to
> 71. `verified on hardware`
> ([10](10-verified-behaviour.md#the-loop-click-an-integer-number-of-periods-is-the-wrong-objective)).

They established the table by building four variants of one patch that differ
only in those record bytes and importing each: only `+0x0F = 0` with the loop
start at `+0x2C` looped.

**What was unknown was narrower than "how the SEQTRAK sustains".** A *sampler
pad* loops through ordinary documented parameters — `50 eA 5F` `Loop On/Off`,
`50 eA 60` `Loop Length`, `50 eA 66` / `6A` the start and end points, all
`from Yamaha Data List` and all `verified on hardware` here, with a write to
the start point accepted ([03e](03e-parameters-element.md)). What has no SysEx
block at all is the loop of a **user waveform referenced by an AWM element** —
a synth or drum track. For that the keybank record in the file is the only
control, which is why the answer had to be found in a `.Y3S` and not on the
wire.

**A loop alone is not enough, and this is the part that bites.**
`verified on hardware` here: a patched waveform imported through the official
app still died at 2.5 s, because the import gives it an envelope whose
**`AEG Decay 2 Level` (`41 ep 3B`) is `0`** — it falls to silence with the key
still down. Writing that one byte to `127` made the same sound **sustain
indefinitely**
([10-verified-behaviour.md](10-verified-behaviour.md#2026-11-23--the-loop-switch-works-and-the-envelope-is-why-nobody-noticed)).

So anyone who patches the two record bytes correctly and hears nothing will
blame the loop. It is the envelope. The machine's own UI exposes only attack
and decay, which is why the advice is to start from a template sound that
already sustains — but over SysEx the envelope is one write away
([03e](03e-parameters-element.md)).

### The rest of the record

| Offset | Field | Value in user records |
|---|---|---|
| `+0x00`, `+0x01` | key range low, high | `00`, `7F` |
| `+0x02`, `+0x03` | velocity range low, high | `01`, `7F` |
| `+0x08` | root key (MIDI note) | `3C` (60) |
| `+0x0B` | ~~channels, 1 = mono, 2 = stereo~~ — **the keybank count**, and the machine writes it | `01` / `02`, `08` in an eight-keybank waveform and **`52` in a fifty-two-keybank one**. `verified on hardware`: a waveform of **eight mono** samples was pushed with `01` in every record and came back with **`08`** in every record, and 52 mono samples with **`52`** ([10-verified-behaviour.md](10-verified-behaviour.md#2026-11-24-later-still--eight-keybanks-written-by-a-host-and-read-back)). "Channels" fitted only because the sole multi-keybank case anyone had seen was stereo, where the channel count and the keybank count are both 2 |
| `+0x24` | u32 sample rate in Hz | `44100`; other rates untested |
| `+0x38` | u32 **written by the machine**, differs per keybank | `verified on hardware` that the machine **overwrites whatever the file carries** on import, and that it is **not a function of the audio**: the same PCM imported twice took `20124` and `47188`. So a host need not compute it. Meaning still unknown; the values rise with allocation order, which would fit a storage offset ([10-verified-behaviour.md](10-verified-behaviour.md#and-0x38-is-written-by-the-machine-not-by-the-file)) |

`waveformN.bin` is a u32 keybank count followed by that many records, so
`4 + 64n` bytes: 68 for one keybank, 132 stereo, and 516 for the eight-keybank
waveform that was written and read back.

### A user waveform on a synth element is **one zone**, for now

`verified on hardware`. A package carrying five keybank records — one per
octave, each with its own key range and root key — is accepted at every step of
the transfer and then **silently flattened**: the machine keeps the first record
and stretches it over the whole audio blob. Pulling the waveform back shows
keybank count `1` and a sample count rewritten to the full blob length
([10-verified-behaviour.md](10-verified-behaviour.md#2026-11-24--a-multi-zone-user-waveform-the-transfer-header-decoded-and-six-attempts-that-were-all-malformed)).

This is not a format limit and **not a firmware limit**. The engine plays
multi-zone waveforms constantly — the factory library is sampled every one to
three semitones — and a user waveform on a real unit already holds two
keybanks: the stereo one, pulled back and counted at `keybanks 2`, two runs of
355 packets, 931,392 bytes each. What is missing is only the **write**
handshake for the second keybank. Three shapes were tried and all three store
one keybank; the header checks its declared size at the end of each stream and
expects exactly one stream per header, so there is no room in it for a second.
A capture of the official app importing a stereo package is the way in.

### The way round it: one element per zone

`verified on hardware`. Every field needed is an ordinary parameter, so a
multisampled instrument can be assembled **live** out of several single-zone
user waveforms — one per element — without touching the keybank problem at all:

| Parameter | Role |
|---|---|
| `41 ep 00` `Element Assign` | `1` turns the element on |
| `41 ep 01` `Wave Select` | `1` selects a **user** wave |
| `41 ep 03` `Wave Number` | 2 bytes, the user wave number (`ContentNumber − 8192`) |
| `41 ep 10` / `11` | `Note Limit Low` / `High` — the zone |
| `41 ep 12` / `13` | velocity limits |
| `41 ep 2E` | element level |

Five elements of one part were pointed at five user waveforms with five key
ranges, and **every field read back as written**, witness unmoved and tempo
answering. That also settles `41 ep 01` / `41 ep 03`, listed as untested above.

**The traps, and they are not optional.** An element switched on from scratch
keeps the Data List defaults, which are *not* what a loaded sound puts in its
elements. Three of them are audible, and they sit in **two different blocks**:

| Address | Parameter | Fresh element | Configured element | What you hear |
|---|---|---|---|---|
| `41 ep 54` | `Pitch Key Follow Sensitivity` | 64 | 96 | at 64 the element ignores the keyboard and plays its sample at the root key whatever note arrives — one frozen note, darkening as you climb |
| `42 ep 0C` | `Filter Gain` (2 bytes) | 102 | 127 | the fresh zones are **quieter**, so the level steps down the moment you leave the configured element's range and stays there |
| `42 ep 1D` | `FEG Depth` | 104 | 64 | a filter envelope sweep the configured element does not have |

So dump the part and **diff every block** against the configured element —
`41 ep` and `42 ep` both — rather than trusting the defaults or the block the
symptom suggests.

**The ceiling is eight zones.** All eight elements of a part answer and take an
assignment over SysEx (`41 (e<<4|p) xx`, `e` = 0-7), `verified on hardware` —
even though a package's `sound.bin` shows only 7 usable blocks. Eight roots
every 3 semitones span two octaves at the factory library's own commonest zone
width; a full keyboard at that density would need 43 zones, so anything wider
than two octaves has to stretch.

**It works, and it was heard.** An eight-zone instrument assembled this way —
a root every 3 semitones from note 48 to 69 — plays each zone at its own pitch
with the level even across the boundaries, confirmed by ear once all three traps
above were written.

The one real cost is that it **does not persist**. The user waveforms stay on
the machine, but the element assignment is live state: it is lost the moment a
sound is loaded onto the part, and `Sound Save` remains an unresolved address
([08](08-bulk-and-files.md#why-save-matters)). Rebuilding it is one command and
no audio transfer —
[`tools/hardware-probe/element_multisample.py`](../tools/hardware-probe/element_multisample.py)
loads the first sound, assigns the eight elements and writes all three
non-inherited parameters, then reads every field back.

### `sound.bin`, and how an element points at a wave

`sound.bin` is 1792 bytes: a header, a 32-byte name as four groups of `00` plus
seven ASCII characters, undecoded common parameters, then **7 element blocks of
141 bytes** (the 8th is `FF`-filled in every file they saw, although Yamaha
documents 8 elements).

Element *k* starts at `0x1E9 + 141 × k`, and its bytes follow **the `41 ep xx`
address order of this repository's own parameter table** — which is exactly the
inheritance Rule 2 warns about, so read it as a cross-reference and not as
confirmation.

The wave reference is a **u16 at `0x1E8 + 141 × k`**:

| Value | Meaning |
|---|---|
| `01 00` | element unused |
| a wave-list number, e.g. `8B 01` = 395 | factory waveform |
| `ContentNumber − 8192`, e.g. 8687 → 495 | a user waveform shipped in this package |

**An element is switched on by that field alone.** In their device-made files,
the only bytes differing between a used and an unused element are those two —
every other element parameter stays at its default. So a multi-sample
instrument is *N* wave numbers in the first *N* blocks. How the u16 relates to
the SysEx fields `Element Assign` / `Wave Select` / `Wave Number` is **not
understood**; its high byte overlaps what the table calls `Element Assign`.
Factory and user references are indistinguishable byte-wise — the importer
resolves them by context, and content numbers are reassigned on import.

### Stopping at key release is **one byte** at `0x88`

A sound can hold a note for as long as the key is down and stop when it is
released, or ignore key release entirely and loop forever. The difference is a
single byte of `sound.bin`, inside the undecoded common region:

| Offset | Value | Behaviour |
|---|---|---|
| `0x88` | `0x02` | the note sustains while the key is held and **stops when it is released** |
| `0x88` | `0x00` | the note loops and **never stops**, key release included |

`verified on hardware` — two sounds carrying the *same* sample, the same
keybank record and the same loop switch differed in twelve bytes of
`sound.bin`. Pushing seven variants through
[`content_push.py`](../tools/hardware-probe/content_push.py), each restoring one
group of those bytes and then one single byte, narrowed the behaviour to `0x88`
alone. The other eleven bytes change nothing audible about key release:

| Offset | Role |
|---|---|
| `0x09`-`0x1A` | the sound name |
| `0x6E`, `0x75`, `0x77`, `0x7C` | no audible effect on key release |
| `0x84`, `0x95` | ˶ |
| `0x96`, `0xA2`, `0xA9` | ˶ |
| `0x143` | ˶ |
| `0x1E8` | the element's wave reference — it differs because the two packages carry different waveform content numbers |

**That byte is `31 1p 0D` `Trigger/Gate Mode`.** Loading each of the two
variants in turn and dumping the part's edit buffer leaves exactly one
behavioural difference between them:

| Parameter | Looping sound | Releasing sound |
|---|---|---|
| `31 1p 0D` `Trigger/Gate Mode` | `00` *Trigger* | `02` *Depend on Voice* |
| `31 1p 1F` `Portamento Time` | `00` | `40`, the default |

So **`Trigger` means "ignore key release"**, which is exactly what a drum hit
wants and exactly what makes a looped sample run forever. `Depend on Voice` —
the Data List default — lets the note stop when the key is let go. The
`Portamento Time` difference rides along: nothing in the package sets it, and
the machine derives it from the same stored field.

The address is also writable live: with the looping sound loaded, `31 18 0D`
read `00`, was written `02` and read back `02`, then restored to `00`, with
`31 17 0D` unmoved at `02` as witness and the tempo answering throughout. Only
the read-back is `verified on hardware` — whether a *live* write changes what
you hear without reloading the sound has not been listened to.

`41 ep 08`, the **element's** own `Trigger/Gate Mode`, is not involved: it reads
`01` (*Gate*) in both dumps. The two edit buffers differ in four bytes in all,
and the other two are the sound name and the element's wave number.

#### What Yamaha does and does not say about it

`from Yamaha Data List`. The parameter is **not new**: the *Data List* lists
`31 1p 0D` `Trigger/Gate Mode` with its three value names (`Trigger`, `Gate`,
`Depend on Voice`, default `02`) and `41 ep 08` with two, and
[appendix H](appendix-h-sound-design-parameters.md) already carries the
footnotes where Trigger and Gate change what the **AEG DECAY** knob edits —
`Release Time` under Gate, `Decay 1/2 Time` under Trigger. What is nowhere in
Yamaha's documentation is **what the setting costs you**: that `Trigger` means
key release is ignored, and that this is why an imported sample loops forever.
The *User Guide* never mentions `Trigger/Gate Mode` at all — no front-panel
combination, no app control.

**But there is a printed control with exactly this behaviour, on the SAMPLER
track only.** User Guide §9.1.5, p. 62: page 4 (ADVANCED), Sound Design knob 3,
`LOOP ON/OFF`, described on p. 108 as toggling "between holding down the key to
repeatedly play the sample (ON), or playing it once each time you press the key
(OFF)". That is the sampler's own `50 eA 5F` `Loop On/Off`
([appendix H](appendix-h-sound-design-parameters.md)), which read `00` on all
seven slots of a real unit.

So the same musical result has two different levers depending on where the
sample lives:

| The sample is on | The lever | Reachable from the front panel |
|---|---|---|
| the **SAMPLER** track | `50 eA 5F` `Loop On/Off` | **yes** — page 4 ADVANCED, knob 3 |
| a **SYNTH** track, as a user wave | `31 1p 0D` `Trigger/Gate Mode` | **no** — nothing printed addresses it |

A user wave on a synth track is the case this repository had to work out, and it
is the one Yamaha left without a control.

The common region's byte offsets are **not** the `31 xp xx` parameter offsets.
The name occupies `0x08`-`0x71` and does align, but immediately after it the two
layouts diverge — the file spends 13 bytes where the edit buffer spends 23 — so
`0x88` cannot be turned into an address by arithmetic, and was not.


### What this changes here

- A **user wave on a non-sampler element is real**, not merely implied by the
  Data List: their element wave field addresses user waveforms directly, and
  the sounds they built play them on synth tracks. The SysEx path for the same
  thing ([`41 ep 01` / `41 ep 03`](#waveforms)) is still untested.
- The factory wave table lives in the `Program` image — offset table at
  `0x2041157C` (2024 × u32), directory at `0x2041351C`, and **19,865 records**
  of 64 bytes at `0x20428B24`, the same record layout as a package's. A
  waveform is multi-zone: its directory entry lists many records. Reported by a
  third party, and **now re-checked against this repository's own image**
  (`from firmware image (static analysis)`, load base `0x20040000`): of the
  19,865 records, **14,595** parse as plausible keybanks — key low ≤ key high,
  root key in range, sample rate one of 22050/32000/44100/48000 — and of those:

  | Key range | Records |
  |---|---|
  | the full keyboard, `0`-`127` | 2,519 |
  | **a restricted range** | **12,076** |

  The most common zone widths are **3, 2 and 1 semitones** (3,117 / 2,754 /
  2,547 records), then 12 (772). Root keys spread over 123 distinct notes.

  So the factory library is **densely multisampled** — a zone every one to
  three semitones on the fine waves — which is the measure of what a single
  user sample stretched across the keyboard is up against, and why
  [one zone per user waveform](#a-user-waveform-on-a-synth-element-is-one-zone-for-now)
  is the gap that matters. This is a fact about the image; what the running
  machine does with these tables was not observed.

  **But "the same record layout as a package's" is too strong, and is hereby
  narrowed.** Only the fields checked above line up: key range at `+0x00`/`+0x01`,
  root key at `+0x08`, sample rate at `+0x24`. Two fields plainly do not:
  `+0x38` reads `FFFFFFFF` in **every** one of the 14,595 records, and `+0x3C`
  is not a sample count — summed over the table it gives 6 × 10¹³ samples, which
  is six orders of magnitude past any plausible library. So the factory table
  shares the record's *front* and diverges later. Do not read package field
  offsets past `+0x24` into it.

  **And the factory audio is not in the firmware image.** The image is 63.75 MiB,
  of which **40 MiB is `FF` erase-filler** and about 17 MiB is code and data;
  classifying it by megabyte finds no region that could hold a sample library,
  against the Data List's 800 MB of preset wave memory. The update file carries
  the tables and the program, not the samples: those live in a memory the
  updater does not touch. `from firmware image (static analysis)` — a fact about
  the file, which is exactly the point here.
- Their factory reading is not clean: `+0x0F` is `1` on 99.7 % of one-shot-looking
  factory records but `0` on a drum (wave 765, Timbale 1), and one Sax zone
  decodes to an 80-sample loop that does not match what is heard. **Factory
  loop ends are not established.**

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
