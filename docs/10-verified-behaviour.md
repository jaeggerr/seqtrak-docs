# 10 — Verified hardware behaviour

Everything in this document was observed on a real Yamaha SEQTRAK. It is the
only `verified on hardware` source in this repository, and it is what makes the
unverified parts credible: wherever it touched a zone known only from the
official app, the zone was real.

The sessions recorded here:

- **2026-08**, over USB MIDI with the SEQTRAK acting as **USB host** and an
  ESP32-S3 running TinyUSB as the attached device. What the machine emits
  spontaneously in that direction.
- **2026-10-22**, over USB MIDI with the SEQTRAK as a **device** on a Mac
  (CoreMIDI port `SEQTRAK`), using
  [`../tools/hardware-probe/seqtrak_probe.py`](../tools/hardware-probe/seqtrak_probe.py)
  (read-only) and
  [`../tools/hardware-probe/write_test.py`](../tools/hardware-probe/write_test.py)
  (one reversible write). Systematic address probing, gesture-by-gesture
  listening, and the first verified write to an undocumented zone.
- **two read-only firmware probes**, also over USB MIDI, which asked whether the
  `0x64` update space answers anything outside an update — in normal mode and
  then in loader mode. See
  [the `0x64` result](#the-firmware-space-0x64--silent-and-that-was-measured).
  Nothing was written and nothing was flashed.

Machine state during the October session: firmware `02 00 00 02`, battery ~70,
tempo 119 BPM, project 0, part 0, sequencer stopped, Wi-Fi off, headphones
unplugged, `MIDI Clock Out` **on**.

## Headline result

**33 addresses queried, 33 answered**, in the first session. Every zone that existed only in static
analysis responds on real hardware: `01 00 xx` and `01 10 xx`, `01 1p xx`,
`30 4D xx` (user scales), `70 40/50/60 xx` (step-record reads), `00 60 xx`
(Wi-Fi), `71 xx xx` (song mode).

That does not by itself prove the *meaning* of each address — see
[semantics](#semantics-proven-by-physical-action) for the three that were proven
by physical action, and [12-open-questions.md](12-open-questions.md) for what is
still only "reachable".

## Identity Reply — exact to the bit

```
→ F0 7E 7F 06 01 F7
← F0 7E 7F 06 02 43 00 41 64 06 0A 00 00 7F F7
```

The pattern derived from the official app's firmware updater
(`F0 7E 7F 06 02 43 00 41 64 06 xx 00 yy 7F F7`) holds: byte 11 is `00`, bytes
13-14 are `7F F7`. Yamaha's own documentation fixes both of the bytes the app
left as variable to `00`, and the hardware agrees. Decoding
`mm = (version − 1.0) × 10` gives `0x0A` → **version 2.0**, matching the OS
V2.00 the unit was running.

## Plumbing already documented by Yamaha

| Parameter | Address | Reply | Value |
|---|---|---|---|
| Speaker Master Volume | `00 00 00` | `3D` | 61 |
| Headphone Master Volume | `00 00 01` | `29` | 41 |
| Tempo | `30 40 76` | `00 77` | 119 BPM — two-byte encoding confirmed |
| MIDI Clock Out | `00 00 2D` | `01` | On |
| USB MIDI TX SysEx | `00 00 10` | `01` | On |

## The `01 xx xx` live-state zone

Previously `from the official app, untested`.

| Parameter | Address | Reply | Value |
|---|---|---|---|
| `FirmwareVersion` | `01 00 00` | `02 00 00 02` | 4 bytes |
| `CompatibleVersion` | `01 00 04` | `01` | 1 |
| `SystemStatus` | `01 10 00` | `00` | 0 |
| `Battery` | `01 10 02` | `46` | 70 |
| `HeadphonePlugStatus` | `01 10 07` | `00` | 0, headphones unplugged |
| `SampleMemoryUsedSize` | `01 10 11` | `00 0B` | 11 |
| `SampleMemoryTotalSize` | `01 10 13` | `03 7E` | 510 |
| `CurrentProject` | `01 10 15` | `00` | 0 |
| `GeneralMode` | `01 10 17` | `00` | 0 |
| `SequencerStatus` | `01 10 20` | `00` | 0, stopped |
| `CurrentPart` | `01 10 27` | `00` | 0 |
| `MasterKnobMode` | `01 10 2D` | `00` | 0 |
| `ParameterLedMode` | `01 10 2E` | `01` | 1 |

## The `01 1p xx` per-part zone, p = 0

| Parameter | Address | Reply | Value |
|---|---|---|---|
| `SoundDesignPage` | `01 10 30` | `00` | 0 |
| `CurrentSound` | `01 10 33` | `00 02` | 2 |
| `PatternKnobMode` | `01 10 39` | `00` | 0 |
| `MasterSlider1Assign` | `01 10 50` | `09` | 9 |
| `SingleSlider1Assign` | `01 10 53` | `09` | 9 |
| `SingleSlider1ControlValue` | `01 10 5C` | `00` | 0 |

These share mid byte `0x10` with the global block because part 0 composes to
`0x10 | 0`. The low byte separates them: `al >= 0x30` is per-part.

## User scales — `30 4D xx`

Absent from the Data List; eight scales of seven pads, one MIDI note per pad.

| Parameter | Address | Value | Note |
|---|---|---|---|
| `Scale1NoteOfPad1` | `30 4D 00` | 60 | C3 |
| `Scale1NoteOfPad2` | `30 4D 01` | 62 | D3 |
| `Scale2NoteOfPad1` | `30 4D 10` | 60 | C3 |
| `Scale8NoteOfPad7` | `30 4D 76` | 70 | B♭3 |

The stride of `0x10` between scales and `0x01` between pads is confirmed, so
`al = (scale − 1) × 0x10 + (pad − 1)` with scale 1-8 and pad 1-7.

## Step record reads — `70 xx xx`

| Request | Address | Reply |
|---|---|---|
| note info, part 0 step 0 | `70 40 00` | `3C 64 00 3C 00 78` |
| note info, part 0 step 1 | `70 40 01` | *(zero data bytes)* |
| parameter info, step 0 | `70 50 00` | *(zero data bytes)* |
| conditional lock, step 0 | `70 60 00` | `00` |

**The body is 6 bytes, not 8.** Part and step live in the address, not in the
data:

```
noteNumber velocity retrigger microTiming gateTimeMsb gateTimeLsb
    3C        64        00         3C          00          78
    60       100         0         60           0         120
```

**An empty step replies with zero data bytes** — that is the marker to test, and
it corresponds to `IsNoteNothing()` in `MIDI.StepNoteInfoMessage`.

> This **corrects** the earlier write-up taken from the official app, which implied an
> eight-field reply including track and step. Do not propagate the eight-field
> reading.

## Wi-Fi — `00 60 xx`

| Parameter | Address | Value |
|---|---|---|
| `WiFiMode` | `00 60 00` | 0 |
| `WiFiReady` | `00 60 01` | 0 |
| `WirelessLAN` | `00 00 16` | 0 |

## Song mode — `71 xx xx`

| Parameter | Address | Value |
|---|---|---|
| `CurrentScene` | `71 10 04` | 0 |
| `ChangePlayMode` | `71 10 06` | 0 |
| `ChangeSceneMode` | `71 50 00` | 0 |

## Semantics proven by physical action

Reaching an address proves the address. Proving what it *means* needs a
controlled gesture. The protocol used: one gesture at a time, and at each step
re-read the three targets **plus three witnesses** that must not move. The
witnesses are what separates "I am reading the right parameter" from "I am
misdecoding a reply".

| Address | Parameter | At rest | Headphones in | Sequencer running | SYNTH 1 selected |
|---|---|---|---|---|---|
| `01 10 07` | `HeadphonePlugStatus` | 0 | **1** | 1 | 1 |
| `01 10 20` | `SequencerStatus` | 0 | 0 | **1** | 0 |
| `01 10 27` | `CurrentPart` | 0 | 0 | 0 | **7** |
| `01 10 15` | *witness* `CurrentProject` | 0 | 0 | 0 | 0 |
| `30 40 76` | *witness* Tempo | 119 | 119 | 119 | 119 |
| `01 10 02` | *witness* `Battery` | 70 | 65 | 70 | 75 |

At every step **exactly one target changed**, the expected one, and the two
fixed witnesses did not move. All three parameters are therefore `verified on
hardware` with their semantics understood, not merely reachable.

`CurrentPart = 7` for SYNTH 1 validates the whole part numbering in one shot:
drums 0-6, SYNTH 1 = 7, SYNTH 2 = 8, DX = 9, SAMPLER = 10.

`Battery` tracks the real charge (the machine charges over USB), which makes it
a poor negative control — but the value is correct.

## Transport reliability

**An isolated Parameter Request is occasionally lost.** Measured: over 10
attempts, `01 10 07` and `01 10 20` each failed once, uncorrelated. The first
read of step 1 came back as "no reply" and looked exactly like a property of the
parameter.

Practical consequences:

- **Never treat the absence of a reply as information.**
- Retry: four attempts per address was enough here (implemented in
  `seqtrak_probe.py`).
- Always keep a known-good control address in the same loop. Without one, a
  false behaviour would have been documented for the headphone parameter.

Do not confuse this with the legitimate case of an **empty step**, which does
reply, with zero data bytes (`70 40 ss`).

**The same rule catches your own bugs, not just the wire's.** In one session an
address appeared to stop answering, and then the whole machine appeared to stop
answering. Both were false: in zsh, `--req $A` with `A="31 47 04"` passes *one*
argument rather than three, `argparse` failed, and a `grep` in the pipeline
swallowed the error. Running the known-good control plan showed the machine was
fine within seconds. Quote your variables, and check a control address before
concluding anything about the device.

## What the machine broadcasts without being asked

### Passive listen, 75 seconds of free manipulation

288 messages, of which only **58 were SysEx**, across **4 distinct addresses**:

| Address | Count | Values | Meaning |
|---|---|---|---|
| `01 10 20` | 1 | `01` | `SequencerStatus` — sent on pressing play |
| `01 10 2E` | 1 | `03` | `ParameterLedMode` — what the LEDs are showing |
| `30 45 03` | 28 | `00`, `01` | Master Effect 3, parameter 1 (2 bytes) |
| `30 45 05` | 28 | `00 08` … `00 05` | Master Effect 3, parameter 2 (2 bytes) |

The remaining ~230 messages were not SysEx: pad and sequencer notes, transport,
Program Change.

Three conclusions:

1. **The `01 10 xx` zone really is broadcast spontaneously.** `01 10 20` and
   `01 10 2E` arrived with nothing requested. The zone is usable by passive
   listening, not only by polling.
2. **A knob move is broadcast at the real parameter address**, not at the
   `01 1p 5C` mirror. To show "what the knob you are turning does", decode the
   received address against the parameter table — which is exactly the use the
   399-entry extraction was made for.
3. **The effect-parameter offset formula is confirmed.** The official app gives
   `al = 0x01 | (parameterNum << 1)`. Live traffic shows Master Effect 3
   (`30 4n xx`, n = 5) parameters 1 and 2 at offsets `03` and `05`:
   `0x01|(1<<1) = 3` and `0x01|(2<<1) = 5`.

Limit of this first window: a single 75-second free-play session, with no record
of which gestures were made or in what order. Notably `01 10 27`
(`CurrentPart`) was **not** broadcast — but nothing says a track change happened
during the window. Hence the second pass.

### Timestamped listen, gesture by gesture

90 seconds with `--watch 90 --timeline`, gestures separated by silences. 613
messages, cut into 7 bursts by the pauses. Each burst was attributed **by its
content**, which is safer than by its expected time.

| Gesture | What the machine emits |
|---|---|
| **Track change** | SysEx `01 10 27` = the part index (seen: `08` then `07`) |
| **Pattern change** | SysEx `30 5p 0F` (seen: `30 57 0F` = `01` — part 7, pattern 2) |
| **Sound change** | **Bank Select MSB + LSB, then Program Change** on the track's MIDI channel — no SysEx `01 1p 33`. (The first listen missed the Bank Select; see [the correction below](#bank-select-is-transmitted--a-documented-conclusion-reversed).) |
| **Knob / slider** | **both at once**: SysEx at the real parameter address *and* a CC on the track's channel, one for one (36 / 36) |
| **Play / Stop** | SysEx `01 10 20` = `01` / `00`, plus realtime `FA` / `FC` |
| **Pads and sequencer** | Note On/Off on the track's MIDI channel |
| *(also)* | SysEx `01 10 2E` `ParameterLedMode` accompanies sound changes and knob moves |

### Correction: a knob emits CC as well

The first pass concluded that a knob emitted only at the real parameter address.
That was incomplete. The burst at 63 s contains **36 SysEx `31 27 09` and 36 CC
on channel 8**, in exact correspondence. Both routes are available:

- the **SysEx** gives the exact identity of the parameter — here Insertion
  Effect A of part 7, parameter 4 — to be decoded against the parameter table;
- the **CC** gives a controller number, which needs the CC → parameter mapping.

For a display, SysEx is the right source: it is self-describing.

The `01 1p 5C` mirror (`SingleSliderNControlValue`), on the other hand, **was
never emitted**. It serves the app, not gesture tracking. That conclusion holds.

> This **corrects** an earlier claim that `01 1p 5C` was how to follow a knob.
> It is not.

### Part → MIDI channel confirmed

The track-change bursts each contain a note on the new track's channel:
`01 10 27` = `08` with a note on channel 9, then `01 10 27` = `07` with a note
on channel 8. So **MIDI channel = part index + 1**. During playback, notes
arrived on channels 1, 2, 4, 5, 7, 9 and 10 — parts 0, 1, 3, 4, 6, 8 and 9.

### Second confirmation of the effect-parameter offset

`31 27 09`: `31 2p xx` is Insertion Effect A with `p = 7`. Offset `09`
corresponds to parameter 4 through the official app's formula
`al = 0x01 | (parameterNum << 1)` → `0x01|(4<<1) = 0x09`. A second independent
confirmation, after the Master Effect one.

## The first verified write

The first **write** test on a zone absent from the Data List: the user scales.
Protocol: read → write → re-read → restore, with the restore in a `finally`
block and a neighbouring address as witness. Script:
[`../tools/hardware-probe/write_test.py`](../tools/hardware-probe/write_test.py).

```
STEP 1  target 30 4D 00 = 60   witness 30 4D 01 = 62
STEP 2  F0 43 10 7F 1C 0C 30 4D 00 43 F7        (write 67)
STEP 3  target 30 4D 00 = 67   witness 30 4D 01 = 62   ✓
STEP 4  F0 43 10 7F 1C 0C 30 4D 00 3C F7        (restore 60)
        target 30 4D 00 = 60                           ✓
```

Three things are established:

1. **Parameter Change** `F0 43 10 7F 1C 0C ah am al dd F7` works exactly as
   documented, on an address known only from the official app.
2. The write is **localised**: the neighbouring pad did not move, so
   `al = (scale − 1) × 0x10 + (pad − 1)` addresses exactly one pad.
3. The write is **immediately readable back**, which gives a write/verify cycle
   usable for testing the other zones.

The machine was returned to its initial state.

## Writing a note into a pattern — the full cycle

The most consequential result in this document: **patterns can be composed from
outside the machine.** Tested end to end, write then delete, with a neighbouring
empty step as witness. Script:
[`../tools/hardware-probe/step_write_test.py`](../tools/hardware-probe/step_write_test.py).

### The scan reads out the real pattern

Reading the first 16 steps of part 0 (KICK) through `70 (40|tt) ss`:

```
step  0  #   step  4  #   step  8  .   step 12  #
step  1  #   step  5  .   step  9  .   step 13  .
step  2  #   step  6  .   step 10  #   step 14  .
step  3  .   step  7  .   step 11  .   step 15  .
```

Every occupied step holds `3C 64 00 3C 00 78` — note 60, velocity 100,
retrigger 0, micro timing 60, gate 120 — and every empty step replies with
**zero data bytes**. So a whole pattern is readable, step by step.

### Write

```
F0 43 10 7F 1C 0C 70 00 00 03 3C 64 00 78 F7
                   │  │  │  │  │  │  └──┴─ gate 120, 14-bit
                   │  │  │  │  └─ velocity 100
                   │  │  │  └─ note 60
                   │  │  └─ step 3
                   │  └─ part 0
                   └─ ah = 70 (step record), am = 0x00 | track (add)
```

Reading step 3 back: `3C 64 00 3C 00 78` — note and velocity exactly as
written, gate read back as 120. **The machine filled in `retrigger = 0` and
`micro timing = 60` itself**, since the add message does not carry them. So 60
is the neutral micro-timing value, and `70 (10|tt) 00` adjusts around that
centre rather than around 0.

Step 5, taken as the witness, stayed empty: the write is localised to the
targeted step.

### Delete

```
F0 43 10 7F 1C 0C 70 20 00 03 F7
                   │  │  │  └─ step 3
                   │  │  └─ al = 00
                   │  └─ am = 0x20 | track (delete)
                   └─ ah = 70
```

Step 3 went back to zero data bytes. The machine was returned to its initial
state.

### Precondition

**The sequencer must be stopped.** The script refuses to run when `01 10 20`
reads `1`.

### What this unlocks

Reading *and* writing patterns are now both verified, with a reliable
empty-step marker. That is enough to build a pattern generator, an external
editor, or an importer that brings a pattern in from another tool — with no
Yamaha app anywhere in the chain.

## Bank Select IS transmitted — a documented conclusion reversed

The most important correction in this repository. **Two earlier sessions
concluded the SEQTRAK never transmits Bank Select. That was wrong.**

Turning the sound-select knob emitted, on *every* preset change:

```
CC 0  = 63     Bank Select MSB
CC 32 = 7      Bank Select LSB
Program Change 14, 16, 17, 27, 28, 32, 33, 38, 39, 40
```

Ten Program Changes, ten CC 0, ten CC 32 — systematically, not only at bank
boundaries. And it matches the Data List's table exactly: MSB 63 = Sound
(Drum / Synth / DX), LSB 0-31 = preset banks 1-32, so LSB 7 is preset bank 8.

All three transmit masks read back with every bit set, so **the bitmask is not
cosmetic**:

| Address | Port | Value | CC | BS | PC |
|---|---|---|---|---|---|
| `00 00 0B` | Legacy MIDI (TRS) | `0x70` | 1 | 1 | 1 |
| `00 00 0F` | USB | `0x70` | 1 | 1 | 1 |
| `00 00 13` | Bluetooth | `0x70` | 1 | 1 | 1 |

### What this changes

The old conclusion was that a local preset table could not resolve a name on
its own, because a received Program Change gave only a position in an unknown
bank. **Bank plus program is sufficient**, so the local catalogue in
[appendix-c-sound-list.md](appendix-c-sound-list.md) does resolve a preset name
from passively received MIDI. The `11 02 pp` bulk dump is no longer *required*
for that — it remains the right route for **user** sounds and for exact names.

The August observation was made with the SEQTRAK as USB host and a
custom-firmware peripheral receiving, whose on-screen log was a nine-line ring
buffer read live. One sound-knob turn produces about 30 messages in a second, so
the Bank Select pair scrolled past. Two sessions agreeing did not make it true —
they shared an instrument, and that instrument could not establish an absence.
See [the same cause behind the FX-slider claim](#the-august-no-sysex-claim-falls--and-why).

## The four per-track knobs: Control Change only

85 seconds of listening while the four knobs of the selected track were turned
one at a time. **66 messages, zero SysEx**, in four clean bursts:

| Burst | Messages | Control |
|---|---|---|
| 1 | CC 0 = 63, CC 32 = 7, 10 × Program Change | **Sound Select** |
| 2 | CC 26 = 2, a single message | **Mono/Poly/Chord**, set to Chord |
| 3 | CC 10, 26 messages, 87 → 114 | **Pan** |
| 4 | CC 7, 9 messages, 117 → 127 | **Volume** |

All on channel 8, part 7 (SYNTH 1), the selected track.

These four are exactly the four entries of page 1 of the Synth sound-design
table in
[appendix-h-sound-design-parameters.md](appendix-h-sound-design-parameters.md) —
Sound Select, Mono/Poly/Chord, Pan, Volume — which is an independent
confirmation of that table, and which identifies burst 2: CC 26 value 2 is
`Mono/Poly/Chord` = Chord, per [the CC map](../data/cc-map.csv).

**These are the per-track knobs, not the FX section.** The CC range cited for the
effect controls elsewhere (102-115) did not appear here because those controls
were not touched. The FX sliders were measured separately and behave
differently — they emit **both** voices; see
[the FX slider result](#the-fx-sliders-emit-both-voices--and-sysex-carries-strictly-more).

## The FX sliders emit both voices — and SysEx carries strictly more

100 seconds, three sliders turned across three different FX blocks.
**390 messages: 6 distinct SysEx addresses and 171 Control Changes**, in eight
attributable bursts.

| Burst | SysEx | Control Change | Reading |
|---|---|---|---|
| FX button press | `01 10 2E` = 3 | — | mode change |
| slider | `31 27 15` × 34 | CC 107, ch 8, × 34 | Single Effect, part 7 |
| slider | `30 44 05` × 35 and `30 44 15` × 35 | CC 105, ch 1, × 35 | Master Effect 2 |
| slider | `30 45 03` × 56 and `30 45 05` × 56 | CC 106, ch 1, × 56 | Master Effect 3 |
| FX button press | `01 10 2E` = 2, then = 1 | — | mode changes |

The observed controller numbers match the Data List exactly: CC 107 is Single
Effect parameter 1, CC 105 is Master Effect 2 parameter 1, CC 106 is Master
Effect 3 parameter 1.

### One slider drives several parameters

The most useful result here. Count the two voices against each other:

| Block | CC messages | SysEx messages | SysEx addresses |
|---|---|---|---|
| Single Effect | 34 | 34 | 1 |
| Master Effect 2 | 35 | 70 | 2 |
| Master Effect 3 | 56 | 112 | 2 |

**The CC reports the slider's position — one message per step. The SysEx reports
every parameter the effect preset actually moves.** Where a preset drives two
parameters from one slider, each step produces two SysEx messages and still only
one CC.

The two voices are therefore **complementary, not redundant**, and the SysEx
voice is strictly more informative. That also explains an earlier capture of
Master Effect 3 parameter 2 at `30 45 05`: that parameter has **no CC assigned
at all** — the Data List gives Master Effect 3 only CC 106, for parameter 1 — so
it moved and only SysEx reported it.

### Which channel the CC arrives on

| Block | CC channel |
|---|---|
| Master Effect | **channel 1**, whatever part is selected |
| Single / Insertion Effect | the **track's** channel (8 here, part 7) |

Consistent with master effects being project-wide rather than per-part. A
listener has to expect both.

### Following the active FX block

**Not** through the slider-mode flags. `MasterEffectSliderMode` (`01 10 1A`),
`ReverbSliderMode` (`1B`), `VariationSliderMode` (`1C`) and
`InsertionEffectSliderMode` (`01 1p 31`) were **none of them emitted** anywhere
in the capture. They appear to be app-internal.

What does change is `01 10 2E` `ParameterLedMode`, which took **3, then 2, then
1** as the FX button cycled. So to follow the active FX block passively, watch
`ParameterLedMode`. Its full 0-43 scale is still undecoded — see
[12-open-questions.md](12-open-questions.md).

### The August "no SysEx" claim falls — and why

This is the **second** `verified on hardware` claim in this repository to be
overturned, after Bank Select, and it failed for the **same reason**: both were
read off the same instrument. 34, 70 and 112 SysEx messages per gesture are
unmissable on an instrument that can see them.

An earlier version of this document blamed USB-MIDI SysEx reassembly in that
receiver. **That was wrong**, and the receiver's code has since been read: it
handles all four relevant code index numbers (`0x4` start/continue, `0x5`,
`0x6`, `0x7` end), it strips realtime bytes embedded inside a SysEx *before*
reassembly, it guards against an unterminated SysEx, and it decodes Bank Select
MSB and LSB explicitly. The parsing was sound. The same session's own notes also
record that it *did* receive SysEx, including `01 10 xx` parameter changes —
a reassembly bug would have lost all of it, not a selective subset.

There was also a logical tell, available without reading any code: **the
proposed cause did not cover both effects.** Bank Select is `CC 0` and `CC 32` —
plain Control Change, one 4-byte USB-MIDI packet each. A receiver that loses
SysEx while passing every CC cannot explain a missed Bank Select. A mechanism
that contradicts one of the two failures it claims to explain is the wrong
mechanism, and noticing that needs no hardware at all.

**The cause was the display, not the parser.** The on-screen log was a **nine-line
ring buffer, read live**. Turning one FX slider produces about **105 messages in
1.2 seconds** (35 CC interleaved with 70 SysEx); turning the sound knob produces
about 30 in a second. Nine lines scrolling at that rate show only the tail of
the burst. Both false conclusions were **negative** claims — "never sends X" —
inferred from a window far too small to support them.

The right instrument was already there, unused: that firmware prints a
cumulative per-CIN counter (`cin 4:120 5:8 9:12 F:2880`). A non-zero count on
CIN `0x4`, `0x6` or `0x7` means SysEx is arriving, and a counter is immune to
scrolling. That one line would have settled both questions immediately.

> **The rule this vindicates, in its sharper form:** two agreeing observations
> are not two independent observations when they share an **instrument** — and
> the shared instrument here was not the MIDI receiver, it was a nine-line log.
> The failure mode is **absence inferred from a sampling window too small for
> the burst**. To claim that something never happens, you need an instrument
> that can *establish absence*: a cumulative counter, or a complete timestamped
> capture — never a scrolling view of a fast burst.

## `31 4p 03` LFO Tempo Speed: the Data List wins

The last genuinely unexplained disagreement between the Data List (5-24) and the
app extraction (5-52, displayed 5-24), settled by a write sweep on part 7
with restore — [`../tools/hardware-probe/probe_write.py`](../tools/hardware-probe/probe_write.py):

| Wrote | Read back | Verdict |
|---|---|---|
| 24 | 24 | accepted as written |
| 25 | 24 | clamped to 24 |
| 30 | 24 | clamped to 24 |
| 40 | 24 | clamped to 24 |
| 52 | 24 | clamped to 24 |
| 60 | 24 | clamped to 24 |

Original value 11, restored. **The machine clamps at 24**, so the Data List's
range is right and the extraction's 52 is an app-side artefact with no effect on
hardware. This also demonstrates the general technique: a write sweep with
restore resolves any range disagreement.

It also confirms that the per-part sound zone answers for a **non-zero** part.
The whole LFO block of part 7 responds:

```
31 47 00 = 0     31 47 03 = 11    31 47 06 = 0
31 47 01 = 0     31 47 04 = 0     31 47 0B = 66
31 47 02 = 52    31 47 05 = 0     31 47 0C = 0
```

## Documented defaults do not match a machine in use

Settings read from two different units, against the Data List defaults:

| Parameter | Address | Documented default | Read from hardware |
|---|---|---|---|
| MIDI Clock Out | `00 00 2D` | `01` (On) | `Off` in 2026-08; `On` in 2026-10 after the user enabled it |
| Sink Current Setting | `00 00 2E` | `00` (Auto) | `Auto` |
| USB MIDI TX CC/BS/PC | `00 00 0F` | `00` | CC reported **on** |
| USB MIDI TX SysEx | `00 00 10` | `00` (Off) | **On** |

The lesson is simple: **read the settings, do not assume the defaults.** Several
of the behaviours that look like device limitations are just switches. The
`F8` clock was "missing" in August purely because `00 00 2D` was off on that
unit.

## 2026-08 session: the SEQTRAK as USB host

What an attached class-compliant USB MIDI device receives, with the SEQTRAK in
"To Device" mode:

- **Notes** on each track's own channel: yes.
- **SysEx**, including `01 10 xx` live-state Parameter Changes when the machine
  is manipulated: yes.
- **Transport** `FA` / `FB` / `FC`: yes.
- **MIDI clock `F8`**: not received, because `00 00 2D` was off, not because of
  the host direction. Enabling it makes the clock arrive, and the playhead
  position can be computed at 24 ppqn — **6 clock ticks per 16th step**.
- The machine **answers Parameter Requests** in this direction, so tempo and
  system settings are readable without the app.
- It **answers Bulk Dump Requests** too: `11 02 pp` returns the ~30-block burst,
  and the preset name comes out of the `31 0p 00` block (88 bytes, 7-bit packed,
  11 groups of 8). Fast enough that scrolling presets at the knob shows no
  perceptible delay.
- **Program Change: yes. Bank Select: not seen** — not even crossing a bank
  boundary (`PC 127` → `PC 0` with nothing between), although `00 00 0F` claims
  `BS` is enabled. **This observation has since been overturned**: the machine
  does transmit Bank Select. See
  [the correction below](#bank-select-is-transmitted--a-documented-conclusion-reversed).
  The most likely explanation for the August result is a reception problem on
  the ESP32 side, not machine behaviour.
- **About 95 % of the USB traffic is padding**: fixed-size transfers filled out
  with null USB-MIDI packets (code index number `0x0`). Filter them.

Also measured in that session, while building a display against the machine:

- **A Parameter Request round trip takes about 250 ms.** Fast enough that a
  cold-start fill of a display is a transition rather than a wait, and fast
  enough to follow preset scrolling at the knob with no perceptible lag.
- **The MIDI clock can drive a playhead.** Once `00 00 2D` is on, the position
  computes at 6 clock ticks per 16th step, and this was confirmed rendering on
  screen. The caveat is that each track has its own pattern length
  (`30 5p 16`-`20`), so a single global cursor is only correct when every track
  shares the master length.
- **Mute is readable per track** at `30 5p 29`, and **the selected pattern is
  broadcast** at `30 5p 0F` when it changes on the device (first seen
  2026-07-20 over BLE with SysEx transmission on).
- **The four effect knobs emitted Control Change (CC 102-115), not SysEx.**
  This sits awkwardly beside the October measurement, where Master Effect 3
  parameters *did* arrive as SysEx at `30 45 03` and `30 45 05`. Both readings
  are recorded; the disagreement is in
  [12-open-questions.md](12-open-questions.md). The safe design is to accept
  **either** voice as a trigger.

### Something confirmed absent

**A step's note length is not exposed anywhere reachable.** There is no
sequence-data block in the project dump, and nothing for it in
`Project Track General`. Two workarounds were considered: measure the
Note On → Note Off interval in the live stream while the sequencer plays, or
sweep `01 10 00`-`01 10 3F` while editing a step and watch for the offset that
moves. Neither has been tried.

This is a verified *absence*, which is worth as much as a verified presence: it
stops the next reader from searching for it. Note that the step-record read
path (`70 (40|tt) ss`, `verified on hardware` above) *does* return a gate time
— so the length of a step is reachable after all, just not through the project
dump. The absence applies to the bulk-dump route only.

## 2026-10-22, later session: re-typing a drum track works

The track-type change documented in [13-track-types.md](13-track-types.md) was
`from the official app, untested` when it was written. It has since
been exercised on the machine over USB, project 0, sequencer stopped, not
sampling, firmware read at `01 00 00` = 4194306 (`0x400002`).

```
sent      F0 43 10 7F 1C 0C 01 33 00 06 02 F7      part 6 → SYNTH
received  F0 43 10 7F 1C 0C 01 33 01 06 00 F7      ack, PartIndex 6, Result 0
```

What this establishes, all `verified on hardware`:

1. **`01 33 00` is the command and `01 33 01` is its acknowledgement.** The
   reply arrived in under 3 s with no retry.
2. **`Result = 0` is `Success`** — one value of the result table confirmed. The
   other seven remain inferred from the enum names.
3. **`type = 2` is SYNTH.** `PartAwmType` for part 6 (`01 16 3C`) went from
   **1** to **2**.
4. **The part travels in the data, not the address.** The other six parts
   (`01 10 3C` … `01 15 3C`) were read as witnesses and none moved.
5. **The sound is replaced, not kept.** `CurrentSound` for part 6
   (`01 16 33`) went from **456** to **4099**. 4099 is outside the range of
   drum sounds observed on parts 0-6 (2 … 553), so the firmware loads a default
   belonging to the synth space — that last step is an inference, the two
   readings are not.

   **Practical consequence: after converting a track, assign its sound
   explicitly.** Bank Select + Program Change on the part's own channel is the
   route that was later verified end to end; `01 1p 33` is the read-back. Do
   not rely on what was there.

Still not measured, and listed in
[12-open-questions.md](12-open-questions.md#track-types-and-song-mode--what-is-not-settled):
whether all six patterns are wiped or only the selected one (part 6 of project
0 held no known content to compare), what `Result` a refusal returns (none was
provoked), and what happens on a part ≥ 7 (not attempted).

> **Measurement chain.** Single session, single instrument, one machine. Point
> 4 is the strongest of the five because it used witnesses; points 1-3 and 5
> are single positive observations, which is what this repository's evidence
> rules ask to be said out loud. None of them is a negative claim.

## Writing a whole song — the sequencer, end to end

A complete 1320-note song was written into project 0 of a real unit and read
back: 11 parts, 41 patterns of 128 steps, 11 song-mode scenes. Everything in
this section is `verified on hardware` and detailed where it belongs — in
[04-sequencer-editing.md](04-sequencer-editing.md) and
[14-song-mode.md](14-song-mode.md). The register, shortest first:

| Finding | Where |
|---|---|
| Step record (`70`) answers **only on a part whose type is DRUM**; nothing on a re-typed part or on tracks 7-10 | [04](04-sequencer-editing.md#which-model-a-track-accepts-is-not-a-choice--it-follows-the-track-type) |
| The drum piano roll (`22`/`25`) answers for parts 0-6 and works on a re-typed part | [04](04-sequencer-editing.md#verified-on-hardware) |
| The synth piano roll (`72`/`75`) is indexed **locally 0-3**, not by global part number | [04](04-sequencer-editing.md#the-synth-block-is-indexed-locally-0-3) |
| A piano-roll instant holds **several notes** — the only route to a chord | [04](04-sequencer-editing.md#verified-on-hardware) |
| `eventTime = step × 120 + 60`; 60 is the neutral micro-timing, not an offset to ignore | [04](04-sequencer-editing.md#ticks) |
| `eventTime` is **not quantised** — 20-tick spacing inside one step survives | [04](04-sequencer-editing.md#verified-on-hardware) |
| `Pattern Select` silently clamps at 2 unless `Pattern Select Mode` (`30 40 79`) is 1 | [04](04-sequencer-editing.md#pattern-select-only-reaches-patterns-3-6-when-pattern-select-mode-is-1) |
| `DeletePattern` (`01 1p 37`) clears a pattern | [04](04-sequencer-editing.md#clearing-a-pattern) |
| `AddScene` / `RemoveScene` take the scene number **in the data** | [14](14-song-mode.md#addscene-and-removescene-settled-on-hardware) |
| Scene Info is 33 bytes: patterns at 2-12, mutes at **14**-24 | [14](14-song-mode.md#what-a-scene-info-reply-contains) |
| `CurrentSound` = catalogue number − 1, confirmed by writing 10 presets | [06](06-sounds-presets.md#reading-back-which-sound-is-loaded) |
| 1320 messages at 2 ms with no loss | [14](14-song-mode.md#7-what-to-test-on-hardware-in-order) |

> **Measurement chain.** One machine, one session, one instrument — a Python
> script over USB MIDI reading every address back with retries. Each positive
> claim above is a write followed by a read that returned the written value.
>
> The two claims that are **negative** in form — that `70` does not answer on
> non-DRUM tracks, and that `75` does not answer above n = 3 — were not taken
> from a single silence. Each was a sweep over several addresses with repeated
> attempts, run in the same loop as tracks that *did* answer, so a dead link or
> a dropped reply would have shown up as silence everywhere. That is the
> minimum this repository's rule 4 asks for. It is still weaker than a
> cumulative counter over the whole stream, and it does not exclude some other
> precondition making those addresses answer in another state.
>
> One claim in this register was **wrong on the first measurement and caught by
> read-back**: patterns written to slots 3 and 4 had all landed on slot 2. The
> write reported nothing unusual. That is the case for always reading back.

## 2026-10-22, hardware session: `01 1p 3C` answers, for every part

[13-track-types.md](13-track-types.md#6-partawmtype-01-1p-3c-is-state-not-the-command)
described `PartAwmType` as the address the app reads at startup to learn each
track's type, but the address had never been queried: it was not among the 33
probed in the first session. The iOS client reads it on every connection, so
whether it answers at all decided whether that read ever returns.

**It answers, and it never dropped once.** Four Parameter Requests per address,
eleven addresses, with the tempo (`30 40 76`) read as a live control after every
target so that a silent machine could not be mistaken for a silent address:

```
44/44 target replies, 44/44 control replies
```

| Part | Address | Value | The track on that part |
|---|---|---|---|
| 0 | `01 10 3C` | `01` | KICK — a drum track |
| 1 | `01 11 3C` | `01` | HATC — a drum track |
| 2 | `01 12 3C` | `01` | HATO — a drum track |
| 3-6 | `01 13 3C` … `01 16 3C` | `02` | drum tracks re-typed to SYNTH earlier the same day |
| 7 | `01 17 3C` | `02` | SYNTH 1, a native synth track |
| 8 | `01 18 3C` | `02` | SYNTH 2, a native synth track |
| 9 | `01 19 3C` | `04` | DX, the FM track |
| 10 | `01 1A 3C` | `05` | SAMPLER |

All `verified on hardware`. Machine state: firmware `02 00 00 02`, project 0,
sequencer stopped, tempo 123 BPM.

### Two things this settles

**1. The address exists beyond parts 0-6.** The app only ever installs
`PartAwmType` streams for parts 0-6 — `AwmTrackManager.SetupModelStreamsForMidi`
iterates `Enumerable.Range(0, 7)`, and `ParameterModel.GetAwmTrackType` rejects
an index ≥ 7. That is a property of the app, not of the firmware: parts 7-10
answer the same request perfectly well. A client is free to read them.

**2. Values `04` and `05` are real, and the machine emits them.** This matters
because it closes a question that
[13-track-types.md](13-track-types.md#decoding-the-value) left open with an
explicit warning that it was **not** a fact:

> One hypothesis, **not a fact**: 4 and 5 might stand for the non-AWM engines
> (DX, sampler) seen from the PCApp address space […]

The DX track reads `04` and the sampler track reads `05`. Since the part
numbering is itself `verified on hardware` (drums 0-6, SYNTH 1 = 7,
SYNTH 2 = 8, DX = 9, SAMPLER = 10), those two readings are measurements, not
interpretations.

**What is measured**: the eleven values above, and that `04` and `05` are
values the firmware really reports.
**What is inferred**: that `PartAwmType` is best read as *the engine backing the
part*, of which only `1`, `2` and `3` are valid targets for a re-type. That
reading fits every value observed, but no gesture has yet been made to test it —
for instance by watching the address on part 10 while the sampler track changes
state. Treat it as the leading reading, not as established.

### A consequence for clients decoding this address

The app's receive-side decoder maps the value through
`w8 = (value - 1) & 0xFF ; if w8 >= 3 then Void`, so `00`, `04` and `05` all
become `Void`. It is tempting to read that as "0-5 is just the factory's
declared bound, and only 1-3 are meaningful values". **That reading is now too
strong.** `04` and `05` are values the hardware actually sends, on two of the
eleven parts, every time they are asked.

So `Void` in the app means *"not a track I can re-type"*, which is correct
behaviour for the DX and sampler tracks — it does not mean *"not a value the
machine produces"*. A client that treats `04`/`05` as an invalid or unknown
encoding, rather than as the FM and sampler engines, will discard a valid
reading on parts 9 and 10. Any decoder returning `nil` or an error for those two
values is rejecting normal traffic.

> **Measurement chain.** One machine, one session, one instrument: a Python
> script over USB MIDI
> ([`probe_awmtype.py`](../tools/hardware-probe/probe_awmtype.py)) issuing four
> Parameter Requests per address with a known-good control address interleaved
> after every target. Every claim above is positive in form — an address was
> asked and a value came back — so none of them rests on an absence. The
> control answered 44 times out of 44, so no target silence had to be
> interpreted at all.

## 2026-10-22, hardware session: types `01` and `03` on the wire

Until now only `type = 02` (SYNTH) had ever been sent to a machine. The other
two values of the re-typing command were `from the official app,
untested`, and the enum's own trap — the UI order being DRUM, DrumKit, SYNTH
while the wire order is DRUM, SYNTH, DrumKit — meant a wrong guess would have
produced a drum kit where a synth was wanted, silently.

Both remaining types were sent to part 2 of project 0 (HATO, an open-hat drum
track, deliberately sacrificed; the song it belonged to is regenerable from
source). Sequencer stopped (`01 10 20` = `00`), not in Song mode
(`01 10 17` = `00`), the other six drum parts read before and after as
witnesses.

### `type = 03` → DRUMKIT

```
sent      F0 43 10 7F 1C 0C 01 33 00 02 03 F7
ack       F0 43 10 7F 1C 0C 01 33 01 02 00 F7     part 2, Result 0 (Success), 0.38 s
read-back F0 43 30 7F 1C 0C 01 12 3C F7  ->  03
```

### `type = 01` → DRUM

```
sent      F0 43 10 7F 1C 0C 01 33 00 02 01 F7
ack       F0 43 10 7F 1C 0C 01 33 01 02 00 F7     part 2, Result 0 (Success), 0.12 s
read-back 01 12 3C  ->  01
```

All `verified on hardware`:

1. **The three-value encoding is complete and correct on the wire**: `01` DRUM,
   `02` SYNTH, `03` DRUMKIT. Each was asked for and each was read back as the
   value asked for. The UI/wire mismatch is confirmed as a real hazard rather
   than a reading of the official app.
2. **`Result = 0` on both**, so `Success` now has three observations behind it
   instead of one. The other seven result codes remain inferred from enum names
   — still no refusal has been provoked.
3. **The acknowledgement is prompt**: 0.38 s and 0.12 s, no retry needed.
4. **The change is localised.** The other six drum parts were re-read after each
   change and none moved.
5. **A part can be round-tripped.** `01` → `03` → `01` returned part 2 to the
   type it started at, so the command is not one-way.

### Both `01 33 00` and `01 33 01` travel machine → host

> **This corrects a claim written earlier in this same session.** An earlier
> revision of this section said "`01 33 00` is never echoed back — `verified on
> hardware`". **That was wrong**, and it was wrong in this repository's
> signature way: the evidence was two host-sent changes that produced no echo,
> plus a 60-second window that contained **no front-panel gesture at all** — it
> received zero SysEx of any kind and the track's type never moved. A window in
> which the thing never happened cannot show what the thing emits. The claim
> was a negative resting on an instrument that had nothing to observe. See
> [evidence discipline](../AGENTS.md), rule 4.

With the gesture actually performed, the picture is the opposite.

**Host-originated change** (`01 33 00` sent from the computer): the machine
replies with `01 33 01` only. No echo of the command. Two for two.

**Front-panel-originated change**: the machine sends **both**, unprompted. Part
2 was re-typed to Synth from the front panel (hold the CLAP track knob, hold
Drum key 11 for five seconds) while the host sent **nothing at all**:

```
received  F0 43 10 7F 1C 0C 01 33 00 02 02 F7     the command form: part 2, type 02
received  F0 43 10 7F 1C 0C 01 33 01 02 00 F7     the acknowledge: part 2, Result 0
received  F0 43 10 7F 1C 0C 01 12 3C 02 F7        PartAwmType pushed as state
```

Twelve SysEx messages arrived in that window, at seven addresses, with nothing
requested:

| Address | Values | What it is |
|---|---|---|
| `01 10 27` | `02` | `CurrentPart` — selecting the CLAP track |
| `01 33 00` | `02 02` | **the change command, emitted by the machine** |
| `01 33 01` | `02 00` | the acknowledgement, part 2, Success |
| `01 12 3C` | `02` | `PartAwmType` for part 2, pushed as state |
| `01 12 39` | `01 00`, `01 01` | `PatternKnobMode`, two data bytes |
| `01 10 2E` | `01`, `3A`, `3B` | `ParameterLedMode` following the LED display |
| `01 10 18` | `00`, `02` | `DrumPadMode` |

Read-back afterwards: `01 12 3C` = `02`, up from `01`. The type really changed.

**Three things this settles**, all `verified on hardware`:

1. **`01 33 01` does arrive spontaneously.** A host does not have to send
   anything to learn that a track was re-typed on the machine. Cache
   invalidation keyed on this message works.
2. **`01 33 00` is bidirectional.** It is the command form in *both*
   directions, not a host-only message. This independently confirms a reading
   taken from the official app, which has a receive filter that
   matches `01 33 00` *arriving from the machine* — a handler that would have
   looked like dead code under the earlier, wrong claim.
3. **`01 1p 3C` is broadcast on change**, not merely readable. A client can
   follow track types passively.

**Consequence for a client:** a receive path **must** decode `01 33 00`, and it
must not assume that a message at that address came from another host on the
link. It may well be the machine reporting what its own user just did.

> **Measurement chain.** One machine, one session, one instrument: a Python
> script over USB MIDI
> ([`retype_part2.py`](../tools/hardware-probe/retype_part2.py)) that keeps
> every inbound SysEx in a list for the whole run — nothing is consumed or
> pruned between phases — and re-reads the target plus six witness parts around
> each change. The restore sits in a `finally`.
>
> **The pattern deletion was not measured.** Part 2's patterns were destroyed
> as expected, but no before/after step scan was taken, so this session adds
> nothing to the open question of whether all six patterns are wiped or only
> the selected one.

## 2026-10-22, hardware session: the SEQTRAK does not send `F2` over USB

**Song Position Pointer is never transmitted.** An external display therefore
cannot read the sequencer's position off the wire; it has to count clocks.

This is a **negative claim**, the kind this repository has got wrong twice, so
the instrument comes first.

### The instrument

[`listen_counter.py`](../tools/hardware-probe/listen_counter.py) counts every
inbound message **cumulatively, per status byte**, for the whole run. The
documented run was:

```bash
python3 tools/hardware-probe/listen_counter.py --cues --timeline
```

`--cues` walks the operator through the gesture list that the totals below
cover. Nothing
scrolls, nothing is sampled, nothing is pruned: the totals at the end cover
every byte that arrived.

It carries its own **positive control**. Before listening to the machine it
opens a virtual CoreMIDI port, pushes four `F2` messages and one `F8` through
it into the same callback and the same counting function, and refuses to claim
anything if they are not all counted:

```
F2 injected: 4, F2 counted: 4   |   F8 injected: 1, counted: 1
  decoded SPP position=0     from F2 00 00
  decoded SPP position=1     from F2 01 00
  decoded SPP position=384   from F2 00 03
  decoded SPP position=16383 from F2 7F 7F
control PASSED
```

So a count of zero afterwards means *absent from the stream*, not *invisible to
the instrument*. `rtmidi` was opened with `ignore_types(sysex=False,
timing=False, active_sense=False)` — nothing filtered.

**The limit of that control, stated rather than glossed.** The injection enters
through a *virtual* port, not the SEQTRAK's port: two distinct CoreMIDI sources
and two distinct `MidiIn` instances, configured identically. So the control
establishes "this code, with these flags, counts an `F2` arriving from a
CoreMIDI source", not "counts an `F2` arriving from the SEQTRAK's port
specifically". CoreMIDI does not filter by source, so the gap is narrow, but it
is real. What closes it in practice is the run itself: on that same SEQTRAK
port, in the same pass, `FA`, `FC`, `F8` and `FE` were all counted — so the
path carrying system bytes from the machine into this counter was demonstrably
working while `F2` stayed at zero.

### The transmit gates were open

Every switch that could have suppressed it was read first, four attempts each,
with the tempo interleaved as a live control:

| Address | Parameter | Value |
|---|---|---|
| `00 00 2B` | Transmit Sequencer Control | `01` — **on** |
| `00 00 2D` | MIDI Clock Out | `01` — on |
| `00 00 0E` | USB MIDI Transmit Channel Message | `01` — on |
| `00 00 10` | USB MIDI Transmit System Exclusive | `01` — on |
| `00 00 23` | USB To Host MIDI Thru | `03` — Both |

### The run

108.1 s, **6656 messages**, gestures called out one at a time and performed by
the owner on the machine:

| Status | Name | Count |
|---|---|---|
| `80` | Note Off | 409 |
| `90` | Note On | 409 |
| `F0` | SysEx | 84 |
| `F8` | Timing Clock | 5316 |
| `FA` | **Start** | 4 |
| `FC` | **Stop** | 4 |
| `FE` | Active Sensing | 430 |
| **`F2`** | **Song Position Pointer** | **0** |
| `F3` | Song Select | 0 |
| `F1` | MTC quarter frame | 0 |

Gestures covered: the `[⏻/PLAY]` toggle four times; pattern changes with the
sequencer stopped **and** while playing; entering and leaving Song mode three
times; scene changes; and playback inside Song mode with a scene change
arriving on its own.

**`FA` and `FC` are the counter-evidence that matters.** Start and Stop are
System messages on the same path to the host, and they arrived, four of each,
timestamped against the transport gestures. The route is demonstrably open. The
machine simply never puts an `F2` on it.

### What this does and does not establish

**Established**: over USB MIDI, with every transmit gate on, across transport
toggles, pattern changes in both transport states, Song-mode entry and exit,
scene changes and song playback, the SEQTRAK emitted zero Song Position
Pointers in 108 s and 6656 messages, measured by a cumulative counter whose
ability to see `F2` was proven in the same run.

**Not established**: behaviour over TRS MIDI or BLE (not measured); behaviour
while slaved to an external clock, which is the one state where a device most
often emits SPP and which was not exercised; and whether some setting reachable
only from the official app gates it. `F2` appears nowhere in the User Guide and
there is no transmit flag for it in the parameter tables.

**Consequence for a display.** Position must be derived by counting `F8`
against each track's own pattern length. `FA`/`FC` give the transport edges and
`01 10 20` confirms them in SysEx, but nothing announces an absolute position —
so after a pattern change or a scene change a clock-counting display has no way
to resynchronise its bar position from the machine.

## 2026-10-22: live-state addresses confirmed by the same gestures

The 108-second run above also attributed six broadcast addresses to gestures,
because each burst was identified by its content. All `verified on hardware`
as **observed values**; the semantics marked *inferred* were not isolated with
witnesses.

| Address | Parameter | Observed | Status |
|---|---|---|---|
| `01 10 17` | `GeneralMode` | `00` outside Song mode, `02` inside, over **three** entries and three exits | was `from the official app, untested`; the two values are now measured, the reading "2 = Song mode" is inferred from the gesture it accompanied |
| `01 10 18` | `DrumPadMode` | `00` outside Song mode, `13` (19) inside | same standing: values measured, meaning inferred |
| `01 10 20` | `SequencerStatus` | `01` / `00`, alongside `FA` / `FC` each time | already verified; confirmed again, 8 transitions |
| `30 5p 0F` | Pattern select, part 7 | `00` … `05` — the **whole** 0-5 range on the wire | confirms patterns are 0-based on the wire and that all six slots are reachable |
| `71 10 04` | `CurrentScene` | `02` | reachable and broadcast |
| `71 50 00` | `ChangeSceneMode` | pulses `01` then back to `00` on each scene change | it is a momentary flag, not a persistent mode |

### `01 10 2D` answers with one byte but broadcasts two

Worth flagging because it breaks the assumption that an address has one width.

- A **Parameter Request** for `01 10 2D` replies with **1 data byte** (`00`).
- The machine **broadcasts** the same address with **2 data bytes**, observed
  18 times, alternating `04 04` and `01 01`.

The extraction declares `MasterKnobMode` as size 2, range 0-16262, so the
two-byte broadcast matches the declared width and the one-byte reply does not.
Whether the reply is truncated when the value is small, or the two forms carry
different things, is **not settled** — added to
[12-open-questions.md](12-open-questions.md).


## 2026-10-22, hardware session: the BLE link measured

A macOS CoreBluetooth central was connected to the machine directly, so that
the negotiated MTU and the raw notification packets could be read before any
MIDI layer touched them. Device advertised as **`SEQTRAK_53B17B`**, confirming
the `SEQTRAK_` + six characters form, at RSSI −43 dB.

> **Running this needs the Terminal, not a Bash tool call.** macOS TCC kills a
> CoreBluetooth process that has no Bluetooth usage description attributable to
> it: the Swift interpreter aborts with
> `__TCC_CRASHING_DUE_TO_PRIVACY_VIOLATION__`, and so does a compiled binary
> with an embedded `__info_plist`, ad-hoc signed or not, when it is launched
> from a sandboxed tool. Launched from the user's own Terminal the same binary
> reaches `poweredOn` immediately.

### The negotiated write ceiling — `verified on hardware`

| What | Value |
|---|---|
| `maximumWriteValueLength(.withoutResponse)` | **20 bytes** |
| Implied negotiated ATT MTU | **23 bytes** — the BLE minimum, never upgraded |
| `maximumWriteValueLength(.withResponse)` | 512 bytes |
| Characteristic properties | `notify`, `writeWithoutResponse`, `read` |

**The real ceiling is 20 bytes per packet.** The 512 figure is CoreBluetooth's
queued-write maximum and is not usable here, because the characteristic **does
not advertise `.write`** at all — only `writeWithoutResponse`. This repository
previously described the properties as "notify (subscribe for input), write or
write-without-response (for output)"; on this unit there is no plain `write`
property, so the choice does not exist and `.withoutResponse` is the only path.

After the 1-byte header and a 1-byte timestamp, **18 bytes of MIDI fit in one
packet**. A Parameter Change (`F0 43 10 7F 1C 0C ah am al dd F7`, 11 bytes)
fits; a bulk dump does not, and must be fragmented.

Reconnection behaved as the documentation says: the second run rediscovered the
peripheral by service scan within a second, with no new pairing gesture.

### Framing confirmed on real traffic — `verified on hardware`

The corrected framing in [§BLE MIDI packet framing](#ble-midi-packet-framing)
holds. Two messages in one packet, each with its **own one-byte** interleaved
timestamp:

```
B0 9C B2 00 3F 9C B2 20 01
│  │  └──────┘ │  └──────┘
│  │  CC 0 =63 │  CC 32 = 1
│  │           └─ timestamp, ONE byte
│  └─ timestamp, ONE byte
└─ header
```

```
B1 94 C2 7B 94 F8
      └──┘    └─ Timing Clock, after its own timestamp
      PC 121
```

So the one-byte interleaved timestamp is real, and a running timestamp of two
bytes would have mis-parsed this traffic. **Bank Select is transmitted over BLE
too**: `CC 0 = 63`, `CC 32 = 1`, then `Program Change 121`, on channel 3 — the
same triplet already verified over USB.

### The `F7` terminator **is** timestamped — `verified on hardware`

This was the point of the capture: the machine was suspected of emitting an
**un-timestamped `F7`**, the form that broke an earlier decoder. **It does not.**

A Parameter Request for the tempo was written to the characteristic over BLE,
and the reply came back as a single packet:

```
B1 89 F0 43 10 7F 1C 0C 30 40 76 00 7B 89 F7
│  │  └──────────────── SysEx ───────────┘ │  │
│  │                                        │  └─ F7, the terminator
│  │                                        └─ timestamp 0x89, immediately before it
│  └─ timestamp 0x89
└─ header 0xB1
```

A second message arrived unprompted in the same window:

```
B2 B7 F0 43 10 7F 1C 0C 01 10 2E 01 B7 F7      ParameterLedMode = 01
```

**Both `F7` bytes are preceded by their own one-byte timestamp. Two out of
two, zero un-timestamped.** The timestamp before `F7` repeats the value used at
the start of the message (`89`…`89`, `B7`…`B7`), i.e. the same millisecond. So
the machine follows the MMA framing, and a decoder **must** expect a timestamp
in front of the terminator rather than treating `F7` as reachable directly.

Note also that the tempo reply decodes to `00 7B` = **123 BPM**, the same value
read over USB — so a Parameter Request works over BLE, reply included.

### SysEx does cross the BLE link — correcting this section's first draft

> **An earlier revision of this section, written minutes before, was headed
> "No SysEx crossed the BLE link".** That was drawn from a single 50-second
> window of knob and sound gestures in which 2853 packets contained zero `F0`
> bytes while CC and Program Change arrived normally. The observation is real,
> but the heading generalised it into a property of the transport, and the very
> next capture disproved that: two SysEx messages, one a request reply and one
> a spontaneous `01 10 2E` broadcast.

What stands after both captures:

| Observation | Status |
|---|---|
| A Parameter Request over BLE gets a SysEx reply | `verified on hardware` |
| The machine sends *some* SysEx spontaneously over BLE (`01 10 2E`) | `verified on hardware` |
| A 50 s window of knob sweeps and sound changes produced CC and PC but **no** SysEx, where the same gestures over USB produce SysEx at the real parameter address *as well as* CC | observed once, **unexplained** |

The last row is an open question, not a conclusion about the flags
(`00 00 12` = `01`, `00 00 13` = `70`, `00 00 14` = `01` throughout). It may be
that knob-move parameter broadcasts are not mirrored to Bluetooth, or that
those particular gestures did not produce them. **One window is not enough to
say which**, and this document is not going to guess a second time.

### `00 00 11` = `00` does not mean Bluetooth MIDI is off

While the BLE link was established and carrying Control Change, Program Change,
SysEx, clock and active sensing, `00 00 11` (`BluetoothMidiInOut`) was read over
USB four times and returned **`00`** every time. An earlier revision of this
repository, written hours before, called it "the master switch" and said it was
the one thing that had to be turned on. **That reading is contradicted.** What
the address actually reports is unknown, and it is in
[12-open-questions.md](12-open-questions.md).

> **A warning about the obvious instrument.** A first pass scanned each packet
> for bytes `>= 0xF0` and reported "42 un-timestamped `F7`". **That was an
> artifact, not a finding** — and it pointed the wrong way on the one question
> the capture existed to answer. An interleaved timestamp is
> `0x80 | (time & 0x7F)` and therefore takes the values `F1 F3 F5 F7 F9 FB FD
> FF` routinely: in `88 8A F7 F8` the `F7` is a timestamp, not an EOX. **Any
> byte-level scan of a BLE-MIDI packet will invent SysEx terminators.** Only a
> parser that tracks position in the packet and SysEx state across packets can
> answer the question; [`ble_parse.py`](../tools/hardware-probe/ble_parse.py)
> does, and it found the truth to be the exact opposite of the artifact.

> **Measurement chain.** One machine, one session. A Swift CoreBluetooth
> central ([`ble_trace.swift`](../tools/hardware-probe/ble_trace.swift))
> recording every notification packet to a file, parsed afterwards by
> [`ble_parse.py`](../tools/hardware-probe/ble_parse.py). The MTU is read from
> the connection and needs no traffic, so it is the strongest result here. The
> `F7` result is positive in form: two terminators were captured and both were
> timestamped. Two observations is thin, but it is two more than the zero this
> question had before, and it is enough to retire the un-timestamped-`F7`
> hypothesis as a description of what this machine emits.

## 2026-10-22: the `30` block is per-project — and a project switch does **not** persist

Yamaha's *User Guide* §4.2 says "Projects are saved automatically when SEQTRAK
is turned off or when switching projects." That had never been tested, and a
sibling session had reached the opposite assumption — that a project switch
would discard the edit buffer and lose an unsaved song. **The guide is right.**

Method ([`test_edit_buffer.py`](../tools/hardware-probe/test_edit_buffer.py)),
following the systematic re-read rule in
[14-song-mode.md](14-song-mode.md#re-read-the-whole-state-and-compare-it-rather-than-picking-a-witness)
rather than choosing a witness: write a distinctive marker, snapshot **28
addresses** before and after, diff them, and confirm `01 10 15` at every step.

```
project 0, Tempo 30 40 76       00 7B  (123 BPM)   -> wrote 01 47  (199 BPM)
project 0, ScalePad1 30 4D 00   3C     (note 60)   -> wrote 43     (note 67)
  both read back as written

switch to project 7   (Bank MSB 64, LSB 0, Program 7)
  01 10 15 = 7
  Tempo there      = 00 61  (97 BPM)   <- project 7's own tempo
  ScalePad1 there  = 3C     (note 60)  <- NOT project 0's 43

switch back to project 0
  01 10 15 = 0
  diff of all 28 addresses, before-switch vs after-switch:  NOTHING MOVED
  Tempo     = 01 47   the marker survived
  ScalePad1 = 43      the marker survived
```

### Three results, all `verified on hardware`

**1. A project switch preserves the live state — but this does not show it was
saved.** Both markers survived the round trip, and so did the other 26
addresses, so nothing is *lost* by switching. That much stands.

> **This section first concluded "switching projects saves the outgoing
> project", and that was wrong.** The test cannot distinguish the two
> explanations: the state was written out and read back, *or* project 0's edit
> buffer simply never left RAM during a 0 → 7 → 0 round trip. A value that
> survives without the machine ever losing power is evidence of neither.
>
> The [forced-termination test](#the-forced-termination-discards--and-it-caught-the-flaw-above)
> run afterwards settles it against the first reading: at that point the last
> project switch had, on the "it saves" theory, committed 123 BPM — yet the
> machine came back on 181 BPM, the value written before the previous *power
> off*. So the project switch did not write to the store that survives a
> forced termination.
>
> Yamaha §4.2's wording ("saved … when switching projects") is therefore **not
> confirmed** by this test, and is contradicted on the only reading that would
> make it useful to a client. It is possible that "saved" means a weaker tier
> than the one a power-off writes; nothing here establishes which.

**2. Project selection by Bank Select + Program Change works.** `Bank MSB 64`,
`LSB 0`, `Program n` moved the machine to project 7 and back, confirmed by
`01 10 15` each time. That row of the table in
[06-sounds-presets.md](06-sounds-presets.md#bank-select-and-program-change) was
`from Yamaha Data List`; it is now measured.

**3. The `30 xx xx` block is per-project, user scales included.** This is the
unplanned finding, and the more useful one. Project 7's tempo read `00 61`
where project 0's read `01 47`, and — less obviously — **`30 4D 00` read `3C`
in project 7 while project 0 held `43`**. The user scales are therefore *not*
global settings: each project carries its own eight scales.

> **This corrects an assumption in the test's own script**, which printed
> "same value => the zone is global" on the basis that a scale pad would be
> system-wide. The values proved otherwise. A client that reads or restores
> user scales must know which project is current — the same precondition
> [14-song-mode.md](14-song-mode.md) states for pattern writes applies to the
> `30` block as a whole.

### And a normal power-off saves too — `verified on hardware`

§4.2 names two moments. The project switch above was the first; this is the
second. Same method, split across the power cycle because the USB port goes
away with the machine
([`test_power_off.py`](../tools/hardware-probe/test_power_off.py), phases 1
and 2).

```
project 0  Tempo 30 40 76      00 7B  (123 BPM)  -> wrote 01 35  (181 BPM)
           ScalePad1 30 4D 00  3C     (note 60)  -> wrote 47     (note 71)
  both read back as written, 27 addresses snapshotted to disk

[power/PLAY] held 2 s -> off -> held 2 s -> on      (guide 3.2.1)

  diff of all 27 addresses, before power-off vs after power-on: NOTHING MOVED
  Tempo     = 01 35   survived
  ScalePad1 = 47      survived
```

**Both markers survived, and so did everything else** — `CurrentPart`,
`GeneralMode`, each part's `PatternSelect`, every `PartAwmType`,
`PatternSelectMode`. The machine comes back on the state it was switched off
in, not on a default.

### The forced termination discards — and it caught the flaw above

`verified on hardware`, and the most instructive result of the session because
it invalidated an earlier conclusion of the same session rather than adding to
it.

§3.2.2: holding `[⏻/PLAY]` **and** `[PROJECT↑]` together switches the machine
off, and "any changes that were made after SEQTRAK was started and before
forced termination will not be saved."

Method ([`test_forced_term.py`](../tools/hardware-probe/test_forced_term.py)):
pin a baseline, write a marker over it, force-terminate, read back.

```
live state                       Tempo 00 7B (123 BPM)   ScalePad1 3C (note 60)
"baseline pinned" by a project round trip 0 -> 7 -> 0, re-read as 00 7B / 3C
marker written over it           Tempo 01 21 (161 BPM)   ScalePad1 4A (note 74)

[power/PLAY] + [PROJECT up] held together -> off -> normal power-on

  Tempo     = 01 35  (181 BPM)
  ScalePad1 = 47     (note 71)
```

**Neither the marker nor the pinned baseline.** `01 35` and `47` are the values
written before the *previous normal power-off*, two tests earlier. The machine
reverted past the baseline, to the last state a power-off had written.

Two things follow.

1. **The forced termination does discard post-startup edits.** §3.2.2 is
   confirmed: the 161 BPM marker, written after startup, is gone.
2. **The project round trip did not commit anything.** Had it done so, 123 BPM
   would have come back. This is what retires the earlier "switching projects
   saves" conclusion, and the mechanism is now clear: that test watched a value
   survive while the machine never lost power, which proves only that the value
   stayed in memory.

> **The flaw was in my own instrument, and it was invisible from inside the
> test.** Pinning a baseline with a project round trip assumed the very thing
> under investigation. A value re-read as unchanged after the round trip looked
> like confirmation that it had been committed; it was just the same RAM. The
> forced termination is what exposed it, because it is the only gesture that
> throws uncommitted state away.
>
> **So the forced termination is the right instrument for any "did this
> persist?" question on this machine.** The protocol: write the marker, perform
> the gesture whose durability you are testing, force-terminate, power on, read
> back. Marker present → the gesture persisted it. Marker gone → it did not. A
> normal power-off cannot be used for this, because it saves on its own and
> would report success for any gesture at all.

**Practical consequence, and the one that matters.** The 1320-note song in
project 0 survived all of this — part 0 still reads its sixteen steps on the
four-on-the-floor grid, checked after both power cycles. It was persisted by
the **normal power-off**, not by any project switch. A client that tells a user
their work is safe because the machine changed project is, on this evidence,
wrong.

### The three power-off paths are not equivalent

`from Yamaha Data List`, and worth having in one table because only one of the
three is safe for unsaved work and the names do not make that obvious:

| Path | Gesture | Saves? |
|---|---|---|
| **Normal power-off** (§3.2.1) | hold `[⏻/PLAY]` **2 s or longer** | **Yes** — `verified on hardware`, above |
| **Auto Power Off** (§3.2.3) | 30 minutes idle, when not charging | Yes — "the current project will be saved automatically". Untested. Disabled or re-enabled by holding the lower-left Drum key while switching on |
| **Forced termination** (§3.2.2) | hold `[⏻/PLAY]` **+ `[PROJECT↑]`** | **No** — `verified on hardware`: a marker written after startup was gone, and the machine reverted to the last power-off state |

So the equivalent of pulling the plug is a documented *button combination*, not
an accident. **A client that tells a user "your edits are safe, just switch
off" is right for §3.2.1 and wrong for §3.2.2**, and the two gestures differ by
one extra button.

All three are now accounted for: the normal power-off persists (measured), the
forced termination discards (measured), and Auto Power Off claims to save but
has not been tested. The project switch, despite §4.2, is **not** a save — see
the correction above.

### One address that did not answer

`01 1A 33` (`CurrentSound` for part 10, the sampler) returned nothing on four
attempts, in all three snapshots, while `01 10 33` and `01 17 33` answered
every time in the same loops. Per this repository's standing rule that is **not
yet evidence** of anything — but it is a reproducible non-answer with live
controls beside it, which is the shape worth chasing. Added to
[12-open-questions.md](12-open-questions.md).

> **Measurement chain.** One machine, one session, one instrument: a Python
> script over USB MIDI re-reading 28 addresses into a dict at three points and
> diffing them, with the project switch behind a human prompt and the marker
> restore in a `finally`. The decisive result is a **positive**: a value
> written before the switch was read back after it. The per-project scoping of
> `30 4D 00` rests on two readings in two projects, which is thinner — it
> shows the value did not follow the machine across the switch, not yet how
> many scales each project carries.

## The firmware space `0x64` — silent, and that was measured

`verified on hardware`. Two read-only sessions asked whether the firmware-update
address space is reachable outside an update. It is not, in either mode, and the
negative is instrumented rather than assumed: a `FirmwareVersion` control at
`01 00 00` sat in the same loop and answered.

| Mode | Addresses probed | Attempts | Replies | Control in the same loop |
|---|---|---|---|---|
| normal | `64 00 00`, `64 01 00`, `64 02 00`, `64 06 00` | 24 (6 loops × 4) | **0** | 5 / 6 |
| loader | `0x64` read sweep | 12 | **0** | — |

Two further results from the loader-mode run:

- the loader answers the Universal Identity Request with
  `F0 7E 7F 06 02 43 00 41 64 06 00 00 01 7F F7`, byte 11 `00` against `0A` in
  normal mode — the cheap way to confirm which mode the machine is in;
- **entering and leaving loader mode was reversible**: normal → loader →
  identity → reboot → normal, machine back to its initial state, nothing
  written.

> **Measurement chain.** One machine, two read-only sessions, a Python script
> over USB MIDI. The normal-mode negative is sound: the control proves the link
> was live while `0x64` stayed silent, which is exactly what this repository
> asks of a negative claim. The loader-mode negative carries a reserve — the
> `change-mode` was never acknowledged on that run, so the silence may be
> gated rather than absolute. Recorded in
> [12-open-questions.md](12-open-questions.md#firmware); the full write-up is in
> [09-firmware.md](09-firmware.md#what-the-hardware-has-actually-said-about-0x64).

## 2026-10-22, hardware session: writing a whole palette into a slot

`verified on hardware`. A complete project palette — eleven preset sounds, their
shaping, the send and master effects, a user scale, a key and a tempo, and
**no notes** — was written into project slot 0 over USB MIDI and read back
address by address. 82 of the 83 verified addresses matched the source palette;
the one that did not is the SAMPLER part, below.

Driven by `seqtrak-generator/generate.py` and checked by a separate
`seqtrak-generator/verify.py` process that reads every written address back and
compares it to the palette file — not a scrolling log.

### A preset load is not ordered against the Parameter Changes that follow it

The first run loaded each part's preset with Bank Select MSB/LSB plus a Program
Change, waited 20 ms, then wrote that part's `31 1p` sound parameters, one pass
per part. Read-back afterwards:

| Parts | Symptom | `01 1p 33` read | expected |
|---|---|---|---|
| 0, 2, 6, 9 | correct | correct | correct |
| 1, 5, 8 | right sound, **shaping lost** — Volume and both sends back at the preset's own values | correct | correct |
| 3 | **wrong sound** | 882 | 355 |
| 4 | **wrong sound** | 1587 | 384 |
| 7 | **wrong sound** | 954 | 907 |

The second and third runs sent all eleven Program Changes first, each followed
by 250 ms and a `01 1p 33` read-back before moving on, and only then wrote the
`31 1p` parameters in a second pass. **Eleven of eleven confirmed on the first
attempt, on both runs**, and every shaping value survived.

So the remedy is established: **load every preset first, confirm each part's
`01 1p 33`, and shape afterwards.** The **mechanism is not**. A timing race
accounts cleanly for the lost shaping on parts 1, 5 and 8 — the preset finishes
loading after the parameter writes and overwrites them — but not for parts 3, 4
and 7 landing on a *different sound*, and the three wrong values share no
constant offset with the intended ones. See
[12-open-questions.md](12-open-questions.md).

### Master Effect 1-4 are address-mid `0x43`-`0x46`, and an undefined address swallows writes in silence

The same run first sent the four master-effect blocks to address-mid `03`-`06`,
using the master-effect *ordinal* instead of the composed mid byte
(`0x40 | (2 + n)`). There was no error and no effect. Those four addresses
answered **0 of 16** Parameter Requests across two runs, while `30 41 00`,
`30 42 00` and the tempo control at `30 40 76` answered in the same passes.

Re-sent to the composed addresses, one at a time, every type read back exactly:

| Address | Written | Read back |
|---|---|---|
| `30 43 00` | `0C 28` CONTROL FILTER | `0C 28` |
| `30 44 00` | `02 10` TEMPO CROSS DELAY | `02 10` |
| `30 45 00` | `0C 70` VINYL BREAK | `0C 70` |
| `30 46 00` | `08 00` VCM COMPRESSOR 376 | `08 00` |

Two things follow. The composition rule for master effects is confirmed by a
write, not only by traffic. And **an address outside the documented map accepts
a Parameter Change without complaint and answers no Parameter Request** — so a
silent write is not evidence that an address exists.

### Bank MSB 62 did not load a preset SAMPLER element, from either channel tried

`verified on hardware`, with witnesses. Part 10's sound name was read out of the
`31 0A 00` block of a single-track bulk dump (`11 02 0A`).

| Step | Sent | Part 10 `31 0A 00` name | Witness part 0 `01 10 33` |
|---|---|---|---|
| before | — | `''`, engine byte `05` | 49 |
| on channel 11 (part 10's own) | MSB 62, LSB 1, PC 124 | `''` | 49 |
| on channel 1 (element-1 reading) | MSB 62, LSB 1, PC 124 | `''` | **49, unchanged** |

Parts 9 and 7 were read in the same pass and carried the names written to them,
`FM Ambient Pad` and `Fat Sine`, so the name route itself was working. The part
*is* a sampler part — engine byte `05` — with no element loaded.

That part 0's sound did not move establishes something positive:
**bank MSB 62 is not read as an ordinary sound bank on channel 1.** Which route
*does* load a preset sampler element is **not established**, and two channels
are not a proof of impossibility — settling it needs a sweep over all eleven
channels with a witness on every part. See
[12-open-questions.md](12-open-questions.md).

### A slot carries the previous project's track types, and nothing complains

`verified on hardware`, and it cost a wrong project before it was noticed.
Project slot 0 was overwritten with a palette that re-typed parts 5 and 6 to
SYNTH and left the rest alone. Afterwards `01 1p 3C` read:

| Part | Track | `01 1p 3C` | What the palette had loaded |
|---|---|---|---|
| 0, 1, 2 | KICK, SNARE, CLAP | `1` DRUM | drum presets — correct |
| **3** | HAT 1 | **`2` SYNTH** | `Lo-Fi Short Closed Hat 1` |
| **4** | HAT 2 | **`2` SYNTH** | `Bright Open Hat 1` |
| 5, 6 | re-typed | `2` SYNTH | synth presets — correct |

Parts 3 and 4 were already typed SYNTH when the session began, left that way by
whatever previously occupied slot 0. **A Drum preset loads onto a SYNTH-typed
part with no error and no refusal**: Bank Select plus Program Change was
accepted, `01 1p 33` read back the expected catalogue number, and every other
address matched the palette. 82 verified addresses agreed while two of the
eleven tracks were the wrong kind of track.

The lesson for anyone writing a project over SysEx: **assert the type of parts
0-6, do not assume it.** `01 1p 3C` is the only address that reveals it, and it
is not implied by anything else you can read back.

### Track type `01` (DRUM) is now verified, and the broadcast sequence captured

`verified on hardware`. Previously only `02` (SYNTH) had been exercised. A
reversible cycle on part 5 — SYNTH → DRUM → SYNTH — and the repair of parts 3
and 4 — SYNTH → DRUM — all acknowledged with result `0` and moved
`PartAwmType`, with the other parts as witnesses throughout:

| Sent | Ack | `01 1p 3C` after | Witnesses |
|---|---|---|---|
| `01 33 00 05 01` | `01 33 01 05 00` | `1` | parts 4, 6 unchanged |
| `01 33 00 05 02` | `01 33 01 05 00` | `2` | parts 4, 6 unchanged |
| `01 33 00 03 01` | `01 33 01 03 00` | `1` | — |
| `01 33 00 04 01` | `01 33 01 04 00` | `1` | — |

`03` (DRUMKIT) remains untested.

What the machine emits for one type change, in order, captured with a cleared
buffer:

```
01 1p 3C   [new type]      the new PartAwmType, before the acknowledgement
01 33 01   [part, 00]      the acknowledgement, result 0
01 10 2E   [58] then [1]
01 18 30   [1] then [2]    PCAppDrumKitStatus, two or three messages
```

> **A correction, recorded because it looked like a device fact.** An earlier
> run of this session read the acknowledgement as `[part, 01]` — result
> `Cancel` — on two successive re-types that nevertheless succeeded. That was
> the instrument: the receive buffer was not cleared before waiting, so the
> wait matched a stale message. With the buffer cleared, every acknowledgement
> in the table above read `0`. Nothing about `01 33 01` needed changing; this
> note exists so the wrong reading is not rediscovered as a discrepancy.

### A preset carries its own effect sends, and overriding them hard is audible

`verified on hardware`. The palette's first version wrote per-part
`31 1p 19` (Reverb Send) and `31 1p 1A` (Variation Send) over whatever the
preset had loaded. On the DX part the result was a **constant drone**, reported
by the user before any measurement pointed at it.

Reloading DX preset 1990 (`FM Ambient Pad`) with no parameter writes at all
showed what the preset actually ships, against what had been imposed on it:

| `31 19 xx` | Preset's own value | Overridden to |
|---|---|---|
| `19` Reverb Send | **12** | 92 |
| `1A` Variation Send | **0** | 48 |
| `2C` AEG Attack | 64 | 88 |
| `2F` AEG Release | 64 | 96 |
| `36` Filter Cutoff | 64 | 64 → 50 |
| `14` Volume | 100 | 72 |

A send of 92/127 from a sustaining pad into a 5.5 s hall (`30 41 03` = 48,
table 23) with a lengthened release does not decay between events.

Surveying the sends the factory presets ship with, across five parts of five
different categories:

| Part | Preset | Reverb Send | Variation Send |
|---|---|---|---|
| 0 | Rumble Kick 2 | 0 | 0 |
| 2 | Thin Clap + Reverb 1 | 0 | 0 |
| 6 | Tingsha Bell 1 | 0 | 0 |
| 8 | Tiny Combo Bars 1 [Chord] | 0 | 0 |
| 9 | FM Ambient Pad | 12 | 0 |

So **the factory presets are essentially dry**, and the send reverb and send
delay buses are unused until a host or the user raises a send. Two consequences
for anyone writing a project over SysEx: a preset's sends are part of its
design and should not be overwritten wholesale; and setting a send *effect
type* alone changes nothing audible, because nothing is feeding it.

### Dry/Wet on a send block does not take

`verified on hardware`. Writing `30 42 15` (TEMPO CROSS DELAY parameter 10,
Dry/Wet Balance, at `al = 0x01 | (10 << 1)`) with 90 read back **0**, four
attempts, while parameters 1, 2, 3 and 5 of the same block read back exactly
the values written in the same pass:

| Parameter | `al` | Written | Read back |
|---|---|---|---|
| 1 Delay Time L>R | `03` | 10 | 10 |
| 2 Delay Time R>L | `05` | 8 | 8 |
| 3 Feedback Level | `07` | 92 | 92 |
| 5 Feedback High Damp | `0B` | 6 | 6 |
| **10 Dry/Wet Balance** | `15` | **90** | **0** |

Consistent with a send bus being wet by definition, so the parameter exists in
the effect's table but is bypassed in this slot. This also confirms the
`al = 0x01 | (k << 1)` offset rule by write-and-read-back on five parameters of
one block, where it had previously been confirmed only by observing traffic.

### A per-part sound backup and restore, round-tripped

`verified on hardware`. Backing a part up by reading every individually
addressable parameter, and restoring it by writing them all back, works
completely — which makes it the restore route to trust over replaying a bulk
dump, whose write direction is still untested.

Part 8 (SYNTH 2, `Tiny Combo Bars 1 [Chord]`) answered **every** address asked
of it, across seven blocks:

| Block | Addresses asked | Answered |
|---|---|---|
| `31 08` sound name | 100 | 100 |
| `31 18` sound general | 57 | 57 |
| `31 28` insertion A | 27 | 27 |
| `31 38` insertion B | 26 | 26 |
| `31 48` sound LFO | 36 | 36 |
| `31 58` arpeggiator | 19 | 19 |
| `30 58` project track | 16 | 16 |

The bulk dump of the same part (`11 02 08`) returned **25 blocks, 2162 bytes**.

The round trip: three parameters were deliberately changed — Volume 90 → 20,
Filter Cutoff 64 → 100, Reverb Send 30 → 120 — then the record was replayed as
181 Parameter Changes (the name block skipped) and read back.
**181 restored, 0 differing, 0 unread**, and the three damaged values returned
to 90, 64 and 30.

Two details that make it work: reload the recorded sound with Bank Select plus
Program Change **first**, because the record does not carry the `41 ep` / `42 ep`
element data; and check `01 10 15` is still the project the backup came from,
since nothing in the sound protocol names a project.

### Rename and save, end to end

A bulk dump at `10 00 04` with slot prefix `00 00` named slot 0, then `01 32 00`
with data `01` saved it. The `0B 00 00` project list, read before and after,
shows the replacement and nothing else moved:

| Slot | Before | After |
|---|---|---|
| 0 | `'Test'`, 123 BPM | `'Dub Techno'`, 122 BPM |
| 1, 2, 7 | `'doowap'` 137, `'Tremolo'` 97, `'Gay'` 97 | unchanged |
| 3-6 | `''` | unchanged |

### The `CurrentProject` precondition earned its place again

The machine was on **project 7** when the session began, while the target was
slot 0. Nothing in the editing protocol carries a project number, so writing
without reading `01 10 15` first would have overwritten a different project and
reported success — the failure mode already recorded in
[14-song-mode.md](14-song-mode.md#read-currentproject-before-writing--it-is-a-precondition-not-a-detail).

> **Measurement chain.** One machine on OS V2.00, USB MIDI as a CoreMIDI device
> on a Mac, writes paced at 2 ms. Every read pass carried the tempo at
> `30 40 76` as an in-loop control and made four attempts per address. The
> preset-ordering result was reproduced across three runs — one failing, two
> passing — and the verification ran in a separate process against the palette
> file, so a write and its check never shared a code path. What this chain
> cannot support is the `0 of 16` silence at mid `03`-`06` as an absolute: it is
> four addresses over two runs with a live control, which is good evidence that
> they are not readable, not a survey of the whole `30` block.

## Reproducing any of this

```bash
python3 tools/hardware-probe/seqtrak_probe.py --list
python3 tools/hardware-probe/seqtrak_probe.py --identity
python3 tools/hardware-probe/seqtrak_probe.py --req 30 40 76 --size 2
python3 tools/hardware-probe/seqtrak_probe.py --watch 90 --timeline
```

The prober is read-only by default; `--set` asks before writing.
`write_test.py` performs the reversible write cycle above. Both need `rtmidi`.

## 2026-10-23, hardware session: the host can drive the transport

The first session run from a **third-party client's own code** rather than from
`tools/hardware-probe/`: the Swift `SeqtrakDevice` layer of the `seqtrak-next`
iOS app, driven by a macOS harness (`SeqtrakProbe`) so the same code path the
phone uses could be exercised with readable output. Transport: USB. Machine
state: project unchanged, sequencer stopped at the start of every run, tempo
122 BPM, battery 100 %.

Every run opened and closed with a read of the control address `30 40 76`, and
every run that changed anything restored it in a `defer`.

### 1. `FA` and `FC` sent *by the host* start and stop the sequencer

This is the finding. The MIDI Implementation Chart documents System Real Time
commands as recognised, and this repository had observed `01 10 20` change
"alongside FA/FC" — but that was the machine's **own** transport being driven
from its front panel. The outbound direction had never been measured.

```
sequencer before: stopped        (01 10 20 → 00)
→ FA
   01 10 20 reads: 1 — running
   realtime echo seen: FA
→ FC
   01 10 20 reads: 0 — stopped
control address still answers: 122 BPM
```

`verified on hardware`. A host can therefore offer a transport button, which
was previously an open risk for any client: the capability map in
`seqtrak-next/product/03-protocol-capability-map.md` listed it as the single
highest-value unmeasured claim.

### 2. `01 10 20` is broadcast, not only polled

During the same run the machine sent **two unsolicited Parameter Changes at
`01 10 20`** — one after `FA`, one after `FC`.

The instrument matters here, so: the handlers that counted them were installed
**after** the awaited reply to the run's only request for that address, and no
other request for it was outstanding. Both messages were therefore volunteered
by the machine. Counted cumulatively, not read off a scrolling view.

`verified on hardware`, from one clean run. A client does not need to poll
transport state; it can follow it.

### 3. Tempo write, read back and restored

```
tempo before: 122 BPM
→ write 126 BPM     (F0 43 10 7F 1C 0C 30 40 76 00 7E F7)
   read back: 126 BPM
· restore: 122 BPM
```

`verified on hardware`. `30 40 76` joins the user scale pad (`30 4D 00`) and the
sequencer step (`70 tt 00`) as a zone with a verified write.

### 4. Drop rate over USB: 40 requests, 40 replies

[Transport reliability](#transport-reliability) records an isolated Parameter
Request being lost roughly 1 in 10, measured over 10 attempts. A larger sample
through a different client, on USB, lost none:

```
40 isolated requests to 30 40 76 → answered 40/40, lost 0
```

**Both measurements stand; neither is retracted.** Getting 0 losses in 40 draws
at p = 0.1 has probability 0.9⁴⁰ ≈ 1.5 %, so the two samples disagree about the
underlying rate rather than about one unlucky run. What differs between them —
transport, client, machine state, firmware — is not established here, and the
retry-four-times rule stays in force for every client regardless. Added to
[12-open-questions.md](12-open-questions.md).

### 5. The round trip is about 3 ms, not 250 ms

The first Parameter Request after connection, with no queue pacing pending,
completed in **2.84 ms**. The other 40 measured 49.9-55.0 ms — a floor imposed
by the client's own 50 ms inter-message delay, not by the machine.

One clean sample, so treat the figure as an order of magnitude rather than a
measurement: what it establishes is that a sweep of the eleven track addresses
costs milliseconds of machine time, and that any multi-second figure for such a
sweep is a property of the client's pacing.

### 6. Reconfirmed in passing

| Fact | What was seen |
|---|---|
| Channel = part + 1 | With the sequencer running, Note On arrived on channels 1, 2 and 3 for KICK, SNARE and CLAP |
| `01 10 02` is a battery percentage | Read `64` = 100 % on a fully charged unit; the earlier session read `46` = 70 % |
| MIDI clock flows while running | 216 `F8` in a 4 s window at 122 BPM, consistent with 24 PPQN |

### 7. `01 1p 33` decoded, and one part that stays silent

The same run read `CurrentSound` on all eleven parts and resolved each against
the preset catalogue. Ten resolved; the categories match the parts they sit on,
which is the same evidence pattern that closed the mapping in
[06-sounds-presets.md](06-sounds-presets.md):

| Part | Value | Catalogue | Name |
|---|---|---|---|
| 0 KICK | `00 31` | 50 | Rumble Kick 2 |
| 1 SNARE | `01 5F` | 224 | Analog Rim 1 |
| 2 CLAP | `02 18` | 281 | Hand Clap + Reverb 2 |
| 3 HAT 1 | `02 73` | 356 | Lo-Fi Short Closed Hat 1 |
| 4 HAT 2 | `03 00` | 385 | Bright Open Hat 1 |
| 7 SYNTH 1 | `07 0B` | 908 | Fat Sine |
| 9 DX | `0F 41` | 1990 | FM Ambient Pad |
| 10 SAMPLER | — | — | **no reply** |

`01 17 33` was read a second time through `tools/hardware-probe/seqtrak_probe.py`
and returned `07 0B` = 907 → catalogue 908, matching the Swift client exactly.
Two clients, one address, same answer.

**`01 1A 33` did not answer** — four attempts from the Swift client and four
from the Python prober, while `01 17 33` answered immediately before and after.
`01 1A 3C` answered on that same part in the 2026-10-22 session, so neither the
part nibble nor the address family is at fault. Written up as a question rather
than a conclusion: [12-open-questions.md](12-open-questions.md).

### 8. A track's insertion effect type can be changed, `31 2p 00`

The earlier sessions established that the insertion blocks are readable and
that their values can be written back. This run changed one to a **different**
type and the machine took it:

```
SYNTH 1 (part 7) insertion A before: 08 10  CLASSIC COMPRESSOR
                 insertion B:        0D 2F  LP-HP FILTER
→ write 01 02    SPX HALL
   machine reports: 01 02  SPX HALL
· restore: 08 10 written back
```

`verified on hardware`. Restoring a value you just read proves the address
accepts a write; writing a different, meaningful value proves the **type codes
in [appendix-a-effect-types.md](appendix-a-effect-types.md) address real
effects**, which is the part a client depends on.

Measured through the `seqtrak-next` Swift client over USB, with `30 40 76` read
before and after, and the original restored in a `defer`.

**This contradicts a line in [12-open-questions.md](12-open-questions.md)**
that still said only two zones had verified writes. That prose predates both
the insertion-block rows in `data/hardware-verified.csv` and the tempo write of
the same session; it has been corrected rather than left to mislead.

### 9. Five more addresses of the sound-design block answer

The eight parameters behind the machine's own knob pages
([appendix-h](appendix-h-sound-design-parameters.md), pages 2 and 3) were read
on part 7. All eight answered; five had never been queried on hardware before.

| Address | Parameter | Read | Was it already verified? |
|---|---|---|---|
| `31 1p 2C` | AEG Attack Time | `40` | no — new |
| `31 1p 2D` | AEG Decay Time | `40` | no — new |
| `31 1p 36` | Filter Cutoff Frequency | `40` | yes, write verified on all eleven parts |
| `31 1p 37` | Filter Resonance/Width | `40` | no — new |
| `31 1p 19` | Reverb Send | `00` | yes |
| `31 1p 1A` | Variation Send | `00` | yes |
| `31 1p 48` | 2bandEQ Low Gain | `40` | no — new |
| `31 1p 4D` | 2bandEQ High Gain | `40` | no — new |

Every value matches the Data List's documented default, which is consistent
with a factory preset and is **not** independent evidence of meaning: reaching
an address only proves it exists. The five new rows are recorded as reachable,
not as understood.

The write to `31 1p 36` was exercised again (`40` → `6E` → restored) and
behaved as the earlier session recorded. Noted here only because it was run
from a different client; it adds nothing the reference did not already have.

### 10. Bluetooth, from a third-party client

The first Bluetooth session in this repository run from a client other than the
official app. USB unplugged, pairing armed from the front panel (hold `[ALL]`,
press `[SWING]`), scanning from a macOS harness over `SeqtrakConnect`.

```
found: SEQTRAK_xxxxxx at -51 dBm — connecting
✓ connected over bluetooth
✓ control address 30 40 76 answers: 122 BPM
→ wrote the three transmit flags 00 00 11, 00 00 13, 00 00 14
   battery reads 100 %
   sequencer stopped
```

(The advertised name carries a per-unit suffix; it is redacted here because it
identifies one machine and nothing in the protocol depends on it.)

`verified on hardware`: the MMA service UUID `03B80E5A-…` is what the machine
advertises, a Parameter Request round-trips over BLE, and the documented
transmit-flag sequence is accepted.

### 11. The drop rate is not explained by the transport

The same instrument that got 40/40 on USB got **40/40 on Bluetooth**:

| Transport | Sample | Answered | Median round trip |
|---|---|---|---|
| USB | 40 | 40 | 52.9 ms |
| Bluetooth | 40 | 40 | 58.5 ms |

Both medians are floored by the client's own 50 ms inter-message delay, so the
difference between them is roughly 6 ms and is the only part attributable to
the link.

This **weakens** the most obvious explanation for the disagreement recorded in
[12-open-questions.md](12-open-questions.md), where an earlier session measured
roughly 1 in 10 requests lost. Whatever differs between the two sets of
measurements, it is not USB versus Bluetooth on this unit. The question stays
open and the retry-four-times rule stays in force.

**Not compared:** the full-sweep durations. The USB figure of 1.42 s and the
Bluetooth figure of 4.03 s were measured on different workloads — the sweep
gained two reads per track between them — so putting them side by side would
be meaningless.

### 12. The live stream arrives over Bluetooth too

The same four-second window as the USB run, this time with the cable out:

```
MIDI clock (F8)      221
SysEx addresses      2
  01 10 20  ×2     transport, broadcast on start and on stop
  01 10 2E  ×1     ParameterLedMode, already documented as broadcast
Note On, by channel
  ch 1 KICK ×16 · ch 2 SNARE ×9 · ch 3 CLAP ×2
```

`verified on hardware`. Everything a host needs to follow the machine live —
the clock a playhead has to be counted from, the per-track note activity, and
the transport broadcasts — crosses Bluetooth once the three transmit flags are
written. A wireless client is not restricted to polling.

The counts are not compared with the USB run's: the windows were started by
hand and the note totals depend on where in the pattern each one opened.

### 13. `30 40 7A` and `30 40 7C` are two fields, and the swing is centred on 128

`data/parameters.csv` prints the parameter at `30 40 7C` as "Pattern Master Step
LSB Swing Offset MSB Swing Offset LSB", which is this repository's known
rendering artefact when the Data List puts several lines in one cell — the same
artefact already noted for `42 ep 37` in
[12-open-questions.md](12-open-questions.md). Read byte by byte, the block
resolves cleanly:

| Address | Data bytes | Read | What it is |
|---|---|---|---|
| `30 40 7A` | 2 | `01 00` = 128 | Pattern Master Step, documented 1-128 |
| `30 40 7B` | — | no reply | the LSB of the field above, not an address of its own |
| `30 40 7C` | 2 | `01 0A` = 138 | Swing Offset |
| `30 40 7D` | — | no reply | likewise |
| `30 40 7E` | 1 | `00` | Scale, documented 0-7 |
| `30 40 7F` | 1 | `40` | Key, documented `40`-`4B` |

**The swing's centre was then measured, not inferred.** A write sweep with the
original restored in a `finally`:

```
value   accepted as   verdict
 60      70           clamped
 69      70           clamped
 70      70           accepted
128     128           accepted
186     186           accepted
187     186           clamped
200     186           clamped
```

The field's real bounds are **70 to 186**, which is exactly 128 ± 58. The Data
List's display range "-58 - 0 - +58" therefore maps as **`display = value −
128`**, and `30 40 7C` is a 14-bit field centred on 128 like the micro-timing
scale is centred on 60.

`verified on hardware`, measured through the `seqtrak-next` Swift client over
USB with `30 40 76` read before and after. This is the same method that closed
the last disagreement between the two parameter sources — a value the machine
clamps tells you the real bound, and the bounds tell you the centre.

### 14. `00 00 11` reads `Off` on a unit that is talking over Bluetooth

The repository already warns that `00 00 11` reading `00` does not mean
Bluetooth is off. On 2026-10-23 that warning was confirmed as directly as it
can be: in one session, on one unit, **Bluetooth MIDI carried a full
connection, reads, writes and the live stream** — and a read of `00 00 11`
afterwards, over USB, returned `00`.

```
MIDI
  Local control           On    (raw 1)
  MIDI (TRS) in/out       On    (raw 1)
  USB MIDI in/out         On    (raw 1)
  Bluetooth MIDI in/out   Off   (raw 0)      ← while BLE had just worked
```

So whatever `00 00 11` reports, it is not "can this machine speak Bluetooth
MIDI". A client must not gate its Bluetooth behaviour on it, and a diagnostic
that reports "Bluetooth is disabled" from this value is wrong.

Two of the thirteen settings read in the same sweep also differ from their
published defaults — `00 00 22` Legacy MIDI Thru read `3` against a documented
`0`, and `00 00 1F` Record Quantize read `0` against a documented `3` — which
is the same lesson as the table above, on a third unit-state.

All thirteen settings the app exposes answered: `00 00 00`, `01`, `06`, `09`,
`0D`, `11`, `1D`, `1F`, `20`, `22`, `23`, `24`, `25`.

### 15. Step attributes: three of the four are now verified

[12-open-questions.md](12-open-questions.md) listed `70 (10|tt)` as the
highest-value write that had never been tried. Three of its four attributes
round-tripped on the first attempt, on part 0 (KICK), into a step that was
**empty before the test** so that `delete` was an exact undo:

```
step 4 of KICK, empty
add                 → velocity 100, micro timing 60, retrigger 0

70 10 01  velocity        wrote 70, reads 70    ✓
70 10 00  micro timing    wrote 70, reads 70    ✓   shown as +10
70 10 03  retrigger       wrote  1, reads  1    ✓   shown as ×2
70 60 00  probability     reads 0 (one byte, as documented)

delete              → step empty again
```

`verified on hardware`, measured through the `seqtrak-next` Swift client over
USB, sequencer stopped, `30 40 76` read before and after.

**The micro-timing centre is confirmed by arithmetic as well as by the add.**
Writing `70` and reading `70` on a scale the Data List gives as −60…+59 means
the neutral value is 60, which is what the machine fills in by itself when a
note is added. A client that treats this field as centred on 0 is 60 ticks out.

`70 10 04`, the conditional lock, was **not** written — only read, where it
answered one byte. It stays on the untested list.

### 16. The conditional lock closes the set — all four step attributes verified

The one attribute left after [§15](#15-step-attributes-three-of-the-four-are-now-verified).
Same method: a step of KICK that was empty beforehand, so deleting it was an
exact undo whatever the write did.

```
probability on a fresh note: 0
  wrote 3  → accepted      shown as level 4
  wrote 7  → accepted      shown as level 8
  wrote 0  → accepted      shown as level 1
delete → step empty again
```

`verified on hardware`. **`70 (10|tt)` is now verified in all four of its
attributes** — micro timing `00`, velocity `01`, retrigger `03` and conditional
lock `04` — which retires the first entry on the untried-writes list in
[12-open-questions.md](12-open-questions.md) completely.

The eight probability levels are `0`-`7` on the wire; the machine shows them as
lit keys rather than as percentages, so a client has no percentage to display
and should not invent one.

### 17. The synth event block answers on an empty pattern

A read-only sweep of `75 ((n<<4)|(idx>>7)) (idx&7F)` for n = 0-3, indices 0-7,
on a project whose synth patterns are empty:

```
SYNTH 1 (n=0), SYNTH 2 (n=1), DX (n=2), SAMPLER (n=3)
  every index → 0 data bytes
```

`verified on hardware` as a reachability result only. **Zero data bytes is an
answer** — the same marker an empty drum step gives — so the block replies and
the patterns are empty, which is a different fact from the block being
unreachable. It confirms the earlier sweep that found n = 0-3 replying and
n = 4-11 silent.

Nothing here distinguishes the two competing readings of `75`, because neither
can be tested against a reply that carries no data. That disagreement stays
open in [12-open-questions.md](12-open-questions.md).

This matters to clients for one reason: a third-party app concluded from the
`70` block answering only on DRUM parts that melodic step editing was
unreachable. It is not — the synths have their own block — and that conclusion
has been corrected in the project that made it.

### 18. The FM engine answers, all four operators

The `48 09` (DX Common) and `49 o9` (DX Operator) blocks had **never been
queried on hardware** — no row for either in `data/hardware-verified.csv`
before today. Read on the DX part of a project holding the preset *FM Ambient
Pad*:

```
COMMON — 14 of 14 controls answered
  Algorithm              9      (range 0-11, so algorithm 10 of 12)
  Pitch Bend Sensitivity 66     (range 40-88, centred on 64: +2 semitones)
  LFO Wave 0 · LFO Speed 16 · LFO Delay 0 · LFO PMD 0
  PEG Rate 1-4 all 64 · PEG Level 1-4 all 64

OPERATOR 1-4 — 25 of 25 controls answered, each
  op 1: EG rates 59 60 80 50, levels 100 115 127 …
  op 2: EG rates 100 84 80 50, levels 127 72 0 …
```

**114 addresses, 114 replies.** `verified on hardware` as a reachability and
read result: the values differ per operator in the way a real patch does, which
is consistent with them being that patch's envelopes, but nothing here proves
the meaning of any individual address — only that the whole block answers.

The reserved rows the reference lists inside both blocks were not queried.

This is the engine where the hardware is least able to help: four operators of
twenty-five controls each, reached through four knobs and eight LEDs, with
every advanced parameter collapsing to the panel word `OTHER`.

## 2026-10-23, hardware session: the AWM element blocks answer, and a multi-byte field answers only at its base address

`41 ep` and `42 ep` — the AWM elements' oscillator/amplitude/pitch and
filter/EQ/LFO blocks — had no row in
[`../data/hardware-verified.csv`](../data/hardware-verified.csv) before today.
They are the blocks the panel reaches least: 77 and 53 real controls per
element, eight elements per part, behind four knobs.

**Method.** Read-only. 128 Parameter Requests over USB, four attempts each,
0.6 s per attempt: low bytes `00`-`1F` of both blocks, on elements 1 and 2 of
part 7 (SYNTH 1), so `41 07`, `41 17`, `42 07` and `42 17`. The tempo at
`30 40 76` was interleaved as the control address every eight requests. Nothing
was written. The run was done twice.

| What | Result |
|---|---|
| Control address `30 40 76` | answered **16 of 17** interleaved checks |
| Element addresses | **108 of 128** answered |
| Silent addresses | 20, the **same 20** on both elements and in both runs |

**The 20 silent addresses are exactly the continuation bytes of multi-byte
fields**, with no exceptions in either direction:

| Block | Silent lows | The field they are inside |
|---|---|---|
| `41` | `04` | `41 ep 03` Wave Number, size 2 |
| `42` | `02`, `08`, `0B`, `0D`, `14`, `16`, `18`, `1A`, `1C` | the size-2 fields based at `01`, `07`, `0A`, `0C`, `13`, `15`, `17`, `19`, `1B` |

And the base address answers with the **whole** field, not its first byte:

| Address | Reply | Field |
|---|---|---|
| `41 07 03` | `05 06` | Wave Number, 2 bytes |
| `42 07 01` | `01 3E` | Filter Cutoff Frequency, 2 bytes |
| `42 07 07` | `00 00` | HPF Cutoff Frequency, 2 bytes |
| `42 07 00` | `00` | Filter Type, 1 byte |
| `42 07 1D` | `62` | FEG Depth, 1 byte |

So: **a Parameter Request is answered at the base address of a field and
nowhere inside it, and the reply carries every byte of the field.**
`verified on hardware`. This is also an instrument: a silent address inside a
documented multi-byte field is a structural silence, not a dropped reply, and
must not be counted as one.

**One place the size column groups rather than describes.** `41 ep 1B` is
printed as "reserved, size 5". Its five addresses `1B`-`1F` each answered
individually with `00`, so that row is five one-byte reserved slots the table
put on one line — not one five-byte field. The rule above is about genuine
multi-byte parameters; do not read a size column as proof of one.

**What this does not establish.** Nothing about what any of the 108 addresses
*means*: they answered, with plausible per-element values, and no witness test
was run on any of them. No element address has been written.

Reproduce with
[`../tools/hardware-probe/element_read.py`](../tools/hardware-probe/element_read.py).

### The same rule on a second block, and the size column checked against the machine

`31 1p` (Sound Common / General, 73 rows) and `31 4p` (Sound Common / LFO, 39
rows) were then read in full on part 7, read-only, four attempts each, control
address interleaved every eight requests. Only addresses the reference claims
exist were asked for.

| What | Result |
|---|---|
| Control address `30 40 76` | **14 of 14** |
| Documented addresses answered | **112 of 112** |
| Replies whose width differed from the documented `size` | **0 of 112** |

So on 112 addresses the Data List's size column is exactly what the machine
returns — seven of them two bytes, the rest one. `verified on hardware`.

The seven two-byte fields were then asked for at their continuation address as
well (`31 1p 18`, `25`, `3A`, `3E`, `42`, `47`, `4C`), which the reference gives
no row for:

| Base | Reply | Continuation | Reply |
|---|---|---|---|
| `31 1p 17` Detune | `08 00` | `31 1p 18` | silent |
| `31 1p 24` Micro Tuning Scale | `00 00` | `31 1p 25` | silent |
| `31 1p 39` 3bandEQ Low Frequency | `00 76` | `31 1p 3A` | silent |
| `31 1p 3D` 3bandEQ Mid Frequency | `01 29` | `31 1p 3E` | silent |
| `31 1p 41` 3bandEQ High Frequency | `01 1B` | `31 1p 42` | silent |
| `31 1p 46` 2bandEQ Low Frequency | `00 66` | `31 1p 47` | silent |
| `31 1p 4B` 2bandEQ High Frequency | `01 10` | `31 1p 4C` | silent |

Seven for seven, control address 7 of 7. The base-address rule is now seen on
two different blocks.

**What measured it.** Both runs used the same request-and-wait loop
(`element_read.py`, `sound_common_read.py`, `continuation_check.py` in
[`../tools/hardware-probe/`](../tools/hardware-probe/)), so these are two
observations through one instrument design, not two independent instruments.
What they do establish independently is the *addresses*: different blocks,
different fields, same behaviour, and in every run a control address that was
answering.

## 2026-10-23, hardware session: the SAMPLER block `50 eA` answers, and a sample name comes off the machine

`50 eA` — the SAMPLER track's seven sample slots — had never been queried. It
is 88 addresses of packed name followed by four parameters, 103 documented
rows in all.

**Method.** Read-only, over USB, four attempts per address, control address
`30 40 76` checked once per slot. All seven elements, so 616 name addresses and
28 parameter addresses: **672 requests, 0 silent, control 7 of 7.** Nothing was
written. Reproduce with
[`../tools/hardware-probe/sampler_read.py`](../tools/hardware-probe/sampler_read.py).

**The names decode.** The 88 bytes of each slot, unpacked 7-into-8 as
[02-sysex-format.md](02-sysex-format.md#names) describes, give readable UTF-8:

| Slot | Name | End point | At 44.1 kHz |
|---|---|---|---|
| 1 | `Ambient - Pad & Noise 1` | 631871 | 14.33 s |
| 2 | `Singing - Female - Ah 1` | 94239 | 2.14 s |
| 3 | `Riser - Noise 1` | 285391 | 6.47 s |
| 4 | `Laser - Blast 2` | 17631 | 0.40 s |
| 5 | `Noise - Fade In 1` | 168495 | 3.82 s |
| 6 | `Bird 1` | 8623 | 0.20 s |
| 7 | `Bongo3 High 3` | 2175 | 0.05 s |

This is the first sample name this project has read off the hardware, and it
is also the first time the 7-into-8 name decoding has been checked against real
data rather than against the official app it came from. Every slot was pure ASCII, so
the carrier byte was `00` throughout: **the bit order inside a group is still
untested**, exactly as [SoundName.decodeName7Bit] already warns.

**The four-byte fields answer at their base address with four bytes**, which is
the third block on which the base-address rule holds, and the first with fields
wider than two bytes.

| Address | Field | Size | Reply width |
|---|---|---|---|
| `50 eA 5F` | Loop On/Off | 1 | 1 |
| `50 eA 60` | Loop Length | 4 | 4 |
| `50 eA 66` | Start Point | 4 | 4 |
| `50 eA 6A` | End Point | 4 | 4 |

**What the positions mean is an inference, not a measurement.** Read 7-bit
big-endian across the four bytes, the end points give durations that match the
names — 50 ms for a bongo hit, 14.3 s for an ambient pad — and the largest sits
just under the 16-second ceiling [01-overview.md](01-overview.md) documents. On
all seven slots Start Point was `0` and End Point equalled Loop Length, which is
what untrimmed factory samples would look like. No witness test was run: nothing
here establishes the unit, and no sample was trimmed and re-read.

## 2026-10-23, hardware session: the project blocks, and where the Data List's size column is wrong

`30 41` (Send Reverb), `30 42` (Send Delay), `30 47` (Master EQ) and `30 4B`
(A/D Part General) read in full, read-only, four attempts each, control address
interleaved every eight requests.

| What | Result |
|---|---|
| Control address `30 40 76` | **15 of 15** |
| Documented addresses answered | **120 of 120** |
| Replies whose width differed from the documented `size` | **16** |

The sixteen are **all `reserved` rows** — `30 41 33`-`41` and `30 42 33`-`41`,
listed every two addresses with size 2, answering with one byte. Every
non-reserved row matched its documented size, as on the 112 addresses of
`31 1p` / `31 4p` and the sampler's four-byte fields.

**Which of the two readings is right was then measured.** If they are one-byte
slots the table printed at a two-byte stride, the addresses the table skips
should answer; if they are two-byte fields and the reply is somehow truncated,
those addresses should be silent like every other continuation byte measured
today.

| Address | In the table | Reply |
|---|---|---|
| `30 41 33`, `35`, `37`, `39`, `3B`, `3D`, `3F`, `41` | listed | one byte, `00` |
| `30 41 34`, `36`, `38`, `3A`, `3C`, `3E`, `40`, `42` | **not listed** | one byte, `00` |
| `30 41 31` Reverb Parameter 23/24 | listed, size 2 | `00 00` |
| `30 41 32` | not listed | **silent** |

Sixteen for sixteen, with a genuine two-byte field and its silent interior in
the same run and the control address at 4 of 4. So these are **sixteen one-byte
reserved slots that the Data List printed at a two-byte stride**, and its size
column is wrong for them. `verified on hardware`.

Two things follow:

1. **The base-address rule is untouched.** `30 41 31` still answers with both
   its bytes and `30 41 32` is still silent, measured alongside the
   counter-example.
2. **Asking is a better instrument than the size column.** Whether an address
   is the interior of a multi-byte field can be settled by requesting it — a
   silent address inside a field, an answering address beside one. A client
   that trusts the size column alone will be wrong on at least these sixteen
   rows; one that drops a reply whose width does not match what it expected
   will simply not show them, which is the right outcome for reserved slots.

Reproduce with
[`../tools/hardware-probe/block_read.py`](../tools/hardware-probe/block_read.py)
(`"Project Common / Send Reverb"` …) and
[`../tools/hardware-probe/reserved_stride.py`](../tools/hardware-probe/reserved_stride.py).

### The effect slot mapping checked against a loaded effect

A parameter block names an effect's slots by number alone — `30 41 0B` is
"Reverb Parameter 5" whatever is loaded — and
[`../data/effect-parameters.csv`](../data/effect-parameters.csv) says what each
number means per type. That table came out of the Data List and had never been
checked against a machine.

The unit's send reverb read `30 41 00` = `01 00`, which
[`../data/effect-types.csv`](../data/effect-types.csv) resolves to **REV-X
HALL**. Its 24 numbered slots were then read from the same run as the block
survey above and compared with what the table says REV-X HALL does with them:

| Slot | Table says | Documented range | Read |
|---|---|---|---|
| 1 | Reverb Time | 0 - 69 | 30 |
| 2 | Diffusion | 0 - 10 | 10 |
| 3 | Initial Delay | 0 - 127 | 9 |
| 4 | HPF Cutoff Frequency | 0 - 52 | 12 |
| 5 | LPF Cutoff Frequency | 34 - 60 | 44 |
| 6 | Room Size | 0 - 31 | 24 |
| 7 | High Ratio | 1 - 10 | 8 |
| 8 | Low Ratio | 1 - 14 | 5 |
| 9 | Decay | 0 - 63 | 34 |
| 10-24 | `---`, unused by this type | — | **0, all fifteen** |

**Nine for nine inside their ranges, and fifteen for fifteen reading zero.**
The ranges are narrow and all different — `1 - 10`, `1 - 14`, `34 - 60` — so a
slot mapping that was off by even one position would very likely have put a
value outside at least one of them; and the slots the table marks unused are
exactly the ones holding zero.

That is a consistency check on **one** type, not a proof of the table's other
107 (block, type) pairs, and no witness test was run: nothing was changed and
re-read. What it does establish is that the table's slot numbering lines up
with the block's addresses for this effect, which is the part a client has to
get right before it can label anything.

`reverse-engineered from app traffic` would be the wrong marker here — nothing
was observed in traffic. The table is `from Yamaha Data List`; this run is a
hardware consistency check on it, recorded as such in
[`../data/hardware-verified.csv`](../data/hardware-verified.csv).

## 2026-10-23, hardware session: the four master effects, and the slot table checked on four more types

`30 43` through `30 46` read in full, read-only, four attempts each, control
address interleaved: **156 of 156 documented addresses answered, control 20 of
20.** Thirty-two replies did not match the documented size — the same reserved
rows at `33`-`41`, now seen in four more blocks, which reproduces the
one-byte-slot-at-a-two-byte-stride finding above.

**Four effects were loaded, and each is one its slot accepts.**

| Slot | Type bytes | Type | `assignable_to` says |
|---|---|---|---|
| Master 1 (`30 43`) | `0C 28` | CONTROL FILTER | Single, Master 1, Master 2, Master 3 |
| Master 2 (`30 44`) | `02 10` | TEMPO CROSS DELAY | Single, Send, Master 1, Master 2, Master 3 |
| Master 3 (`30 45`) | `0C 70` | VINYL BREAK | Single, Master 1, Master 2, Master 3 |
| Master 4 (`30 46`) | `08 00` | VCM COMPRESSOR 376 | Chain, Single, Master 1, **Master 4** |

Four for four, and the two tight cases both fit: VINYL BREAK is not listed for
Master 4 and is not in it, while VCM COMPRESSOR 376 is listed for Master 1 and
Master 4 only and is in Master 4. That is a check on `assignable_to` in
[`../data/effect-types.csv`](../data/effect-types.csv), which had never been
compared with a machine.

**The slot table holds on four more types.** Every slot the table names for the
loaded type read inside its documented range — **23 of 23, none outside** —
with ranges as narrow as `0 - 1`, `0 - 4`, `1 - 10`, `52 - 76` and `64 - 127`:

| Type | Slots named | All in range |
|---|---|---|
| CONTROL FILTER | 5 | yes |
| TEMPO CROSS DELAY | 7 | yes |
| VINYL BREAK | 5 | yes |
| VCM COMPRESSOR 376 | 6 | yes |

Together with the REV-X HALL check above that is **32 named slots on five
types, none out of range**, across both parameter tables.

### Open: five slots the table does not name are not zero

Of the 73 slots the table leaves unnamed for these four types, 68 read `00` —
which is what an unused slot should look like, and what all fifteen of REV-X
HALL's unused slots did. Five did not:

| Address | Type loaded | Slot | Read |
|---|---|---|---|
| `30 44` 13-16 | TEMPO CROSS DELAY | not listed at all in the table | 22, 64, 46, 64 |
| `30 46` 6 | VCM COMPRESSOR 376 | `---` | 1 |

The table gives TEMPO CROSS DELAY only twelve slots, where CROSS DELAY has
sixteen. The four values look like the EQ Mid group other types put around
there — `22` inside Frequency's `14 - 54`, `64` at the centre of Gain's
`52 - 76`, `46` inside Width's `1 - 120` — but that is a resemblance, not a
reading.

The candidate explanation is that the block is shared and a previously loaded
type's bytes linger in the slots the current one does not use. **It is
untested**, and testing it means switching an effect type, which is a write and
is audible. Until then, a client must not infer that a slot the table leaves
unnamed is zero, and must not name it after the slot a neighbouring type uses.

### The data-assign tables, applied to the values read

[`../data/effect-data-assign-tables.csv`](../data/effect-data-assign-tables.csv)
converts an effect parameter's raw byte into what the machine shows: 63 tables,
7330 rows, named per parameter by the `data_assign_table` column of
[`../data/effect-parameters.csv`](../data/effect-parameters.csv). Applied to the
REV-X HALL send read above, with no further requests:

| Slot | Raw | Table | Shown |
|---|---|---|---|
| 3 Initial Delay | 9 | 5 | 14.3 ms |
| 4 HPF Cutoff Frequency | 12 | 3 | 80 (Hz) |
| 5 LPF Cutoff Frequency | 44 | 3 | 3.2k (Hz) |

A 14 ms pre-delay and a band from 80 Hz to 3.2 kHz is what a reverb send is
usually set to, which is one more sign the slot numbering is right — and, like
the range check above, it is consistency, not proof. No parameter was changed.

Two things to know before using these tables:

- **The value strings already carry their own magnitude** — `3.2k`,
  `THRU(20.0k)` — so they are display strings, not numbers to scale. Appending
  a unit taken from the documented display range gives `3.2k kHz` if you are
  not careful.
- **A table is per parameter per type, and most parameters have none.** 240 of
  the 1445 parameter rows name one. REV-X HALL's own Reverb Time has no table
  and a display range of `0.3s - 18.0s`, where SPX HALL's Reverb Time uses
  table 4 and runs to `30.0s`. The same parameter name on two types is not the
  same parameter.

## 2026-10-23, hardware session: the machine sends Timing Clock while the sequencer is stopped

A 90-second passive listen with
[`../tools/hardware-probe/listen_counter.py`](../tools/hardware-probe/listen_counter.py),
which counts cumulatively and carries its own positive control. Nothing was
sent to the machine during the window.

| Status | Count |
|---|---|
| `F8` Timing Clock | **4396** |
| `FE` Active Sensing | 361 |
| everything else, including `FA`, `FC`, `F2`, notes and SysEx | **0** |

The instrument's `F2` control passed before the window, so the zeros are
absence from the stream rather than blindness.

**The sequencer was stopped the whole time.** `01 10 20` read `0` immediately
after, and no `FA` or `FC` appears in the count — had it started or stopped
during the window, one of them would be there. So it was stopped before, after,
and throughout.

**4396 clocks in 90.1 s is 48.79 a second, which at 24 PPQN is 122.0 BPM** —
against `30 40 76` reading 122 in the same minute. `verified on hardware`.

Two things follow for any client:

1. **A live tempo is free.** The clock arrives unasked and tracks the tempo
   knob the instant it moves, where the parameter address only answers when
   you ask. Deriving the tempo from clock arrivals needs no polling at all.
2. **A clock-counted playhead must be gated on the transport state, not on the
   clock.** The clock runs while the machine is still, so a playhead driven by
   tick count alone advances through silence. `01 10 20`, or the `FA`/`FC` the
   machine broadcasts, is what says whether it is moving.

What this does **not** establish: what the machine sends while it is playing,
or while the front panel is being used. The window caught an idle machine, and
the counts above are about that machine.

## 2026-10-23, hardware session: a two-byte Parameter Change is accepted, and a one-byte write to a wide field is ignored

This was the open question that made the whole effect surface read-only. It is
now closed. `read → write → read back → restore`, restore in a `finally`,
witness address in the same loop, sequencer checked stopped (`01 10 20` = `00`)
before anything was sent. Everything was restored and verified restored.

### The two-byte write

Target `30 41 0B`, Reverb Parameter 5, which on the loaded REV-X HALL is LPF
Cutoff Frequency with a documented range of 34-60. Witness `30 41 09`
(Parameter 4), control `30 40 76`.

| Step | Target | Witness | Control |
|---|---|---|---|
| before | `00 2C` (44) | `00 0C` | `00 7A` |
| wrote `00 32` (50) | reads `00 32` | `00 0C` | `00 7A` |
| restored `00 2C` | reads `00 2C` | `00 0C` | `00 7A` |

**The machine accepts a two-byte Parameter Change**, on an effect parameter,
and nothing else moved. `verified on hardware`.

### The same address written with one byte

| Step | Sent | Target reads |
|---|---|---|
| one-byte write | `28` (40) | `00 2C` — unchanged |

**A one-byte write to a two-byte field is ignored.** It does not set the MSB
and it does not set the LSB; the field keeps its value. That is the most benign
of the three possibilities this repository listed, and it means a client that
sends one byte by mistake corrupts nothing — but it also silently does nothing,
so a client must still match the documented width.

### The packing, with a non-zero MSB

Every two-byte write up to here had an MSB of `00`, so the encoding itself —
"1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0" — had never been exercised. Run on
the tempo, which is documented 5-300, witness `30 40 7C` (swing offset):

| Wrote | Sent as | Read back | Decoded |
|---|---|---|---|
| 130 | `01 02` | `01 02` | 130 |
| 200 | `01 48` | `01 48` | 200 |
| 61 | `00 3D` | `00 3D` | 61 |

Three for three, two of them with a non-zero MSB, witness unmoved throughout,
tempo restored to `00 7A`. **7-bit big-endian is confirmed on the wire in both
directions.** `verified on hardware`.

### What is still untested

**Three bytes and up.** The sampler's `Loop Length`, `Start Point` and
`End Point` are four bytes each and nothing has ever written one. They read
correctly (above), but a wrong guess there moves a sample's boundaries, so they
stay read-only until someone tries it on a sample they can afford to lose.

Reproduce with
[`../tools/hardware-probe/wide_write_test.py`](../tools/hardware-probe/wide_write_test.py)
and
[`../tools/hardware-probe/msb_test.py`](../tools/hardware-probe/msb_test.py).

## 2026-10-23, hardware session: a melodic step can be written, and the piano-roll reply shapes are not what the reference said

The synth piano roll (`72`-`76`) had only ever been read. This closes the last
large capability gap in this project: **a melodic pattern can be written.**

All four melodic lists read empty before any of this ran — SYNTH 1, SYNTH 2,
DX and SAMPLER all answered index 0 with zero data bytes — so nothing of the
owner's was at risk, and that emptiness is itself the witness: anything left
behind afterwards would have been ours. The sequencer was checked stopped
(`01 10 20` = `00`), the tempo was interleaved as the control address, DX was
read as a second track that must stay empty, and every run deleted what it
added in a `finally`. Every run ended with the list empty again.

### Add, read and delete

Three notes written to SYNTH 1 (local index 0) with `72 00 00`, read back with
`75 00 idx`, deleted with `74 00 idx` highest index first:

| idx | Written | Read back |
|---|---|---|
| 0 | `00 00 00 3C 64 00 00 0C` | identical |
| 1 | `00 0C 00 43 64 00 00 0C` | identical |
| 2 | `00 18 00 48 64 00 00 0C` | identical |

Events land at consecutive indices in the order they are added, and index 3
answered empty throughout. `verified on hardware`.

### Correction: the `75` reply is the write payload, not the documented shape

This document previously said a `75` reply parses as `eventType, partNumber,
eventTime (16 bits), note, onVelocity, offVelocity, gateTime (16 bits)` — nine
bytes, event type first, part number second.

**It is eight bytes, and it is the add payload verbatim:**

```
eh el tt nn vv ov gh gl
│  │  │  │  │  │  └──┴─ gate time, 14-bit
│  │  │  │  │  └─ note-off velocity
│  │  │  │  └─ note-on velocity
│  │  │  └─ note number
│  │  └─ event type (00 = Note)
└──┴─ event time in ticks, 14-bit
```

There is no part number in the reply, and the event type is the **third** byte,
not the first. A client written to the old description reads the event time as
a type and the note as a velocity.

### Correction: the index lookup answers on `76`, not `77`

This document said `ah = 77` carries the index replies. It does not. A lookup
sent as `76 00 <part>` with `eh el tt nn 00 00` is answered at **`76 01 00`** —
`am = 01` marks the reply — with the query echoed and **the index appended as a
14-bit pair**:

| Looking for | Reply body | Index |
|---|---|---|
| tick 0, note 60 | `00 00 00 3C 00 00` + `00 00` | 0 |
| tick 12, note 67 | `00 0C 00 43 00 00` + `00 01` | 1 |
| tick 24, note 72 | `00 18 00 48 00 00` + `00 02` | 2 |

Three for three.

**A note that is not in the list is answered too, with the pair omitted.**
Asking for tick 96, note 127 — absent — gave `00 60 00 7F 00 00`, six bytes
rather than eight. So **absence is signalled by the length**, and a client must
check it: without that control, a trailing `00 00` meaning "index 0" would be
indistinguishable from "not found". That control is why this is stated as a
fact rather than a reading.

Reproduce with
[`../tools/hardware-probe/pianoroll_write.py`](../tools/hardware-probe/pianoroll_write.py)
and
[`../tools/hardware-probe/pianoroll_index.py`](../tools/hardware-probe/pianoroll_index.py).

### Four bytes, the last untested width

The sampler's trim points are the only four-byte fields, and nothing had ever
written one. Target: slot 7 ("Bongo3 High 3", the shortest at ~49 ms), its
Start Point, which read `00 00 00 00` on all seven factory slots — so restoring
zero is not a guess but what was read. Witness: the End Point of the same slot.

| Step | Start Point | End Point (witness) |
|---|---|---|
| before | `00 00 00 00` = 0 | `00 00 10 7F` = 2175 |
| wrote `00 00 01 00` (128) | reads `00 00 01 00` = 128 | `00 00 10 7F` |
| restored | `00 00 00 00` | `00 00 10 7F` |

**A four-byte Parameter Change is accepted**, and 128 carries into the third
byte, which is what makes it a test of the packing rather than of one byte.
`verified on hardware`.

**So every width the reference uses is now verified in both directions** — one
byte, two and four, all 7-bit big-endian, most significant seven bits first.

**What a trim point still does not tell you is how long the sample is.** The
end point of an untrimmed slot is the closest thing to a length anyone has, so
a client can move a boundary inward safely and has nothing to justify moving
one outward past where it was first read.

Reproduce with
[`../tools/hardware-probe/four_byte_write.py`](../tools/hardware-probe/four_byte_write.py).

## 2026-10-23, hardware session: the USB link recovers on its own after the cable is pulled

The last untested path in this project's client, and the only one no amount of
software could settle. `USBTransport` registers a CoreMIDI notification block,
so it *should* come back when the device reappears — and "should" is what this
repository exists to replace.

One process watched the connection state across the whole event, without being
restarted:

```
   0.0 s  connected: true  SEQTRAK
  11.6 s  → LOST
 398.2 s  → CONNECTED  SEQTRAK
 398.6 s  the machine answered after the return: 122 BPM
```

Two things, and the second is the one that matters:

1. **The loss is noticed.** Pulling the cable moved the client to disconnected
   within the quarter-second sampling interval.
2. **The return is noticed *and the link works*.** Connected is a claim the
   transport makes; a reply is evidence. The tempo was requested after the
   return and answered, through the same long-lived client.

**The six-and-a-half-minute gap was an accident that improved the test.** The
cable first plugged back in was the wrong one, so the device was genuinely
absent for that whole time. A client that recovers after six minutes is a
better result than one that recovers after two seconds — nothing here depended
on the notification arriving promptly.

### Two things this run says about instruments, not about the machine

**A fixed window makes the person race a clock they cannot see.** The first
attempt watched for 150 seconds and told the owner to "press Enter", when
nothing was waiting for a key. He unplugged, possibly after the window closed,
and the run produced nothing. The probe now waits for the event — gone *and*
back — rather than for the clock.

**An empty output is not a measurement.** While the wrong cable was in,
`system_profiler SPUSBDataType` returned **zero lines** — not an empty device
list, no output at all, because the command produces nothing in that
environment. It was briefly read here as "the Mac sees no USB device", which is
the same mistake as reading a missing SysEx reply as an answer. The only sound
evidence during that stretch was CoreMIDI's port list, from a tool known to
work.

Reproduce with `swift run SeqtrakProbe reconnect` in
[`seqtrak-next`](../../seqtrak-next/) — from a real terminal, since the probe
builds a CoreBluetooth central.

## 2026-10-23, hardware session: a sung melody written to SYNTH 1, and three single-shot verifications broadened

A twenty-note melody, transcribed from a voice memo, was written to SYNTH 1
(global part 7) of project 0 and read back event by event. The run also had to
empty the project first, which exercised `DeletePattern` and `RemoveScene` at a
scale neither had been tried at. All of it is `verified on hardware`. The
instrument is
[`../../seqtrak-songs/tools/tudu_write.py`](../../seqtrak-songs/tools/tudu_write.py),
driving `seqlink.py` (five retries per read, 2 ms between writes), with the
tempo at `30 40 76` read before and after as the control address.

### The synth piano roll carries velocity and gate values other than the defaults

`72 0p 00` was already verified with three notes at the step-record defaults.
This run wrote **twenty** events on SYNTH 1 — note numbers 51 to 63, velocities
90 to 110, gate times 120, 240, 360, 480 and 600 ticks, event times 60 to 4980
— and read all twenty back at `75 00 idx`.

| What varied | Values written | Read back |
|---|---|---|
| `eventTime` (14-bit) | 60, 420, 540 … 4980 | identical, all twenty |
| `noteNumber` | 51, 54, 56, 57, 58, 61, 63 | identical |
| `onVelocity` | 90, 92, 93, 95, 98, 100, 102, 104, 106, 110 | identical |
| `gateTime` (14-bit) | 120, 240, 360, 480, 600 | identical |

So the 14-bit MSB/LSB split holds for `gateTime` above one step as well as for
`eventTime`, and velocity is stored per event rather than per part. Index 20
replied with **zero data bytes**, which is how the end of a twenty-event list
was established rather than assumed.

The events were added in ascending time order and came back at indices 0-19 in
that same order. Whether the machine sorts an out-of-order insertion is **not**
established here — nothing was written out of order.

### `DeletePattern` reaches the native synth parts, and the slot travels in the data

`01 1p 37` had been seen once, clearing one pattern of five events on a
**re-typed** part. Here it was sent 66 times — six slots × eleven parts — with
no `PatternSelect` write anywhere in the loop, since the slot number is in the
data.

Afterwards every part's **currently selected** pattern was read back and found
empty: steps 0-15 at `70 (40|p) ss` on parts 0-4 (DRUM), and index 0 of the
piano roll on parts 5-10 (`25` for parts 5-6, `75` for 7-10).

| Parts | Read | Result |
|---|---|---|
| 0-4, DRUM | `70 (40\|p) 00`-`0F`, four attempts each | replied, zero data bytes, all 16 steps |
| 5-6, re-typed SYNTH | `25 (p<<4) 00`, five attempts | replied, zero data bytes |
| 8, native SYNTH 2 | `75 10 00`, five attempts | replied, zero data bytes |
| 9, DX (`PartAwmType` 4) | `75 20 00` | replied, zero data bytes |
| 10, SAMPLER (`PartAwmType` 5) | `75 30 00` | replied, zero data bytes |

**This is a positive measurement of emptiness, not an absence.** An empty step
and an empty piano-roll index both *reply*, with zero data bytes; the probe
distinguished that reply from a timeout and would have printed
`indetermine` for a silence. None appeared.

**The claim is bounded to the selected slot.** Six slots per part were cleared,
but only the selected one was read back on each part, so this run says nothing
about the other five. Clearing an unselected slot remains
`from the official app, untested`.

### `RemoveScene` survives ten consecutive removals

`71 20 00` had been seen once — scene 3 added and removed again. Project 0 held
eleven scenes from a previous session. Scenes 15 down to 1 were each read at
`71 40 sc` first and removed only if they answered with data; ten removals
followed, 300 ms apart.

All sixteen scene indices were then re-read, four attempts each: **only scene 0
answered with data.** Scene 0 was never asked to be removed, so whether a
project can be left with no scene at all is still open.

### Also written and read back

| Address | Written | Read back | Note |
|---|---|---|---|
| `30 40 76` Tempo | 89 | 89 | was 122; also the control address all run |
| `30 40 7A` PatternMasterStep | 48 | 48 | the CSV had a read, not a write |
| `30 5p 16` Pattern1Step, eleven parts | 48 | 48 on all eleven | adds 48 to the 12/14/16/32 already measured |
| `30 5p 10` Pattern1BarLength | 3 | **0**, on parts 0 and 7 | the write did not take — see below |
| `01 1p 33` CurrentSound, part 7 | Bank 63/11 + PC 108 | 1516 | catalogue number minus one, as documented |

### `30 5p 10` does not hold a bar length written to it

`Pattern1BarLength` was written as `3` on all eleven parts, in the same loop as
`30 5p 16` (`Pattern1Step`, written 48). Read back afterwards, five attempts
each: **`30 5p 16` reads 48 on all eleven parts, and `30 5p 10` reads 0 on parts
0 and 7.** `verified on hardware`.

The control is the companion write in the same loop: a transport fault would
have taken both fields down, and `30 5p 16` came back correct on every part. The
tempo at `30 40 76` was also read before and after and held at 89.

What this does **not** settle: the field was never read *before* the write, so
"the write was ignored" and "the write landed as 0" cannot be told apart here,
and only two of the eleven parts were re-read. The Data List gives the range as
`0 - 8`, so 0 is a legal value rather than an error code. The reference's own
`reserved` label for this address is consistent with the reading that the bar
length is derived from `Pattern1Step` rather than stored, but that is inference,
not measurement. `30 5p 16` is the field to write. Added to
[12-open-questions.md](12-open-questions.md).

`RemoveProjectAddress` (`01 40 00`) was **not** sent. "Emptying" project 0 here
means every part's pattern cleared and every scene but the first removed; track
types and the other parts' sound assignments were left exactly as they were.

## 2026-10-23, hardware session: why a freshly written track was silent, and two writes settled on the way

The melody written to SYNTH 1 above was correct in the piano roll and inaudible
on the machine. Two independent things were holding it down, neither of them in
the sequencer, and finding them settled `30 5p 00` and `71 1p 02` — both of
which had a definition from the official app and **no** hardware column.

### Two silencers, and they are not the same field

A read-only sweep of all eleven parts — track volume `30 5p 00`, mute
`30 5p 29`, sound volume `31 1p 14` — gave this:

| Part | `30 5p 00` TrackVolume | `30 5p 29` Mute | `31 1p 14` SoundVolume |
|---|---|---|---|
| 0-6 | 100 | 0 (off) | 66-108 |
| **7, 8, 9** | **0** | 0 (off) | 80-90 |
| 10 | 100 | 0 (off) | 60 |

And `SceneInfo` for scene 0 (`71 40 00`, 33 bytes) carried
`[0,0,0,0,0,0,1,1,1,1,1]` in bytes 14-24 — **parts 6 to 10 muted**.

So the track was silenced twice over, by two fields that look alike and are not:

- `30 5p 29` (`Mute` in the Data List, `OutputSelect` in the official app, `0`/`125`)
  read **0** on every part. It was not the mute in play.
- `30 5p 00` (`Volume`, 0-127) read **0** on part 7. This is the field that
  silences a track.
- the scene's own mute byte, reached by `71 1p 02`, is a **third** mechanism,
  and it was set even though `GeneralMode` read 0 — outside Song mode.

**A project that does not sound is not necessarily a sequencer problem.** Both
silencers were left behind by an earlier song written into the same slot, and
`DeletePattern` does not touch either: clearing every pattern of a project
leaves its volumes and its scene mutes exactly as they were.

### `30 5p 00` is the track volume — write verified

`verified on hardware`. Written `100` to part 7 where it read `0`, read back
`100`. Parts 0 and 6 were read before and after as witnesses and held at 100,
and the tempo at `30 40 76` held at 89 across the whole cycle.

### `71 1p 02` (`ChangeMute`) takes `<scene> <mute>` in the data — write verified

`verified on hardware`, and it confirms the composite-range reading in
[14-song-mode.md](14-song-mode.md#the-composite-maxima-confirm-it): the declared
maximum 1921 is `15 × 128 + 1`, scene and mute, not a scalar bound.

```
send    F0 43 10 7F 1C 0C 71 17 02 00 00 F7     part 7, scene 0, mute off
read    F0 43 30 7F 1C 0C 71 40 00 F7           SceneInfo, scene 0
before  … bytes 14-24 = 0 0 0 0 0 0 1 1 1 1 1
after   … bytes 14-24 = 0 0 0 0 0 0 1 0 1 1 1
```

Byte `14 + part` is the mute, part 0 at byte 14 — the indexing this repository
already described, now exercised by a write. **The ten other mute bytes did not
move**, which is what makes this a measurement of that byte rather than of the
message.

## 2026-11-05, hardware session: the loader takes seven seconds to acknowledge, and `0x64` is silent anyway

Read-only. Four loader-mode cycles on the one unit, with
`tools/loader_probe.py` and then a new `tools/loader_probe_timed.py` in the
sibling analysis project. Nothing was written: no `SendingStart`, no block
header, no block data, so no write path into flash was ever opened.

### What was established

| Claim | Evidence |
|---|---|
| The change-mode `64 00 00` with data `01` **is** acknowledged in loader mode | `← F0 43 10 7F 1C 0C 64 00 02 01 F7` at **+7.04 s** after the request |
| `0x64` answers no Parameter Request in loader mode, with the mode acknowledged | seven addresses, 2.5 s window each, nothing; Identity control answered in 0.01 s after **every** one, 7/7 |
| While a change-mode is pending, the loader answers nothing else | a run sending eight change-modes 0.65 s apart saw the Identity control silent 8/8, then answering once the ack had landed |
| Entering and leaving loader mode is reversible | four cycles, the unit back to `mm = 0A` (v2.0) and the `01 00 00` witness answering each time |

The addresses tried were `64 00 00`, `64 00 01`, `64 00 02`, `64 01 00`,
`64 01 03`, `64 02 00` and `64 06 00`.

### How three earlier runs got it wrong

This is the third time in this repository that a negative claim came from an
instrument that could not establish absence, and it is worth being concrete
about the shape of the error, because it was not a silly one.

The earlier probers listened for **0.25 s** after each request. The
acknowledgement arrives at **+7 s**. So it was never seen, and the runs
concluded "change-mode not acknowledged, `0x64` silent, inconclusive".

Worse, the third run — the one that finally put a control in the loop — caught
the acknowledgement *inside the listening window of an unrelated request*:

```
   64 06 00  -> F0 43 10 7F 1C 0C 64 00 02 01 F7
```

Read naively that says `64 06 00` answered, and it was briefly reported that
way. It did not. That was the change-mode acknowledgement from six seconds
earlier, credited to whichever request happened to be in flight when it
landed. **A reply is not attributable to a request unless the input was drained
before the send and the arrival time is known.**

What fixed it: a drain before every send, windows of seconds rather than
milliseconds, the arrival time printed for every message, and the control sent
after *each* probe rather than once at the start.

### Consequence

The reserve that
[09-firmware.md](09-firmware.md#what-the-hardware-has-actually-said-about-0x64)
carried is lifted, and it closes as a **firm negative**: there is no SysEx read
path into `0x64`, in normal mode or in loader mode. The resident loader's code
cannot be reached from the wire, so the signature question stays open and now
has no cheap instrument left — every remaining step either writes to the
machine or needs a hardware dump of the flash.

## 2026-11-05, hardware session: the seven-second acknowledgement reproduces, and the real transport works

Read-only in effect: the rehearsal mode of `tools/sysex_updater.py` enters
loader mode, enters update mode, waits for the acknowledgement and stops. No
block header, no block data, so no write path into flash was opened.

| Claim | Evidence |
|---|---|
| The mode acknowledgement arrives at **7.04 s** | reproduced to the hundredth, by two different tools on two runs — `loader_probe_timed.py` earlier, the updater's own transport now |
| `64 00 00` with data `01` is acknowledged by `64 00 02` with data `01` | `← F0 43 10 7F 1C 0C 64 00 02 01 F7` |
| The updater's transport reaches update mode unaided | witness, reboot, re-enumeration, settle, loader identity (byte 11 = `00`), mode, acknowledgement — every step first try |
| Leaving update mode and rebooting returns the unit to normal | identity back to `mm = 0A` (v2.0), `01 00 00` witness answering, battery `01 10 02` reading 100 % |
| Entering and leaving loader mode is reversible | **five** cycles now on this unit |

A timing that reproduces to the hundredth across two independently written
tools is worth more than the figure itself: it says the delay is something the
loader does deterministically, not scheduling noise. Any client in this space
needs windows of seconds. The 0.25-second windows that three earlier runs used
could not have seen it, which is what made those runs inconclusive.

What this does **not** touch: whether a block transfer works. The rehearsal
stops one step before the first header message, which is also the step that
arms a transfer. The create/acknowledge handshake order around each window is
still unestablished and still only a real transfer will settle it.

## 2026-11-05, hardware session: an interrupted firmware write, and the machine came back

**The most important result in this area, and it was not obtained on purpose.**
A real transfer of the official OS 2.00 file was interrupted by a defect in the
sender, leaving the unit with the `Installer` block fully sent (never written, as found on 2026-11-14) and the
`Program` block **9.9 % sent**. The machine then presented every symptom of
being bricked. It recovered completely.

### What was written, exactly

> **Corrected 2026-11-14: nothing was written.** The sender never sent the
> create request `64 01 02` and never handed over to the `Installer`, so the
> loader buffered the data and nothing reached flash. The table below records
> what was **sent**
> ([2026-11-14](#2026-11-14-hardware-session-the-first-complete-sysex-update-and-the-play-from-page-patch-works)).

| | |
|---|---|
| `Installer` | all 4 create cycles, 1,048,576 bytes, every window acknowledged |
| `Program` | **1,062,576 of 10,780,511 bytes** — 4 windows plus 4 packets of the fifth |
| Then | the device stopped answering flow control and the sender aborted |

The file was Yamaha's own, unmodified, and the **same version the unit was
already running** (`2.00.2`). So the partially rewritten region received its
own content. That is the mildest possible partial write, and it bounds what
this session can claim.

### The symptoms

- No reply to any SysEx: Identity Request and `01 00 00` both silent, probed for
  **two minutes** with 4-second windows. The USB port still enumerated.
- `[⏻/PLAY]` held normally did **not** power the unit off.

### The recovery

1. **Forced termination — hold `[⏻/PLAY]` + `[PROJECT↑]`** (User Guide §3.2.2,
   p. 22). This worked, and it is the step that saved the unit.
2. Power on normally. The machine hung for roughly **30 seconds**, then booted.
3. Everything was back: `mm = 0A` (v2.0), `FirmwareVersion` reading `02 00 00
   02` = 2.00.2 unchanged, tempo, sequencer state and speaker volume all
   answering, battery 100 %, **and the owner's projects intact**.

### What this changes

This document and [09-firmware.md](09-firmware.md) both carried the line that
**no recovery path could be verified to exist**. One now has been, for this
failure mode: an interrupted `Program` transfer is survivable, and forced
termination is the way out. Yamaha's own "if the unit becomes inoperable by
accident, run the updater again" is corroborated in spirit — the updater was
never re-run, and the unit recovered on its own.

### What it does not change

- **One unit, one run, and the mildest partial write there is**: identical
  content over identical content. It says nothing about recovering from a
  partial write of a *different* or *modified* image, which is the case that
  matters for custom firmware.
- The interruption happened in the `Program` phase. The `Installer` phase — the
  first 1.6 % of a transfer, whose destination in flash is still unknown — was
  not interrupted, so it remains the untested sliver.
- The USB-stick recovery (`[KICK]` + `[BAR LENGTH]` while switching on) was
  prepared but **never needed**, so it is still untested.

### The defect, recorded because it is the lesson

> **Overturned on 2026-11-14** ([below](#2026-11-14-hardware-session-the-sysex-transfer-stops-at-the-same-byte-every-time)).
> With every window at 20 seconds, a second transfer stopped at **the same
> byte**. The short timeout was a real defect, but it was **not** what stopped
> this transfer: the device stops answering there. The paragraph below is kept
> as it was written.

The sender's per-packet flow-control window was **5 seconds**, set in a file
written hours after this same session measured a **7.04-second** latency on this
unit, twice, with independently written tools — and made a point of it. A
timeout below a known latency is not a risk that materialised, it is a defect.
The device had almost certainly not stopped; the sender gave up.

The exit path compounded it: it sent the leave-mode command and the reboot 2 ms
apart, when a mode command takes about seven seconds and the loader answers
nothing else while one is pending. The reboot went nowhere, which is why the
unit was left hung rather than simply idle in update mode.

Both are fixed: every window is now 20 seconds, and the exit waits for its
acknowledgement before rebooting.

## 2026-11-14, hardware session: the SysEx transfer stops at the same byte every time

A second real transfer, this time of a **modified** file: the play-from-page
build ([09](09-firmware.md#a-play-from-page-patch-built-and-then-flashed-2026-11-14)),
sent by `tools/sysex_updater.py --write` with every window at 20 seconds. The
owner authorised the write. USB-C, Mac on mains, official app closed, battery
100 %.

| Step | Result |
|---|---|
| Witness `01 00 00`, reboot to loader, re-enumeration, loader identity (byte 11 = `00`) | each first try |
| Enter update mode | acknowledged after **7.04 s**, the same figure as on 2026-11-05 |
| `Installer`, 4 windows | all acknowledged |
| `Program`, windows 1 to 4 | all acknowledged |
| `Program`, window 5 | **no flow-control reply after its 4th packet**, in 20 s: **1,062,576 bytes** sent |
| Leave update mode | not acknowledged in 20 s; reboot sent anyway |
| Identity and `01 00 00` right after | silent, 4 tries each |

**1,062,576 bytes is exactly where the 2026-11-05 transfer stopped**: 4 windows
of 262,144 bytes plus 4 packets of 3,500. Two transfers, two different
`Program` streams and two different timeouts (5 s, then 20 s) both stop on the
same packet. So the stop is the **device's** behaviour at that point, not a
sender timeout. `verified on hardware`, two runs.

**Cause, found the same day, `from official app`:** the
sender skipped a stage. After the `Installer`, the official app leaves update
mode, lets the unit reboot into the freshly written `Installer`, checks that
the Identity Reply's byte 12 reads `02`, and enters update mode again before
sending the `Program` (details in
[09](09-firmware.md#there-is-no-sendingstart-command)). This repository's sender
went straight on, so the **resident loader** received the `Program` block. It
took 4 windows plus 4 packets, just over the `Installer`'s own 1 MiB, and then
stopped answering. The sender now does the hand-over, and refuses to send the
`Program` unless byte 12 reads `02`. Not yet run on hardware.

**Recovery, a second time.** Forced termination (`[⏻/PLAY]` + `[PROJECT↑]`),
then a normal power-on. The owner reports that the machine started and that
nothing was lost. Then, read back: identity `mm = 0A`, `FirmwareVersion`
`02 00 00 02` = 2.00.2, battery 100 %. `verified on hardware`.

**What this recovery does and does not say.** Found later the same day:
the sender also never sent the create request `64 01 02`, so **nothing was
written to flash at all**, by this run or the earlier one. The loader buffered
about 1 MiB and stopped answering. What was survived is a stalled transfer,
not a partial write. Surviving an interrupted write is still untested.

**The patch is not installed.** The cable route cannot install anything until
the window-5 stop is understood. The USB-stick route is the one a third party
reports working with a modified `Program`.

## 2026-11-14, hardware session: the first complete SysEx update, and the play-from-page patch works

Same day, same unit, owner's go-ahead. Three more runs of the corrected sender,
each one closer to the official app; the third went through.

| Run | Sender | Result |
|---|---|---|
| 3 | hand-over to the `Installer` added | stopped before the `Program`: after leaving the loader, identity byte 12 still read `01`. Nothing of the `Program` sent |
| 4 | waits for `64 01 03` at the end of each 256 KiB window | no `64 01 03` in 60 s after window 1: the window ended on `64 01 00`. Then, on the next attempt, `64 01 05` (error) right after the first header |
| **5** | **one header per block, `64 01 02` once at the end of the block** | **complete** |

Run 5, `verified on hardware`:

| Step | Observed |
|---|---|
| Loader, update mode | acknowledged at **7.04 s** (third session with this exact figure) |
| `Installer`, one header, 300 packets, then `64 01 02` | `64 01 03` at once |
| Leave update mode | the **port vanished 0.51 s later** (no `64 02 00` seen) |
| Identity after re-enumeration | `F0 7E 7F 06 02 43 00 41 64 06 00 00 02 7F F7`: **byte 12 = `02`, the `Installer`**, first time seen |
| Enter update mode on the `Installer` | `64 00 02 01`, **immediately** (the loader takes 7 s) |
| `Program`, one header, 3,111 packets across 42 windows, then `64 01 02` | `64 01 00` after every packet, `64 01 03` at once |
| Leave update mode, reboot | normal mode: identity `mm = 0A`, `FirmwareVersion` `02 00 00 02`, battery 100 % |

So the full protocol is the one in
[09](09-firmware.md#there-is-no-sendingstart-command), and every earlier run
was missing a piece of it: the create request `64 01 02`, one header per block
(not per window), and the hand-over to the `Installer`. None of the earlier runs
wrote anything to flash, which is why every one of them was survived.

**The patch works**, reported by the owner: on a track with a melody over
several pages, with the sequencer stopped, `[PAGE]` to page 2, then
`[⏻/PLAY]`, and playback started at page 2. The modified `Program` was
therefore accepted over SysEx too, with no signature in the way.

**One oddity, not explained.** On a song the owner had made before, the
melody already spanned several pages but the track showed **one** page, and
`[BAR LENGTH]` had to be pressed to see the others. The patch writes nothing
related to length (its two hooks touch only the start position), so it is
*inferred* not to be the cause; not tested against the stock firmware. A read
of the loaded project in the same session found `Pattern 1 Bar Length`
(`30 5p 10`) = 0 on all eleven tracks while `Pattern 1 Step` (`30 5p 16`)
ranged from 8 to 64: the displayed page count follows the step length, not
that field. Which project the owner had played, and its lengths before the
change, were not captured. Afterwards, on the patched firmware, the owner
switched to another project with several pages and saw all of them at once:
the patched firmware shows multi-page patterns normally, which points to the
first song's own lengths rather than to the patch (*inferred*).

## 2026-11-15, hardware session: two failed updates with the MiniLab patch, and a second recovery by forced termination

Same unit, owner's go-ahead, the sender that completed run 5 on 2026-11-14
(`tools/sysex_updater.py --write`), the file `8Z33OS_pfp_minilab.PGM`
(play-from-page plus the MiniLab patch,
[09](09-firmware.md#the-minilab-3-patch-built-and-not-flashed-2026-11-15)).
The dry run against the simulated receiver passed first. **Neither run
completed, and the patch was not shown to be running afterwards.**

| Run | Observed | Marker |
|---|---|---|
| 1 | Loader, update mode acknowledged at **7.04 s**. `Installer` created. Leave update mode: `64 02 00` at +3.44 s (run 5 saw the port vanish at +0.51 s instead), identity byte 12 = `02`. `Program`: `64 01 00` after every packet of windows 1-41 and of the first 35 packets of window 42. **No `64 01 00` in 20 s after the last packet** (packet 35 of window 42, 270 bytes, all 10,870,674 bytes sent). No `64 01 05` either. The create request `64 01 02` was therefore **never sent**. Exit acknowledged; the unit came back in normal mode, identity `mm = 0A`, `FirmwareVersion` `02 00 00 02`, tempo readable | `verified on hardware` |
| 2 | Same file, a few minutes later, the sender changed only to log stray replies and wait 60 s on a block's last packet. Loader at 7.04 s, `Installer` created, leave update mode: port gone at +1.01 s, and **it never came back** (watched for more than a minute; no USB device at all). The owner: the unit "does not react at all any more" | `verified on hardware` |
| Recovery | Forced termination `[⏻/PLAY]` + `[PROJECT↑]`, then a normal power-on: the port was back 28.7 s after the watch started, identity `mm = 0A`, `FirmwareVersion` `02 00 00 02`, tempo `00 61`, and the owner reports a normal start | `verified on hardware` |

**What this establishes.** The forced termination recovers the unit from a
hang **after the `Installer` block was created** (run 2). The 2026-11-05
recovery was from a stalled transfer before any create; this one is a step
further. It still says nothing about an interrupted `Program` write.

**What it does not establish:**

- **Which `Program` the unit is running.** After the recovery, a cumulative
  counter on the USB port (150 s, every message keyed by type) saw 26 sound
  changes on channel 8, each as CC 0 + CC 32 + Program Change, and **zero**
  SysEx with Arturia's manufacturer ID. That is what the unpatched firmware
  would do, and also what the patched one would do if its hook is not on the
  Sound Select path or its transmit does not reach USB. The create request
  was never sent in run 1, so the old `Program` still running is the simpler
  reading (*inferred*).
- **Why run 1's last packet got no flow-control reply.** The two files end
  the same way (the LZSS stream stops cleanly mid-group in both), and every
  earlier packet was acknowledged. What differs from run 5: the last packet
  carries 270 bytes instead of 28, and the stream is 242 bytes longer. Not
  explained.
- **Why run 2 hung at the hand-over.** The `Installer` block is byte-identical
  to the one that handed over correctly in run 1 and in run 5. The only
  difference found is history: run 2 followed a `Program` transfer that had
  been abandoned without a create. Not explained.

The sender now keeps the last stray replies and prints them when a wait fails
(`fw_midi.py`); run 2 failed before that could say anything.

### What the `Installer`'s code says about run 1 (static, same day)

`from firmware image (static analysis)`: the `Installer` block read in ARM mode
at `0x10000000` (`seqtrak-firmware-analysis/tools/installer_tools.py`).
Nothing was sent to the unit for this.

| Item | Address | What the image shows |
|---|---|---|
| Block-data handler `64 02 02` | `0x10003380` | checks the packet number against the counter at state `+5` (mismatch → error `0x0F`), unpacks (`0x100031CC`, 0 → error `0x10`), hands the bytes to `0x10000C2C` (negative → error `0x11`), and **only then** sends `64 01 00` (template at `0x10064850`) |
| Error reply | `0x10003340` | sends the template at `0x100648A8`, which is `64 01 05`, and stores the code at state `+8` |
| Accumulate and write | `0x10000C2C` | drops the 4-byte length prefix of a compressed block, stages input 256 KiB at a time, decompresses (`0x10002A6C`) into one output buffer at `0x101C1EBC`, and does **nothing else until the received count reaches header `+0x7C`** (or the output reaches 64 MiB). On that last call it runs the per-type check (`+4` of the type's entry in `0x1006D570`: the `#8Z33` tag and the sum) and then `0x10000688` |
| Write | `0x10000688` | the type's `+0xC` hook, then four stages with a progress callback each (`0x1000241C`; `0x1000258C`; `0x10002774`, failure → `5`; `0x1000286C`, failure → `6`; `0x1000258C` again, failure → `7`), then the type's `+0x10` hook. Read as erase, program and verify (*inferred* from the shape; the leaf routines were not read) |
| Create request `64 01 02` | `0x1000350C` | compares two counters (error `0x12` if they differ), sends `64 01 03`, sets a flag, and calls two routines that only loop over a table sending 4-byte tuples to `0x10037B88` (*inferred*: the LEDs) |
| Leave update mode | `0x10003598` | with the create flag set, the same kind of LED loop (`0x10001B30`); without it, the other two. No write was found in either path |

**So the whole `Program` is written inside the handler of the block's last
packet, before that packet's `64 01 00`.** The create request that follows
writes nothing. This changes the reading of run 1:

- the missing reply is most simply the write still running when the sender's
  20-second window closed (*inferred*; run 5's write must then have finished
  inside 20 s, and that run logged no times, so the two cannot be compared);
- the leave-mode acknowledgement arrived afterwards, which a busy handler
  could not have sent, so the write had returned by then, without an error
  reply (*inferred*);
- **the patched `Program` is therefore most likely on the unit since run 1**,
  and run 2 changed nothing in it. The sentence above calling the old
  `Program` "the simpler reading" is withdrawn.

If that is right, the 26 sound changes with no Arturia SysEx mean cave N is
not doing its job: the Sound Select path does not reach the hook, or the
transmit does not reach USB. Both were listed as assumptions of the build.
It also means cave N ran, or was bypassed, 26 times without disturbing the
unit.

**Not settled, and not attempted:** a reversible test that would tell the two
firmwares apart from the host (arm cave T with CC 9 on channel 1, send CC 19
on channel 1, see whether KICK's pan moves, restore with CC 10). It is a
write, and the owner had agreed to a read-only investigation.

Run 2's hang at the hand-over is still unexplained.

The sender now waits 300 s for the reply to a block's last packet
(`LAST_PACKET_WINDOW` in `fw_midi.py`).

### Settled the same day: the patched `Program` is running, and cave T works

Owner's go-ahead for a reversible write. Host on the USB port, Parameter
Requests with four tries each, tempo `30 40 76` as the witness in every
snapshot, restore in a `finally`.

| Step | `30 50 01` (KICK pan) | `31 10 15` | Tempo |
|---|---|---|---|
| Before | `40` | `40` | `00 61` |
| Control: CC 10, channel 1, value `50` | **`50`** | `40` | `00 61` |
| Control restored: CC 10 = `40` | `40` | `40` | `00 61` |
| CC 19, channel 1, value `20`, **before** any CC 9 | `40` | `40` | `00 61` |
| CC 9 on channel 1 (127, then 0), then CC 19 = `20` | **`20`** | `40` | `00 61` |
| Restored: CC 10 = `40` | `40` | `40` | `00 61` |

`verified on hardware`:

- **The MiniLab patch is on the unit.** CC 19 is not in the SEQTRAK's CC map
  and did nothing until CC 9 had been seen; after it, CC 19 moved KICK's pan
  exactly as CC 10 does. Only cave T does that. So run 1 did write the
  `Program`, as the static reading predicted, and **a `Program` block is
  complete once its last packet has been received; the create request is not
  needed for the write**.
- **Cave T works**: arming on CC 9, the table (CC 19 → CC 10), and the
  default current track (channel 1).
- **CC 10 on a track's channel writes `30 5p 01`** (Project Track Pan), not
  the sound's own pan `31 1p 15`. New for [cc-map](../data/cc-map.csv).

**Why no sound name was sent** (`from firmware image (static analysis)`).
The build's claim that `0x20143948` is the only site that transmits a Bank
Select was wrong: it listed the callers of `0x2013BA04`, not the callers of
the port routine under it. The port-level Bank Select + Program Change
(`0x203C6308`) has **17** call sites. Five are in the UI code
(`0x200CC4F4`, `0x200CC640`, `0x200CC75C`, `0x200CC810`, `0x200CC888`, in
routines reached from `0x200D4680`), which calls it directly on its own port
object (`[ui+0x20]`) with the part as the channel: `0x200CC640` and
`0x200CC75C` pass MSB `0x3F` (factory sound), `0x200CC4F4` MSB `0x3E`, and
the other two `part type | 0x20`. The Sound Select knob is *inferred* to go
through these, not through the engine's event emitter. This is the
negative-claim rule again: "the only site" needed a search of every caller
of the lowest routine.

**A second build** hooks the two MSB `0x3F` sites as well (cave U): it builds
the same message, copies it into the port's SysEx buffer (`[port+0x38] + 4`,
skipped if the buffer does not exist yet) and queues it with the port routine
`0x203C6460(port, len, 0)`, the way the UI's own sender at `0x200A8494` does,
then continues into `0x203C6308`. Checked off-device like the first
(`minilab_patch_check.py`: 2,032 messages equal the model, nothing sent
without a buffer or for another MSB, registers and stack preserved). Image
sha256 `307d6745…bd9dd6`, file `8Z33OS_pfp_minilab2.PGM`. **Not flashed.**

### Runs 3 and 4: two complete updates, the write time measured, and the sound name on the wire

Same day, owner's go-ahead for each. The sender now waits 300 s for the reply
to a block's last packet and prints how long it took.

| Run | File | Last `Installer` packet | Last `Program` packet | Result |
|---|---|---|---|---|
| 3 | `8Z33OS_pfp_minilab2.PGM` | answered after 0.01 s | answered after **20.73 s** | complete, `64 01 03` at once after the create request |
| 4 | `8Z33OS_pfp_minilab3.PGM` | 0.02 s | **18.90 s** | complete |

`verified on hardware`:

- **The `Program` write takes about 19 to 21 seconds and happens before the
  reply to the block's last packet.** That is the cause of run 1's failure:
  the old 20-second window sits inside that range. Run 5 of 2026-11-14 passed
  under it by luck.
- After the create request, **leave update mode was not acknowledged within
  20 s** in either run; the reboot command was sent anyway and the unit came
  back in normal mode both times (identity `mm = 0A`, `FirmwareVersion`
  `02 00 00 02`, tempo `00 61`). Run 5 of 2026-11-14 logged an
  acknowledgement there. Not explained.
- Right after run 4's reboot, `FirmwareVersion` did not answer in five tries
  and the tempo answered on the fourth; ten seconds later everything answered
  on the first try. Read as the unit still starting (*inferred*).
- The hand-over to the `Installer` worked in both runs (port gone at +0.51 s
  and +1.51 s). Run 2's hang did not recur and is still unexplained.

**Run 3's build did not send the name.** Four sound changes on SYNTH 1 with
the Sound Select knob, counted cumulatively on the USB port: 4 × (CC 0, CC 32,
Program Change), **0** SysEx with Arturia's ID. So the knob does not go
through `0x200CC640` / `0x200CC75C` either.

**The knob's handler is `0x200DEFF0`** (`from firmware image (static
analysis)`): a method of a per-part object (part at `+0x10`, current sound at
`+0x12`) that takes the port and a signed step, computes the next or previous
sound (`0x20278C94` / `0x20278D5C`), and, if it changed, calls
`0x203C6308(port, part, program, 0x3F, LSB, 0)` at **`0x200DF084`**. Its two
siblings do the same for MSB `part type | 0x20` (`0x200DF2CC`) and MSB `0x3E`
(`0x200DF3EC`).

**Run 4's build hooks `0x200DF084` as well, and the name is sent**,
`verified on hardware`: 19 sound changes with the knob (SYNTH 1), same
cumulative counter, **27** SysEx with Arturia's ID, each
`F0 00 20 6B 7F 42 04 01 60 01 <name> 00 02 SYNTH 1 00 F7` with a name from
the preset list (`Space Walking`, `Industrial`, `Outer Planet`, `Perplex`,
`Metamorphosis`, `Men In Yellow`, `InsideTheWormhole`, `Blaster Beam`,
`Lost in Asia [Arp]`, `Nibelungen [Arp]`, `J-Pop [Arp]`, `Celesta [Arp]`
were the last twelve). The owner reports the unit behaving normally.

Not established by this: why 27 messages for 19 Program Changes (the name
may be sent by more than one of the hooks for some changes, or some Program
Changes were not transmitted; the capture did not pair them); the KICK
changes the owner made do not appear in the last twelve Program Changes kept
by the capture; and **nothing has been seen on the MiniLab's screen yet**:
the capture was on the USB port with a computer as host, not with the
MiniLab attached.

### The name on the MiniLab's screen (owner's report, same day)

The MiniLab 3 plugged into the SEQTRAK's USB-C port, in its Arturia program,
third build of the patch on the SEQTRAK: **the owner reports that the sound
name is displayed** when Sound Select is turned. `verified on hardware`, by
the owner reading the screen; which sounds and how many were not recorded.

Two things follow:

- the name message reaches the device attached in host mode, not only a
  computer in device mode;
- **the MiniLab needs no DAW connect message** to show family `01` text in
  its Arturia program: it had been powered off and on again (it is powered by
  the SEQTRAK) since the last connect message was sent to it, and the patch
  sends none.

Not reported yet: the translated controls with the MiniLab attached
(`Shift` + key, a note, then the encoders, faders and pads). The translation
itself was measured from a computer above.

### Run 5: the fourth build, and what it sends

Same day, owner's go-ahead. `8Z33OS_pfp_minilab4.PGM`
([09](09-firmware.md#the-minilab-3-patch-fourth-build-the-screen-follows-the-track-and-the-control-2026-11-15)),
battery 90 %.

| Step | Observed | Marker |
|---|---|---|
| Update | complete. Last `Program` packet answered after **20.80 s**. Leave update mode again not acknowledged within 20 s | `verified on hardware` |
| After the reboot | identity `mm = 0A`, `FirmwareVersion` `02 00 00 02`, tempo `00 61`, each on the first try once the port had been stable for 12 s | `verified on hardware` |
| The periodic hook | the unit starts and runs normally with a cave called from the manager's update (owner's report, and everything below) | `verified on hardware` |
| MiniLab attached, Arturia program | the owner reports the **parameter names shown when the encoders are turned**, and the track name shown, but **no sound name** | `verified on hardware`, owner reading the screen |

A capture with a computer as host then showed what is sent, every message in
order with its time (`SCREEN` is the Arturia SysEx, as `line 1 / line 2`):

| Gesture | Sent |
|---|---|
| Select SYNTH 1 (first time since power-on) | `01 10 27` = `07`, then ` / SYNTH 1` 30 ms later |
| Sound Select on SYNTH 1, three steps | `Lost in Asia [Arp] / SYNTH 1`, `Blaster Beam / SYNTH 1`, `InsideTheWormhole / SYNTH 1`, each 20-30 ms **before** its Program Change (channel 8, MSB 63, LSB 14, programs 98-100) |
| Select KICK | `01 10 27` = `00`, then ` / KICK` |
| Sound Select on KICK, three steps | `Tight Punchy Kick 2`, `3`, `4` ` / KICK`, with Program Changes on channel 1, MSB 63, LSB 0, programs 1-3 |
| Select DX, Sound Select twice | ` / DX`, then `FM Digital Brass / DX`, `FM Brass / DX` (channel 10, MSB 63, LSB 15, programs 74, 75) |
| Select SYNTH 1, KICK, DX again | `InsideTheWormhole / SYNTH 1`, `Tight Punchy Kick 4 / KICK`, `FM Brass / DX` |

`verified on hardware`, all of it:

- **Cave P works**: it follows the selected track, within about 30 ms.
- **`01 10 27` is the selected track**, broadcast on selection: `07`, `00`,
  `09` for SYNTH 1, KICK, DX. (`from official app` until now.)
- **The knob handler `0x200DEFF0` serves drum, synth and DX tracks alike**:
  names were sent for all three.
- The catalogue arithmetic `k = LSB × 128 + program` gives the right name on
  all three engines.
- The owner's "no sound name" is the limit the build was known to have: a
  track shows its sound only after that sound has been changed since
  power-on. It is not a fault in what is sent.

### A fifth build, not flashed: learn each track's sound without a change

`from firmware image (static analysis)`. The Sound Select knob object (vtable
at `0x203C8BB8`: `+0x8` the step handler `0x200DEFF0`, `+0xC` a setter
`0x200DDCFC`) is built with its current sound at `+0x12` set to **0**
(`0x200E87C0`, and the stand-alone constructor `0x200E204C`), its track at
`+0x10`, and at `+8` the track's model block (`[model+0x1D0] + track × 0xF8 +
0x38`). It is then handed to a binding routine (`0x200E8448`). The setter,
`strh r2, [r0, #0x12]` then the object's `+0x10` method, is the only other
writer of `+0x12` in this class. So the real sound reaches the object through
the setter (*inferred*: the binding was not read).

The fifth build replaces the setter's first instruction with a branch to a
seven-instruction cave that stores the sound for the object's track, replays
the instruction and continues. Checked like the others (the setter is part of
the 60,000-step random run; values of 2,032 and above are treated as
unknown). Image sha256 in the build log; file `8Z33OS_pfp_minilab5.PGM`.

Not established: **when** the firmware calls the setter. If it is not called
at start-up and project load for every track, this build changes nothing
visible.

### Runs 6 and 7: the fifth build, a second stop at the hand-over, and the sound known without a change

Same day, owner's go-ahead. `8Z33OS_pfp_minilab5.PGM`, image sha256
`7b32bfc0…48ac77a`.

| Run | Observed | Marker |
|---|---|---|
| 6 | Loader at 7.04 s, `Installer` created, leave update mode: port gone at +1.01 s and **never back** (watched 45 s). Nothing of the `Program` sent. The owner then started the unit **with an ordinary long press on `[⏻/PLAY]`**, no forced termination; identity `mm = 0A` 35 s into the watch | `verified on hardware` |
| 7 | Same file, a minute later: hand-over at +0.50 s, last `Program` packet answered after **20.23 s**, complete. Normal mode afterwards, version and tempo on the first try | `verified on hardware` |

**The hand-over failure is the unit switching off, not hanging** (*inferred*
from run 6: a plain power-on brought it back). That re-reads run 2 of this
morning, where the forced termination was used without first trying a plain
power-on. Two occurrences in seven hand-overs today, both logged as "port
gone at +1.01 s"; the five that worked logged +0.50 s, +0.51 s (twice),
+1.51 s and a `64 02 00` at +3.44 s. The sender polls every 0.5 s, so this is
not a timing measurement. Cause unknown. Nothing is lost when it happens: the
`Program` has not been touched, and the update can simply be started again.

**Cave S works**, `verified on hardware`. After run 7, with no sound changed
since the reboot, a capture with a computer as host (every message in order):

| Selected | `01 10 27` | Screen message, 20-40 ms later |
|---|---|---|
| KICK | `00` | `Tight Punchy Kick 4 / KICK` |
| SNARE | `01` | `Bright Clap 1 / SNARE` |
| HAT 1 | `03` | `Tight Closed Hat 1 / HAT 1` |
| HAT 2 | `04` | `Bright Open Hat 1 / HAT 2` |
| SYNTH 1 | `07` | `InsideTheWormhole / SYNTH 1` |
| SYNTH 2 | `08` | `More Fatty / SYNTH 2` |
| PERC 2 | `06` | `Shaker 1 / PERC 2` |

So the firmware does call the knob object's setter `0x200DDCFC` for each
track at start-up, with the track's current sound, and the fifth build knows
every track's sound without a change. KICK and SYNTH 1 show the sounds the
owner had left on them before the reboot. The names for the other tracks
were not compared with an independent read of `01 1p 33`.

An earlier seven-minute capture in this session recorded nothing at all, not
even `01 10 27`, with the port listed; the unit had most likely been
unplugged and plugged back while the listener held the old port. It is
recorded as void, not as silence from the unit.

**The fifth build with the MiniLab attached** (owner's report, same day).
First attempt: nothing at all on the MiniLab's screen, not even when a fader
was moved. After unplugging the MiniLab and plugging it back: it works. The
owner did not say which program the MiniLab was in during the empty-screen
episode, or whether `Shift` had been pressed since the SEQTRAK's reboot, so
the cause is not established. Two things are lost at every SEQTRAK reboot and
either would give an empty screen: the MiniLab, powered by the SEQTRAK,
restarts and may not come back in its Arturia program; and cave T is
disarmed until CC 9 is seen again.

### Run 8: the sixth build, and the main encoder steps the pattern

Same day, owner's go-ahead. `8Z33OS_pfp_minilab6.PGM`, image sha256
`a697d1da…3c967f`, battery 95 %. Complete on the first try: hand-over with a
`64 02 00` at +3.44 s, last `Program` packet answered after **20.20 s**. Normal
mode afterwards.

Then from a computer on the USB port, sequencer stopped (`01 10 20` = 0),
Parameter Requests with four tries, the screen messages captured in the same
loop:

| Sent on channel 1 | Screen message | `30 50 0F` (KICK) | `30 57 0F` (SYNTH 1) |
|---|---|---|---|
| (before) | | `00` | `00` |
| CC 114 = 65, **before** any CC 9 | none | `00` | `00` |
| CC 9, then CC 114 = 65 | `KICK Pattern / 2` | `01` | `00` |
| CC 114 = 65 | `KICK Pattern / 3` | `02` | `00` |
| CC 115, CC 113, CC 112 | none | `02` | `00` |
| (restored by Parameter Change) | | `00` | `00` |
| CC 114 = 66 | `KICK Pattern / 2` | `01` | |
| CC 114 = 62 | `KICK Pattern / 1` | `00` | |
| CC 114 = 62 again, at pattern 1 | none | `00` | |
| CC 114 = 65 six times, 10 ms apart | `KICK Pattern / 2`, once | `01` | |

`verified on hardware`: the firmware's own pattern routine `0x200CD0F4` can
be called from the periodic hook; the step goes both ways; nothing happens
below pattern 1; the 200 ms limit holds; the other track did not move.

**A side effect of this test, not undone.** The first message, CC 114 = 65
before arming, reached the unit as an ordinary controller, and CC 114 is
*Send Delay Assigned Parameter 2*. Its previous value was not read, so it was
not restored. The test should have armed first, or read `30 42` before.

Not tested: a step while the sequencer runs (the queued path, row `0xEB`);
patterns 4-6 with Pattern Select Mode normal; the encoder itself, with the
MiniLab attached.

## 2026-11-15: `01 10 21` is writable while the sequencer plays

A third party reported that writing `01 10 21` (`RecordingStatus`) arms and
stops recording
([12-open-questions.md](12-open-questions.md#opened-by-a-third-party-receive-side-report-2026-11-14)).
Run here over USB with
[`tools/hardware-probe/receive_side.py`](../tools/hardware-probe/receive_side.py):
every state below is three Parameter Requests — `01 10 20`, `01 10 21` and the
tempo `30 40 76` as a control — each retried up to five times. The tempo
answered 137 at every one of the eleven states read over the two runs (stopped, then playing), so no reply was lost. The
sequencer was started and stopped from the host with `FA` / `FC`.

| Sequencer | Sent | `01 10 20` read back | `01 10 21` read back |
|---|---|---|---|
| stopped | — | 0 | 0 |
| stopped | `F0 43 10 7F 1C 0C 01 10 21 01 F7` | 0 | **0** |
| stopped | `… 01 10 21 00 F7` | 0 | 0 |
| playing (after `FA`) | — | 1 | 0 |
| playing | `… 01 10 21 01 F7` | 1 | **1** |
| playing | `… 01 10 21 00 F7` | 1 | **0** |
| playing | `… 01 10 21 01 F7` | 1 | **1** |
| playing | `… 01 10 21 00 F7` | 1 | **0** |
| stopped (after `FC`) | — | 0 | 0 |

`verified on hardware`:

- **`01 10 21` is a command as well as a status.** While the sequencer plays,
  the value written is the value read back, in both directions, twice.
- **With the sequencer stopped, writing 1 is not taken**: it still reads 0 1.5 s
  later, and the sequencer does not start. So the write does not behave like a
  press of `[REC]` from a stopped machine, which the third party's report does
  not distinguish.
- **The write is not echoed.** In the 1.5 s after each write the machine sent
  note messages from the playing pattern and no SysEx at all.
- Writing it does not disturb `01 10 20`.

Not established, and not to be read into the above:

- that the machine **records notes** while `01 10 21` reads 1. No key was
  pressed and no pattern was read back; only the status was observed;
- what the front panel shows — nobody was watching `[REC]`;
- that `[REC]` *emits* this address. That is a separate claim, still only
  reported;
- the stopped case is one attempt. It is a negative result supported by a
  read-back with a control, not by repetition.

## 2026-11-15: a Program Change needs its own Bank Select, every time

The same third-party report said a bare Program Change does nothing on the DX
track. Run here over USB with `receive_side.py --pc --part 9`, sequencer
stopped. The instrument is `01 19 33` (`CurrentSound`, catalogue number − 1),
read 0.5 s after each step and retried up to five times; the tempo control read
137 at the end.

| Step | Sent on channel 10 (part 9, DX) | `01 19 33` read back |
|---|---|---|
| before | — | 1961 (bank LSB 15, program 41) |
| A | `C9 2A` — Program Change 42 alone | **1961**, unchanged |
| B | `B9 00 3F`, `B9 20 0F`, `C9 2B` — MSB 63, LSB 15, Program Change 43 | **1963**, as predicted (15 × 128 + 43) |
| C | `C9 2C` — Program Change 44 alone, straight after B | **1963**, unchanged |
| restore | `B9 00 3F`, `B9 20 0F`, `C9 29` | 1961 |

`verified on hardware`, on part 9:

- **A Program Change with no Bank Select before it is ignored.** Step A is a
  negative result, and the instrument can carry it: the same read moved in step
  B and moved back on restore, in the same run.
- **The bank is not latched on the channel.** Step C came one message after a
  complete triplet and was ignored all the same. The Bank Select pair is
  consumed by the Program Change that follows it.
- The triplet selects the predicted sound — a further confirmation of
  [the bank arithmetic](06-sounds-presets.md#reading-back-which-sound-is-loaded).

Limits: one part (DX), one run, USB. Not tried: `CC 32` + Program Change
without `CC 0`; a drum or synth part; a bank pair sent some time before the
Program Change rather than immediately; the System switches `00 00 07` /
`00 00 08`. A bare Program Change could in principle have changed something
that `01 19 33` does not report; nothing suggests it, and nobody listened.


## 2026-11-23 hardware session — an AWM element really does play a user wave

The claim this project had been circling since 2026-11-21 is now measured: a
**non-SAMPLER element reaches user wave memory**, and the number it points at is
the one written in the `.Y3S` that put it there.

A clavioline note was rendered offline, imported as a WAV onto **SYNTH 2**
(part 8) through the official app, and that sound exported as a `.Y3S`. The
file was dissected, then the machine was asked what it was holding.

### The reads

One process, port held open, MIDI clock and active sensing filtered, four
attempts per address, the tempo as control at both ends of the loop. **44 of 44
replies.**

| Address | Read | Means |
|---|---|---|
| `30 40 76` | `00 78` | **control** — 120 BPM, 4/4 at the start and again at the end |
| `41 08 01` | **`01`** | SYNTH 2 element 0 `Wave Select` = **User** |
| `41 08 03` | `03 11` | its `Wave Number` = **401** |
| `41 07 01` | `00` | **witness** — SYNTH 1 element 0 is on a *preset* wave |
| `41 07 03` | `03 7F` | witness — preset wave 511 |
| `41 00 01` | `00` | **witness** — KICK element 0 is on a preset wave |
| `01 18 33` | `20 04` | SYNTH 2 `CurrentSound` = **4100** |
| `01 10 20` | `00` | sequencer stopped |
| `01 10 01` | `00` | not in contents-management mode |
| `01 10 15` | `00` | current project 0 — UI "project 1" is `0` on the wire |

Two witnesses that must not move read the opposite value in the same loop, so
`41 ep 01` is read as a per-element field and not as something global.
`verified on hardware`.

### Three numbers that match the file, exactly

This is the part worth keeping. The `.Y3S` exported from this very sound was
parsed independently, before any of these reads:

| Quantity | In the file | On the machine |
|---|---|---|
| the element's wave reference | `401`, as `ContentNumber − 8192` = 8593 − 8192 | `41 08 03` = **401** |
| the sound's content number | `<ContentNumber>4100</ContentNumber>` in `sound.xml` | `01 18 33` = **4100** |
| the element's wave kind | a user waveform shipped in the package | `41 08 01` = **1 (User)** |

So the third party's rule — that an element refers to a user waveform as
`ContentNumber − 8192` — is no longer only *reported*: it is **verified on
hardware** for this case. The sound's number and its file's `<ContentNumber>`
are also equal, but see
[the later entry](#the-same-session-what-a-refusal-names-and-a-namespace-that-is-not-what-it-looks-like):
a content dump request for sound 4100 finds nothing, so that equality is not
evidence that the two namespaces are the same.

### What this retires

- **"Can a non-SAMPLER element point at a user wave?"** — yes, measured, for an
  AWM2 **synth** part over SysEx. The Data List's note that only the SAMPLER
  track is *fixed* to User is confirmed by implication: the others choose, and
  this one chose.
- The same question for a **drum** part (0-6) is still open. Nothing here
  touched one, and the two drum witnesses read `00`.

### A measurement fault, named so it is not repeated

For two days the machine "did not answer" Parameter Requests while answering
Identity Requests. Two causal stories were floated and **both were wrong**:
that contents-management mode suspends the parameter path, and that a Parameter
Change wakes it for a window. Neither survived its test — writing
`01 10 01 = 1` did not reproduce the silence, and the path answered for 30 s
with no write at all.

The cause was the **instrument**. The silent runs invoked a fresh process per
request, opening and closing the MIDI port each time, with no filtering, while
the machine was emitting MIDI clock continuously — about 48 `F8` a second,
**with the sequencer stopped** (`01 10 20` = `00`, measured above). Holding one
port open and filtering timing bytes made every address answer 4/4 immediately.

This is the third time this repository has been bitten by its own measuring
chain, after the two overturned negative claims. The rule it adds:

> **An open-and-close-per-request prober is not a valid instrument while the
> machine is flooding the port.** Hold the port open for the whole run and
> filter timing and active-sensing bytes. A one-shot probe is fine on a quiet
> link and misleading on a busy one — and the link is busy whenever clock is
> running, which is **not** the same as the sequencer running.

## 2026-11-23, later — the content channel works, and the audio comes back byte for byte

The whole read path of the content channel was exercised on a real unit, and
the sample that came back is **identical to the file the official app had
exported from the same sound**. Everything in this section is
`verified on hardware`.

### The request, refused and then accepted

The request form recovered from the official app was sent verbatim:

```
F0 43 20 7F 1C 0C 05 43 11 F7     ; ah 05 = Waveform, content number 8593
```

`am = 0x43`, `al = 0x11` by the documented rule — `((8593 >> 7) | 0x40) & 0x7F`
and `8593 & 0x7F`. The machine accepted the address and echoed it back, so the
rule is measured, not inferred.

**Outside contents-management mode it refuses, and names the reason:**

```
F0 43 00 7F 1C 00 0C 0C 01 22 00 09 05 43 11 00 … F7      (21 bytes)
```

- result **`09` = `NotContentManagementMode`** — the first result code of that
  table ever seen on the wire;
- the refusal arrives at **`01 22 00`** (`InfoAckAddress`), *not* `01 20 00`;
- the message is exactly the **21-byte acknowledgement frame** recovered from
  the app, byte count `00 0C` = 12, result at `0x0B`, the acknowledged `ah am
  al` at `0x0C`-`0x0E`.

`01 10 01` is a real control: written `1` it reads back `1`, written `0` it
reads back `0`, and the machine echoes the Parameter Change back. **In that mode
the request is answered with data.**

### The transfer

One request, then every message acknowledged with the 21-byte reply at
`01 21 00` built as the app builds it. The machine sent:

| Order | Address | Count | What |
|---|---|---|---|
| 1 | `05 43 11` | — | the contents dump header, carrying `00 01 00 00` |
| 2-85 | `0A 43 11` | 84 packets | **sample data**, indices 0-83, 3017 bytes each |
| 86 | `09 43 11` | 1 packet | **waveform data**, 204-byte payload |

**Samples before the waveform** — the dependency order recovered from the app,
confirmed by the machine's own choice of what to send next. The transfer ran to
completion and stopped on its own.

### The audio

The 84 payloads concatenated give 251,968 encoded bytes. Dropping the **first
two bytes** of that stream and unpacking 7-into-8 most-significant-first gives
**220,465 bytes, every one identical to the `sample0.bin`** of the `.Y3S` the
official app had exported from this sound earlier the same day — 220,465 of
220,465 compared, 100 %.

That single comparison verifies, at once: the request form, the content-number
rule, the mode precondition, the dump header, the data-packet layout (count at
`0x0B`, index at `0x0D`, payload at `0x0F`), the acknowledgement that drives the
transfer, the send order, and the 7-into-8 bit order.

**Two bytes are unexplained.** The packed stream starts two bytes late: the
first payload begins `00 00` and the data is aligned only after them. Later
packets' payloads are data-dependent from their first byte. So the two bytes
look like a one-off prefix at the start of a content's data rather than a
per-packet field — observed once, meaning unknown.

### Corrections this run forces

- **`0xBB8` = 3000 is an *encoded* payload size, not a raw one.** 2625 raw
  bytes travel per packet. An earlier pass wrote the opposite.
- The 7-into-8 **bit order is most-significant first**, now recorded in
  [02-sysex-format.md](02-sysex-format.md#strings-and-blobs-7-into-8-packing).
  It had never been written down, and an ASCII name cannot reveal it.

### The same session: what a refusal names, and a namespace that is not what it looks like

Three more things fell out of asking for a **sound** and an **element** instead
of a waveform. `verified on hardware`.

#### The dump header comes back with the request's own address

```
F0 43 00 7F 1C 00 08 0C 03 60 04 00 00 00 00 0D F7      (17 bytes)
```

Byte count `00 08` = 8 — the Model ID, the three address bytes and four data
bytes — and the address is `03 60 04`, exactly the kind and content number
asked for. So a dump header is echoed back before anything else, and its four
bytes are the interesting part:

| Those four bytes | Meaning |
|---|---|
| `00 01 00 00` plus counts, byte count 22 | a transfer follows — this is what the **waveform** request returned |
| `00 00 00 00`, byte count 8 | **nothing to send** |

#### A refusal names what it is refusing, and it can be the host's own reply

```
F0 43 00 7F 1C 00 0C 0C 01 22 00 7F 01 21 00 00 00 00 00 30 F7
```

Result `7F` = 127 `UnknownError`, and the acknowledged address it carries is
**`01 21 00`** — the address the *host* sends its acknowledgements to. The
machine is not rejecting the request; it is rejecting **the acknowledgement**
that followed an empty header. A client must therefore read the
acknowledged-address field of a refusal to know which end was at fault, and
not assume a refusal is always about the request.

#### `CurrentSound` is not a content number

`01 18 33` read **4100** on SYNTH 2, and the `.Y3S` exported from that sound
carries `<ContentNumber>4100</ContentNumber>`. The two numbers agree. But a
content dump request for **sound 4100** returns the empty header above, and so
does element 0; a project request returns no header at all.

So the agreement between those two numbers must not be read as "the content
channel serves that sound at that number". Either sounds are addressed in
another namespace on this channel, or they are not retrievable by it in the
state this unit was in. **Open.** The waveform, by contrast, answered at the
number its own XML declared — 8593 — and delivered every byte.

This revises the earlier entry in this document, which drew the stronger
conclusion that an imported sound "kept its content number". What is measured
is only that the two numbers are equal.

### What the content channel actually serves — a bounded survey

The asymmetry above was worth pinning down, so a range of content numbers was
probed for each kind. The probe sends the request, reads the header and
**never acknowledges** — an empty header acknowledged is what produced the
`127` above. `verified on hardware`.

| Kind | Numbers tried | Result |
|---|---|---|
| waveform | 8593, 8592, 8594, 8191, 8200, 0, 1 | **8593 answered** (byte count 22) and **8592 answered** (byte count 26). The rest returned the empty header |
| sound | 4096-4111, 4248, 4263, 4264, 0, 1, 2, 2032, 2047 | every one returned the **empty header** |
| element | 0-7, 128, 256 | every one returned the **empty header** |
| project | 0, 1, 2, 7 | **no reply at all** — not even a header |

Three distinct behaviours, and the run carries its own positive control: the
waveform answered in the same session, through the same code, between the
silent ones. So the sound and element results are about those requests and not
about the instrument.

**What this establishes.** On this unit, in this state, the content channel
served **waveforms only**, and only at user numbers (≥ 8192). A project request
is not merely empty, it is unanswered, which suggests it is handled on a
different path rather than refused.

**A hypothesis, not a finding.** The official app's own entry point for pulling
content takes a **project UUID** alongside the type and the number. Sounds and
elements may therefore have to be requested inside a project context that is
established first — plausibly through `10 00 02`
([§Control addresses](08-bulk-and-files.md#control-addresses)) — which nothing
here did. Untested.

**And a side find: there are two user waveforms**, 8592 and 8593, where only
one import was expected. 8592's header declares a byte count of 26 against
8593's 22, so it carries more — more samples, most likely a stereo pair. Not
pulled.

### Exact reproduction, and what a stereo waveform does not send

Two refinements close this out.

#### The 7-into-8 tail

The first runs lost the final partial group, so a 68-byte keybank table came
back as 63 and the sample as 220,465 of 220,470. A trailing group of `1 + m`
bytes yields `m` raw bytes by the same rule. With the tail decoded, the same
request reproduces the exported `.Y3S` **exactly**:

| File | Pulled | In the `.Y3S` | |
|---|---|---|---|
| `sample0.bin` | 220,470 bytes | 220,470 bytes | **identical** |
| `waveform0.bin` | 68 bytes | 68 bytes | **identical** |

Not "100 % of the bytes compared" — the same length and the same bytes. The
read path of the content channel is exact.

#### Withdrawn: "a stereo waveform sends one keybank"

An earlier pass in this same session concluded that only the first keybank's
audio arrived. **That was wrong, and it was the client's fault.** The count and
the packet index are **per content**, and the index restarts at `0` for each
one: a stereo waveform sends its two keybanks as **two runs of the same
indices**. Keying the reassembly on the packet index alone silently overwrote
the first run with the second, and the arithmetic then closed perfectly on one
keybank — which is what made the wrong answer look confirmed.

Traced properly, waveform **8592** sends **710 sample messages**, `count = 355`
throughout, indices `0`-`354` **twice**, then its body. Reassembled as two runs
it gives **931,392 bytes per keybank**, 1,862,784 in all, each matching its
declared size.

> **The trap, for anyone writing a client:** split a new stream every time the
> index returns to `0`. Nothing else in the message distinguishes one content's
> packets from the next one's — the address stays the parent waveform's.

#### The dump header's per-sample entries are **sizes**

Also corrected. An earlier pass had them as each sample's waveform and
keybank numbers. The wire says otherwise. Waveform 8592's header:

```
00 01 00 00 | 00 00 | 00 00 | 00 00 | 00 00 00 02 | 00 38 6C 40 | 00 38 6C 40
```

- the four metadata bytes, then sound, element and waveform counts all `0` —
  and the waveform count is `0` **because a waveform is what is being sent**,
  exactly as documented;
- sample count **2**;
- then two 4-byte entries, both `00 38 6C 40` = **931,392** — each sample's
  **byte size**, not a number. It is the `DataSize` its `sample<i>.xml` carries.

The mono case agrees: byte count 22 = `0x12 + 4 × 1`, one entry, and 220,470
encodes as `00 0D 3A 36`.

#### `+0x38` takes the same pair of values a third party reported

The two keybanks of waveform 8592 read `+0x38` = **27715** and **37821**, in
that order. Those are `0x6C43` and `0x93BD` — **exactly the pair, in the same
order**, that `rechandler`'s notes report for the two keybanks of a resampled
export on a different unit
([06-sounds-presets.md](06-sounds-presets.md#two-independent-third-party-sources-and-who-found-what)).

Two readings, and this run cannot choose between them:

- the two contents are the same audio, so the agreement is trivial;
- or **`+0x38` is not derived from the audio at all**, which would explain why
  neither analyst could find a checksum in it.

Against the second: our own **mono** waveform, audio generated for this test and
never seen anywhere else, reads `20124`, while the third party's mono example
reads `20140` — different audio, different values, so it is not a constant
either. Whatever it is, it varies, and it is not a function of the samples in
any obvious way. **Open**, with one more data point than before.

## 2026-11-23 — a **drum** element accepts a user wave

The question opened two days ago, and the last one of this run that could be
settled without an ear.

KICK is part 0, a drum part. Its element 0 was pointed at the clavioline user
waveform and put back, read → write → read-back → restore with the restore in a
`finally`:

| | `41 00 01` Wave Select | `41 00 03` Wave Number |
|---|---|---|
| before | `00` — Preset | `07 7F` = 1023 |
| written | `01` | `03 11` = 401 |
| **read back** | **`01` — User** | **`03 11` = 401** |
| after restore | `00` | `07 7F` = 1023 |

Witnesses in the same loop: SNARE (`41 01 01`/`03`) stayed at Preset 1166 and
SYNTH 1 (`41 07 01`) at Preset, neither moving at any point, and the tempo
control answered 120 before, during and after. `verified on hardware`.

**So a drum element takes a user wave reference.** Together with the synth
result earlier today, the Data List's note that *only the SAMPLER track is
fixed to User* is now confirmed from both sides: the others choose, and both a
synth part and a drum part were made to choose.

> **What this does not establish.** The parameter accepts the value and reports
> it back; nobody listened. Whether the drum part then *sounds* the user wave
> is a different claim and needs an ear on the machine. This repository has been
> burned before by reading a successful write as a successful behaviour.

## 2026-11-23 — writing content: accepted at every step, and never applied

The first attempt to **write** through the content channel. The result is a
clean negative, and worth having precisely because the machine never complains.

### What was sent

The patched clavioline waveform — the same audio already on the unit, with the
record's loop switch at `00` and the loop start at 3282 — written over the
existing waveform **8593**:

| Step | Message | Acknowledgement |
|---|---|---|
| 1 | contents dump header, `ah 05`, 1 sample declared with its size | **result 0** |
| 2 | 84 sample packets, `ah 0A`, indices 0-83 | **result 0** on every one |
| 3 | the waveform body, `ah 09`, UUID, order, tags, categories, the 68-byte record | **result 0** |

### What happened

**Nothing.** Read back through the same channel, the record still reads
`+0x0F` = `01` (one-shot) and `+0x2C` = `0`, and the audio is unchanged. Sample
memory read `11` before and `11` after. The machine accepted a complete,
well-formed transfer and discarded it.

Repeated with the header declaring **waveform count 1** instead of 0: same
three acknowledgements of `0`, same unchanged record.

### What this pins down

- The write **frame** is right: a malformed body is refused with `127`, a
  `sound` kind with `7`, and the correct header with `0` — the machine is
  parsing what it is sent, not ignoring it.
- The **packet framing** had to match the machine's own exactly, and does: the
  7-into-8 stream is packed over the **whole content** and then cut into
  3000-byte packets — the groups do **not** restart per packet. Encoding each
  2625-byte chunk separately gets 83 packets accepted and the 84th refused
  with `127`, because its length no longer matches. Done right, the numbers
  reproduce the machine's own: 251,968 encoded bytes, 84 packets, the last of
  2,968.
- So what is missing is **not** the frame, the addressing, the packing or the
  acknowledgements. **The write direction is machine-initiated**, and an
  unsolicited dump is parsed, acknowledged and discarded. The app's send entry
  point sends nothing at all — it sets a directory, creates a queue, registers
  a receipt callback and arms the timeout — and what drives a send is its
  **request handler**, which decodes the content kind and number out of the
  same 10-byte Bulk Dump Request a host uses to read. The machine asks; the
  host answers. How the app gets the machine to ask is the open end: an
  inventory exchange is the obvious candidate, since the managed side queries
  the sound and element attributes before sending.

> **For anyone trying this: it is safe so far.** Three complete transfers were
> accepted and discarded with no change to the record, the audio or the sample
> memory. That is not a guarantee — it is what happened three times.

## 2026-11-23 — the loop switch works, and the envelope is why nobody noticed

**A patched user waveform sustains indefinitely on this unit.** The third
party's claim is reproduced here, on a second machine, with the confound their
own test did not have to face.

### The run

1. A clavioline note was rendered offline, imported as a WAV through the
   official app onto **SYNTH 2**, and exported as a `.Y3S`.
2. That file's keybank record was patched in two bytes — `+0x0F` from `01` to
   `00`, `+0x2C` to `3282` (a loop start of 52,512 frames, 1.1907 s) — and
   nothing else, the audio untouched.
3. The patched file was imported through the app. It landed on part 8 as user
   wave **404**: `41 08 01` read `01` (User) and `41 08 03` read `404`,
   `verified on hardware`.
4. **It still died at 2.5 s, fading out.**
5. Its amplitude envelope was read, and the cause was there:

| Address | Field | Read |
|---|---|---|
| `41 08 33` | AEG Attack Time | `0` |
| `41 08 34` | AEG Decay 1 Time | `60` |
| `41 08 3A` | AEG Decay 1 Level | `127` |
| `41 08 35` | AEG Decay 2 Time | `84` |
| `41 08 3B` | **AEG Decay 2 Level** | **`0`** |

The envelope holds at full through decay 1 and then **falls to silence** over
decay 2, with the key still down. No loop can be heard under that.

6. `41 08 3B` was written to `127` — read back `127`, with `41 07 3B` on
   SYNTH 1 unmoved at `0` as witness and the tempo answering before and after.
7. Held again: **the note sustains indefinitely.**

### What this establishes, and the one gap

The loop switch and loop start do what the third party reported, and the
owner's ear is the instrument — the only one there is for this.

**The record was then read back off the machine**, through the content channel,
and it holds the patch: wave 404 reads `+0x0F` = `00` (loop) and `+0x2C` =
**3282** — a loop start of 52,512 frames, 1.1907 s, the exact value written into
the file. Its audio is byte-identical to the file's. Nothing is assumed about
what the import did; the whole chain is measured.

#### And `+0x38` is written by the machine, not by the file

The record on the machine differs from the file in **exactly two bytes**, and
they are `+0x38` and `+0x39`: the file carries `9C 4E` (20124), the machine
holds `54 B8` (**47188**). Everything else matches.

So **the machine overwrites `+0x38` on import.** Whatever a host puts there is
replaced — which is why neither third party could find a checksum in it: it is
not the host's field.

And it is **not a function of the audio**, which this run settles. The same
PCM, byte for byte, was imported twice: as wave 401 it took `20124`, as wave
404 it took `47188`. Identical samples, identical length, two different values.
That rules out every content-derived candidate — sums, CRCs, Adler, peak, RMS —
that both analysts had been testing.

The four values now known, in the order they were created, hint at what it
might be instead:

| Content | `+0x38` |
|---|---|
| wave 401 (first import) | 20124 |
| wave 400, keybank 0 / keybank 1 (stereo) | 27715 / 37821 |
| wave 404 (same audio as 401, imported later) | 47188 |

Rising with allocation order, which would fit a storage offset or an allocation
handle. **A hypothesis, on four points.** Writing it down so the next person
starts from somewhere.

### The finding that matters more than the loop

**A sample imported as a WAV through the official app arrives with an envelope
that fades to silence**: `AEG Decay 2 Level` = `0`. So a correctly patched loop
is inaudible on a freshly imported sample, and anyone who patches the two
record bytes and hears nothing will conclude the patch failed. It did not — the
envelope did. One byte at `41 ep 3B` is the difference, and the machine's own
UI exposes only attack and decay, which is why the third party's advice was to
start from a template sound whose envelope already sustains.

### Withdrawn: "a looped sample does not stop on key release"

An earlier pass in this session published a six-row table concluding that a
looping user wave never stops once `AEG Decay 2 Level` is `127`. **That table is
withdrawn.** Its rows were not a clean matrix: the wave the part was pointing at
changed under the experiment without being re-read, and the reason is the next
finding. Nothing in it can be attributed to the envelope.

### Loading a sound discards live element writes

`verified on hardware`, and it explains the above. Element parameters written
over SysEx (`41 ep xx`) live in the part's working state. **Assigning a sound to
that part reloads its elements from storage and throws those writes away.**

Observed as a silent revert: part 8's element 0 was pointed at user wave 404,
confirmed by read; later the same address read **401** — the unpatched wave —
with no write of ours in between, after sounds had been loaded on the track.
Every envelope experiment run across that boundary was therefore comparing two
different waveforms without knowing it.

> **The consequence for anyone patching loops:** a loop cannot be installed by
> writing element parameters. It has to be in the **content** — the waveform's
> own keybank record, shipped in a `.Y3S` — which is precisely why the third
> party distributes files rather than a list of parameters.

### The third party's pack works, and it answers the question

Seven patches from `giddycadet`'s free pack were imported on this unit. Played
on SYNTH 2 with the patch exactly as shipped — wave 405, its own envelope,
nothing of this project's written over it — the note **holds while the key is
held and stops when it is released.**

So the behaviour is not "forever" in the sense of unstoppable. The loop makes
the sample endless; the envelope's release still ends the note. `verified on
hardware` by the owner's ear, which is the only instrument for it.

### Their envelope, read out of the files

All seven patches carry the **same** amplitude envelope, element 0, differing
only in attack:

| Field | Address | Value |
|---|---|---|
| AEG Attack Time | `41 ep 33` | `0` on the basses, `83` on the pads |
| AEG Decay 1 Time | `41 ep 34` | `97` |
| AEG Decay 2 Time | `41 ep 35` | `64` |
| AEG Release Time | `41 ep 37` | `83` |
| AEG Init Level | `41 ep 38` | `0` |
| AEG Attack Level | `41 ep 39` | `127` |
| AEG Decay 1 Level | `41 ep 3A` | `119` |
| **AEG Decay 2 Level** | `41 ep 3B` | **`116`** — not `127` |

The sustain level is `116`, which is worth knowing: an import from the official
app leaves it at `0`, and the obvious guess of `127` is not what a working patch
uses.

**But their envelope alone is not enough.** Applied byte for byte to this
project's own patched waveform, the note did **not** behave: it played the
sample once and stopped. The difference is in the waveform, not the envelope.

### The difference: their sample lengths are all multiples of 64

| Patch | `n` frames | `n % 16` | `n % 64` |
|---|---|---|---|
| Airplane Drone | 134,208 | 0 | 0 |
| Analog Pad | 241,920 | 0 | 0 |
| Fat Fuck Friday | 67,968 | 0 | 0 |
| Hypnotizing Pulse | 270,144 | 0 | 0 |
| Of the Spheres | 165,312 | 0 | 0 |
| Sizzle & Whoosh | 188,352 | 0 | 0 |
| Warm Reese | 174,528 | 0 | 0 |
| **this project's patch** | **110,235** | **11** | **27** |

All seven of theirs are divisible by 64. Ours is divisible by nothing.

The loop runs from the start point **to the end of the data**, and the start
point is counted in **16-sample blocks** — so a sample length that is not a
multiple of 16 leaves the loop's end in the middle of a block. **That is a
hypothesis**, not a measurement: it is the only structural difference left in
the record numbers, and it has not been tested. A re-rendered 117,888-frame
version exists to test it, which needs another import.

### A correction to their spec: the element block base

Their `.Y3S` spec places element 0's block at `0x1E9` in `sound.bin`. **In the
files here it is at `0x14A`.** Located by searching for the nine-byte sequence
this machine had just reported for addresses `41 ep 33`-`3B` — it occurs exactly
once in the file — so the anchor is hardware-backed rather than assumed, and
with it every envelope field read out of a `.Y3S` matches what the part reports.
The gap is 159 bytes, which is not a multiple of their 141-byte stride, so one
of the two numbers is simply wrong rather than off by a block.

## 2026-11-23 — writing a sound: the header is refused cold, and why that is hard to fix

Having seen the official app's import on the wire, the transfer was rebuilt as
the app does it — announce a **Sound** (kind `03`) and ship the chain. The very
first message is refused.

### What the machine answers

`verified on hardware`. The contents dump header for kind `03`, content number
4120, with the record and sound of a real `.Y3S` behind it:

```
-> F0 43 00 7F 1C 00 16 0C 03 60 18 00 01 00 00 ... F7
<- F0 43 01 7F 1C 00 0C 0C 01 21 00 07 03 60 18 ... F7     result 7
```

Result **`7` `PacketLoss`** — which from the machine means something nearer
"not expected now" than a lost packet. Every variant was refused the same way:

| Variant | Result |
|---|---|
| device byte `00`, `02`, `0F` | `7` |
| device byte `01`, `10` | no acknowledgement at all |
| sound count `1` instead of `0` | `7` |
| waveform count `0` | `7` |
| sample count `0`, no entry | `7` |
| every count zero | `7` |

So it is **not** the header's contents. And the contrast is sharp: a **Waveform**
header (kind `05`) is accepted with `0` cold, in the same session, at several
content numbers. The machine will begin a waveform transfer unprompted and
refuses to begin a sound one.

### A lead that turned out to be nothing

Two messages appear immediately before **both** of the app's transfers in the
capture, at unusual addresses: `00 61 02` and `00 60 01`. They looked like an
arming handshake. They are not — `00 60 01` is **`WiFiReady`** and `00 61 02`
belongs to the Wi-Fi security family ([03a](03a-parameters-system.md)). Periodic
state, coincidentally placed. Recorded so nobody else spends time on it.

### The wall, stated plainly

A MIDI input port receives what the **machine** sends. The app's outgoing
messages go to the device and are invisible to any other client, so the one
thing that would settle this — what the app sends before its header — cannot be
captured this way.

**The instrument that would work is a man-in-the-middle:** a virtual MIDI
destination that the app is pointed at instead of the hardware, relaying to the
real device and logging both directions. That is the next step for anyone
continuing this, and it would expose the whole import, not just the half the
machine answers with.


### The Sound header is refused whatever it carries — a state, not a payload

Eleven header variants were sent for kind `03` (Sound): five device bytes, four
count combinations, and four forms of the per-sample entry (size, waveform
number plus keybank, waveform number alone, waveform number minus 8192).
**Every one was refused with result `7`.** In the same session a kind `05`
(Waveform) header was accepted with `0` with *any* of those payloads.

So the refusal does not depend on the message. It depends on something about
the machine, and the app's code does not explain it: the app sends the same
frame, the same address and the same counts a host would.

`verified on hardware`, and recorded mainly so the next attempt does not spend
its time on the payload.

### Priming the inventory does not unlock a Sound header, and `0C 11 01` is the user-sound listing

The app queries the content attributes before it sends, so the inventory
exchange was the obvious gate. It is not.

`0C 11 01` is confirmed as the **user-sound listing**: it appeared unprompted in
the capture of the app's own import, and requesting it directly with
`F0 43 20 7F 1C 0C 0C 11 01 F7` returns the same two-message reply, carrying the
names of every user sound on the unit. `0C 12 01` and `0C 01 01` answer too.
`verified on hardware` — and it upgrades that zone, which this repository had
only `reverse-engineered from app traffic`.

But a kind `03` header sent **immediately after** the listing is still refused
with `7`, exactly as when sent cold. Three listing modes were tried.

So the tally for the Sound header, all `verified on hardware`: eleven payload
variants, five device bytes, three inventory primings — every one refused with
`7`, while a Waveform header is accepted with `0` throughout. Nothing a host can
say changes it.

**The power cycle was tried, and it changes nothing.** The unit was switched
off and on, confirmed answering, put into contents-management mode, and the
kind `03` header was the very first content message sent: **`7` again**. So the
refusal is not a half-open transfer left by the earlier runs.

That closes the cheap hypotheses. The tally is **twenty variants** of a Sound
header — eleven payloads, five device bytes, three inventory primings, and one
cold start after a power cycle — every one refused with `7`, while a Waveform
header is accepted with `0` under all the same conditions.

> **For whoever picks this up: do not brute-force the header.** It has been
> brute-forced. The difference is not in what the host says, and the app's code
> contains no step before the header. Two instruments could still settle it,
> and nothing else obviously can: a **virtual MIDI destination** relaying
> between the app and the device, which would show the app's outgoing side —
> invisible to any other client — and the **firmware image**, which is the only
> place that knows why the machine says no.
>
> One reading worth testing first, because it would reframe everything: the
> acceptance of a Waveform header may not mean "ready to receive". It may be the
> machine agreeing to *send* that waveform — the same address space serves
> both directions, and a read request for a waveform is answered, while a sound
> is not ([§What the content channel actually serves](#what-the-content-channel-actually-serves--a-bounded-survey)
> found exactly that asymmetry for reads). If so, no host has ever had a write
> accepted here, and the write direction remains entirely unproven.

### The lock is reachable from a script, and a map of which headers it accepts

Two things settle, and together they sharpen the problem rather than solve it.

#### Writing `01 10 01 = 1` engages the real lock

Not merely a flag that accepts a value. Written from a script, the machine
**reacts on its own**: `01 10 18` (`DrumPadMode`) goes to **21** without being
asked. That is exactly what it did for the official app, which was captured
reporting `01 10 01 = 1` at 94.753 s and `01 10 18 = 21` just before. So a host
can put the machine into the same content-management state the app's project
menu puts it in, and the machine's own state push proves it.

`verified on hardware`. The state is **not** the difference between a host and
the app.

#### Which header kinds the machine accepts, in that state

One header per `ah`, same payload throughout, back to back in the locked state:

| `ah` | Header for | Result |
|---|---|---|
| `02` | project (kind) | **`0`** |
| `03` | **sound** (kind) | `7` |
| `04` | element (kind) | `7` |
| `05` | waveform (kind) | **`0`** |
| `06` | project data | `7` |
| `07` | sound data | `127` |
| `08` | element data | `127` |
| `09` | waveform data | **`0`** |
| `0A` | sample data | `127` |
| `01`, `0B` | — | no acknowledgement |

Three are accepted — `02`, `05`, `09` — and a sound is refused in **both**
address spaces. It is not the content number: `02` with number 0 is accepted
while `04` with number 0 is refused. And `09`, which is a *body* address, is
accepted while carrying a *header* payload, which should be meaningless.

So the refusal is keyed on the kind itself, in a way no reading of the app
explains: the app sends a sound header and the machine takes it. Something
about a host that is not its own content-management session is being rejected,
and neither the message, the mode, the number nor the payload is that something.

> **This is an unresolved contradiction, not a conclusion.** The app does it;
> a script in the same state with the same bytes cannot. Either the app sends
> something before the header that no other client can observe, or the machine
> distinguishes the two in a way nothing here has reached. The map above is
> recorded so the next attempt starts from facts rather than from this
> repository's guesses, of which this section has already withdrawn several.

### The man-in-the-middle route is closed: the app picks its port itself

The one instrument that would have shown the app's outgoing traffic was tried
and does not work.

A pair of virtual CoreMIDI ports was created, named exactly **`SEQTRAK`**, with
the real device already opened behind them so everything would be relayed. The
official app was then disconnected and reconnected and an import performed.

**Zero messages arrived at the virtual destination.** The app opened the real
port. That is consistent with what its own strings say: it has
`MidiConnect` / `MidiDisconnect` screens and a "Connect To Midi Ports Error"
string, but **no port picker** — it discovers the device by name and opens it
itself. With two ports of the same name it took the hardware.

So the app's outgoing side cannot be observed from another client on this
machine, and the question it would have answered — what, if anything, the app
sends before a Sound header — stays open. `verified on hardware` as a negative
about the method, not about the protocol.

What remains is the **firmware image**: 66 MB of ARM with no symbols and no
hard-coded message templates, since the machine builds its replies in code.
Locating the content-dump receive path there is a project of the same order as
the analyses that produced this repository's firmware document, not a next step.

## 2026-11-23 — a host CAN install a `.Y3S`, and the blocker was one stray bit

**Writing content works.** A `.Y3S` built from scratch by this project — not an
export — was pushed over SysEx and the machine created the sound. Everything
written here earlier about the write direction being impossible,
machine-initiated or state-dependent is **withdrawn**: the obstacle was a bug in
this repository's own address rule.

### The bug

The rule published here was `am = ((n >> 7) | 0x40) & 0x7F`. The real rule is
`am = (n >> 7) & 0x7F`, no `| 0x40` — read straight off the official app's
traffic, which addresses sound 4103 as `03 20 07`.

The extra bit is **invisible for waveforms**: their numbers start at 8192, so
`n >> 7` is already ≥ 64 and bit 6 is set anyway. Every waveform operation
therefore worked, including the read that reproduced a sample byte for byte. For
**sounds**, numbered near 4100, bit 6 is clear and the bit corrupts the address.
That is the whole explanation for the Sound header being refused with `7`
through twenty header variants, a power cycle, three inventory primings and a
man-in-the-middle attempt. **The machine was right every time.**

### The transfer that worked

Content-management mode on (`01 10 01 = 1`), then:

| Message | `ah` | Acknowledged |
|---|---|---|
| contents dump header, kind Sound, counts `0/0/1/1`, one entry carrying the PCM's **byte size** | `03` | `0` |
| 90 sample packets, addressed on the **waveform**, 3000 encoded bytes each | `0A` | `0` on every one |
| the waveform body | `09` | `0` |
| the **sound body** | `07` | `0` |

Then `01 10 01 = 0`. The header's body was byte-identical to the app's own:
`00 01 00 00 | 00 00 | 00 00 | 00 01 | 00 00 00 01 | 00 0E 32 00`, those last
four bytes decoding to 235,776 — the sample's size.

### How it was verified

Not by the acknowledgements, which had read `0` before while nothing landed.
**`01 10 09` `UserSoundEmptyContentCount` went from 2029 to 2028** across the
push, and sample memory grew. The same counter decrements by one in the capture
of the app's own import, which is what suggested it as the instrument.

### How it was found

By **capturing both directions** with a monitor that can see what another
application sends. This project's own attempts could only ever observe the
machine's half of the conversation, and the error lived in the other half. The
owner proposed that capture after the analysis here had twice concluded, in
public, that the thing was impossible.

## 2026-11-23 — key release is one byte, and the parameter that looks like it is not it

With a host now able to install a `.Y3S`
([previous section](#2026-11-23--a-host-can-install-a-y3s-and-the-blocker-was-one-stray-bit)),
the sustain question became answerable by experiment instead of by reading.

Two packages carrying the **same** 235,776-byte sample, the same 68-byte
keybank record and the same loop switch behaved differently: one held the note
while the key was down and stopped on release, the other looped forever. Their
`sound.bin` files differ in twelve bytes.

Seven variants were built, each one starting from the looping package and
restoring one group of those bytes from the working one, and each was pushed to
the machine as its own user sound:

| Sound | Bytes restored | Stops at key release |
|---|---|---|
| `clavi-A` | `0x6E`, `0x75`, `0x77`, `0x7C` | no |
| `clavi-B` | `0x84`, `0x88`, `0x95` | **yes** |
| `clavi-C` | `0x96`, `0xA2`, `0xA9` | no |
| `clavi-D` | `0x143`, `0x1E8` | no |
| `clavi-B1` | `0x84` only | no |
| `clavi-B2` | `0x88` only | **yes** |
| `clavi-B3` | `0x95` only | no |

So **`sound.bin` offset `0x88` alone** decides it: `0x02` stops the note at key
release, `0x00` makes it loop forever. `verified on hardware`.

All seven transfers were accepted at every step, and
`01 10 09` `UserSoundEmptyContentCount` fell from 2028 to 2023 over the first
five, which is the instrument that proves five separate sounds were created
rather than one slot being overwritten five times.

### The parameter that is not it

`41 ep 08` `Trigger/Gate Mode` is the obvious candidate — `Trigger` would
plausibly mean "ignore key off". It is not the control:

| Step | Reading |
|---|---|
| `41 08 08` before | `1` (Gate), on a sound that stops at key release |
| `41 07 08` witness | `1` |
| write `41 08 08` = `0` (Trigger), read back | `0` |
| `41 07 08` witness after | `1`, unmoved |
| `30 40 76` tempo, as control, throughout | `00 78` |
| the sound, played on that element | **still stops at key release** |

The write landed and changed nothing audible, so `41 ep 08` is not the byte at
`0x88`. `41 08 08` was restored to `1` afterwards. `31 1p 0D`
`Trigger/Gate Mode` reads `2` on SYNTH 1 and SYNTH 2 alike, so it does not
discriminate between the two behaviours either. Both `verified on hardware`.

`01 18 33` `CurrentSound SYNTH 2` read `00 00` with a user sound loaded on that
track, four attempts, tempo answering before and after — so it does not report
user sound numbers, and it cannot be used to select one. `verified on hardware`.

**What stays open**: which `31 xp xx` or `41 ep xx` address corresponds to
`sound.bin` offset `0x88`. The common region's offsets are not the parameter
offsets — the name alone occupies `0x08`-`0x5F` as eleven 7-bit-packed groups
against a hundred parameter addresses — so the mapping cannot be read off by
arithmetic. Settling it needs a wide parameter dump taken with each of the two
sounds loaded in turn, and loading a user sound onto a track from the host is
itself not yet possible.

## 2026-11-23 — `31 1p 0D` is the answer, and the previous section's `41 ep 08` test was void

### First, the retraction

The [previous section](#2026-11-23--key-release-is-one-byte-and-the-parameter-that-looks-like-it-is-not-it)
reported a write to `41 08 08` that "changed nothing audible" and concluded from
that experiment that the element's `Trigger/Gate Mode` is not what governs key
release. **That experiment was void**: the write went to part 8 (SYNTH 2), and
the sound being played and listened to was on part 7 (SYNTH 1). The two tracks
were never compared, so the test could only ever have come back negative.

It was caught by reading `01 1p 35` `CurrentSoundName` on every part: SYNTH 1
held `clavi-B2` and SYNTH 2 held `bis-disperses`. The conclusion happens to
survive — see below — but it now rests on a dump comparison instead, and the
write test is withdrawn. This is the third claim in this repository overturned
by an instrument that could not see what it was asked about, and the second
where a track mix-up was the cause.

### Reading the name back is one message

`01 1p 35` `CurrentSoundName` answers a plain Parameter Request with 100 bytes,
7-bit packed, holding the loaded sound's name — for **user** sounds as well as
presets. It answered on all eleven parts, four attempts each, tempo as control.
`verified on hardware`. That is much cheaper than the thirty-block edit-buffer
burst, and it is the only practical way to tell which user sound a Program
Change landed on.

`01 1p 33` `CurrentSound` is the opposite: it read `00 00` on a part holding a
user sound, and writing `858` to it did nothing — the loaded sound was unchanged
and the address still read `00 00`, with the neighbouring part's name unmoved.
It reports, it does not select, and it does not report user sounds at all.
`verified on hardware`.

### The user bank enumerated

Sweeping MSB 63, LSB 32, programs 0-31 on SYNTH 2's channel and reading
`01 18 35` after each triplet:

| Programs | What loaded |
|---|---|
| 0-27 | 28 distinct user sounds, **in creation order**, the most recent last |
| 15, 16, 17 | nothing — the name stayed on the previous sound |
| 28-31 | nothing, as documented for unsupported program numbers |

`verified on hardware`. So user sound *k* from zero is LSB `32 + k // 128`,
program `k % 128`, and the bank has holes: a program that loads nothing looks
exactly like one that reloads what is already there. Always read the name back.
The 128-per-bank size is still unmeasured — only 28 sounds existed.

### And the answer

`clavi-B1` (program 25, `sound.bin` `0x88` = `0x00`, loops forever) and
`clavi-B2` (program 26, `0x88` = `0x02`, stops at key release) differ in that
one byte and the name. Loading each in turn and dumping the part's edit buffer
with `11 02 08` gives four differing bytes in 25 blocks:

| Block, offset | Parameter | Looping | Releasing |
|---|---|---|---|
| `31 08 00` + `0x09` | a Sound Name byte | `31` | `32` |
| **`31 18 00` + `0x0D`** | **`31 1p 0D` `Trigger/Gate Mode`** | **`00` *Trigger*** | **`02` *Depend on Voice*** |
| `31 18 00` + `0x1F` | `31 1p 1F` `Portamento Time` | `00` | `40`, the default |
| `41 08 00` + `0x04` | the element's wave number | `29` | `2A` |

`verified on hardware`. **`Trigger` means "ignore key release"** — the right
behaviour for a drum hit, and the reason a looped sample runs forever.
`Depend on Voice`, the Data List default, lets the note stop when the key is
released. `Portamento Time` rides along: nothing in the package sets it, so the
machine derives it from the same stored field.

`41 ep 08`, the element's own `Trigger/Gate Mode`, reads `01` (*Gate*) in **both**
dumps, so it is not the discriminator. That is the evidence replacing the void
write test above.

The address takes a live write: with `clavi-B1` loaded, `31 18 0D` read `00`,
was written `02` and read back `02`, then restored to `00`, with `31 17 0D`
unmoved at `02` as witness and the tempo answering throughout. `verified on
hardware` for the read-back only — **whether a live write changes what you hear
without reloading the sound has not been listened to.**

### Why the official app's imports never sustained

Two independent things are set wrong by a WAV import through the official app,
and both had to be found before a note would hold and then stop:

| Address | After an app import | What it costs |
|---|---|---|
| `41 ep 3B` `AEG Decay 2 Level` | `00` | the note fades to silence with the key held |
| `31 1p 0D` `Trigger/Gate Mode` | `00` *Trigger* | key release is ignored, so a looped sample never stops |

Offline cross-check, no hardware: all **seven** of the third-party preset pack's
patches carry `0x88` = `0x02`, and **every** package exported after an app WAV
import carries `0x00`. That is what the pack's author had changed, and the loop
switch in the keybank record was only half the story.

## 2026-11-23 — removing a user sound is blocked on a number nothing will tell you

`01 41 00` `RemoveSoundAddress` takes **the content number**. Nothing on the
machine will say what a user sound's content number is, so the command cannot be
aimed, and it was **not sent**.

Three read-only routes were tried, all dead ends:

| Route | What it gives | Why it does not help |
|---|---|---|
| `01 1p 33` `CurrentSound` | `00 00` for a user sound | does not report user sounds at all |
| the browser's category list, `0C mm pp` | an entry's "sound ID" as `[bank LSB] [program]` | bank and program, never a content number |
| a content request, `03 am al` | the content itself | every number tried refused |

The content sweep is the substantive one. With `01 10 01` engaged, a sound
content request (`F0 43 20 7F 1C 0C 03 am al F7`) was sent for **every** number
from 4096 to 4135 — the band the app's own exported `sound.xml` points at, which
gives `ContentNumber` 4100 for a sound whose waveform at 8593 *does* pull — and
the machine refused all but two:

| Number | Answer |
|---|---|
| 4096, 4099-4135 | refused at `01 22 00`, **result 127** |
| 4097 | one body, with a name that does not decode and `0x88` = `0x01` — not reproduced, not claimed |
| 4098 | nothing at all |

`verified on hardware`, `01 10 01` restored in a `finally`. **Result 127 is not
in the app's `Bulk.Result` enum**, which stops at 54; it is what an unusable
content number produces. So a user sound's content number is not in the band
its own exported package names, and the write path works only because
`content_push.py` *proposes* a number that the machine then reassigns silently.

Note the asymmetry that hid this: waveform numbers (8593, 8598) pull cleanly,
and sound numbers in the same style do not.

**What would settle it**: the app knows these numbers, so something tells it —
most likely an inventory exchange over the content channel, which earlier
sessions had to prime three times before a push would take. That exchange has
not been decoded. Until it is, deleting a user sound is an operation only the
official app can aim.

### A stray bit found in the pull tool

Fixing the address rule in the documentation left the same `| 0x40` in
[`content_pull.py`](../tools/hardware-probe/content_pull.py), where it had been
harmless: waveform numbers are above 8192 and already carry that bit. It would
have corrupted every *sound* address the moment anyone pulled one. Removed. The
sweep above is the first run that used sound addresses at all, which is how it
surfaced — a retraction is not finished until the tools are re-read.

## 2026-11-24 — a multi-zone user waveform: the transfer header decoded, and six attempts that were all malformed

The aim was a multisampled instrument — one note rendered per octave, five key
zones — because a single sample stretched across the keyboard is what makes an
imported instrument fall apart when you change octave. It does not work yet, but
six attempts against the machine turned a blank in the header into three decoded
fields and one sharp blocker.

### The header, field by field

The sound header (`ah 03`) that opens a content transfer carries 18 bytes. The
single-sample form that works is `[0,1,0,0] [0,0] [0,0] [0,1] b4(1) b4(size)`.
Varying the fields one at a time, each attempt stopping at the header so nothing
was installed:

| Field | Tried | Answer |
|---|---|---|
| the 2-byte field at offset 8 | `0`, `1`, `2`, `5` | **all accepted** — the machine does not validate it |
| the first `b4` | `1` | accepted |
| the first `b4` | `2`, `5` | **refused, result 127** — but the header sent was malformed; see the retraction at the end of this section. A well-formed `8` is accepted |
| the second `b4` | one sample's size, or the total of five | accepted either way |

So that first `b4` **must be 1**, and the second is the byte length of the
packet stream that follows. `verified on hardware`. The earlier comment in
`content_push.py` reading the fields as "sound=0, element=0, waveform=1,
sample=1" is wrong about the last one: it is not a sample count, because no
value but 1 is allowed.

### What the declared size governs

Declaring the total of five samples and then sending only the first sample's
stream is refused — **on the stream's last packet**, result 127, every earlier
packet accepted. So the size in the header is the length the machine expects the
stream to reach, and it checks it at the end. `verified on hardware`.

That gives two working shapes:

| Shape | Outcome |
|---|---|
| five headers, each declaring one sample's size, each followed by that sample's packets | all five streams **accepted**; the waveform body carrying 5 keybank records is then **refused**, result 127 |
| one header declaring the total, one continuous stream of the five samples concatenated | everything **accepted**, header to sound body |

### And the blocker: the second shape is accepted and then silently flattened

The accepted transfer was pulled straight back off the machine
([`content_pull.py`](../tools/hardware-probe/content_pull.py), waveform 8621).
All 495,488 bytes of audio came back, and the record did not:

| Field | Sent | Stored |
|---|---|---|
| keybank count | **5** | **1** |
| key range, root key | `0`-`41`, note 36 (zone 0) | `0`-`41`, note 36 — zone 0's, kept |
| `+0x3C` sample count | 60,480 (zone 0 only) | **247,744** — the whole blob |
| `+0x30` last index | 60,479 | 247,743 |
| `+0x2C` loop start | 1,378 blocks | 1,378 — kept |

`verified on hardware`. The machine took the five-record table, **kept the first
record, and stretched it over the entire blob**. Nothing was refused and nothing
warned: the sound it builds plays all five notes end to end, as an 11.2-second
loop, on keys 0-41 only. A transfer being accepted at every step is not evidence
that it was stored as sent — this is the second time that has caught us, after
the keybank run that reassembled perfectly while dropping a stereo waveform's
first zone.

### What would settle it

This repository already records, from the read side, that a stereo waveform's
two keybanks arrive as **two packet runs, each with its own count and indices
restarting at 0**, under one waveform. That is the shape neither attempt above
used: the five-header shape gave each run its own header, and the blob shape
gave five runs' worth of audio one set of indices. The write side needs the same
two-run shape under a **single** header — and what the header then declares as
its size is exactly what is not known.

~~**One capture settles it**: the official app importing a *stereo* `.Y3S`, which
is the minimal two-keybank case, both directions.~~ **That capture had already
been taken** — see the retraction below. Until then a user waveform on
a synth element is one zone, and a multisampled instrument has to go the other
route — several elements in one sound, one waveform each — whose file layout is
also unresolved: element 0's envelope sits at `0x14A` and its wave pointer at
`0x1E8`, which are 158 bytes apart and cannot both fit the 141-byte stride the
third-party source reports, so the base of element 1 is a guess and was not
tried.

> Two sounds named `clavi-multi` are now on the unit, at user bank programs 28
> and 29, and both are the flattened result described above. They are test
> residue, not instruments.

### Later the same day — the keybank route is closed, the element route is open

Pushing further on the multi-zone problem settled both halves of it.

**A `kind 05` header creates a new waveform.** Announcing each extra keybank
with `ah 05` on the waveform number, instead of `ah 03` on the sound number,
gets every stream accepted *and* the five-record waveform body accepted —
result 0 throughout, where the sound-kind announcement had the body refused.
But pulling the results back shows what was really stored: waveform 8622 and
waveform 8623 each hold **one keybank of 44,096 samples, both of them zone 0**.
The first stream is kept, the later ones are acknowledged and discarded, and the
five-record table is applied as record 0.

So, three shapes tried and `verified on hardware` for all three:

| Shape | Accepted | Stored |
|---|---|---|
| one header, one concatenated stream | fully | 1 keybank, stretched over the whole blob |
| one header per sample, `ah 03` | streams yes, body **refused** | — |
| one header per sample, `ah 05` | fully | 1 keybank per waveform, all holding the **first** stream |

**A user waveform gets exactly one keybank through this path.** The header's
size field is checked at the end of each stream, and exactly one stream is
expected per header — declare the total and the first stream's last packet is
refused; declare one zone's size and the *second* stream's last packet is
refused. There is no room left in the header for a second keybank, which is why
the capture of the app importing a stereo package is still the only way in.

#### But the element route works, and it is all live parameters

The other route needed no file-layout guesswork at all, because every field
exists as an ordinary `41 ep xx` parameter. Five single-zone sounds were pushed,
each creating its own user waveform (**432**-**436**), and then five elements of
part 8 were assigned by hand:

| Element | Address | Wave | Note limits |
|---|---|---|---|
| 0 | `41 08 xx` | 432 (root 36) | `0`-`41` |
| 1 | `41 18 xx` | 433 (root 48) | `42`-`53` |
| 2 | `41 28 xx` | 434 (root 60) | `54`-`65` |
| 3 | `41 38 xx` | 435 (root 72) | `66`-`77` |
| 4 | `41 48 xx` | 436 (root 84) | `78`-`127` |

`41 ep 00` `Element Assign` = 1, `41 ep 01` `Wave Select` = 1 (user wave),
`41 ep 03` `Wave Number`, `41 ep 10`/`11` `Note Limit Low`/`High`, `41 ep 12`/`13`
velocity limits, `41 ep 2E` level and the envelope on each. **Every one read
back exactly as written**, with `41 07 03` unmoved on SYNTH 1 as witness and the
tempo answering throughout. `verified on hardware`.

That closes the question of whether the element wave fields work over SysEx,
which [06](06-sounds-presets.md#waveforms) had listed as untested: `41 ep 01` and
`41 ep 03` do, for user waves, on a synth part.

**What is not established**: whether it *sounds* like a five-zone instrument.
The parameters hold; nobody has played it yet. And it does not persist — live
element writes are lost when a sound is loaded, and `Sound Save` is still an
unresolved address, so this assembly has to be rebuilt on every power cycle
until that is found.

> So the one-zone limit is **not** a firmware limit. The engine plays multi-zone
> waveforms all day — the factory library is sampled every one to three
> semitones — and a user waveform on this very unit already holds two keybanks
> (the stereo one, waveform 8592, pulled back and counted). What is missing is
> the write handshake for the second keybank, and a way to save an element
> assembly.

#### The trap in assembling elements by hand: `41 ep 54`

The five-zone assembly above played, and it played wrong in a way worth
recording: the pitch stopped rising part-way up the keyboard and every key above
that point sounded **the same note**, with only the timbre darkening as the
player went higher.

Dumping the part and diffing element 0's block against elements 1-4 named the
cause in one line. Seven bytes differed, four of them intended (the wave number
and the note limits) and one decisive:

| Offset | Parameter | Element 0 | Elements 1-4 |
|---|---|---|---|
| **`0x54`** | **`Pitch Key Follow Sensitivity`** | **96** (`0x60`, the Data List default) | **64** (`0x40`) |
| `0x2F` | `Level Velocity Sensitivity` | 84 | 64 |
| `0x34` | `AEG Decay 1 Time` | 97 | 127 |
| `0x35` | `AEG Decay 2 Time` | 64 | 100 |

**`41 ep 54` = 64 means the element does not track the keyboard in pitch**: it
plays its sample at the root key whatever note arrives. The filter still follows
the key, which is exactly the "same note, darker as you go up" the player
described. `verified on hardware`.

An element that an existing sound configured carries 96; an element switched on
from scratch over SysEx does not. **Assigning a wave, a zone and a level to a
fresh element is not enough** — `0x54` has to be written too, and so does
anything else element 0 carries that the untouched blocks do not. Diff the
blocks rather than trusting the Data List defaults: the default for this
parameter is `0x60`, and the element blocks of a loaded sound hold `0x40`.

All five elements were then aligned and read back identical apart from wave
number and note limits, witness unmoved and tempo answering. Each waveform's
root key survived the import — waveform 436 pulled back with root `84`, key
range `0`-`127`, its loop start and length intact.

#### The ceiling: eight elements, so eight zones

`verified on hardware`. **Eight** elements are addressable live on a part —
`41 (e<<4|p) xx` for `e` = 0-7 — and all eight were written and read back on
part 8: eight user waves, eight note-limit ranges, `41 ep 54` at 96 on every
one, witness unmoved and tempo answering. An edit-buffer dump of the part
returns the matching eight blocks, `41 08 00` through `41 78 00`, of 109 bytes
each.

That is also the ceiling of this route. [06](06-sounds-presets.md#soundbin-and-how-an-element-points-at-a-wave)
reports 7 usable element blocks in a package's `sound.bin`, the 8th `FF`-filled;
over SysEx, on a loaded sound, all eight answer and all eight take an
assignment.

Eight zones is enough to **match Yamaha's own density over about two octaves**:
a root every 3 semitones spans 24 semitones, and the factory library's commonest
zone widths are 3, 2 and 1 semitones. It is not enough for a keyboard: 128 keys
at 3 semitones would need 43 zones. So the element route gives a good two
octaves, and anything wider has to stretch — which is the measure of what the
keybank route would buy if its write handshake were known.

A worked example now on the unit: roots at 48, 51, 54, 57, 60, 63, 66 and 69,
zones `0`-`49`, `50`-`52`, `53`-`55`, `56`-`58`, `59`-`61`, `62`-`64`, `65`-`67`
and `68`-`127`, with the two outer elements widened so nothing is silent.

#### Normalising each zone to the same peak is a mistake

Worth recording because it is the obvious thing to do and it is wrong. The eight
zone samples were each normalised to the same **peak**, which sounded uneven at
the zone boundaries — "surtout le volume", in the player's words.

Measured on the files, the loop region of each:

| | Peak-normalised | One common gain |
|---|---|---|
| loop RMS, lowest zone → highest | 9,770 → 12,027 | 9,770 → 9,903 |
| total spread across the set | **1.80 dB, rising** | **0.12 dB** |

The engine's own output *falls* with pitch — the eight renders peaked 14,759
down to 12,153. Normalising each one to an equal peak does not merely remove
that contour, it **inverts it** into a rising ramp, because the crest factor
changes with pitch. Applying a **single gain to the whole set** instead, sized
so the loudest zone reaches the target, keeps the instrument's natural contour
and leaves the RMS flat to a tenth of a decibel.

The element blocks were ruled out first: a part dump showed all eight identical
apart from wave number and note limits, with `41 ep 2E` level at 100 and
`41 ep 4D` `Level Key Follow Sensitivity` at 64 on every one. `verified on
hardware`. So the step was in the audio, not the parameters — worth checking in
that order, since a parameter is far quicker to read than a sample is to analyse.

A second finding from the same measurement, and it bounds what multisampling can
do here: the spectral centroid of the eight loops rises **more slowly than the
fundamental** — 252 → 610 Hz where f0 goes 131 → 440 Hz, a factor 2.4 against
3.4. So the engine's timbre darkens relative to pitch as it climbs. A sample
stretched a semitone carries its whole spectrum with it, so at every zone
boundary the brightness steps by roughly what three semitones of the natural
contour would have done. Denser zones are the only cure, which is what the
eight-element ceiling caps.

#### An element switched on from scratch differs in **two** blocks, not one

The volume step the player reported was real, and it was neither the audio nor
the block this session had been looking at. It is worth the space because the
diagnosis went wrong twice first.

The report was precise: do3 (note 48) louder than ré3 (note 50), and **the
softer level then holds for every note above** — a step, not a one-note
anomaly. A MIDI capture of the two keys gave their numbers and so the elements:
48 is element 0 at its exact root, 50 is the first note of element 1.

What the audio and the `41 ep` block said:

| Checked | Result |
|---|---|
| the two samples' RMS over 100 ms, 300 ms, 500 ms and the loop | matched within **0.04 dB** |
| the `41 ep` blocks of the two elements | **3 bytes** differ — wave number and the two note limits, all intended |

So neither. The cause was in the **`42 ep`** block, filter/EQ, which had not been
compared:

| Offset | Parameter | Element 0 | Elements 1-7 |
|---|---|---|---|
| `0C`-`0D` | **`Filter Gain`** (2 bytes) | `01 7F` = **127** | `01 66` = **102**, the Data List default |
| `1D` | **`FEG Depth`** | **64** (neutral) | **104**, the default |

`verified on hardware`. Element 0 carried more filter gain and no filter
envelope sweep, because the loaded sound's file configured it. Elements switched
on by hand kept the Data List defaults, which are quieter. Written across and
read back, all eight elements now differ in **nothing** but wave number and note
limits — both blocks, zero remaining bytes.

So the full list of what a fresh element does **not** inherit:

| Address | Parameter | Fresh | Configured |
|---|---|---|---|
| `41 ep 54` | `Pitch Key Follow Sensitivity` | 64 — ignores the keyboard | 96 |
| `42 ep 0C` | `Filter Gain` | 102 | 127 |
| `42 ep 1D` | `FEG Depth` | 104 | 64 |

**The lesson is the method, not the list.** An element spans at least two
parameter blocks, `41 ep` and `42 ep`, and a part dump returns both. Diffing
only the one the symptom suggests cost two wrong hypotheses here — a level
normalisation and a loop-window search, both measured, both irrelevant — and
two listening tests. Diff every block the dump gives you before theorising about
the audio: a parameter reads in seconds, and the Data List defaults are not what
a loaded sound puts in its elements.

#### The loop click: an integer number of periods is the wrong objective

The eight-zone instrument clicked at the loop point on some zones and not
others — mild on the zone rooted at note 48, "vraiment très fort" on the one
playing si3. Measuring the join explained it and ranked the zones in the order
the player had put them.

The join is where the sample's end is followed by its loop start, so continuity
is a **waveform match** between the window before `start` and the window before
the end. Measured on the eight packages as built — loop length chosen as an
integer number of periods of the equal-tempered fundamental, snapped to a
multiple of 16:

| Zone root | Join correlation | Sample jump |
|---|---|---|
| 48 | 0.81 | 1,047 |
| 51 | 0.71 | 1,141 |
| 54 | 0.47 | 2,629 |
| 57 | 0.67 | 29,318 |
| **60** | **0.04** | **24,691** |
| 63 | **−0.49** | 17,736 |
| 66 | **−0.49** | 14,536 |
| 69 | 0.43 | 31,221 |

Root 48 is the best of a bad set and root 60 — which plays si3 — is near zero,
exactly as reported. Two are anti-correlated.

**Why the arithmetic fails.** The tone carries detuned partials, so it is not
periodic at the fundamental at all; it is periodic at the much longer beat
period. An integer number of f0 periods therefore lines up nothing. Searching
instead for the length that **maximises the waveform correlation at the join**,
coarse then fine, finds that beat period and lands on:

| Zone root | Join correlation | Sample jump | Loop length |
|---|---|---|---|
| 48 | 0.99993 | 6 | 1.222 s |
| 51 | 1.00000 | 4 | 0.366 s |
| 54 | 1.00000 | 31 | 1.080 s |
| 57 | 0.99999 | 28 | 1.350 s |
| 60 | 0.99999 | 5 | 1.336 s |
| 63 | 1.00000 | 66 | 0.828 s |
| 66 | 0.99996 | 71 | 0.205 s |
| 69 | 1.00000 | 52 | 0.652 s |

`verified on hardware` for the transfer and the assembly; the audible result is
the player's to judge.

**And one self-inflicted constraint, now removed.** This repository's own
builder asserted `n % 16 == 0`, carrying the 16-sample granularity of the loop
*start* over to the loop *length*. Only the start needs it: `+0x2C` is stored
divided by 16, while `+0x3C` is a plain u32 sample count — and the template
file's own count is 110,235, an odd number, which should have settled it
earlier. The constraint cost up to eight samples of misalignment at every join,
on top of the wrong objective.

### Retracted, 2026-11-24 — the header was malformed, and the answer was already in this repository

The three sections above conclude that the transfer header's first `b4` "must be
1", that it is therefore not a sample count, and that "there is no room left in
the header for a second keybank". **The measurements are sound and the
conclusion is wrong.**

[08-bulk-and-files.md](08-bulk-and-files.md#the-headers-payload) already
documented the header's payload, `verified on hardware`, from a capture of the
official app importing a **stereo** package — the very capture the sections
above kept asking for:

| Offset | Size | Contents |
|---|---|---|
| `0x15` | 4 | sample count |
| `0x19` | **4 × n** | **one entry per sample: its byte size** |

and the Yamaha byte count as `0x12 + 4n`. A stereo header carried **two**
entries of 931,392.

So every refused attempt declared a count of 2 or 5 while sending a payload
sized for one entry. The message was the wrong length, and **result 127 was
answering that, not the count**. Nothing about multi-keybank writing was
established by those runs, in either direction.

What stands, and what does not:

| Claim | Status |
|---|---|
| the 2-byte count at offset 8 is not validated | **stands** — `0`, `1`, `2`, `5` all accepted |
| the second `b4` is the stream's length, checked at its end | **stands** |
| the first `b4` must be 1 | **withdrawn** — it is the sample count |
| a user waveform gets only one keybank through this path | **withdrawn as a conclusion**; still what every attempt *produced*, but no attempt sent a well-formed header |
| the machine flattened a 5-record table onto the whole blob | **stands** as an observation — of a transfer whose header was malformed |

A correctly sized header **has since been tried, and accepted** — see
[the section that follows](#2026-11-24-later--the-eight-sample-header-is-accepted-and-127-was-answering-the-length),
where declaring 8 samples with 8 size entries returns result 0 and the same
count with one entry returns 127. The package is built and waiting
(`clavi-kb8.Y3S`, one waveform, eight keybanks, each with its own matched loop),
and the pusher that sends one size entry per sample is written; the full
transfer has not been run.

**Two process failures, worth more than the field.** The answer was in this
repository, in the document the new section was appended to, about a hundred
lines above it — and a contradicting claim was written without reading it. Then
the gap it left was reported to the owner four separate times as "one capture
would settle it", when that capture was the source of the table all along.
Before measuring a message, read what this repository already says about it; a
measurement that contradicts an existing `verified on hardware` entry is a
reason to stop and reconcile, not to add a second section.

## 2026-11-24, later — the eight-sample header is accepted, and 127 was answering the length

The retraction above left one thing unmeasured: whether a *correctly sized*
multi-sample header is accepted. It is. Three headers were sent, each alone,
with nothing behind it and `ContentsManagementMode` restored in a `finally`, so
nothing was installed —
[`../tools/hardware-probe/probe_header_count.py`](../tools/hardware-probe/probe_header_count.py).

| Header | Sample count at `0x15` | Size entries from `0x19` | Payload | Yamaha count | Result |
|---|---|---|---|---|---|
| control, one sample | 1 | 1 | 18 B | `0x16` | **0** |
| eight samples, well formed | 8 | 8 | 46 B | `0x32` | **0** |
| eight declared, one entry | 8 | 1 | 18 B | `0x16` | **127** |

Four runs of each, all four agreeing, no missing reply. `verified on hardware`.

The third row is the point: it reproduces deliberately the shape the six earlier
attempts sent. Same count, same field, same value — and the only difference that
turns 0 into 127 is the message's length. **Result 127 was answering the length,
not the count.** The field at `0x15` accepts 8.

The arithmetic that makes a header well formed:

| | |
|---|---|
| payload length | `14 + 4n` bytes |
| Yamaha byte count | `0x12 + 4n` |

So `n = 1` gives the 18-byte header that was taken for the only legal form, and
every larger `n` needs 4 more bytes per sample. The 18-byte header is not a
fixed-size structure with a count inside it; it is the smallest member of a
family.

Machine state: firmware answering 4/4 on every address, sequencer stopped
(`01 10 20` = `0`), `ContentsManagementMode` = `0`, tempo 120, 1988 free **sound**
slots (`01 10 09` `UserSoundEmptyContentCount`).

### How high the count goes

The same instrument, header alone, with the count swept and the size entries
always matched to it. `verified on hardware`, four runs of each:

| Declared samples | Payload | Yamaha count | Result |
|---|---|---|---|
| 8 | 46 B | 50 | 0, 0, 0, 0 |
| 16 | 78 B | 82 | 0, 0, 0, 0 |
| 43 | 186 B | 190 | 0, 0, 0, 0 |
| 64 | 270 B | 274 | 0, 0, 0, 0 |
| 88 | 366 B | 370 | 0, 0, 0, 0 |
| 128 | 526 B | 530 | 0, 0, 0, 0 |

So the count field is not capped below 128, and 43 — the number of 3-semitone
zones a full keyboard needs at the factory library's commonest density — is
nowhere near a boundary. A 128-sample header is 526 payload bytes, well inside
the 3992-byte message payload area, so the frame does not constrain it either.

**This is the header and nothing else.** `KeybankFull` is result code 5 and
exists, so a cap exists *somewhere*; it was not reached here, and a header does
not exercise it. The only count carried through a whole transfer and read back
is **8**. Sample memory is the other untested limit: one sample per semitone at
the sizes used here is on the order of 15 MB.

### What this does not say

**Nothing was installed, so nothing in *this* section says a user waveform can
hold more than one keybank.** An accepted header is a message the machine agreed
to receive, not a stored result — the same distinction that
[rule 3](../CLAUDE.md) draws between a table's bytes and a table's behaviour.

| Claim | State |
|---|---|
| a well-formed header may declare 8 samples | **`verified on hardware`** |
| 127 was answering the message length | **`verified on hardware`** — by the reproduction in row 3 |
| a host can store more than one keybank | **answered the same day, and yes** — the full transfer was then run and read back: [the next section](#2026-11-24-later-still--eight-keybanks-written-by-a-host-and-read-back) |

## 2026-11-24, later still — eight keybanks written by a host, and read back

**A user waveform takes more than one keybank through the SysEx content
channel. Eight of them, with their key zones.** The conclusion that it does not
is withdrawn; so is every explanation that was built on it. The cause was the
malformed header, and nothing else.

`verified on hardware`. One run,
[`../tools/hardware-probe/push_keybanks.py`](../tools/hardware-probe/push_keybanks.py)
against `clavi-kb8.Y3S` (one waveform, eight keybanks, eight matched loops),
then [`../tools/hardware-probe/content_pull.py`](../tools/hardware-probe/content_pull.py)
to read back what was stored.

### What the eight keybanks are

Worth stating because it is what makes the zones worth having. The eight zones
are **not one file repitched**. Each root is an independent synthesis at its own
pitch: eight offline renders of the same synthesiser voice of the owner's own at
MIDI notes 48, 51, 54, 57, 60, 63, 66 and 69 — eight files of the same duration
(4.1 s) and distinct content. That is what gives each zone its own timbre and
its own level, and it is also why a **single common gain** across the set is
required rather than a per-sample normalisation, which inverts the engine's
falling level contour into a rising ramp
([above](#normalising-each-zone-to-the-same-peak-is-a-mistake)). Each one's loop
window was chosen by waveform match at the join, not by counting periods
([the loop click](#the-loop-click-an-integer-number-of-periods-is-the-wrong-objective)).

### The transfer

| Step | Sent | Acknowledged |
|---|---|---|
| `ah 03` header | 8 samples, 8 size entries, 46-byte payload, Yamaha count `0x32` | result 0 |
| `ah 0A` packets | eight runs, each restarting its index at 0: 65, 38, 59, 77, 62, 48, 28, 51 packets | every one result 0 |
| `ah 09` waveform body | the 516-byte record table (`4 + 64 × 8`) | result 0 |
| `ah 07` sound body | the sound, its wave pointer rewritten | result 0 |

`01 10 09` went from 1988 to **1987**. That counter is
`UserSoundEmptyContentCount`, so what it shows is the **sound** that was
created, not the waveform — the address was misread when this section was first
written, and the sentence that stood here drew the right conclusion from the
wrong instrument. **Corrected, and it does not change the conclusion**, which
rests on the read-back below: content number 8653 is one waveform holding eight
keybanks. The waveform counters are `01 10 0D` `UserWaveformEmptyContentCount`
(1578 free) and `01 10 0F` `UserWaveformTotalContentCount` (1648); neither was
read before the transfer, so no before-and-after exists for them.

Sample memory, read afterwards: `01 10 11` `SampleMemoryUsedSize` = 23 of
`01 10 13` `SampleMemoryTotalSize` = 510. The unit is not established — an
earlier session read 11 used, and other transfers happened between the two
readings, so the difference cannot be attributed to this one.

### What came back

The dump request for the new waveform (content number 8653) answers with a
header reading **`samples = 8`** and the eight byte sizes in order, then sends
eight separate packet runs and the body.

| | Sent | Back |
|---|---|---|
| record table | 516 B | 516 B, keybank count field = **8** |
| audio | 8 samples, 1,112,816 B | **all eight byte for byte** (SHA-1 equal) |

And the zones survived intact — every key range, root key and loop point
identical to what was sent:

| Keybank | Key range | Root | Loop start | Frames |
|---|---|---|---|---|
| 0 | 0-49 | 48 | 1896 | 84,244 |
| 1 | 50-52 | 51 | 2056 | 49,044 |
| 2 | 53-55 | 54 | 1848 | 77,196 |
| 3 | 56-58 | 57 | 2520 | 99,836 |
| 4 | 59-61 | 60 | 1400 | 81,300 |
| 5 | 62-64 | 63 | 1656 | 62,996 |
| 6 | 65-67 | 66 | 1688 | 36,044 |
| 7 | 68-127 | 69 | 2312 | 65,748 |

Contiguous, no gap, no overlap, covering 0-127.

### The two bytes per record the machine rewrites

Of the 64 bytes in each record, exactly **three** came back changed, the same
three in all eight records.

| Offset | Sent | Back | Reading |
|---|---|---|---|
| `+0x0B` | `01` in every record | **`08` in every record** | **not the channel count.** The audio is eight *mono* samples, and the machine wrote the **keybank count**. "Channels, 1 = mono, 2 = stereo" fitted only because the single multi-keybank case anyone had examined was stereo, where both numbers are 2 — corrected in [06-sounds-presets.md](06-sounds-presets.md#the-rest-of-the-record) |
| `+0x38`, `+0x39` | `4E9C` in every record | a **different** value in each: `A7CA`, `03BC`, `BED6`, `DAFC`, `B539`, `A5C3`, `C5E2`, `D610` | confirms what was already recorded: the machine overwrites it, per keybank, and a host need not compute it. Eight distinct values from one transfer is a stronger instrument than two imports of the same PCM, and it still rules out any function of the audio — the eight payloads differ, but so would eight hashes; what it adds is that the field is assigned **per record within a single transfer** |

Everything else in all eight records — key range, velocity range, pan, root
key, loop switch, sample rate, loop start, frame count — came back unchanged.

### What this costs the earlier write-ups

| Claim | State |
|---|---|
| a user waveform gets only one keybank through this path | **withdrawn** — eight, verified |
| "there is no room left in the header for a second keybank" | **withdrawn** — the room is `14 + 4n` |
| the machine flattens a multi-record table onto one blob | **withdrawn as a property of the machine**; it is what a *malformed* transfer produced |
| `+0x0B` is the channel count | **withdrawn** — it is the keybank count |
| the element route is "the way round it" | **it is still the only route that has been heard.** See the correction below: a host-written multi-keybank waveform stores perfectly and does not play |

The multisampled instrument the whole line of work was after is **writable** in
one transfer, as one waveform, persistent because it is content and not live
state.

> **Correction, later the same day: writable is not playable.** An earlier
> version of this paragraph stopped at "writable" and let the reader assume the
> rest. It does **not** play. A 52-keybank waveform built this way, loaded on a
> part, produces **no sound at all** —
> [the diagnosis](#2026-11-24-night--a-host-written-multi-keybank-waveform-stores-perfectly-and-does-not-play).
> Writing and reading back is `verified on hardware`; a working instrument is
> not. The element route remains the only multisample that has been heard.

### How this was missed for six attempts

Every attempt varied the count and never the message length, so every attempt
was malformed in the same way and the machine answered the same way. The field
table in [08-bulk-and-files.md](08-bulk-and-files.md#the-headers-payload) had
recorded one 4-byte size entry per sample, `verified on hardware`, from a stereo
import — about a hundred lines above the section that concluded the opposite.
The measurement was not wrong; it was never the measurement that was asked for.

## 2026-11-24, same evening — 52 keybanks, one per semitone, and a body is not one message

A multisampled instrument with **one sample per semitone** over MIDI 36-87, as
one waveform with 52 keybanks, written by a host and read back. `verified on
hardware`. Content number **8654**.

### What went on, and what came back

| | Sent | Back |
|---|---|---|
| keybanks | 52, roots 36-87, one per semitone, zones contiguous over 0-127 | **52**, zones and roots identical |
| record table | 3332 B = `4 + 64 × 52` | 3332 B |
| audio | 52 samples, 7,251,232 B | **52 of 52 byte for byte** (SHA-1 equal) |

Counters, read four times each before and after:

| Address | Before | After |
|---|---|---|
| `01 10 0D` `UserWaveformEmptyContentCount` | 1578 | **1577** |
| `01 10 09` `UserSoundEmptyContentCount` | 1987 | 1986 |
| `01 10 11` `SampleMemoryUsedSize` | 23 | **30** |
| `01 10 13` `SampleMemoryTotalSize` | 510 | 510 |

**One waveform for 52 keybanks**, now on the right counter. And the sample
memory unit follows from it: **+7 for 7,251,232 bytes**, so one unit is about
1 MiB and the machine holds about 510 MiB of sample memory. The unit was
recorded as "not established" before this.

### A body is cut at 3000 payload bytes, like a packet

This was found by accident and it matters more than the instrument. The
52-record table came back as **707 bytes of its 3332**, and the metadata parsed
as nonsense. `python-rtmidi` was ruled out first — 5000-byte SysEx messages pass
through a virtual port intact — so the arriving data was logged message by
message:

| Body message | Payload |
|---|---|
| 1 | **3000 B** |
| 2 | 934 B |

3000 + 934 = 3934 encoded → 3332 raw, the whole table. So **`ah 07` / `08` /
`09` bodies are not one message**: the machine cuts them at **3000 payload
bytes**, the same `0xBB8` as a packet, with no count or index of their own —
they are simply consecutive.

`content_pull.py` stored every body message at index 0 and so kept only the
last. Fixed. Nothing had been pulled big enough to show it: the largest body
read before this was 720 bytes.

### The three bytes the machine rewrites, at 52 records

Exactly the same three as at eight, and one of them now settles a field.

| Offset | Sent | Back |
|---|---|---|
| `+0x0B` | `01` in all 52 records | **`52` in all 52 records** |
| `+0x38`, `+0x39` | one value in all 52 | 48 and 50 distinct values |

**`+0x0B` is the keybank count.** Eight keybanks gave `08`, fifty-two give
`52`, and the audio is mono throughout; the "channels, 1 = mono, 2 = stereo"
reading is finished. Everything else in all 52 records — key range, velocity
range, pan, root key, loop switch, sample rate, loop start, frame count — came
back unchanged.

### Why 52, and why that is not the machine's limit

52 is the ceiling of **the sender used here**, which puts the whole record table
in one message: the table is `4 + 64n` bytes, 7-into-8 encoding makes it
`⌈·/7⌉ × 8`, and with the 130 bytes of body metadata it must fit the 3992-byte
payload area. `n = 52` gives 3938 and fits; `n = 53` gives 4012 and does not.

But the machine's own *send* path cuts a body at 3000 bytes, so a **chunked
send** would plausibly carry a larger table. That has not been tried, and
`KeybankFull` (result code 5) exists and has not been reached. So:

| Claim | State |
|---|---|
| 52 keybanks in one waveform, written and read back | **`verified on hardware`** |
| a body arrives cut at 3000 payload bytes | **`verified on hardware`** |
| `+0x0B` is the keybank count | **`verified on hardware`** at 8 and at 52 |
| 52 is the most a host can write | **not established** — it is this sender's one-message limit, not a measured cap |

The instrument itself: roots 36-87 one per semitone, the outer two zones
widened to 0 and 127. The range stops at 87 because the engine's level is flat
from 21 to 87 and then collapses — RMS 4706 at 72, 4543 at 88, 2364 at 96 — so
notes above 87 would make the top of the keyboard vanish. All 52 loop joins
measured at a waveform correlation of 0.9999 or better, and a single common gain
of 1.6363 was applied to the whole set.


## 2026-11-24, night — a host-written multi-keybank waveform stores perfectly and does not play

**The 52 keybanks are stored, verified byte for byte, and silent.** Loaded on a
part, the instrument produces no sound at all. This is the gap between the two
things the earlier sections proved and the one thing they did not test.

### What has been ruled out, and how

The sound was loaded on part 8 (SYNTH 2), `01 18 35` reading `clavi-hq52`. One
address at a time, with part 7 (`clavi-B2op`, a user sound that **does** sound)
as the comparison:

| Suspect | Ruled out by |
|---|---|
| the wave pointer | `41 08 03` reads **462** = content 8654, the waveform the machine assigned. The machine fixes the pointer up itself; the number written into `sound.bin` at `0x1E8` does not have to be right |
| the element | all 192 addresses of `41 ep` and `42 ep` read on part 7 and part 8. **Two differences only**: the wave number, and `41 ep 37` `AEGReleaseTime` at `0` against `83` — set back to 83, still silent |
| the part, and the sound | pointing part 8's element 0 at waveform **426** — the one part 7 uses — makes it **sound**, with nothing else changed. One write separated silent from sounding |
| the record structure | the 64 bytes of three of the 52 records read against the sounding waveform's single record, field by field. They differ only where they must: key range, root key, loop start, last frame, frame count, and the `+0x0B` the machine writes. Every other field is identical |
| the audio | all 52 samples came back from the machine byte for byte, SHA-1 equal to what was sent |

So the element, the part, the sound, the pointer, the record layout and the
audio are all accounted for. What is left is the **multi-keybank waveform
itself**.

### What is not known

The deciding test was interrupted: whether the **8**-keybank waveform (content
8653, number 461) plays. If it does, the fault is the count or something that
scales with it; if it does not, a host-written multi-keybank waveform does not
play at all, whatever the count. **Neither of this project's two multi-keybank
waveforms has ever been heard** — the eight-zone instrument that *was* heard
was the element route, eight separate single-keybank waveforms.

A second control is worth running in the same session: waveform **8592**, the
stereo package the official app imported, is a two-keybank waveform the machine
made itself. Whether it plays on the same element says whether multi-keybank
playback works on this machine at all.

> **No crash.** The machine left the MIDI bus immediately after the write that
> would have begun this test, and the owner confirms they unplugged it. Recorded
> because the coincidence is exactly the shape of a host-reachable crash, and it
> was not one.

### What this costs the claims above

| Claim | State |
|---|---|
| a host can **write** 8 and 52 keybanks into one waveform | **`verified on hardware`**, unchanged |
| the record table and audio read back intact | **`verified on hardware`**, unchanged |
| a host can build a multisampled instrument that **plays** | **not established** — this is the open question now |
| the element route is superseded | **withdrawn** — it is the only multisample that has been heard |
