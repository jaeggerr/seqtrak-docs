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
