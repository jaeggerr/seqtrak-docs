# 01 — The machine

What the SEQTRAK is, how it is organised, and the numbers you need before
building a message.

Everything here is `from Yamaha Data List` or from the *SEQTRAK User Guide*
(OS V2.00), except where a line says otherwise.

## What it is

The Yamaha SEQTRAK is a battery-powered groovebox: an 11-track sequencer with
four sound engines, a sampler, a built-in speaker and a microphone, in a
343 × 97 × 38 mm, 0.5 kg box. **It has no screen.** Its entire display surface
is a silkscreened index of about twenty words with one LED each, plus a column
of eight LEDs (the "Global Meter") that shows every numeric value as "how many
dots are lit" — roughly 12 % resolution — and never shows the name of anything:
not the sound, not the effect, not the project.

That is the reason this repository exists. The protocol below is how a host
reads out what the hardware cannot show, and writes back what its front panel
cannot reach.

## Specifications

| | |
|---|---|
| Tone generators | AWM2 (sample playback) and FM with 4 operators |
| Maximum polyphony | AWM2: 128 voices, FM: 8 voices |
| Wave memory | Preset 800 MB (as 16-bit linear), user 500 MB |
| Preset sounds | 2032 (Drum + Synth + DX) plus 392 SAMPLER sounds = 2424 |
| Preset waveforms | 2024, addressable 1-4096 |
| Effects | 12 reverb types, 9 delay types, 85 master-effect types, 85 single-effect types, 5-band master EQ, LP-HP filter per track |
| Tracks | 11 |
| Track types | DRUM, DRUMKIT, SYNTH, DX, SAMPLER |
| Projects on device | 8 |
| Sequencer | up to 128 steps per pattern block, 6 patterns per track, 16 scenes in Song mode |
| Sampling | 44.1 kHz, 16- or 24-bit WAV, up to 16 seconds per sample |
| USB audio | 44.1 kHz, 24-bit, 2 in / 2 out |
| Connectors | USB-C (power, MIDI to host, MIDI to device, audio), PHONES, AUDIO IN, MIDI IN/OUT via the included converter cable |
| Wireless | Bluetooth MIDI; Wi-Fi 2.4 GHz for app data transfer |
| Battery | 2100 mAh / 7.6 Wh lithium-ion, 3-4 h use, 3-5 h charge, 6 W consumption |
| Power input | USB Power Delivery, 4.8-5.2 V at 1.5 A or more |

## Tracks, parts and MIDI channels

The eleven tracks are fixed. Internally they are **parts**, numbered from 0; the
protocol always uses the part number, and the MIDI channel is the part number
plus one. `verified on hardware` — see
[10-verified-behaviour.md](10-verified-behaviour.md).

| Part | Track | Group | MIDI channel |
|---|---|---|---|
| `0` | KICK | Drum | 1 |
| `1` | SNARE | Drum | 2 |
| `2` | CLAP | Drum | 3 |
| `3` | HAT 1 | Drum | 4 |
| `4` | HAT 2 | Drum | 5 |
| `5` | PERC 1 | Drum | 6 |
| `6` | PERC 2 | Drum | 7 |
| `7` | SYNTH 1 | Synth | 8 |
| `8` | SYNTH 2 | Synth | 9 |
| `9` | DX | DX | 10 |
| `10` (`0x0A`) | SAMPLER | SAMPLER | 11 |

The MIDI channel assignment is fixed and cannot be changed.

Addresses that are per-part write that part number into one nibble of the
address-mid byte — `30 5p xx` for a track, `31 1p xx` for its sound, and so on.
[02-sysex-format.md](02-sysex-format.md) sets out the composition rules.

### Which parts accept which blocks

| Block | Parts |
|---|---|
| Project Track (`30 5p`) | 0-10 |
| Chord Notes of Scale (`30 6p`, `30 7p`) | 7-9 (Synth and DX only) |
| Sound Common Name / General / Insertion A / B (`31 0p`, `31 1p`, `31 2p`, `31 3p`) | 0-10 |
| Sound LFO (`31 4p`) | 0-8 and 10 (not DX) |
| Sound Arpeggiator (`31 5p`) | 7-9 (Synth and DX only) |
| AWM element Oscillator / Filter (`41 ep`, `42 ep`) | parts 0-8 and 10, elements 0-7 |
| FM Common (`48 09`) / Operator (`49 o9`) | the DX part only, operators 0-3 |
| SAMPLER Sample (`50 eA`) | elements 0-6 |

### Track types

**Parts 0-6** (the drum tracks) can be re-typed, and only those:

- **Drum** — one sound on the whole track.
- **DrumKit** — seven sounds across the seven keys.
- **Synth** — the track becomes an AWM2 synth.

That is how a host gets more than two synth voices out of the machine. The
command is `01 33 00` with `<part> <type>`, it is acknowledged on `01 33 01`,
and **it deletes the track's pattern and replaces its sound**. The round trip
is `verified on hardware`. Full protocol, type table and the trap in it:
[13-track-types.md](13-track-types.md).

Parts 7-8 are AWM2 synths, part 9 is the 4-operator FM engine ("DX"), part 10
is the sampler. None of those three can be re-typed.

The current type of a part is readable at `01 1p 3C` (`PartAwmType`, declared
0-5, of which only 1 = Drum, 2 = Synth, 3 = DrumKit are understood by the app).
It is a **status read, not the command** — see
[13-track-types.md](13-track-types.md#6-partawmtype-01-1p-3c-is-state-not-the-command).
`from the official app, untested`.

## Pads, keys and scales

- Seven **Drum keys** × 2 rows give the 16-step grid; holding a lit key for two
  seconds opens the Substep setting (none, ×2, ×3 as 8th triplet, ×3 as 16th
  triplet, ×4).
- Step **probability** has 8 levels, set by holding a lit key and pressing
  `[MUTE]`.
- **Micro timing** shifts a step off the grid; the protocol range is
  -60 to +59 ticks.
- The **Synth keys** play the current scale. There are eight scales per project,
  each seven pads wide, and the notes are editable over SysEx at `30 4D xx`
  (`verified on hardware`, including a write) — see
  [03a-parameters-system.md](03a-parameters-system.md) and
  [10-verified-behaviour.md](10-verified-behaviour.md).
- Chords are per track and linked to the project's scale. A note above G8 is
  played one octave down.

## Memory layout

- **8 projects** on the device, plus a temporary/edit-buffer slot (Program
  Change 8 under bank MSB 64).
- Each project holds 11 tracks, a tempo (5-300 BPM), volume, swing, 8 scales and
  one song of up to 16 scenes.
- Each track holds up to 6 patterns, a sound assignment and effects.
- Sound memory: 32 preset banks and 16 user banks of 128 (bank MSB 63).
- Sampler elements: 4 preset banks and 8 user banks of 128 (bank MSB 62); under
  MSB 62 the MIDI **channel number is read as the element number**, and Program
  Change 72 and above are temporary areas used by the sampler.

## Powering a MIDI device from the USB-C port

The SEQTRAK's USB-C port can act as a **USB host** and power an attached MIDI
device with **up to 500 mA**. It supplies **nothing at all** when its own
battery is at 2 LEDs of the Global Meter or less (User Guide §15.2.1). This is
the constraint that governs bus-powered companions such as an external display
or a controller keyboard.

In the other direction, a computer supplies at most 500 mA to the SEQTRAK, which
can drain the internal battery under load; use the USB-C cable to a charger if
you want to play while charging.

## MIDI Thru defaults

MIDI data arriving from outside can be forwarded to another interface. Defaults:
**MIDI (TRS): off, USB: on, Bluetooth: on** — in both cases limited to channel
messages and system realtime messages. Arpeggiator trigger notes and notes on
muted tracks are not forwarded. On USB, Thru only works when connected to a
computer or the SEQTRAK app.

The matching parameters are `00 00 22` (Legacy MIDI Thru), `00 00 23` (USB To
Host MIDI Thru) and `00 00 24` (Bluetooth MIDI Thru), each 0-3 for
Off / Channel / Realtime / Both.

## What the hardware cannot show you

Ranked by how badly a host is needed, with User Guide page numbers:

| Gap | On the hardware | p. |
|---|---|---|
| Any sound-design parameter value (0-127) | 8 LEDs, "rough indication" | 59-63 |
| Which parameter is being edited | one of ~20 fixed index words; everything advanced collapses to "OTHER" | 16, 60 |
| Tempo | 5-300 BPM on 8 LEDs | 18, 26 |
| Sound / preset name | nothing at all, for 2032 presets | 36, 98 |
| Effect type and preset name | a category word plus a number 1-8 | 73 |
| Project name | nothing — slot 1-8 only | 23, 86 |
| Swing, master volume, scale, key, octave | 8 LEDs, and only while the button is held | 27, 48, 94 |
| Pattern length, current bar | only while held | 31, 40 |
| Which mode you are in | Scene mode, Real-time Input and Step Input have no indicator | 42, 51, 79 |
| Metronome / quantize / count-in state | no persistent indicator | 24, 27, 47 |
| Battery level | needs a two-handed button combination | 20 |
| Selected pattern per track (1-6) | press the knob, count LED flashes, decode yellow versus cyan | 33 |

## Where to go next

- Build a message: [02-sysex-format.md](02-sysex-format.md)
- Find a parameter: [03a](03a-parameters-system.md) through
  [03g](03g-parameters-sequencer.md)
- Write notes into a pattern: [04-sequencer-editing.md](04-sequencer-editing.md)
- Follow what the user is doing: [05-live-state.md](05-live-state.md)
- What has actually been tested: [10-verified-behaviour.md](10-verified-behaviour.md)
