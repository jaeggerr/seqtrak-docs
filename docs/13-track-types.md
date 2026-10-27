# 13 — Re-typing a drum track (DRUM / DRUMKIT / SYNTH)

OS V2.00 lets any of the seven drum parts become an AWM2 synth track, a
seven-sound drum kit, or a plain one-sound drum track. This is how a host gets
more than two synth voices out of the machine.

The protocol was recovered from the official app, then
**exercised on real hardware**: part 6 was converted to SYNTH and acknowledged.
The round trip, the acknowledge address, `type = 2` and the effect on the
assigned sound are `verified on hardware` —
[10-verified-behaviour.md](10-verified-behaviour.md#2026-10-22-later-session-re-typing-a-drum-track-works).
Everything else here is `from the official app, untested`, and each
section says which it is.

> **It is destructive.** The pattern on that track is deleted, and the sound is
> replaced. The pattern claim is the app's own warning, quoted verbatim in
> [§5](#5-it-is-destructive); the sound claim is measured.

## 1. The message

```
request      F0 43 10 7F 1C 0C 01 33 00 <part> <type> F7
acknowledge  F0 43 10 7F 1C 0C 01 33 01 <part> <result> F7
```

`verified on hardware` as a round trip:

```
sent      F0 43 10 7F 1C 0C 01 33 00 06 02 F7
received  F0 43 10 7F 1C 0C 01 33 01 06 00 F7
```

The reply came back in under 3 s with no retry, `PartAwmType` for part 6 went
from 1 to 2, and the other six parts did not move.

| Field | Range |
|---|---|
| `part` | `00`-`06` — drum parts only, see [§4](#4-which-parts-can-be-re-typed). The part is in the **data**, not the address: `verified on hardware` with the six other parts as witnesses |
| `type` | `01` DRUM, `02` SYNTH, `03` DRUMKIT. `01` and `02` are both `verified on hardware` — SYNTH to DRUM and back on part 5, plus two SYNTH to DRUM repairs on parts 3 and 4, each acknowledged with result `0` ([10-verified-behaviour.md](10-verified-behaviour.md)). `03` is not |
| `result` | see [§3](#3-the-acknowledgement--01-33-01) |

To make drum part `p` a synth track:

```
F0 43 10 7F 1C 0C 01 33 00 0p 02 F7
```

Both addresses carry two data bytes, so the message is built with
`CreateByteArrayParameterChange`, not the one-byte Parameter Change form. See
[02-sysex-format.md](02-sysex-format.md).

## 2. The type table, and the trap in it

### The enum

The app's track-type enum:

| Name | Value |
|---|---|
| `Void` | 0 |
| `AwmDrum` | 1 |
| `AwmSynth` | 2 |
| `AwmDrumKit` | 3 |

There is no value for DX or SAMPLER. Those parts are not AWM tracks and this
mechanism does not reach them.

### From track type to the byte on the wire

| Track type | Index | Byte on the wire (index + 1) |
|---|---|---|
| `AwmDrum` (1) | 0 | 1 |
| `AwmSynth` (2) | 1 | 2 |
| `AwmDrumKit` (3) | 2 | 3 |

The result matches the `ChangeAwmTypeRequestMessage.AwmType`
enum exactly (`AwmDrum = 1`, `AwmSynth = 2`, `AwmDrumKit = 3`), which is an
independent confirmation of the arithmetic.

### The same change from the front panel

`from Yamaha Data List` — *SEQTRAK User Guide* §6.7, "Changing the Track Types
[OS V2.00]". Worth having here because it is the only way to make the machine
originate the change rather than receive it, and because it confirms the order
trap from Yamaha's own documentation.

1. Press and hold the **Drum Track knob** of the track to change. Drum keys 9
   to 11 light up: **9 = Drum, 10 = DrumKit, 11 = Synth**.
2. Still holding the knob, press and hold the key for the wanted type for
   **five seconds**. The global meter flashes to show progress.
3. The key lights **purple** when the change is complete.

The guide states two constraints in the same section: the track's sequence data
is deleted, and the type cannot be changed during project playback — matching
the `SequencerPlaying` refusal code in the enum.

The key numbering is the **UI order** (Drum, DrumKit, Synth), one more
independent statement of the mismatch described just above.

### The UI order is not the wire order

| | DRUM | DRUMKIT | SYNTH |
|---|---|---|---|
| UI radio-button index | 0 | 1 | 2 |
| SysEx index | 0 | 2 | 1 |
| **byte on the wire** | **1** | **3** | **2** |

The app keeps the two orders apart explicitly: `AwmDrum` 0, `AwmDrumKit` 1,
`AwmSynth` 2 is the **display** order, and it is converted to the wire order
above before anything is sent.

**Confusing the two sends a DRUMKIT where a SYNTH was meant.** On screen the
order is DRUM, DRUMKIT, SYNTH; on the wire it is DRUM, SYNTH, DRUMKIT.

## 3. The acknowledgement — `01 33 01`

The acknowledge address is `01 33 01`, the same block as the request.

The payload is `<part> <result>`, read the same way as the request.

**Both forms travel machine → host** — `verified on hardware`. When the change
is made on the **front panel**, the machine emits `01 33 00 <part> <type>`
*and* `01 33 01 <part> <result>` with nothing requested, and pushes
`01 1p 3C` as state. When the change is sent by a **host**, only `01 33 01`
comes back. So a receive path must decode the command form as well; the
official app's receive filter for it is live code.
Method and the raw capture:
[10-verified-behaviour.md](10-verified-behaviour.md#both-01-33-00-and-01-33-01-travel-machine--host).

### Result codes

`ChangeAwmTypeAcknowledgeMessage.Result`:

| Code | Name | Status |
|---|---|---|
| 0 | `Success` | `verified on hardware` — returned after a successful conversion |
| 1 | `DoNothing` | inferred from the enum name; never observed |
| 2 | `SequencerPlaying` | inferred from the enum name; never observed |
| 3 | `Sampling` | inferred from the enum name; never observed |
| 4 | `MixerOrSongMode` | inferred from the enum name; never observed |
| 5 | `ContentMode` | inferred from the enum name; never observed |
| 6 | `Busy` | inferred from the enum name; never observed |
| 127 | `UnknownError` | inferred from the enum name; never observed |

The names imply four preconditions: the sequencer must be stopped, the machine
must not be sampling, must not be in mixer or Song mode, and must not be in
content-management mode.

> **Only code 0 has been seen. The app never reads `Result` at all.** None of
> its five acknowledge handlers looks at anything but the part index.
>
> So the code **numbers and names** are certain, `Success = 0` is confirmed,
> and the other seven are inferred from naming alone. No refusal has been
> provoked yet. To confirm a change actually happened, re-read `01 1p 3C`
> ([§6](#6-partawmtype-01-1p-3c-is-state-not-the-command)) rather than trusting
> an acknowledgement you have not decoded.

### Should a host wait for it?

Yes. The app subscribes to `Observable.First<ChangeAwmTypeAcknowledgeMessage>()`
**before** sending, and calls `CommonMessageBox.Hide()` when it arrives — it
blocks its own UI until the acknowledgement.

But remember the standing rule from
[10-verified-behaviour.md](10-verified-behaviour.md): **a missing reply is never
information**. If nothing arrives, retry, then read `01 1p 3C`.

## 4. Which parts can be re-typed

**Parts 0-6 only**, as far as the app is concerned: it rejects any index from
7 up with `GetAwmTrackType: Invalid index`, and it follows `PartAwmType` on
parts 0-6 only.

The three concrete types `ParameterModel.ChangeAwmTrackType` instantiates are
`DrumTrackModel`, `DrumPartSynthTrackModel` and `DrumKitTrackModel` — all three
are drum *parts*. Parts 7-8 (`SynthTrackModel`), 9 (`FMTrackModel`) and 10
(`SamplerTrackModel`) live in separate arrays in `ParameterModel` and do not
implement `IAwmTrack`.

**A re-typed drum track is a `DrumPartSynthTrackModel`, not a
`SynthTrackModel`.** It is not the same class as parts 7-8, even though the app
reuses the same editing screen for both.

Open points:

- Nothing in the app distinguishes part 0 from the other six, so all seven
  presumably accept all three types. Not verified.
- **No limit on the total number of converted tracks appears anywhere in the
  app** — no counter, no check. If the firmware imposes one it would surface as
  a non-zero `Result`, which the app ignores, so the app would not notice it
  either. Unknown.
- What the firmware does with `part >= 7` is unknown; the app never sends it.

## 5. It is destructive

Not an inference — it is written in the app, for the user.

Choosing a new type in the app sends nothing at first: it opens a confirmation
box, and only the OK button sends the message of [§1](#1-the-message). The
box's English text:

| Key | Text |
|---|---|
| `Msg_ChangeAwmTrackType` | "ARE YOU SURE YOU WANT TO PROCEED?\nTHE PATTERN CREATED IN THE CURRENTLY SELECTED TRACK TYPE WILL BE DELETED." |
| `Msg_ChangeAwmTrackType_Button` | "OK" |
| `ChangeTrackType_Title` | "CHANGE TRACK TYPE" |
| `ChangeTrackType_Description` | "Please select DRUM, DRUMKIT, or SYNTH. The original pattern data will be deleted." |

Both strings name the **pattern**; neither mentions the sound.

On the app side, a type change throws the track away and builds a new one,
sound included. That is a full reload of local state.

### The sound is replaced too — `verified on hardware`

The warning text names only the pattern, but the sound does not survive either.
Measured on part 6, converting DRUM → SYNTH:

| | before | after |
|---|---|---|
| `CurrentSound` part 6 (`01 16 33`) | **456** | **4099** |

4099 is outside the range of drum sounds observed on parts 0-6 (2 … 553), so
the firmware loads a default from the synth space — that reading of *why* is an
inference; the two values are measured.

> **After converting a track, assign its sound explicitly with `01 1p 33`.**
> Whatever was there is gone.

### Still not settled

**Are all six patterns wiped, or only the current one?** The wording ("the
pattern created in the currently selected track type") reads more like all of
the track's content in its current type. Not measured — the part used in the
hardware test held no known content to compare. Assume all six.

### Order of work on real hardware

1. Back the project up first, or accept losing it.
2. Stop the sequencer — `01 10 20` must read `0`.
3. Not in Song mode, mixer, sampling or content-management mode
   (`01 10 01` = 0, `01 10 22` = 0).
4. Send the change; wait for `01 33 01` for that part.
5. Re-read `01 1p 3C` to confirm.

Convert tracks **before** building any Song-mode scenes: `MixerOrSongMode` is a
documented refusal reason.

## 6. `PartAwmType` (`01 1p 3C`) is state, not the command

They are two different mechanisms, and only one of them is a command.

| | `01 33 00` | `01 1p 3C` |
|---|---|---|
| Kind | command, acknowledged on `01 33 01` | PCApp parameter, 1 byte |
| Part carried in | the data (`data[0]`) | the address (`am = 0x10 \| part`) |
| Declared range | 1-3 | **0-5** |
| App sends it | yes, on user action | never on its own initiative — see below |
| App reads it | — | yes, by Parameter Request at startup |

### Decoding the value

When the app receives `01 1p 3C`, it converts the value to a track type: values
1-3 map to themselves, anything else to `Void` (0).

| Value | Resulting `TrackType` |
|---|---|
| 0 | `Void` — the app does nothing useful |
| **1** | `AwmDrum` |
| **2** | `AwmSynth` |
| **3** | `AwmDrumKit` |
| 4 | `Void` |
| 5 | `Void` |

**That table describes the app, not the machine.** Only 1, 2 and 3 are
re-typing targets, with exactly the same encoding as `01 33 00`; the app maps
everything else to `Void` because everything else is a track it cannot re-type.

**4 and 5 are real values, `verified on hardware`.** This page used to carry a
hypothesis explicitly marked *not a fact* — that 4 and 5 might be the non-AWM
engines. The address has since been queried on all eleven parts, four attempts
each, 44 replies out of 44:

| Part | Value | The track there |
|---|---|---|
| 0-2 | `01` | drum tracks |
| 3-6 | `02` | drum tracks re-typed to SYNTH |
| 7, 8 | `02` | SYNTH 1, SYNTH 2 |
| 9 | `04` | DX — the FM track |
| 10 | `05` | SAMPLER |

Part numbering is itself `verified on hardware`, so the DX track reporting `04`
and the sampler reporting `05` are measurements. What remains an **inference**
is the reading that `PartAwmType` names *the engine backing the part*; it fits
every observed value but has not been tested by a gesture. Full method in
[10-verified-behaviour.md](10-verified-behaviour.md#2026-10-22-hardware-session-01-1p-3c-answers-for-every-part).

> **Do not conclude that 0-5 is merely the factory's declared bound and that
> only 1-3 occur.** Two of the six values arrive from the hardware on every
> read of parts 9 and 10. A decoder that returns `nil`, `unknown` or an error
> for `04` and `05` is rejecting normal traffic rather than catching a fault.

### Does the app ever write it?

The app does have a write path to `01 1p 3C`, but it only fires when the value
changes locally, and the only thing that changes it locally is a value received
from the machine, with sending switched off for the duration.

That is the standard echo-suppression pattern, so in practice the app never
*originates* a write to `01 1p 3C`; it only follows state pushed by the machine.
From the app's point of view `01 1p 3C` is a **status read**.

Whether the firmware would *act* on a write to `01 1p 3C` is unknown. Use
`01 33 00`, which is the path the app exercises, and use `01 1p 3C` to check:

```
F0 43 30 7F 1C 0C 01 1p 3C F7
```

## 7. Nearby per-part addresses worth having

`am = 0x10 | part`. From [data/parameters.csv](../data/parameters.csv).

| `al` | Name | Range |
|---|---|---|
| `32` | `ReserveChangePattern` | 0-6 |
| `33` | `CurrentSound` | 0-6143, 2 bytes |
| `35` | `CurrentSoundName` | 87-byte string |
| `36` | `DrumPatternPage` | 0-7 |
| `37` | `DeletePattern` | 0-5 |
| `3C` | **`PartAwmType`** | 0-5 |
| `3D` | `DrumKitCurrentElement` | 0-6 |
| `48` | `DeletePatternElement` | 0-6 |

## 8. What is left to test on hardware

Done: the round trip, `Result = 0` on success, `type = 02` → SYNTH, the part
being carried in the data, and the sound being replaced. See
[10-verified-behaviour.md](10-verified-behaviour.md#2026-10-22-later-session-re-typing-a-drum-track-works).

Remaining, in order of usefulness:

1. **Are all six patterns wiped, or only the selected one?** Write a known note
   into each of the six patterns of a drum part, convert, and read them back.
2. ~~**`type = 01` (DRUM) and `type = 03` (DRUMKIT).**~~ **Done** — both were
   sent to part 2 on 2026-10-22, both acknowledged with `Result = 0`, both read
   back as the value asked for, and the part was round-tripped `01` → `03` →
   `01`. The whole encoding is now `verified on hardware`:
   [10-verified-behaviour.md](10-verified-behaviour.md#2026-10-22-hardware-session-types-01-and-03-on-the-wire).
   A front-panel re-type was also captured: the machine sends `01 33 01`
   **spontaneously**, together with `01 33 00` and a `01 1p 3C` state push.
3. **What `Result` a refusal returns.** Start the sequencer and send the
   command; `SequencerPlaying = 2` is the prediction. That one experiment would
   confirm or demolish the whole result table.
4. **`part >= 7`.** The app never sends it, so the firmware's response is
   entirely unknown — treat as risky.
