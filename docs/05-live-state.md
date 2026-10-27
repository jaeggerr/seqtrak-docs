# 05 — Live state: the `01 xx xx` zone

The address-high `01` space is the SEQTRAK's **live session and editing state**:
which project is loaded, which part is selected, what the sliders are assigned
to, whether the sequencer is running, how full the sample memory is. None of it
is in the Yamaha Data List.

For anything that mirrors what a user is doing — an external display, a watch
app, a controller that follows the hardware — this is the zone that matters.

Source: `from the official app, untested`, from the `PCApp`
namespace, except where a row or note says `verified on hardware` or
`reverse-engineered from app traffic`. 20 addresses in this zone have now been
read back from a real unit; see
[10-verified-behaviour.md](10-verified-behaviour.md).

The full machine-readable table is
[03b-parameters-live-state.md](03b-parameters-live-state.md) and
[`../data/parameters.csv`](../data/parameters.csv).

## How the zone is addressed

| Mid | Block |
|---|---|
| `01 00 xx` | identity: firmware version |
| `01 10 xx`, `al < 0x30` | global session state |
| `01 1p xx`, `al >= 0x30` | per-part editing state, `p` = part number |
| `01 20 xx`, `01 22 xx` | bulk acknowledgement addresses |
| `01 31 xx` | defragmentation |
| `01 32 xx` | project save |
| `01 34 xx` | factory reset |
| `01 40`-`01 42` | remove project / sound / element |

> **The `01 10` overlap matters.** Part 0's per-part block composes to mid
> `0x10 | 0 = 0x10`, the same mid as the global block. They are separated by the
> low byte: `al < 0x30` (plus `0x70`) is global, `al >= 0x30` is part 0.
> `verified on hardware` — both halves answered in the same session.

## `01 00 xx` — identity

| `al` | Parameter | Size | Notes |
|---|---|---|---|
| `00` | `FirmwareVersion` | 4 | returned `02 00 00 02` on a unit running OS V2.00 — `verified on hardware` |
| `04` | `CompatibleVersion` | 1 | returned `01` — `verified on hardware` |

## `01 10 xx` — global session state

| `al` | Parameter | Range | Status |
|---|---|---|---|
| `00` | `SystemStatus` | 0-1 | `verified on hardware` (read `00`) |
| `01` | `ContentsManagementMode` | 0-1 | must be `1` for content operations — see [08-bulk-and-files.md](08-bulk-and-files.md) |
| `02` | `Battery` | 0-100 | `verified on hardware` (read 70, tracks the real charge) |
| `03` | `AutoPowerOffTime` | 0-6 | |
| `06` | `WiFiStartupResult` | 0-7 | |
| `07` | `HeadphonePlugStatus` | 0-1 | `verified on hardware`, **semantics proven**: 0 → 1 when headphones are plugged in |
| `08` | `ResumeTrigger` | 0-2 | `verified on hardware` |
| `09` | `UserSoundEmptyContentCount` | 2 bytes | |
| `0B` | `UserElementEmptyContentCount` | 2 bytes | |
| `0D` | `UserWaveformEmptyContentCount` | 2 bytes | |
| `0F` | `UserWaveformTotalContentCount` | 2 bytes | |
| `11` | `SampleMemoryUsedSize` | 2 bytes | `verified on hardware` (read 11; unit unconfirmed) |
| `13` | `SampleMemoryTotalSize` | 2 bytes | `verified on hardware` (read 510; probably MB) |
| `15` | `CurrentProject` | 0-7 | `verified on hardware`; also `reverse-engineered from app traffic` — found twice, independently |
| `16` | `CurrentProjectName` | 87 bytes, string | |
| `17` | `GeneralMode` | 0-3 | `verified on hardware` |
| `18` | `DrumPadMode` | 0-20 | |
| `19` | `SynthPadMode` | 0-2 | |
| `1A` | `MasterEffectSliderMode` | 0-1 | **never broadcast** — app-internal, see below |
| `1B` | `ReverbSliderMode` | 0-1 | **never broadcast** |
| `1C` | `VariationSliderMode` | 0-1 | **never broadcast** |
| `1D` | `ClearEffect` | trigger | |
| `1E` | `EffectModeSelect` | 0-1 | |
| `1F` | `UndoRedo` | trigger | |
| `20` | `SequencerStatus` | 0-1 | `verified on hardware`, **semantics proven**: 0 → 1 on play; **broadcast unsolicited** |
| `21` | `RecordingStatus` | 0-1 | |
| `22` | `SamplingStatus` | 0-2 | |
| `23` | `MonitoringStatus` | 0-1 | |
| `24` | `CategoryJumpFavoriteFiltering` | 0-1 | |
| `27` | `CurrentPart` | 0-10 | `verified on hardware`, **semantics proven**: reads 7 when SYNTH 1 is selected; **broadcast on every track change** |
| `28` | `SamplerCurrentElement` | 0-6 | |
| `29` | `NotifyResetPlayCurrentStepCount` | notification | |
| `2A` | `NotifyAllPatternChange` | 0-6 | |
| `2B` | `NotifyBarLengthChange` | 0-1 | |
| `2C` | `NotifySynthPadNoteOn` | 0-6 | |
| `2D` | `MasterKnobMode` | 2 bytes | `verified on hardware` |
| `2E` | `ParameterLedMode` | 0-43 | `verified on hardware`; **broadcast** alongside sound changes, knob moves and FX-block changes. The way to follow the active FX block — see below |
| `2F` | `DeviceID` | 0-1 | |
| `70` | `NotifyChangeProjectWithResume` | 0-1 | |

Two further addresses in this block were seen broadcasting from real hardware
without being identified: `01 10 20` carrying `00` and `01 10 2E` carrying `01`,
both reported as during a running sequencer over USB in host mode (2026-08).
Later work identified them as `SequencerStatus` and `ParameterLedMode`.
`reverse-engineered from app traffic`.

For `01 10 2E` the value fits. For `01 10 20` it does not: `SequencerStatus` is
`01` while playing and `00` while stopped, `verified on hardware` over eight
transitions ([10-verified-behaviour.md](10-verified-behaviour.md)), so a `00`
cannot have been broadcast by a running sequencer. The identification is the
better-evidenced of the two, so what is most likely loose is the 2026-08
session's description of the machine's state — the broadcast was probably the
stop transition. Said plainly because that session's note is the only record of
it, and nobody re-read the state at the time.

## `01 1p xx` — per-part editing state

`p` is the part number, so the mid byte is `0x10 | part`.

| `al` | Parameter | Range |
|---|---|---|
| `30` | `SoundDesignPage` | 0-5 — `verified on hardware` |
| `31` | `InsertionEffectSliderMode` | 0-1 — **never broadcast**, app-internal |
| `32` | `ReserveChangePattern` | 0-6 |
| `33` | `CurrentSound` | 2 bytes — `verified on hardware` (read 2) |
| `35` | `CurrentSoundName` | 87 bytes, string |
| `36` | `DrumPatternPage` | 0-7 |
| `37` | `DeletePattern` | 0-5 |
| `38` | `WritingMotionRecord` | 0-1 |
| `39` | `PatternKnobMode` | 2 bytes — `verified on hardware` |
| `3C` | `PartAwmType` | 0-5 |
| `3D` | `DrumKitCurrentElement` | 0-6 |
| `40` | `SamplingPadSampleSize` | 4 bytes |
| `44` | `CurrentElement` | 2 bytes |
| `46` | `CurrentElementName` | 87 bytes, string |
| `48` | `DeletePatternElement` | 0-6 |
| `50`-`52` | `MasterSlider1..3Assign` | 0-24 — `50` is `verified on hardware` |
| `53`-`55` | `SingleSlider1..3Assign` | 0-24 — `53` is `verified on hardware` |
| `56`-`58` | `SendSlider1..3Assign` | 0-24 |
| `59`-`5B` | `MasterSlider1..3ControlValue` | 0-127 |
| `5C`-`5E` | `SingleSlider1..3ControlValue` | 0-127 — `5C` is readable, but see below |
| `5F`-`61` | `SendSlider1..3ControlValue` | 0-127 |

## How to follow a knob — and how not to

An earlier reading of the official app suggested the `…Assign` / `…ControlValue` pair
was the way to track a knob: `Assign` says which parameter the slider drives,
`ControlValue` its current value. **Hardware says otherwise.**

`01 1p 5C` (`SingleSlider1ControlValue`) is readable on request, but it **was
never broadcast** during 165 seconds of deliberate knob and slider movement.
`verified on hardware`.

What the machine emits depends on which control moves. `verified on hardware`:

- The **four per-track knobs** (Sound Select, Mono/Poly/Chord, Pan, Volume)
  emit **Control Change only, no SysEx at all** — CC 0/32 plus a Program
  Change, CC 26, CC 10 and CC 7 respectively. Measured over 85 seconds: 66
  messages, zero SysEx.
- The **FX sliders** emit **both** voices: a SysEx Parameter Change at each real
  parameter address, plus one Control Change per slider step. Measured over 100
  seconds: 390 messages across 6 SysEx addresses and 171 CCs.

So a client cannot assume SysEx for every gesture, and must accept either voice
as a trigger — **but the two are not interchangeable.**

### The SysEx voice carries strictly more

One slider can drive **several parameters**, and only SysEx reports all of them:

| Block | CC messages | SysEx messages | SysEx addresses |
|---|---|---|---|
| Single Effect | 34 | 34 | 1 |
| Master Effect 2 | 35 | 70 | 2 |
| Master Effect 3 | 56 | 112 | 2 |

The CC reports the **slider position**, one per step. The SysEx reports **every
parameter the effect preset moves**. Master Effect 3 parameter 2 (`30 45 05`)
has no CC assigned at all, so a CC-only listener never learns it moved.

`verified on hardware`.

Also worth knowing for a listener: **Master Effect CCs arrive on channel 1**
regardless of the selected part, while Single and Insertion Effect CCs arrive on
the **track's** channel. Master effects are project-wide, so this is consistent —
but you have to listen on both.

**Where SysEx is available, prefer it.** It is self-describing: decode the
received address against the parameter table
([`../data/parameters.csv`](../data/parameters.csv)) and you have the parameter's
name, range and display mapping without any further lookup. The CC voice gives
only a controller number, which needs the CC map
([`../data/cc-map.csv`](../data/cc-map.csv)) and still cannot distinguish
parameters that share a controller.

The `01 1p 5x` mirror appears to exist for the official app's assignment
display, not for gesture tracking.

## What the machine broadcasts without being asked

`verified on hardware`, from a timestamped gesture-by-gesture listen.

| Gesture | What is emitted |
|---|---|
| Track change | SysEx `01 10 27` = the new part index |
| Pattern change | SysEx `30 5p 0F` = the new pattern, 0-indexed |
| Sound change | **Bank Select MSB + LSB, then Program Change** on the track's channel — no SysEx |
| Knob or slider | SysEx at the real parameter address **and** a CC on the track's channel |
| Play / stop | SysEx `01 10 20` = `01` / `00`, plus realtime `FA` / `FC` |
| Pads and sequencer notes | Note On/Off on the track's channel |
| FX button press | SysEx `01 10 2E` `ParameterLedMode` — observed taking 3, then 2, then 1 as the block cycled |
| Sound change, knob move | SysEx `01 10 2E` `ParameterLedMode` alongside |

So a passive listener can keep track of the selected part, the selected pattern,
transport state, the loaded preset and every parameter edit, with no polling at
all — the sound change carries its Bank Select, so the preset resolves straight
out of the local catalogue (see
[06-sounds-presets.md](06-sounds-presets.md)). What it cannot get passively is
the name of a **user** sound, and the mute/solo state (CC 23 and CC 24 are
receive-only).

Nothing in this zone is broadcast unless `Transmit System Exclusive` is on for
the interface in use (`00 00 10` for USB, `00 00 14` for Bluetooth); see
[07-transports.md](07-transports.md).

## Following the active FX block

Use **`01 10 2E` `ParameterLedMode`**, not the slider-mode flags.

The four flags that look like they should report it —
`MasterEffectSliderMode` (`01 10 1A`), `ReverbSliderMode` (`1B`),
`VariationSliderMode` (`1C`) and `InsertionEffectSliderMode` (`01 1p 31`) —
were **none of them emitted** during a capture in which the FX button was
pressed three times. They are readable on request but appear to exist for the
official app's own state, not as notifications. `verified on hardware`.

`ParameterLedMode` did change, taking 3, then 2, then 1. Since it is also what
the hardware LEDs are showing, it is the natural thing for an external display
to mirror. Its full 0-43 scale is undecoded — mapping it is a pure read-only
job with a high payoff, listed in
[12-open-questions.md](12-open-questions.md).

## Other `01` sub-zones

| Address | Parameter | Notes |
|---|---|---|
| `01 20 00` | `AcknowledgeAddress` | the device answers bulk operations here |
| `01 22 00` | `InfoAckAddress` | |
| `01 31 00` | `DefragmentationWaveform` | trigger |
| `01 31 01` | `DefragmentationSampleMemory` | trigger |
| `01 31 02` | `DefragmentationResult` | |
| `01 32 00` | `SendProjectSave` | data `01` |
| `01 34 00` | `FactoryReset` | **destructive** |
| `01 34 01` | `FactoryResetResult` | |
| `01 40 00` | `RemoveProjectAddress` | **destructive** |
| `01 41 00` | `RemoveSoundAddress` | **destructive** |
| `01 42 00` | `RemoveElementAddress` | **destructive** |

`from the official app, untested`. The four destructive addresses
are listed for completeness and for parser safety — do not send them
speculatively.

## `18 00 xx` — drum-kit element status

A companion block to the `01` zone. `from the official app,
untested`.

| `al` | Parameter | Size |
|---|---|---|
| `00` | current drum-kit element | 2 bytes |
| `02` | sound name | 87 bytes, string |
| `03` | sub-category | 1 |
| `04` | delete pattern | 1 |
| `05` | mute | 1 |
