# 11 — Controllers and the CC map

Driving the SEQTRAK from an external MIDI controller, and a worked mapping for
the Arturia MiniLab 3.

The full controller map is [`../data/cc-map.csv`](../data/cc-map.csv).
`from Yamaha Data List`.

## The principle

**One track = one MIDI channel**, fixed: channel = part number + 1 (`verified on
hardware`). So a controller selects a track by choosing a channel, and every CC
it sends on that channel lands on that track.

## Sound-design CCs

The controls a performer actually wants. Channel 1-11 unless stated.

| CC | Parameter | Range | Available on |
|---|---|---|---|
| 7 | Track Volume | 0-127 | all |
| 10 | Track Pan | 1-127 | all |
| 20 | EQ High Gain | 40:-12 dB / 64:0 / 88:+12 dB | all |
| 21 | EQ Low Gain | 40:-12 dB / 64:0 / 88:+12 dB | all |
| 25 | Drum Pitch | 40:-24 / 64:0 / 88:+24 | Drum (ch 1-7) |
| 26 | Mono/Poly/Chord | 0:Mono / 1:Poly / 2:Chord | Synth, DX (ch 8-10) |
| 71 | Filter Resonance | 0:-64 / 64:0 / 127:+63 | all |
| 73 | EG Attack Time | 0:-64 / 64:0 / 127:+63 | all |
| 74 | Filter Cutoff Frequency | 0:-64 / 64:0 / 127:+63 | all |
| 75 | EG Decay/Release Time | 0:-64 / 64:0 / 127:+63 | all |
| 91 | Reverb Send | 0-127 | all |
| 94 | Delay Send | 0-127 | all |
| 5 | Portamento Time | 0-127 (0 = off) | Synth, DX, mono only |
| 65 | Portamento Switch | 0:off / 1:on | Synth, DX |
| 27 | ARP Template | 0-15 (0 = off) | Synth, DX |
| 28 | ARP Gate | 0:0 % - 127:200 % | Synth, DX |
| 29 | ARP Speed | 0:200 % / 3:100 % / 9:25 % | Synth, DX |
| 116 | FM Algorithm | 0-11 | DX |
| 117 | FM Modulation Amount | 0-127 | DX |
| 118 | FM Modulator Frequency | 0-127 | DX |
| 119 | FM Modulator Feedback | 0-127 | DX |

> **A conflict.** The Data List gives CC 27 as `ARP TEMPLATE`, range 0-15 with
> 0 = off, matching the 16-entry arpeggio preset list
> ([appendix-f-arpeggio-presets.md](appendix-f-arpeggio-presets.md)). The User
> Guide calls the same controller `ARP TYPE` with range **0-16**. The Data List
> is the authoritative reference for ranges, so treat it as 0-15; the User Guide
> figure is probably a 1-based count. Listed in
> [12-open-questions.md](12-open-questions.md).

### Which CCs the front panel actually sends

`verified on hardware` on part 7 (channel 8): the four per-track knobs are
exactly page 1 of that engine's sound-design table, and they send

| Knob | Emits |
|---|---|
| Sound Select | `CC 0` = 63, `CC 32` = bank LSB, then a Program Change |
| Mono/Poly/Chord | `CC 26` (0 Mono, 1 Poly, 2 Chord) |
| Pan | `CC 10` |
| Volume | `CC 7` |

and **no SysEx at all**. A client that wants to mirror the front panel must
therefore listen to Control Change, not only to SysEx. Which page the four
knobs are on follows the engine — see
[appendix-h-sound-design-parameters.md](appendix-h-sound-design-parameters.md).

## Effect CCs

| CC | Target | Channel |
|---|---|---|
| 102, 103, 104 | Master Effect 1 assigned parameters 1, 2, 3 | 1 |
| 105 | Master Effect 2 assigned parameter 1 | 1 |
| 106 | Master Effect 3 assigned parameter 1 | 1 |
| 107, 108, 109 | Single Effect assigned parameters 1, 2, 3 | the track's |
| 110, 111, 112 | Send Reverb assigned parameters 1, 2, 3 | 1 |
| 113, 114, 115 | Send Delay assigned parameters 1, 2, 3 | 1 |

Controller numbers `from Yamaha Data List`.

**The channel column matters for a listener.** Master Effect CCs arrive on
**channel 1** regardless of which part is selected, while Single and Insertion
Effect CCs arrive on the **track's** channel. `verified on hardware` for CC 105,
106 (channel 1) and CC 107 (channel 8 with part 7 selected); the send-effect
rows are inferred from master effects being project-wide in the same way, and
are untested.

Which parameter a slider actually reaches depends on the effect preset in use —
see [appendix-e-effect-presets.md](appendix-e-effect-presets.md), whose
"Slider 1/2/3" columns are exactly these assignments.

### A CC does not tell you everything a slider did

An FX slider emits **both** a CC and a SysEx Parameter Change, and they are not
redundant: the CC reports the slider position once per step, while the SysEx
reports every parameter the preset moves. One slider on Master Effect 2 produced
35 CCs and 70 SysEx messages across 2 addresses; Master Effect 3 produced 56
CCs and 112 SysEx across 2. Master Effect 3 parameter 2 has **no CC at all**.

So a controller mapping can *drive* the machine through CC perfectly well, but a
client that wants to *mirror* it should decode the SysEx voice. `verified on
hardware` — see
[10-verified-behaviour.md](10-verified-behaviour.md#one-slider-drives-several-parameters).

## Receive-only and transmit-only

- **CC 23 (Mute)** and **CC 24 (Solo)** are **receive only**. The SEQTRAK accepts
  them but never reports its own mute or solo state this way, so a controller
  with latching mute buttons cannot stay in sync by listening. Solo is readable
  at `30 40 68`; mute needs a poll of `30 5p 29` per track.
- **CC 11 (Expression)**, **CC 64 (Sustain)**, **CC 66 (Sostenuto)**, **CC 6/38
  (Data Entry)** and **CC 96/97 (Data Entry inc/dec)** are receive only.
- **Bank Select (CC 0 / 32)** is transmitted as well as received: a sound change
  sends MSB, LSB and then the Program Change, every time. `verified on
  hardware`. An earlier conclusion in this repository said the opposite; it was
  wrong. See
  [10-verified-behaviour.md](10-verified-behaviour.md#bank-select-is-transmitted--a-documented-conclusion-reversed).

## RPN

The SEQTRAK recognises RPN (CC 100 / 101) but **not NRPN** (CC 98 / 99), so
every external control has to go through plain CC. Three RPNs exist, all
receive-only:

| RPN LSB / MSB | Parameter | Data range |
|---|---|---|
| `00 00` | Pitch Bend Sensitivity | `00`-`18` (0-24 semitones) |
| `01 00` | Master Fine Tune | `{mm,ll}` from `{00,00}` through `{40,00}` to `{7F,7F}` |
| `02 00` | Master Coarse Tune | `28`-`40`-`58` (-24 / 0 / +24 semitones) |
| `7F 7F` | RPN reset | leaves internal values untouched |

`from Yamaha Data List`.

## Two switches that silently block Program Change

Both default to on: `00 00 07` (Receive/Transmit Bank Select) and `00 00 08`
(Receive/Transmit Program Change). If preset switching from a controller does
nothing, check these first.

Then check that the controller sends **Bank Select before the Program Change**.
A third party reports that a Program Change on its own selects nothing —
reported, not reproduced here
([12-open-questions.md](12-open-questions.md#opened-by-a-third-party-receive-side-report-2026-11-14)).

---

# Arturia MiniLab 3 mapping

A worked, working example: a MIDI Control Center template that turns a MiniLab 3
into a SEQTRAK editor and finger-drumming surface, with no computer in the loop.
The template is produced by a generator script in the sibling `minilab3` project
(outside this repository).

## Wiring

**USB** (simplest) — MiniLab 3 USB-C → SEQTRAK USB-C. The SEQTRAK is host and
powers the MiniLab, up to 500 mA — and **nothing at all** when its battery is at
2 Global-Meter LEDs or fewer (User Guide §15.2.1). One cable.

**MIDI DIN** — MiniLab 3 `MIDI OUT` (mini jack) → the DIN adapter supplied with
the MiniLab → a MIDI cable → the **MIDI IN** of the converter cable supplied with
the SEQTRAK. The MiniLab then needs its own power (any USB charger or power
bank).

## The idea

On the MiniLab, **`Shift` + a keyboard key changes the keyboard channel**, live,
with no computer. So the eight encoders, both touch strips and the keyboard are
all set to the "Keyboard" channel: `Shift` + key picks a track and the whole
panel follows it at once. That is the sound editor the SEQTRAK hides inside its
app.

The faders and pads stay on fixed channels — otherwise access to the other
tracks would be lost.

## Encoders — follow the selected track

| # | CC | Parameter |
|---|---|---|
| 1 | 74 | Filter Cutoff |
| 2 | 71 | Filter Resonance |
| 3 | 73 | EG Attack |
| 4 | 75 | EG Decay / Release |
| 5 | 91 | Reverb Send |
| 6 | 94 | Delay Send |
| 7 | 10 | Pan |
| 8 | 7 | Volume |

The **Pitch** strip is pitch bend. The **Mod** strip is CC 74, a filter sweep
under the finger — the standard CC 1 would do nothing, since the SEQTRAK does
not receive it.

## Faders — fixed channels, the four melodic tracks

| Fader | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Track | SYNTH 1 | SYNTH 2 | DX | SAMPLER |

Volume (CC 7). The seven drum tracks are set with encoder 8 after selecting
them, and muted from the pads.

## Main encoder

Master effect for the whole project: **Master Effect 1 parameter 1** (CC 102),
and **`Shift` + turn** = **Send Reverb parameter 1** (CC 110).

## Pads bank A — triggering

Note C3 on channels 1 to 8, in Gate mode, velocity- and aftertouch-sensitive.
The SEQTRAK records external MIDI input in real time, so this is finger drumming
straight into the sequencer — something the 16 front-panel keys cannot do.

| Pad | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| | KICK | SNARE | CLAP | HAT 1 | HAT 2 | PERC 1 | PERC 2 | SYNTH 1 |

## Pads bank B — mute

`Shift` + Pad 2 switches bank. The same eight tracks, latching mute (CC 23).

## Limits, and why

Checked against the *SEQTRAK Data List* §3-1-3 and its MIDI Implementation
Chart, and against the MiniLab 3's MCC manual.

**No transport.** For transport the MiniLab 3 can only send Mackie Control
(MCU); it never emits the realtime messages `FA` / `FB` / `FC`, which are the
only ones the SEQTRAK understands. No setting bridges the gap: play and stop from
the MiniLab are impossible.

**A trap worth knowing: `Shift` + Pads 4 to 8.** That is a hard-wired MiniLab
function (MCU transport), not a template assignment, and it cannot be disabled.
It sends Note On on channel 1 (the 86-95 region in standard MCU: Loop, Stop,
Play, Rec…), which the SEQTRAK receives as **KICK** hits. Avoid it while
playing. For the same reason the template sets the main encoder's push to *Off*
rather than its MCU Play default.

**No preset browsing, only shortcuts.** Only pads can send a Program Change;
encoders and faders are limited to CC. So there is no "next sound" button. RPN,
which might have worked around it, covers only pitch-bend sensitivity and tuning
on Yamaha gear.

**NRPN is useless.** The SEQTRAK recognises RPN (CC 100/101) but not NRPN
(CC 98/99), so every control is plain CC.

**Absolute encoders, so value jumps.** The SEQTRAK does not handle relative CC;
MCC offers a Relative mode but it would be misread. There is no soft pickup, so
the first tick can make a parameter jump. That is inherent to the pairing.

**The keyboard channel is not in the template.** It is a global MiniLab setting
(Device Settings → Default Keyboard Channel), so `Store To` does not change it —
but `Shift` + a key does, live, on the device.

## Program Change addressing, for pad shortcuts

The 2032 Drum/Synth/DX sounds share one numbering space under bank MSB 63, with
`LSB = (n − 1) / 128` and `program = (n − 1) mod 128`:

| Target | Bank MSB | Bank LSB | Program | Numbers |
|---|---|---|---|---|
| Drum sound | 63 | 0-6 | 0-127 | 1-855 |
| Synth sound | 63 | 6-15 | 0-127 | 856-1932 |
| DX sound | 63 | 15 | 0-127 | 1933-2032 |
| User sound (banks 1-16) | 63 | 32-47 | 0-127 | — |
| User project 1-8 | 64 | 0 | 0-7 | — |
| Sampler element | 62 | 0-11 | 0-127 | 1-392 |

The pad's channel designates the track, and the sound's engine must match it.
The sampler is the exception: under MSB 62 the machine "regards channel number
as element number", so there the channel designates the element — untested.

## The MiniLab 3's screen: what a host can write on it

Measured on the owner's MiniLab 3 on 2026-11-15, plugged into a Mac over USB,
the SEQTRAK not involved. These are facts about the controller, not about the
SEQTRAK. `verified on hardware` here means: SysEx sent from the Mac on the
`Minilab3 MIDI` port, the owner reading the screen, and for the last two runs
the controller's own program report captured in the same loop. The message
formats come from an unofficial Arturia forum thread
(<https://forum.arturia.com/t/sysex-protocol-documentation/5746>); Arturia
publishes none.

All messages are wrapped as `F0 00 20 6B 7F 42 <data> F7`.

| Message | `<data>` | Result |
|---|---|---|
| Identity Request `F0 7E 7F 06 01 F7` | — | reply `F0 7E 7F 06 02 00 20 6B 02 00 04 04 45 00 02 01 F7`. `verified on hardware` |
| DAW connect | `02 02 40 6A 21` | reply `02 00 40 63 00` (the forum thread reads `40 63` as the pad bank). `verified on hardware` |
| DAW disconnect | `02 02 40 6A 20` | sent once; the screen was back on the program name afterwards. Whether it cleared the text or changed program was not separated |
| Program report, **sent by the controller** on `Shift` + Pad 3 | `02 00 40 62 pp` | `pp` cycles `01` → `02` → `03` → `01`. `verified on hardware` (captured). The owner saw text in the Arturia program and in the DAW program and none in the user program, which fits `01` = Arturia, `02` = DAW, `03` = user (*inferred*: the names were not read against each report) |
| Two lines of text | `04 ff 60 01 <line 1> 00 02 <line 2> 00` | depends on the family byte `ff` and on the active program, below |

| Active program | Family `ff` tried | Text shown |
|---|---|---|
| DAW | `02` | **yes**, and it follows a counter resent twice a second. `verified on hardware` |
| Arturia | `00`, `01`, `03` | **`00` and `01` yes**, `03` no. A single message stayed on screen, and was still there after an encoder was turned. `verified on hardware` |
| User (the SEQTRAK template) | `00`, `02`, `03`-`08` | **none**. For `03`-`08` the controller had reported `40 62 03` in the same capture. `01` was not tried in this program |

**Consequence for the SEQTRAK template.** The template is a user program, and
no message tried writes on the screen while a user program is active. Text is
available in the Arturia and DAW programs, where the controls send the
controller's fixed assignments instead of the template's. So "the template's
mapping plus a sound name on the screen" is not reachable with the messages
tried here. The Arturia program's assignments were captured
next, and they do not replace it.

### What the Arturia program's controls send

`verified on hardware`, same day: a cumulative capture of all four MiniLab
ports on the Mac, keyed by message type, channel and number, while the owner
touched each control once in a stated order (the controller had reported
`40 62 01` at the start of the capture). The mapping to controls is by order
of first appearance.

| Control | Sends | Received by the SEQTRAK as ([cc-map.csv](../data/cc-map.csv)) |
|---|---|---|
| Encoder 1 | CC 74, channel 1 | Filter Cutoff |
| Encoder 2 | CC 71, channel 1 | Filter Resonance |
| Encoders 3-8 | CC 76, 77, 93, 18, 19, 16, channel 1 | not in the SEQTRAK's CC map |
| Faders 1-4 | CC 82, 83, 85, 17, channel 1 | not in the SEQTRAK's CC map |
| Pads 1-8 | notes 36-43, channel 10, with polyphonic aftertouch | notes on DX |
| `Mod` strip | CC 1, channel 1 | not received |
| `Pitch` strip | pitch bend, channel 1 | pitch bend |
| Keyboard | notes on the keyboard channel | notes on that track |
| `Shift` | CC 9, channel 1, 127 on press and 0 on release | not in the SEQTRAK's CC map |
| Main encoder, turned | **CC 114, channel 1, relative** (61-62 one way, 65-66 the other, around 64) | **Send Delay Assigned Parameter 2** |
| Main encoder, pressed | CC 115, channel 1, 127 then 0 | **Send Delay Assigned Parameter 3** |
| `Shift` + main encoder, turned | CC 112, channel 1, relative | **Send Reverb Assigned Parameter 3** |
| `Shift` + main encoder, pressed | CC 113, channel 1, 127 then 0 | **Send Delay Assigned Parameter 1** |

**The controls do not follow the keyboard channel in this program.** After
`Shift` + key moved the keyboard to channel 8 (a key then sent its note on
channel 8), encoder 1 still sent CC 74 on channel 1, fader 1 CC 82 on channel
1, and pad 1 note 36 on channel 10. Same capture method.

**The main encoder row was wrong until a second capture.** The first capture
saw nothing from it and this table said so; a later one (same method, a
`Shift` press as a marker first) recorded the four controllers above. The
first was a missed gesture, not silence. It matters: the SEQTRAK receives
CC 112-115 as send-effect parameters, so on an unpatched unit turning or
pressing that encoder moves the project's delay or reverb.

So with the controller in its Arturia program, two of its twelve knobs and
faders do something useful on the SEQTRAK, and only on KICK. The DAW program's
controls were not captured.

**Two early runs were unusable and are recorded as such.** The first looped
text began with the word `SEQTRAK`, which is also the template's name and what
the screen shows by default. A later run concluded "families `00` and `01`
work in the user program" before the program report was being captured; the
controller was most likely in the Arturia program at the time. Both mistakes
are the same one: reading a result without an instrument for the state it
depended on.

