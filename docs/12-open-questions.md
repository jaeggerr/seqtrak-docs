# 12 — Open questions, conflicts and what to test next

Everything this repository does **not** know, every place its sources disagree,
and the tests that would settle each one — ordered by information gained per
unit of risk.

## Conflicts between sources

These are kept open deliberately. Both readings are recorded; neither has been
silently dropped.

### 1. What `p` counts in the piano-roll read address `75 p0 ee`

| Source | Reading |
|---|---|
| `from the official app, untested` | `am = (part << 4) \| (eventIndex >> 7)`, `al = eventIndex & 0x7F`; `part` is the global part number (0-10); the index addresses an event in a list |
| `reverse-engineered from app traffic` | `am = (p << 4)`, `al` = an index into a **compact list of active steps only**; `p` counts melodic tracks only — Synth 1 = 0, Synth 2 = 1, DX = 2, Sampler = 3 |

Both agree on the 8-byte payload layout and on `72 (p<<4) 00` for writing. They
disagree on what `p` counts and on whether `al` is a split event index or a
compact list index.

**Settled on hardware, but only half of it.** `verified on hardware`: sweeping
`75 (n<<4) idx` over n = 0-11, six indices each, two attempts per address,
**n = 0, 1, 2 and 3 answer and n = 4-11 do not**. SYNTH 1, the machine's part
7, is reached as n = 0. So `p` counts **melodic tracks only, from zero** — the
second reading is right on this point and the first is wrong. Addressing
SYNTH 1 as n = 7 reaches nothing.

The drum block is the opposite: `25 (n<<4) idx` answers for n = 0-6, the
global part numbers. The two blocks index differently, which is probably why
the static reading generalised the wrong one.

**The other half is still open**: whether `al` is a split event index or an
index into a compact list of active steps. One observation bears on it without
closing it, and it was made in the drum block (`25`), not here: on a part
re-typed to SYNTH the indices came back dense and in time order (0,1,2,3 for a
four-note chord), while on a DRUM part they came back spaced exactly like the
occupied steps (0, 1, 2, then empty, then 4, then 10). That looks like *both*
readings being right, each on its own track type — but it has not been tested
in the `75` block, and the test below is still the one to run.

**Neither reading had hardware behind it when this entry was written.** The second one comes from a sibling
project in this tree, not from an outside implementation — it was written from
the same documentation lineage, so its agreement with the official app may be
inheritance rather than confirmation. An earlier version of this document called
it "a third-party app that works against real hardware", which overstated it.
That mislabelling is itself the lesson recorded under
[evidence discipline](../AGENTS.md): with several sessions feeding this
repository, a fact that comes back from a *consumer* of the documentation can
look exactly like external confirmation.

**Test:** on a track with exactly two notes at known steps, request `75 70 00`
and `75 00 00` and see which answers. Then add a third note between the two and
re-read index 1: if it returns the new note, the list is compact. Read-only.
Details in [04-sequencer-editing.md](04-sequencer-editing.md).

### 2. `ARP Template` range — 0-15 or 0-16

| Source | Reading |
|---|---|
| `from Yamaha Data List` | CC 27 `ARP TEMPLATE`, 0-15, 0 = off |
| User Guide §18.3.1 | CC 27 `ARP TYPE`, 0-16, 0 = off |

The arpeggio preset list has exactly 16 entries numbered 1-16, which fits 0-15
with an off-by-one in the naming. The Data List also gives the parameter at
`31 5p 00` as 0-15. The User Guide figure is most likely a 1-based count, but it
is published and so is recorded here.

**Test:** write 16 to `31 5p 00` and read it back. If it clamps to 15, the Data
List is right. Reversible.

### 3. Bank Select — RESOLVED, and the old answer was wrong

**Bank Select is transmitted.** Turning the sound-select knob produced ten
preset changes and ten complete triplets: `CC 0 = 63`, `CC 32 = 7`, then the
Program Change — systematically, not only at bank boundaries. All three
transmit bitmasks read back as `0x70`, every bit set, so the mask is not
cosmetic. `verified on hardware`, 2026-10.

This repository previously recorded the opposite as `verified on hardware`, on
the strength of two sessions months apart. **Both used the same instrument** — a
custom-firmware peripheral whose on-screen log was a nine-line ring buffer read
live — so they were not independent. The receiver's parsing has since been read
and is sound; what defeated it was the **window**. One sound-knob turn produces
about 30 messages in a second, and nine scrolling lines show only the tail.

Consequences, now applied throughout: bank plus program **does** resolve a
preset name from [data/presets.csv](../data/presets.csv), and the `11 02 pp`
bulk dump is no longer required for that — it remains the route for **user**
sounds and exact stored names. See
[06-sounds-presets.md](06-sounds-presets.md) and
[10-verified-behaviour.md](10-verified-behaviour.md#bank-select-is-transmitted--a-documented-conclusion-reversed).

**The lesson is worth more than the fact.** Two agreeing observations are not
two independent observations when they share a receiver. A claim is only as
strong as the weakest link in the measurement chain, and "verified twice" meant
"verified once, twice over".

### 4. Four value ranges where the two sources disagreed — all explained

Of the 257 addresses described by **both** the Data List and the app
extraction, 216 have a comparable value range, and **212 agree exactly** —
including all 37 in the System zone. Four do not. Reproduce with
`python3 tools/cross_check.py`.

| Address | Parameter | Data List | Official app | Reading |
|---|---|---|---|---|
| `31 1p 2C` | AEG Attack Time | `00`-`7F`, shown -64…+63 | 64-127, shown 0…63 | Not a contradiction: this app row comes from `DrumSoundModel`, the **drum** variant, where the app restricts the offset to the upper half. The Data List gives the generic range for all engines. |
| `31 4p 0B` | LFO Box1 Destination | `00`-`44` (0-68) | 0-127 | **Trust the Data List.** 0-68 is exactly the 69 entries of the LFO destination table ([appendix-g](appendix-g-lfo-destinations.md)); the app simply allows the whole byte. |
| `31 4p 03` | LFO Tempo Speed | `05`-`18` (5-24) | 5-52, shown 5…24 | **Resolved: the Data List is right.** A write sweep on part 7 with restore accepted 24 and clamped 25, 30, 40, 52 and 60 all to 24. The app's 52 is an app-side artefact with no effect on hardware. `verified on hardware`. |
| `42 ep 37` | EQ 2 Frequency | `01 03 - 71` | 131-241, shown 503…10144 Hz | **They agree.** This is a two-byte parameter, so the Data List prints one range per byte: MSB `01`-`01`, LSB `03`-`71`. `(1 << 7) \| 0x03 = 131` and `(1 << 7) \| 0x71 = 241`. The apparent conflict is an artefact of this repository rendering two range lines on one row. |

**All four are now explained**: one per-engine restriction, one case of the app
being permissive, one rendering artefact, and one app-side artefact disproved on
hardware. No disagreement between the two parameter sources remains open.

The technique that settled the last one generalises:
[`../tools/hardware-probe/probe_write.py`](../tools/hardware-probe/probe_write.py)
reads an address, tries a list of values, reports each as accepted / clamped /
refused, and restores the original in a `finally`. That is the way to resolve any
future range disagreement.

### 5. What each control emits — RESOLVED, and the old answer was wrong twice

Filed first as a contradiction, then as a coverage gap, now settled. All rows
`verified on hardware`:

| Control | Emits |
|---|---|
| The **four per-track knobs** (Sound Select, Mono/Poly/Chord, Pan, Volume) | Control Change only — `CC 0`/`32` + Program Change, `CC 26`, `CC 10`, `CC 7`. 66 messages over 85 s, **zero SysEx**. |
| The **FX sliders** | **Both voices**: SysEx at every parameter the preset moves, plus one CC per slider step. 390 messages over 100 s, 6 SysEx addresses, 171 CCs. |

**The FX sliders do emit SysEx.** The 2026-08 session that reported otherwise
was wrong, and it was wrong for the **same reason as Bank Select**: both
negatives were read off the same instrument, a nine-line scrolling log, while
bursts of ~105 messages arrived in ~1.2 seconds. (An earlier version of this
document blamed SysEx reassembly in that receiver; its code was then read and
found correct. The fault was the sampling window, not the parser.)

An intermediate reframing in this document said the FX knobs had simply never
been measured. That was right about the earlier capture (those were the
per-track knobs) but wrong to leave the August claim standing as evidence.

The durable finding is in
[05-live-state.md](05-live-state.md#the-sysex-voice-carries-strictly-more): the
two voices are **complementary, not redundant**. One slider can drive several
parameters; the CC reports the slider position, the SysEx reports each parameter
that moved, and some parameters have no CC at all. "Accept either voice" remains
safe advice, but **the SysEx voice carries strictly more**.

Two methodological notes now earn their place in
[AGENTS.md](../AGENTS.md):

- Two agreeing observations are not two independent observations when they share
  an **instrument**. This has now accounted for two documentation failures.
- A *negative* claim needs an instrument that can **establish absence** — a
  cumulative counter or a complete capture, not a scrolling view of a fast
  burst.

### 6. Checksum range — resolved, recorded for provenance

The Data List says the checksum covers "the Byte Count, Start Address, Data and
Check-sum itself". That does not add up on a real captured message; including
the Model ID and **excluding** the byte count does. Verified arithmetically
against the project-rename dump and consistent with both the official app and the
firmware plug-in. Resolved in
[02-sysex-format.md](02-sysex-format.md#bulk-dump) — no further test needed, but
worth re-checking against a second captured bulk dump if one becomes available.

### 7. Documented defaults versus a machine in use

Four System settings read back differently from their published defaults; one
(`MIDI Clock Out`) differed between two sessions because the user changed it.
Not a protocol conflict — a reminder that defaults describe a factory-fresh unit
and nothing else. Table in
[10-verified-behaviour.md](10-verified-behaviour.md#documented-defaults-do-not-match-a-machine-in-use).

### 8. A stale claim about 13 tracks

One sibling project's notes describe a `Track` enum of "11 tracks: kick, snare,
clap, hats, percs, synth1, synth2, DX, sampler, vocoder, looper" — which lists
thirteen names. The actual source code in that project defines exactly eleven,
`kick` through `sampler`, with no vocoder and no looper, and the hardware's
`CurrentPart` range is 0-10 (`verified on hardware`). **There are eleven parts.**
The vocoder and looper do not exist as parts; the note is simply wrong and is
recorded here only so the claim is not resurrected.

### 9. User-scale display mapping

The Data List gives `30 4D xx` as transmitted `0x24`-`0x60` (36-96) displayed as
`C1 … C6`. The official app's own display mapping for the same parameters reports
24-60. Both agree on the transmitted range, which is what matters for the
protocol; the display difference is cosmetic and probably a different note-name
convention inside the app.

**Test:** none needed for protocol work. If a client wants to print note names,
derive them from the MIDI note number rather than trusting either display range.

## Reachable, but semantics unproven

33 of 33 probed addresses answered, which proves they exist. Only **three** have
had their meaning proven by a controlled physical gesture with witnesses
(`HeadphonePlugStatus`, `SequencerStatus`, `CurrentPart`). Everything else in
the `01` zone is "reachable, plausible value, meaning assumed from its name".

The highest-value ones to pin down, each with the gesture that would do it:

| Address | Parameter | Gesture |
|---|---|---|
| `01 10 01` | `ContentsManagementMode` | enter content management in the app, re-read |
| ~~`01 10 21`~~ | ~~`RecordingStatus`~~ | **Partly answered 2026-11-15**: it is writable while the sequencer plays and reads back what was written, `verified on hardware` ([10](10-verified-behaviour.md#2026-11-15-01-10-21-is-writable-while-the-sequencer-plays)). Still open: that `[REC]` emits it, and that notes are recorded once it reads 1 |
| `01 10 22` | `SamplingStatus` | start sampling |
| `01 10 2E` | `ParameterLedMode` | step through index words, tabulate the 44 values. Partly done: 3, 2 and 1 correspond to FX blocks |
| ~~`01 1p 33`~~ | ~~`CurrentSound`~~ | **Answered**: `CurrentSound` = catalogue number − 1, `verified on hardware` by loading 10 known presets and reading each back. [06-sounds-presets.md](06-sounds-presets.md#reading-back-which-sound-is-loaded) |
| `01 1p 35` | `CurrentSoundName` | read it and compare with the `31 0p 00` dump |
| `01 1p 50`-`58` | slider assignments | re-assign a slider in the app, re-read; decode the 25 values |
| `71 10 04` | `CurrentScene` | change scene in Song mode |

All read-only. Use the witness protocol from
[10-verified-behaviour.md](10-verified-behaviour.md#semantics-proven-by-physical-action):
one gesture, three targets, three witnesses that must not move.

## Writes: what has been tried

**Four zones have verified writes**, each with a full read → write → read-back →
restore cycle and a witness address:

- `30 4D 00` — a user scale pad.
- `70 tt 00` — **putting a note into a step**, with `70 (20|tt) 00` as the undo.
  This was the most interesting unknown in the protocol and it now works; see
  [04-sequencer-editing.md](04-sequencer-editing.md#the-verified-round-trip).
- `30 40 76` — the tempo, written and restored on 2026-10-23.
- `31 2p 00` / `31 3p 00` — the insertion effect blocks. The blocks were
  restored by write in an earlier session, and on 2026-10-23 insertion A on
  part 7 was changed to a *different* type (CLASSIC COMPRESSOR → SPX HALL) and
  reported back correctly, which is what establishes that the type codes
  address real effects.

(This list said "two zones" until 2026-10-23, after the third and fourth had
already been measured. If you add a verified write, add it here too.)

Every other write in this repository is still from documentation or static
analysis. Ordered by value, with the undo for each:

1. **Step attributes** — ~~`70 (10|tt)` for micro timing, velocity, retrigger
   and conditional lock.~~ **Three of the four are now `verified on hardware`**
   (2026-10-23): velocity `01`, micro timing `00` and retrigger `03` were each
   written and read back on part 0, into a step that was empty beforehand so
   that `delete` was an exact undo
   ([10-verified-behaviour.md](10-verified-behaviour.md#15-step-attributes-three-of-the-four-are-now-verified)).
   The micro-timing centre of **60** is confirmed: writing 70 reads 70 and
   displays +10. The conditional lock `04` followed the same day: 3, 7 and 0
   were each written and read back, so **all four attributes of `70 (10|tt)`
   are now verified** and this entry is closed. The eight probability levels
   are `0`-`7` on the wire.
2. **Piano roll** — `72`/`73`/`74` with `76` to find an index. The obvious next
   target, but it depends on resolving conflict #1 above first.
3. **Song mode** — `71 00 00` `AddScene` / `71 20 00` `RemoveScene` are a
   matched pair.
4. **Pattern copy / paste** — `77 01 20` and `77 01 21` with `part, pattern`.
   Paste overwrites a pattern, so copy an empty pattern over an empty pattern
   first.
5. **Wi-Fi configuration** — `00 60`-`00 62`. Easy to verify (the machine either
   joins the network or does not) but it writes a credential in clear text over
   the cable.
6. **Drum parameter locks** — `30 00 70`/`71`/`73`. Undocumented and
   unverified; read them first.

Not to be attempted speculatively: `01 34 00` `FactoryReset`, `01 40 00` /
`01 41 00` / `01 42 00` (remove project / sound / element), `01 31 xx`
(defragmentation).

## Unresolved addresses

> **Six bulk control addresses came off this list**; they are now in
> [08-bulk-and-files.md](08-bulk-and-files.md#control-addresses).

| What | Why it is missing |
|---|---|
| 3 of the 399 parameters taken from the official app | address-mid computed at run time, not resolved |
| 7 of the 399 | no enum key resolved, so they appear as `<key=N>` |
| 8 app rows in total | address not resolvable to a concrete byte; excluded from `data/parameters.csv` |
| `0C [mode] [param]` encoding | only two working examples known (`0C 12 01` DX Synth Lead, `0C 02 0F` DX favourites); the general rule is not decoded |
| Sound Common Name offset `66` (sub-type) | values `00`/`01`/`02` observed, meaning inferred, marked TBD in the source |
| Sound browser entry offsets 0-18 and 225-227 | observed constant, purpose unknown |
| Project list slot offset 24 | varies per slot, purpose unknown |

## Track types and Song mode — what is not settled

Both subjects are new in [13-track-types.md](13-track-types.md) and
[14-song-mode.md](14-song-mode.md). The track-type round trip has since been
`verified on hardware`
([10-verified-behaviour.md](10-verified-behaviour.md#2026-10-22-later-session-re-typing-a-drum-track-works));
everything below is what that session did **not** settle. Song mode is no
longer wholly untested: scene creation, scene read-back and per-track pattern
and mute assignment are now `verified on hardware`
([14-song-mode.md](14-song-mode.md)), and what remains open about it is listed
in the table.

| Question | Why it is open |
|---|---|
| What `Result` does `01 33 01` carry other than 0? | `Success = 0` is `verified on hardware`. The other seven are inferred from enum names, and **the app never reads the field** — all five acknowledge handlers touch only `PartIndex`. No refusal has been provoked. |
| Does re-typing wipe all six patterns or only the selected one? | The wording ("the pattern created in the currently selected track type") reads like all of them, but it is not explicit, and the part used in the hardware test held no content to compare. |
| Do `type = 01` (DRUM) and `type = 03` (DRUMKIT) behave like `02`? | Only SYNTH has been sent to a machine. |
| Is there a limit on how many drum tracks can be synths at once? | No counter and no check anywhere in the app. If the firmware imposes one it would surface as a non-zero `Result`, which the app ignores. |
| What does `01 33 00` do with `part >= 7`? | The app never sends it. Treat as risky. |
| What does `01 33 00` do with `type >= 4` — can a drum part be made a DX track? | The app's `AwmType` enum stops at 3 and the app never sends 4, so there is no evidence either way. But `04` is not an arbitrary value: `PartAwmType` reads `04` on part 9 and `05` on part 10, `verified on hardware`, and the favourites message `10 01 xx` uses the same engine codes (`01` Drum, `02` Synth, `04` DX, `05` Sampler). So the firmware has an engine namespace in which 4 means DX. Sending `01 33 00 0p 04` on a scratch drum part and reading `Result` is the cheapest experiment on the question; it deletes that track's pattern. Note that even a success would leave the parameter path missing: the FM blocks are `48 09` and `49 o9`, with the part nibble **fixed at 9**. |
| ~~Can a **drum** element point at a user wave?~~ **Answered at the parameter level** | `verified on hardware` on both kinds of part. SYNTH 2 element 0 read `41 08 01` = `01` after a WAV import; KICK element 0 was then **written** to User with wave 401 and read it back, SNARE and SYNTH 1 unmoved as witnesses, and restored ([10](10-verified-behaviour.md#2026-11-23--a-drum-element-accepts-a-user-wave)). **Still open: whether it sounds.** The field accepts the value and reports it; nobody has listened to a drum part playing a user wave. |
| ~~Does a looped user wave ever stop on key release?~~ **Answered** | Yes. A patch from the third party's pack, played as shipped, holds while the key is held and stops on release ([10](10-verified-behaviour.md#the-third-partys-pack-works-and-it-answers-the-question)). An earlier table in this repository concluding the opposite was withdrawn: the waveform under the experiment had silently changed. |
| Why does *this* project's patched waveform not loop? | Their envelope applied byte for byte to it still plays the sample once. The only structural difference left: all seven of their samples have `n` divisible by 64, ours is 110,235. Since the loop ends at the end of the data and the start is counted in 16-sample blocks, a length that is not a multiple of 16 may leave the loop end mid-block. **Hypothesis, untested** — a 117,888-frame re-render exists to test it. |
| Is the AWM **element** zone writable at all — can a sound be built from scratch over SysEx? | `41 ep` and `42 ep` give 146 addresses per element and 8 elements per part (parts 0-8 and 10): oscillator, amplitude, pitch EG, filter, FEG, EQ, LFO, plus per-element note limits, velocity limits and crossfade. On paper that is a complete multisample instrument. But `data/hardware-verified.csv` holds **no row for `41` or `42`**: the two blocks have only ever been *surveyed read-only* ([10-verified-behaviour.md](10-verified-behaviour.md)). Whether a write lands, is clamped or is ignored is unknown. Installing a finished sound has its own untested route — bulk header/footer `11 02 0p` / `12 02 0p` into a part's sound edit buffer, or `11 03`-`11 12` into one of the 16 user sound banks ([02-sysex-format.md](02-sysex-format.md#bulk-header-and-footer)). |
| ~~How does a host get **PCM** into user wave memory?~~ **Answered, by a third party** | A `.Y3S` **content package** carries the sound and its user waveforms together: a zip with `sound.bin`, 64-byte keybank records and one raw 16-bit PCM file per keybank. Container documented first in [`FORMAT.md`](https://github.com/rechandler/seqtrak_sampler/blob/main/FORMAT.md) (`rechandler/seqtrak_sampler`), the loop fields added in [`Research/docs/10-Y3S-spec.md`](https://github.com/rexendevar/SLOPTRAK/blob/main/Research/docs/10-Y3S-spec.md) (SLOPTRAK); both summarised in [06-sounds-presets.md](06-sounds-presets.md#the-y3s-content-package--how-a-sound-of-your-own-gets-in). *Reported by a third party, not reproduced here.* The SysEx side of the question stands, and it is now the narrow gap: a `.Y3S` describes the **file**, not how it reaches the machine. Bulk selectors `13` and `14`-`1B` carry a sampler element's **metadata** (`50 eA`: name, loop and playback points), never audio, and the machine does not present itself as mass storage (nothing mounts when it is plugged in to a Mac). **Reading is solved, writing is not.** The content channel's read path is now `verified on hardware`: a 220,470-byte sample was pulled off the machine and came back byte for byte ([10](10-verified-behaviour.md#2026-11-23-later-the-content-channel-works-and-the-audio-comes-back-byte-for-byte)). The send direction uses the same frame and the same acknowledgement, so it is within reach, but nothing has been written to a machine. **And reading is solved only for waveforms**: in a bounded survey every sound and element number tried came back with an empty header and every project request went unanswered, with a waveform answering in the same run as the control ([10](10-verified-behaviour.md#what-the-content-channel-actually-serves--a-bounded-survey)). The app's own entry point takes a **project UUID**, so a project context may have to be set first — untested. |
| How does a host make the machine **request** content, so it can be written? | The write direction is machine-initiated: the app's send entry point emits nothing and its request handler answers a 10-byte Bulk Dump Request from the machine ([08](08-bulk-and-files.md#what-has-since-been-recovered--and-most-of-it-is-now-verified-on-hardware)). The exported C entry just forwards to that method, so **the plug-in never initiates**. Whatever tells the machine that content is waiting is elsewhere — the managed side queries the sound and element attributes before a send, so an inventory exchange is the candidate. Until it is found, a host can read content but not write it. |
| What are the **Sound Save** and **Element Save** addresses? | `Project Save` resolved to `01 32 00` with data `01`; the other two did not resolve. They matter because element writes are lost when a sound loads, and a save would commit them. **Do not probe for them**: `01 31 xx` is defragmentation and `01 34 00` a factory reset. |
| Why is every user patch a one-shot while factory pads sustain? **Answered, by a third party** | Two fields of the keybank record: `+0x0F` loop switch (`01` one-shot, `00` loop) and `+0x2C` loop start in 16-sample blocks. The loop runs from there to the end of the data; no loop end is stored. Established by building four variants of one patch differing only in those bytes and importing each. The **envelope must sustain too**, and the machine's UI exposes only attack and decay. *Reported by a third party, not reproduced here* — see [06-sounds-presets.md](06-sounds-presets.md#infinite-sustain-is-a-loop-switch-in-the-keybank-record). The container around those fields was already public before this (`rechandler/seqtrak_sampler`); the two loop fields are what was new. Still open **there**: whether shortening `+0x30` / `+0x3C` ends the loop early, what `+0x38` is, and whether a wrong `+0x38` is rejected on import. |
| What does `PartAwmType` value 0 mean? | **4 and 5 are settled**: the DX track reads `04` and the sampler reads `05`, `verified on hardware` ([10](10-verified-behaviour.md#2026-10-22-hardware-session-01-1p-3c-answers-for-every-part)). `00` has never been seen on any of the eleven parts. Whether it is reachable at all, and in what state, is open. |
| Is `30 5p 10` (`Pattern1BarLength`) writable at all? | A write of 3 on all eleven parts left it reading **0** on the two parts re-read, while `30 5p 16` written in the same loop read back 48 everywhere. `verified on hardware` ([10](10-verified-behaviour.md#30-5p-10-does-not-hold-a-bar-length-written-to-it)). It was not read before the write, so an ignored write and a write that landed as 0 are indistinguishable. Whether the bar length is derived from `Pattern1Step` is open. |
| What does `00 00 11` actually report? | It read `00` on four consecutive requests while a BLE link was established and carrying CC, PC, clock and active sensing. So `00` is not "Bluetooth MIDI off". `verified on hardware` that the two coexist; the meaning is unknown. |
| Why did one BLE window carry no SysEx? | SysEx **does** cross the link — a Parameter Request gets a reply and `01 10 2E` arrives unprompted. But one 50 s window of knob sweeps and sound changes gave 2853 packets with zero `F0`, where the same gestures over USB emit SysEx at the real parameter address as well as CC. Observed once, unexplained. |
| Does the SEQTRAK ever send an un-timestamped `F7`? | **No, as far as measured.** Two SysEx captured over BLE, both with a one-byte timestamp immediately before `F7`, repeating the message's opening timestamp. `verified on hardware` ([10](10-verified-behaviour.md#the-f7-terminator-is-timestamped--verified-on-hardware)). Only two observations, both short single-packet messages; a fragmented SysEx has not been seen. |
| Why does `01 10 2D` reply with 1 byte but broadcast 2? | A Parameter Request for `MasterKnobMode` returns one data byte; the machine spontaneously sends the same address with two (`04 04`, `01 01`, 18 times). The extraction declares size 2. `verified on hardware` that both forms occur; the reason is unknown. |
| Does the SEQTRAK emit `F2` when slaved to an external clock? | It emits none as a master — 0 in 108 s and 6656 messages, cumulative counter with a passing positive control ([10](10-verified-behaviour.md#2026-10-22-hardware-session-the-seqtrak-does-not-send-f2-over-usb)). Clock-slave, TRS and BLE were not exercised. |
| Would writing `01 1p 3C` change a track's type? | The app only ever writes it as a suppressed echo of a received value, so there is no evidence either way. `01 33 00` is the path the app exercises. |
| ~~How is a Song-mode scene created?~~ **Answered** | `AddScene` (`71 00 00`) and `RemoveScene` (`71 20 00`) take the scene number in the **data**; both `verified on hardware`, see [14-song-mode.md](14-song-mode.md#addscene-and-removescene-settled-on-hardware). `ChangeLength` (`71 10 00`) is still untested, and so is the unit it counts in. |
| What unit is a scene's length in? | `ChangeLength` decomposes as `scene × 16384 + length`, length 0-143. 143 is neither 128 nor 144 and no conversion appears in the app. |
| What is the pattern encoding inside `project.bin`? | Undecoded. Structure is mapped (67 × 16 KiB records, `0xFF` filler) in [08-bulk-and-files.md](08-bulk-and-files.md#projectbin--structure-observed-meaning-not); the app itself never touches pattern data. Three reference images ship with the app, so a differential attack is possible — but it needs hardware. |

## Protocol questions with no answer yet

- **`SampleMemoryTotalSize` = 510 — in what unit?** Probably MB, which would
  match the 500 MB of user wave memory in the specifications, but it has not
  been confirmed. Fill the sample memory partway and watch
  `SampleMemoryUsedSize` move.
- **Does the mid-nibble `p` in `01 1p` really range over all 11 parts?** Only
  part 0 has been read in that zone. The *sound* zone does answer for a
  non-zero part — the whole LFO block of part 7 (`31 47 00`-`0C`) reads back —
  so the composition rule is sound in general; `01 1p` specifically is still
  untested beyond part 0. Read `01 17 33` (part 7's `CurrentSound`) and compare
  with part 0's.
- ~~**How is a block of more than 16,383 packets framed?**~~ **Answered.** The
  premise was wrong: the payload is not 128 bytes per message. Packets carry
  3500 image bytes — 4000 SysEx bytes — apiece, never crossing a 256 KiB
  boundary, and their numbers restart at each boundary (`0`-`74`), so neither
  field is ever strained. The `Program` block is one header, 42 windows,
  3,085 packets and one create request (corrected 2026-11-14: this said one
  create cycle per window). See
  [09-firmware.md](09-firmware.md#how-a-block-is-cut-into-packets).
- ~~**Which command arms a block transfer (`SendingStart`)?**~~ **Answered:
  there is no such command.** The block header message arms the transfer by
  itself. The inventory of Parameter Changes the app sends into `0x64` was
  incomplete, though: besides reboot, enter and leave update mode, it sends the
  **create request `64 01 02`** at the end of each block (found 2026-11-14). See
  [09-firmware.md](09-firmware.md#there-is-no-sendingstart-command).
- ~~**What closes a window in the block-transfer handshake?**~~ **Answered on
  hardware, 2026-11-14.** Nothing closes a window: windows only renumber
  packets. A **block** is one header (answered `64 01 00`), packets (each
  answered `64 01 00`), then the create request `64 01 02` (answered
  `64 01 03`). After the `Installer`, the host leaves update mode and the unit
  reboots into the `Installer` (identity byte 12 = `02`). "Nothing static will
  settle it" was wrong: the official plug-in said all of it. See
  [09-firmware.md](09-firmware.md#there-is-no-sendingstart-command).
- **What does the `#8Z33` memcmp actually compare?** Not the head of the
  received payload — that is the compressed LZSS stream, and the check runs in
  the header path before any payload arrives. See
  [09-firmware.md](09-firmware.md#what-the-installers-receive-path-actually-checks).
- **Is the dividable-bulk format used anywhere outside the firmware update?**
  The app's `AckDataIndex = 11` suggests so, but no non-firmware example has
  been captured.
- **Does the `0C` browser zone paginate?** Every observed reply held a single
  entry; the app sends acknowledgements between pages. Request a large category
  and log everything.
- **What are the 44 values of `ParameterLedMode` (`01 10 2E`)?** This is the
  machine telling you which index word is lit — exactly what an external display
  wants. Enumerating it is pure read-only work with high payoff.
- **What are the 25 values of the slider `Assign` parameters?** Same shape of
  question; it would let a display name the parameter a slider is holding
  without decoding the SysEx voice.
- **CC → parameter mapping.** Some controls emit only CC (the four per-track
  knobs), so a complete CC → address table is not merely a convenience: it is
  the only way to interpret those gestures, and it also covers the case where
  `Transmit System Exclusive` is off. Four entries are confirmed already —
  `CC 0`/`CC 32` + Program Change for Sound Select, `CC 26` for
  Mono/Poly/Chord, `CC 10` for Pan, `CC 7` for Volume, on the selected part's
  channel. Build out the rest by turning each control while logging both
  voices, cross-referencing
  [appendix-h-sound-design-parameters.md](appendix-h-sound-design-parameters.md),
  which already names the parameter behind every knob position.
- **Complete the CC → parameter table for the FX blocks not yet seen.**
  Confirmed so far: CC 105 (Master Effect 2 param 1, channel 1), CC 106 (Master
  Effect 3 param 1, channel 1) and CC 107 (Single Effect param 1, the track's
  channel). Still unobserved: **Master Effect 1 (102-104)**, **Send Reverb
  (110-112)** and **Send Delay (113-115)** — including which channel each
  arrives on.
- **Decode `ParameterLedMode` (`01 10 2E`) as an FX-block indicator.** It took
  3, then 2, then 1 as the FX button cycled, so those three values map to FX
  blocks — but the full 0-43 scale is unknown, and the same parameter also
  moves on sound changes and knob moves. Mapping it would let a display name
  the active block and the lit index word without decoding anything else. Pure
  read-only work.
- **MIDI Thru behaviour in detail.** Arpeggiator trigger notes and notes on muted
  tracks are documented as not forwarded; nothing else about the filtering is
  known.
- **A step's note length is absent from the bulk-dump route.** There is no
  sequence-data block in the project dump and no entry for it in
  `Project Track General` (`verified on hardware`). It *is* reachable through
  the step-record read path, which returns a 14-bit gate time — so the open
  question is only whether the project dump hides it somewhere unidentified.
  Untried approaches: time Note On → Note Off in the live stream while playing,
  or sweep `01 10 00`-`01 10 3F` while editing a step and watch which offset
  moves.

## Partly answered: what persists, and what only stays in RAM

Logged open on 2026-10-22, answered twice the same day — the second answer
overturning the first.

| Gesture | Persists uncommitted edits? |
|---|---|
| Normal power-off, `[⏻/PLAY]` 2 s | **Yes**, `verified on hardware` |
| Forced termination, `[⏻/PLAY]` + `[PROJECT↑]` | **No**, `verified on hardware` |
| Project switch | **No evidence that it does, and evidence that it does not** — despite §4.2 |
| Auto Power Off, 30 min idle | claimed by §3.2.3, untested |

The project-switch row is a retraction: a marker surviving a 0 → 7 → 0 round
trip proves only that it stayed in RAM, and the forced-termination test later
reverted past that supposedly-committed value.
[10-verified-behaviour.md](10-verified-behaviour.md#the-forced-termination-discards--and-it-caught-the-flaw-above)
has the method and the correction.

What is **still** open, from the same test:

| Question | What is known |
|---|---|
| Does a project switch persist to **any** store? | It does not reach the one a forced termination respects. Whether §4.2's "saved" names a weaker tier, and what that tier is, is unknown. Testable: marker, project switch, **forced termination**, read back. |
| Does Auto Power Off save? | §3.2.3 says it does, after 30 minutes idle. Untested; it would take a 30-minute wait off the charger. |
| What is Program 8, the "temporary" project? | The Bank 64 table lists `0-8` with 8 = temporary, and §4.6 describes a user-triggered restore point. Whether they are the same slot is unverified — and conflating them is what produced the wrong assumption this test disproved. |
| How many scales does each project carry? | `30 4D 00` proved per-project, so the eight scales are presumably per-project too, but only pad 1 of scale 1 was compared across two projects. |
| Why does `01 1A 33` never answer? | `CurrentSound` for part 10 returned nothing on four attempts in three separate snapshots, while `01 10 33` and `01 17 33` answered in the same loops. A reproducible non-answer with live controls beside it. |

## Firmware

Two of the three questions that used to decide this are **answered**. The
official OS 2.00 file has been analysed
(`from firmware image (static analysis)`):

- **What is the file format?** Answered in full — a two-block container,
  `Installer` and `Program`, with a 128-byte header each, Okumura LZSS on the
  `Program` payload, and a flat ARMv7 (R profile) image at `0x20040000` in the clear. See
  [09-firmware.md](09-firmware.md#the-update-file-os-200). The write direction
  is closed too: a rebuild from named fields reproduces the official file byte
  for byte, and a modified image can be taken through to a coherent `.PGM`.
- **What SoC is this?** A **Yamaha SWX09** (*inferred* from a build path),
  running an eForce RTOS.
- **Does the loader check a signature?** Still open, and **no longer
  decisive** for a `Program`-only change: on 2026-11-14 a `Program` carrying a
  code patch was accepted over SysEx and runs (`verified on hardware`). The
  loader only ever receives Yamaha's own `Installer`. The question still
  decides a modified `Installer`.
- ~~**How does the `Program` image address its strings?**~~ **Answered
  2026-11-10.** At boot, about 6 MiB of the image is copied from `0x20090400`
  to RAM `0x10000000`, and the code points at its strings by their RAM
  address: 8,001 of 8,827 strings in that range have a stored pointer. The
  1 MiB-aligned sweep could not find this, because the alias base
  `0x0FFAFC00` is not 1 MiB-aligned and only one region is affected. The idea
  came from a third-party analysis; the measurement was re-run here. See
  [09-firmware.md](09-firmware.md#strings-in-the-program-image-are-reached-through-a-ram-alias).

**That step is no longer the next one: it is done.** The Installer's
block-receive path has been analysed. It checks the plaintext tag `#8Z33`
and **the additive sum at `+0x40`**, at `0x10001FD4`, and nothing
cryptographic. (Until 2026-11-10 this said the sum was never read: that
reading covered the SysEx handlers and missed the per-type handlers behind
them.) So "no signature in the file" is also "the installer does not check
one". What remains is the resident loader, and only for a modified
`Installer`.

**A modified `Program` is accepted on hardware.** A third party reported it
through the USB-stick route, and this repository reproduced it over SysEx on
2026-11-14 with a code patch. A `Program`-only patch does not depend on the
loader question at all. See
[09-firmware.md](09-firmware.md#the-program-image-from-inside-a-third-party-analysis-2026-11). Everything that the signature search could *not*
have detected is enumerated in
[09-firmware.md](09-firmware.md#what-the-signature-search-could-not-have-detected) —
read that before quoting the verdict anywhere.

**That probe has been run, and it is a firm negative.** Read-only sweeps have
established that `0x64` answers no Parameter Request in **normal** mode (four
addresses, 24 attempts, a control answering in the same loop) and none in
**loader** mode either, with the change-mode acknowledged — it is acknowledged
after about 7 s, which is what three earlier runs with 0.25 s windows had
missed. Seven addresses, 2.5 s each, an identity control answering in 0.01 s
after every one. See
[10-verified-behaviour.md](10-verified-behaviour.md#2026-11-05-hardware-session-the-loader-takes-seven-seconds-to-acknowledge-and-0x64-is-silent-anyway).
Both results are now `verified on hardware` as instrumented negatives, written
up in
[09-firmware.md](09-firmware.md#what-the-hardware-has-actually-said-about-0x64).
The reserve this section used to carry — "silent under these conditions,
because the change-mode was never acknowledged" — is gone.

Switching into loader mode and back out **is reversible** on this unit, four
cycles now, which bounds the risk of looking but says nothing about writing.

**What this costs us.** The cheap instrument is spent. There is no read path
into `0x64` from the wire, so the resident loader's code cannot be reached by
SysEx in any mode. For a `Program`-only patch that no longer matters (see
above). For a modified `Installer`, two routes are left: write to the machine
and find out, or dump the flash in hardware. Neither is free.

Two narrower firmware questions, both answerable from the file:

- **Three header fields are inferred, not proved**: `+0x6E` (block index),
  `+0x74` (compression flag) and `+0x76` (validity flag). Two blocks cannot
  distinguish a flag from a coincidence. A second update file would settle all
  three at once.
- **The second section-table list is unexplained.** Six records, non-contiguous,
  three of them covering `0x15800000`-`0x18000000` with sizes close to those of
  sections `0x11`, `0x20` and `0x21`. Possibly the same data seen from another
  address space, such as the tone generator's. Low confidence.

### Opened by the third-party firmware analysis (2026-11-10)

Each of these is a claim from
[09-firmware.md](09-firmware.md#the-program-image-from-inside-a-third-party-analysis-2026-11)
that nobody has checked here.

| Question | What would settle it |
|---|---|
| ~~Does a modified `Program` really flash?~~ **Answered 2026-11-14: yes**, reproduced here over SysEx with the play-from-page code patch. The stick route is still not tried here | — |
| The play-from-page patch works on hardware (2026-11-14, owner's report; [10](10-verified-behaviour.md#2026-11-14-hardware-session-the-first-complete-sysex-update-and-the-play-from-page-patch-works)). Still open: the behaviour on tracks shorter than the current page, from Song mode, and under an external `FA` | a track shorter than the current page; Song mode; an external `FA` |
| Does `set_param(mgr, 0x29, bpm)` at `0x200A8C50` change the sequencer's tempo, or only broadcast it? The third party now reports their tap-tempo build, which calls it through `bump`, sets the audible tempo ([09](09-firmware.md#follow-up-a-working-code-patch-published-as-sloptrak-2026-11-13)) | not reproduced here: a patched build flashed on this unit, or reading `0x200A870C` and its observer through to the engine |
| Does `[REC]` emit `01 10 21` `01` on press and `00` on release? | a `listen_counter.py` capture while pressing `[REC]`. Read-only and cheap |
| What is the second USB configuration, with four vendor-specific (`0xFF`) interfaces? | `ioreg` or a USB descriptor dump on the host. Read-only |
| Does the SysEx update path reach the per-type checker at `0x10001FD4` too, or only the stick path? Indirect evidence: a `Program` with a correct `+0x40` was accepted over SysEx; a wrong one has not been tried | trace the callers of the `0x1006D570` table from the `64 02 02` handler at `0x3380` |
| Does flashing the stock `8Z33OS_.PGM` back over SysEx restore the unpatched firmware? | one run of `tools/sysex_updater.py` with the stock file, then `[PLAY]` on page 2 starting at page 1 |

### Opened by a third-party receive-side report (2026-11-14)

`iliakole1` on GitHub, building a MIDI router, reported two results in
[issue #2](https://github.com/jaeggerr/seqtrak-docs/issues/2): a SEQTRAK on
OS V2.00, driven from a Mac over USB. Each row is **reported by a third party,
not reproduced here**. No capture or log was attached, and the method is theirs
as described — "worked repeatedly", "no change of sound" — so how each outcome
was observed (by ear, on the LEDs, or by reading an address back) is not known.

| Claim | Status here | What would settle it |
|---|---|---|
| Writing `F0 43 10 7F 1C 0C 01 10 21 01 F7` **arms recording**, and the same with `00` **stops** it. So `01 10 21` is a command as well as a status | **reproduced 2026-11-15, with a condition they did not state**: `verified on hardware` that the address takes the write **while the sequencer plays** (1 reads back 1, 0 reads back 0, twice), and that with the sequencer **stopped** a written 1 still reads 0. Not established: that notes are recorded, and what the front panel shows. [10](10-verified-behaviour.md#2026-11-15-01-10-21-is-writable-while-the-sequencer-plays) | play notes while it reads 1 and read the pattern back; or watch `[REC]`'s LED |
| `[REC]` makes the unit **send** `01 10 21`, `01` then `00` | a second report of [the same claim](09-firmware.md#what-they-report-on-hardware). The two reporters know each other's work (this one cites SLOPTRAK), so it is not independent corroboration | `receive_side.py --panel` |
| A **bare Program Change** on the DX track's channel (`C9 14`, `C9 28`, `C9 3C`) does **not** change the sound | **reproduced 2026-11-15**, `verified on hardware` on part 9: `01 19 33` read 1961 before and 1961 after a bare `C9 2A`, with the full triplet changing it in the same run ([10](10-verified-behaviour.md#2026-11-15-a-program-change-needs-its-own-bank-select-every-time)) | — |
| `CC 0 = 63`, `CC 32 = n`, then a Program Change **does** select a sound on the synth and DX tracks | **already `verified on hardware` here**, by a stronger route: ten presets loaded this way and `01 1p 33` read back, all ten as predicted ([06](06-sounds-presets.md#reading-back-which-sound-is-loaded)). Their report agrees | — |
| The synth and DX tracks need **their own bank LSB**: LSB 0 holds only the first 128 entries of the one shared list, which are drums | consistent with `from Yamaha Data List` and with the catalogue (`data/presets.csv`). What LSB 0 *does* on a synth track — refused, or a drum sound loaded onto it — is not said | load `63 / 0 / n` on part 7 and read `01 17 33` and `01 17 3C` |
| The **sampler** track does not change this way | consistent with `from Yamaha Data List`: under MSB 62 the channel number names the element | — |

One question their report raises and does not answer, and which decides how a
controller has to be programmed:

| Question | What would settle it |
|---|---|
| ~~Is the bank **latched per channel**?~~ **Answered 2026-11-15: no.** A bare Program Change sent right after a full triplet on the same channel is ignored too, `verified on hardware` on part 9 ([10](10-verified-behaviour.md#2026-11-15-a-program-change-needs-its-own-bank-select-every-time)). Still open: whether `CC 32` + Program Change without `CC 0` is enough, and the same test on a drum or synth part | send LSB + PC only; repeat on part 0 and part 7 |
| Do the System switches `00 00 07` / `00 00 08`, and the "receive System Exclusive" setting, gate these? The reporter did not check either | repeat each stage with the switch off |

### Opened by the "sound name on a controller" patch study (2026-11-15)

The pieces are located in the image, in
[09-firmware.md](09-firmware.md#toward-a-sound-name-on-an-attached-controller-patch-static-2026-11-15).
Nothing was built.

| Question | What would settle it |
|---|---|
| ~~Does the MiniLab 3 show text sent to it by SysEx while it runs a user program?~~ **Answered 2026-11-15: no**, with the families tried; yes in its Arturia and DAW programs ([11](11-controllers.md#the-minilab-3s-screen-what-a-host-can-write-on-it)). The Arturia program's controls are captured too: fixed assignments on channel 1, two of twelve useful to the SEQTRAK. Still open: family `01` in a user program, and what the DAW program's controls send | a capture of every control in the DAW program |
| Does a front-panel Sound Select turn go through the event emitter's `0xC1` case at `0x20143948`? | find the producer of the `0xC1` event in the image; or flash a patch that hooks it and turn the knob |
| Which physical outputs are the port objects at `io+0x58` and `io+0x5C`? | read the constructors that fill `port+0x2C` and `port+0x2E` |
| Is bit `0x80` at `port+0x2E` the `00 00 10` `USB MIDI TX SysEx` switch? | follow the system-parameter write for `00 00 10` to the port object |
| For presets 984, 1252, 1630 and 1946 the image and the Data List spell the name differently. Which does `31 0p 00` return? | load each by Bank/PC and dump the name. Read-mostly, cheap |
| Where are `01 1p 33` and `01 1p 35` answered? They are not in the 290-row parameter index table | follow a Parameter Request through the engine parser `0x20147F0C` |
| Which of the five MIDI parser instances (RAM `0x110219D0`, `0x110219E0`, `0x110219F4`, `0x110219F8`, `0x11021AAC`) is the USB host input? ([09](09-firmware.md#toward-a-translate-an-attached-controllers-fixed-ccs-patch-static-2026-11-15)) | read the code that creates each one and the port object it is given |
| ~~Does the MiniLab 3 show text in its Arturia program without a prior DAW connect message?~~ **Answered 2026-11-15: yes** ([10](10-verified-behaviour.md#the-name-on-the-minilabs-screen-owners-report-same-day)) | — |
| The MiniLab 3 patch is built and checked off-device ([09](09-firmware.md#the-minilab-3-patch-built-and-not-flashed-2026-11-15)). Does it work? | flash it; turn Sound Select with the MiniLab in its Arturia program; press `Shift`, play a key, turn each encoder. Flash the stock file back first, once, to know the way back works |
| ~~Which `Program` is the unit running since 2026-11-15?~~ **Answered**: the MiniLab patch, third build ([10](10-verified-behaviour.md#runs-3-and-4-two-complete-updates-the-write-time-measured-and-the-sound-name-on-the-wire)). Still open: run 2's hang at the hand-over; why leave update mode was not acknowledged within 20 s after runs 3 and 4; and the translated controls with the MiniLab attached (the name on its screen is reported working) | `Shift` + key, a note, then each encoder, fader and pad |
| The MiniLab patch is at its fifth build, flashed and working on the wire ([10](10-verified-behaviour.md#runs-6-and-7-the-fifth-build-a-second-stop-at-the-hand-over-and-the-sound-known-without-a-change)). Still open: why the unit sometimes switches off at the hand-over to the `Installer` (2 of 7 on 2026-11-15); why leave update mode is no longer acknowledged within 20 s after a `Program` write; each translated control checked one by one with the MiniLab attached | for the hand-over: read what the loader does on `64 00 00 00`, and log the battery and USB power state at each run |

## A lead worth following: the firmware's own parameter names

The decompressed `Program` image contains a **table of internal parameter name
strings** starting around offset `0x540000` — 6,463 strings in a single 64 KiB
block. These are the names the firmware gives its own parameters, for example
`Element Number`, `Temporary Element Wave Number`, `Temporary Element Keybank`,
`Sampling Level`, `Recording Timer`, `Receive SystemExclusive Blocked`,
`Ui Operate Button`, `Ui Operate Knob`, `Scale Note of Pad 1` through
`Scale Note of Pad 7`, and `Pad Velocity`.

Several of those are recognisably the same parameters this repository documents
by address — `Scale Note of Pad n` is `30 4D xx`, `Pad Velocity` is `00 00 20` —
so this is potentially **the original nomenclature behind the SysEx address
map**, including for the zones Yamaha never published.

**It is a lead, not a correspondence.** No cross-reference has been done between
these strings and the 1753 documented addresses, and the strings carry no
addresses themselves. Establishing the mapping would mean finding the table that
associates them — which, if it exists in the image, would be the single largest
possible addition to this repository's parameter documentation.
`from firmware image (static analysis)` for the strings' existence and content;
nothing is claimed about any link to an address.

## The bank arithmetic is documented and used, but never pinned by measurement

`bank LSB = (n - 1) // 128`, `program = (n - 1) % 128`, MSB 63 for Drum/Synth/DX
and 62 for SAMPLER. It is `from Yamaha Data List`, every client in this tree
relies on it, and nothing contradicts it. But the specific claim *the bank holds
exactly 128 presets* has never been isolated by a measurement, and it is worth
knowing that before quoting the formula as hardware-verified.

**What cannot be used as evidence.** `data/presets.csv`'s `bank_msb`, `bank_lsb`
and `program` columns are **not extracted from the PDF**:
`tools/pdf-extract/sound_list.py` reads `No. | Name | Category` and computes the
three bank fields with this same formula. Comparing a client's arithmetic to
those columns compares the formula to itself and returns zero divergence by
construction. That test was designed and run during this work before the
circularity was spotted.

**What the wire observations do establish.** Two triplets were captured:

| Capture | Observed | Resolves to | What it rules out |
|---|---|---|---|
| USB, sound-select knob | `CC 0 = 63`, `CC 32 = 7`, ten Program Changes (14, 16, 17, 27, 28, 32, 33, 38, 39, 40) | numbers 911-937, all Synth / Bass | bank sizes that would put ten consecutive knob steps outside one coherent category |
| BLE, channel 3 (part 2) | `CC 0 = 63`, `CC 32 = 1`, `Program Change 121` | number 250, Drum / Clap / "Hand Clap 2" | bank sizes below 127 and above ~150 |

The second is the sharper of the two and it is still blunt: the Clap category
spans 48 presets, so sizes **127 to 150 all land inside it**. Sizes 64, 100,
110, 120 and 256 land on a snare, a rim, a rim, a rim and a closed hat. So the
captures bracket the bank size rather than fix it at 128.

**And the BLE pairing has a precondition nobody recorded.** It only argues for
the formula if part 2 was a *drum* track when the triplet was captured — a clap
resolving on the clap track is the whole point. Part 2 was re-typed to SYNTH and
later repaired on the same day
([types `01` and `03` on the wire](10-verified-behaviour.md)), and the capture
session does not say which state it was in. Treat the row above as conditional.

**The clean validation was done and not written down in replayable form.** Ten
presets were loaded by Bank Select + Program Change and `01 1p 33` read back,
all ten returning the predicted number across four bank LSBs
([06](06-sounds-presets.md#reading-back-which-sound-is-loaded)). That measures
the **machine's own** bank arithmetic — it reports `CurrentSound = lsb × 128 +
program` — which is exactly the claim at issue. What is missing is the per-point
detail: which LSBs, which programs, which values came back. Without it the
measurement cannot be audited or replayed, only trusted.

**Protocol to close this properly**, cheap and read-mostly:

1. Pick presets straddling a bank boundary — catalogue numbers 128, 129, 256,
   257, 384, 385 — so a wrong bank size changes the answer instead of landing in
   the same category.
2. For each, send `CC 0`/`CC 32`/Program Change built from the formula on a known
   part, then read `01 1p 33` and record **the triplet sent and the value
   returned**, not just "it matched".
3. A bank size of 127 or 129 would show up at the boundary as an off-by-one in
   the read-back; 128 would not.
4. Record the part's `PartAwmType` (`01 1p 3C`) in the same loop, so the
   precondition that weakened the BLE pairing is not left to memory.

Until that exists, the formula stays `from Yamaha Data List` — which is a
perfectly good standing, and better than a `verified on hardware` the record
cannot support.

## Two questions opened by writing a whole palette (2026-10-22)

### Why does a preset land on the *wrong* sound when a Parameter Change follows it too soon

Established in [10-verified-behaviour.md](10-verified-behaviour.md#a-preset-load-is-not-ordered-against-the-parameter-changes-that-follow-it):
writing a part's `31 1p` parameters 20 ms after its Program Change loses the
shaping on some parts and loads a **different sound** on others. Loading all
eleven presets first, confirming each `01 1p 33`, then shaping, is reliable
across two runs.

The lost shaping has an obvious explanation. The wrong sound does not:

| Part | `01 1p 33` read | expected | difference |
|---|---|---|---|
| 3 | 882 | 355 | +527 |
| 4 | 1587 | 384 | +1203 |
| 7 | 954 | 907 | +47 |

No constant offset, and part 7's bank LSB was right (7) while its program came
back 58 instead of 11. Candidate explanations, none tested: a Bank Select
latched from a neighbouring channel; the Program Change arriving while the
previous part was still loading; `01 1p 33` reporting a transient. The test that
would separate them is to load one part at a time with a long settle, reading
`01 1p 33` on **all eleven** parts after each, so a value appearing on the wrong
part becomes visible.

### Which route loads a preset SAMPLER element

Bank MSB 62 with LSB 1 and Program Change 124 left part 10 with engine byte `05`
and an empty name, sent both on part 10's own channel (11) and on channel 1 —
the reading suggested by "under bank MSB 62 the MIDI **channel** number is read
as the element number" ([06-sounds-presets.md](06-sounds-presets.md#bank-select-and-program-change)).
Part 0's sound was a witness on the channel-1 attempt and **did not move**, which
does establish that MSB 62 is not read as an ordinary sound bank there.

Two channels are not a proof of impossibility. The experiment that would settle
it: sweep MSB 62 across all eleven channels, and after each attempt read part
10's `31 0A 00` name **and** the `01 1p 33` of every part, so an element landing
somewhere unexpected is caught rather than missed. Worth pairing with a read of
the `50 eA` SAMPLER Sample block, which may be the real target.

## Why does `01 1A 33` not answer, when `01 1A 3C` does? (2026-10-23)

`CurrentSound` answers on parts 0-9 and resolves to the right preset every
time. On part 10, the SAMPLER, it is silent: eight attempts across two clients,
with `01 17 33` answering immediately before and after, so the link was not the
problem.

What is not in doubt: the part nibble is right (`01 1A 3C` answered on the same
part in the 2026-10-22 session) and the address family reaches part 10.

The inference worth testing — and it is only an inference — is that the sampler
does not *have* a current sound in the sense this parameter means. Its loaded
material is a set of elements, and under bank MSB 62 the MIDI channel number is
read as the element number. If that is right, the parameter to look for is a
current *element*, not a current sound.

Until someone establishes which, a client should treat the sampler's sound name
as unavailable rather than as empty — they are different facts.

## The drop rate for an isolated Parameter Request (2026-10-23)

Two measurements of the same thing disagree, and both were taken properly, so
both stay.

| Measurement | Sample | Lost | Instrument |
|---|---|---|---|
| [10-verified-behaviour.md](10-verified-behaviour.md#transport-reliability) | 10 requests, `01 10 07` and `01 10 20` | ~1 in 10 | `tools/hardware-probe/seqtrak_probe.py` |
| [10-verified-behaviour.md](10-verified-behaviour.md#4-drop-rate-over-usb-40-requests-40-replies) | 40 requests, `30 40 76` | 0 | the `seqtrak-next` Swift client over USB |

Getting 0 losses in 40 draws at p = 0.1 has probability about 1.5 %, so this is
unlikely to be one lucky run: the two samples disagree about the underlying
rate. What differs between them is not established — candidates are the
transport, the client's queueing, the address queried, the machine's state and
the firmware revision.

**The transport candidate is now weak.** On 2026-10-23 the same client, with
the same instrument, got 40/40 on Bluetooth as well as on USB
([10-verified-behaviour.md](10-verified-behaviour.md#11-the-drop-rate-is-not-explained-by-the-transport)).
Whatever the difference is, it is not USB versus Bluetooth on this unit. The
client's queueing — which paces at 50 ms where the earlier prober did not —
is the candidate that has not been tested.

**The rule does not change while this is open.** Retry four times and keep a
control address in the loop, on every transport. A client that assumes the low
rate and is wrong manufactures false facts; a client that assumes the high rate
and is wrong only costs itself a few milliseconds.

## Documentation gaps in this repository

- The **DX algorithm chart** (Data List p. 161) and the **effect block diagram**
  (p. 60) are graphics, not text, and are not transcribed, because the routing
  they show cannot be recovered from the PDF's text layer. Consult them in
  Yamaha's Data List (see [`../reference/`](../reference/README.md)). These are
  the only two facts this repository does not carry.
- Eight of the 2424 preset names differ from a second, independent extraction of
  the same table only in the spacing around a hyphen (`Reco-reco 1` versus
  `Reco -reco 1`). Both extractions are automated and both are plausible; the
  PDF's own glyph spacing is ambiguous there. Not worth resolving unless exact
  string matching against the official app matters.
- The Data List's **Effect Parameter List** footnotes are captured as a single
  `panel_note` column per effect panel rather than attached to the specific
  parameter they annotate.
- **Closed (2026-10-23): two parameter names carried their own column label.**
  `49 o9 00` was extracted as "Parameter Name ON/OFF" and `30 4C 00` as
  "Parameter Name USB Part Input Mode", with "Description" and "Notes" leaked
  into the neighbouring cells of the same two rows. `param_table.py` bands the
  three centred columns by y and excludes everything within 8 points of the
  word "Address"; on Data List pp. 132 and 152 the column labels sit just
  inside that margin and fell into the first row's band. The extractor now
  strips a leading column label from those three cells, which is unambiguous
  because no parameter is named after its own column. Four cells changed in
  `data/parameters-datalist.csv`; nothing else moved.
- **Still open: three system rows read as one run-on name.** `00 00 0B`,
  `00 00 0F` and `00 00 13` are each named "… Transmit Control Change Transmit
  Bank Select Transmit Program Change" with a range of `0 - 112`. Three rows of
  the PDF share one address band there, so the three switch names were
  concatenated. That the field is a bit field rather than a scalar is already
  `verified on hardware`: all three read `70` = `0b1110000`, three bits set
  ([10-verified-behaviour.md](10-verified-behaviour.md)). What is not yet
  recovered is which bit is which switch, and the generated tables still show
  the run-on name and the scalar bound. Nothing has been written to them.

## ~~A 14-bit Parameter Change has never been sent~~ — CLOSED 2026-10-23

Reading a multi-byte field is now settled on three blocks: the request is
answered at the base address with the field's full width, and the interior is
silent ([10-verified-behaviour.md](10-verified-behaviour.md)). **Writing one has
never been tried.**

The format allows it — a Parameter Change carries `dd … dd`, and the Data List
spells the encoding out as "1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0" — but
that is `from Yamaha Data List`, not a measurement. Nothing establishes:

- whether the machine accepts a two-byte Parameter Change at all, or ignores
  the second byte;
- whether it clamps the composite value or the bytes separately;
- whether a one-byte write to a two-byte address does something (sets the MSB,
  is ignored, or is refused).

This is not a corner case. **Every effect parameter is a two-byte field** —
`30 41 03` onward for the reverb, `30 42` for the delay, `31 2p` / `31 3p` for
the track insertions — so the whole effect surface is currently read-only to
any client that will not guess. The tempo, the swing, the pattern lengths and
the EQ frequencies are two-byte fields too.

**Settled the same day**, on `30 41 0B` with a witness and a verified restore
([10-verified-behaviour.md](10-verified-behaviour.md)):

- the machine **accepts** a two-byte Parameter Change;
- a one-byte write to a two-byte field is **ignored** — it does not set the MSB
  and does not set the LSB, so a client that sends the wrong width corrupts
  nothing and also achieves nothing;
- the 7-bit big-endian packing was confirmed with a **non-zero MSB**: 130 as
  `01 02` and 200 as `01 48`, both read back exactly.

**Four bytes settled too, later the same day**: a sampler start point written
as `00 00 01 00` and read back, witness unmoved, restored. Every width the
reference uses — one, two and four bytes — is now verified in both directions.
What remains unknown is a sample's real length, so a trim point can be moved
inward with confidence and not outward.
