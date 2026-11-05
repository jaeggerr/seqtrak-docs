# 15 — The front panel: controls and gestures

Every other document here describes the machine as a host sees it — addresses,
messages, replies. This one describes it as the **player** sees it: what the
printed controls are called, and which combination of them does what.

Everything below is `from Yamaha Data List` — the *SEQTRAK User Guide* (OS
V2.00), cited by section and page — except the two power-off rows marked
`verified on hardware`, which point at the run that measured them. The machine
has no screen, so almost every function beyond an obvious press is a
**combination**; the guide spells out dozens of them, scattered across 109
pages, and they are collected here.

Two limits of this extraction, stated once:

- The guide's notation (§1.1.1, p. 10) distinguishes a press, a press-and-hold,
  a press-and-hold for *N* seconds, and a turn — but it does so with **figures**,
  which do not survive text extraction. So a duration appears below only where
  the guide's **prose** states one. Where a row says "hold", the guide said
  "hold down" without a number.
- **No gesture here is a protocol fact.** A combination tells you what the
  machine does, not what it transmits. For what a gesture puts on the wire, see
  [05-live-state.md](05-live-state.md) and
  [10-verified-behaviour.md](10-verified-behaviour.md); the one tool built for
  the question is
  [`point2_facade.py`](../tools/hardware-probe/point2_facade.py).

## 1. The controls, as the machine prints them

From §2, pp. 14-18. Use these names — the guide, the app and this repository
all use them, and "the big knob" is ambiguous between the `[ALL]` knob and a
Track knob.

| Printed name | Where | What it is |
|---|---|---|
| `[VOL+]` `[VOL−]` | left side | speaker / `[PHONES]` volume |
| `[DELETE]` | left side | the **modifier** for every delete |
| `[MUTE]` | left side | mute modifier |
| `[SOLO]` | left side | solo modifier |
| `[PAGE]` | left side | step page, and pattern length on drum tracks |
| `[⏻/PLAY]` | left side | power **and** transport |
| `[ALL]` knob | top left | all 11 tracks at once; the **modifier** for most global toggles |
| Track knobs | top left | one per track — `[KICK]`, `[SNARE]`, `[CLAP]`, `[HAT 1]`, `[HAT 2]`, `[PERC 1]`, `[PERC 2]`, `[SYNTH 1]`, `[SYNTH 2]`, `[DX]`, `[SAMPLER]` |
| Drum keys | top left | 16 keys: steps, patterns 1-6, projects 1-8, scenes, track types |
| Record key | top left | real-time and motion recording |
| Synth keys | top left | 7 keys: notes, samples, drum-kit sounds |
| `[BAR LENGTH]` | top left | pattern length on synth and SAMPLER tracks |
| `[OCTAVE]` | top left | ±octave for the Synth keys |
| `[SCALE]` | top left | scale for the Synth keys |
| `[KEY]` | top left | key, in half steps |
| `[REC SAMPLE]` | top left | sampling |
| Index | top right | names the selected parameter or mode |
| Global Meter | top right | the only numeric display: a value, or a status |
| `[UNDO/REDO]` | top right | undo / redo of sound and effect parameters |
| Sound Design knobs 1-4 | top right | sound parameters, by page |
| Sound Design Page button | top right | switches those pages |
| `[CLEAR FX]` | top right | drops the current effect parameter to minimum |
| `[FX]` knob | top right | effect type |
| `[MASTER/SINGLE]` switch | top right | which effect the sliders and `[FX]` knob address |
| `[FX LEVEL]` `[HIGH PASS]` `[REPEATER]` | top right | three touch sliders |
| FX Page button | top right | switches the sliders' parameter page |
| `[BPM+]` `[BPM−]` | right side | tempo, 5-300 BPM |
| `[SWING]` | right side | swing |
| `[PROJECT↑]` | right side | the **modifier** for project scope |

Eleven tracks, seven of them drum tracks (KICK → PERC 2), three synth tracks
(SYNTH 1, SYNTH 2, DX) and the SAMPLER. Part numbers and MIDI channels are in
[01-overview.md](01-overview.md).

## 2. The grammar

The sixty combinations are not arbitrary — six modifiers carry nearly all of
them, and knowing the grammar is faster than remembering the list.

| Form | Means | Example |
|---|---|---|
| `[ALL]` knob **+ a button** | a global toggle, or a mode | `[ALL]` + `[MUTE]` → Mute mode |
| `[DELETE]` **+ a control** | delete whatever that control addresses | `[DELETE]` + Track knob → that track's pattern |
| `[PROJECT↑]` **+ something** | project scope | `[PROJECT↑]` + Drum key → switch project |
| `[PAGE]` **+ something** | paste, step input, page and length | `[PAGE]` + Drum key → paste steps |
| a **Track knob + a Drum key** | that one track's patterns | hold `[SNARE]` + key 4 → its pattern 4 |
| a **lit Drum key + a knob** | a per-step edit | hold key + Track knob → micro timing |
| **press and turn** (not just turn) | coarse: measures, or bigger parameter jumps | press-and-turn `[ALL]` → 16-step increments |
| **hold for 2 s or longer** | a second function on the same control | hold a Drum key 2 s → copy steps |
| **held while switching on** | a service function | `[SAMPLER]` + `[UNDO/REDO]` → factory reset |

Two consequences worth stating. The `[ALL]` knob is a modifier far more often
than it is a control, and **`[DELETE]` + a knob deletes a parameter lock, not a
pattern** — the same modifier means "delete what this control addresses", and
what a Sound Design knob addresses is its own automation.

## 3. Power, battery and service

> **The four combinations held while switching on are the dangerous ones.** One
> of them is a factory reset, and nothing confirms it. The protocol equivalent
> is `01 34 00`, which this repository forbids sending speculatively.

| What | Gesture | Where |
|---|---|---|
| Power on / off | hold `[⏻/PLAY]` **2 s or longer** | §3.2.1, p. 22 |
| **Forced termination** | hold `[⏻/PLAY]` **+** `[PROJECT↑]` | §3.2.2, p. 22 |
| | *Used in anger and it works:* after an interrupted firmware write the unit answered no SysEx and `[⏻/PLAY]` alone would not switch it off. This combination did, and the machine booted normally afterwards. `verified on hardware` — [10](10-verified-behaviour.md#2026-11-05-hardware-session-an-interrupted-firmware-write-and-the-machine-came-back) |
| Battery / charge status, power on | hold `[ALL]` knob **+** `[⏻/PLAY]` → Global Meter: cyan = charging, white = not charging, flashing red = trouble | §3.1.1, p. 20 |
| Auto Power Off on / off (30 min idle) | hold the **lower-left Drum key** while switching on | §3.2.3, p. 22 |
| **Factory reset** | hold `[SAMPLER]` knob **+** `[UNDO/REDO]` while switching on. Global Meter red during init | §16.1, p. 93 |
| Format a USB flash drive | hold `[DX]` knob **+** `[UNDO/REDO]` while switching on. All index lit = done, then `[⏻/PLAY]` to power off | §17.1.1, p. 96 |
| Firmware update from USB | hold `[KICK]` knob **+** `[BAR LENGTH]` while switching on, with `8Z33OS_.PGM` on the drive | §17.1.2, p. 96 |
| Bluetooth pairing, and connection status | hold `[ALL]` knob **+** `[SWING]`. White 2 s then a 30 s pairing window; **cyan blue 2 s = already connected** | §15.1.2, p. 90 |
| Master volume | `[VOL+]` / `[VOL−]`, or hold either **+** turn `[ALL]`; hold alone to scroll | §16.4, p. 94 |

**The two power-off paths are not equivalent, and they differ by one button.**

| Path | Saves unsaved edits? |
|---|---|
| Normal, `[⏻/PLAY]` 2 s | **Yes** — `verified on hardware` |
| Forced, `[⏻/PLAY]` + `[PROJECT↑]` | **No** — `verified on hardware`: a marker written after startup was gone, and the machine reverted to the state of the previous normal power-off |
| Auto Power Off, 30 min idle | Yes per the guide. Untested |

Both measurements, and why the forced termination is the right instrument for
any "did this persist?" question, are in
[10-verified-behaviour.md](10-verified-behaviour.md#the-three-power-off-paths-are-not-equivalent).

## 4. Projects

| What | Gesture | Where |
|---|---|---|
| Switch project | hold `[PROJECT↑]` **+** Drum key 1-8. The current project's key is lit yellow | §4.1, p. 23 |
| Delete project | hold `[PROJECT↑]` **+** `[DELETE]` **+** the Drum key. Leaves one KICK step | §4.4, p. 25 |
| Temporarily save | hold `[PROJECT↑]` **+** the Drum key lit **yellow** (the current project) | §4.6, p. 28 |
| Restore the temporary save | hold `[PROJECT↑]` **+** the Drum key lit **cyan blue** | §4.6, p. 28 |
| Launch Quantize | hold `[PROJECT↑]` **+** turn `[ALL]`; press-and-turn for 16-step steps | §5.1.3, p. 30 |
| Measure-wise stop/start under external MIDI clock, on/off | hold `[PROJECT↑]` **+** press `[PAGE]`. White Global Meter = on (default) | §4.1.1, p. 24 |

Only **one** temporary save exists, it is taken automatically right after a
project loads, and it is discarded by a project switch or a power-off (§4.6).

Saving needs no gesture: a project is written when the machine is switched off
or the project is switched (§4.2) — but see §3 above, where the measured
behaviour is that **a project switch commits nothing**, and only the normal
power-off does.

## 5. Tempo, swing, metronome

| What | Gesture | Where |
|---|---|---|
| Tempo | `[BPM+]` / `[BPM−]`, or hold either **+** turn `[ALL]`. 5-300 BPM; hold alone to scroll | §4.5.1, p. 26 |
| Tempo back to the project's opening value | press `[BPM+]` **and** `[BPM−]` together | §4.5.1, p. 26 |
| Swing | `[SWING]`, or hold `[SWING]` **+** turn `[ALL]`. −58 to +58 ticks on even steps | §4.5.2, p. 27 |
| Swing back to 0 | hold `[DELETE]` **+** press `[SWING]` | §4.5.2, p. 27 |
| Metronome on / off | hold `[ALL]` **+** press `[BPM+]` | §4.5.3, p. 27 |

One step is 120 ticks (§4.5.2). Which steps count as "even" follows Launch
Quantize, not the bar.

## 6. Patterns

| What | Gesture | Where |
|---|---|---|
| Switch pattern, immediately | **turn** a Track knob | §5.1.1, p. 29 |
| Switch pattern, at the next Launch Quantize | **press and turn** a Track knob | §5.1.1, p. 29 |
| Same, all 11 tracks | turn `[ALL]`, or press-and-turn `[ALL]` | §5.1.1, p. 29 |
| Pick a pattern by key, reserved | hold a Track knob **+** press the lit Drum key (1-6 = patterns 1-6) | §5.1.2, p. 29 |
| Pick a pattern by key, immediately | hold a Track knob **+ double-tap** the Drum key | §5.1.2, p. 30 |
| Same, all 11 tracks | hold `[ALL]` **+** press (reserved) or double-tap (immediate) a Drum key | §5.1.2, p. 30 |
| Pattern length, in bars | press `[BAR LENGTH]` → 1, 2, 4 or 8 bars | §5.2, p. 31 |
| Pattern length, in steps | hold `[BAR LENGTH]` **+** turn a Track knob → 1-128 steps; press-and-turn for 16s | §5.2, p. 31 |
| Pattern length, drum track | hold `[PAGE]` **+** turn that Drum Track knob → 1-128 steps | §5.2.1, p. 32 |
| 3 patterns → 6 | hold a Track knob **+** press Drum keys 4-6 lit **blue**. They turn white | §5.3, p. 33 |
| 6 patterns → 3 | hold a Track knob **+** press Drum keys 4, 5 and 6 **simultaneously** | §5.3, p. 33 |
| Delete the selected pattern | hold `[DELETE]` **+** press a Track knob (LED flashes red), or `[ALL]` for every track | §5.4, p. 34 |
| **Copy** a pattern | hold a Track knob (or `[ALL]`) **+** press a Drum key **2 s or longer**. Global Meter flashes white | §5.5, p. 34 |
| **Paste** a pattern | hold the Track knob (or `[ALL]`) **+** `[PAGE]` **+** press a Drum key | §5.5, p. 34 |
| **Copy** the current track's steps | hold a Drum key **2 s or longer** | §5.9, p. 39 |
| **Paste** steps | hold `[PAGE]` **+** press a Drum key | §5.9, p. 39 |

A LED flashing **yellow** means one of patterns 1-3 is selected, **cyan blue**
one of 4-6 (§5.1.1).

Lengthening a pattern copies an existing measure into the new one — 2nd and 3rd
from the 1st, 4th from the 2nd, 5th from the 1st, 6th from the 2nd, 7th from
the 3rd, 8th from the 4th — unless the new measure already holds data (§5.2,
p. 32). **Shortening loses nothing**: the data outside the range come back if
the length is restored.

Copy and paste work across track types only in the combinations of §5.5.1
(p. 35): drum→drum of the *same* type, drum-as-Synth↔synth tracks, and
SAMPLER→SAMPLER. Effect parameters are not pasted when the two tracks' effect
types differ.

## 7. Tracks and sounds

| What | Gesture | Where |
|---|---|---|
| Select a track | press its Track knob | §5.6, p. 36 |
| Audition a track | press its Track knob **while playback is stopped** | §5.6, p. 36 |
| Change the sound | turn **Sound Design knob 1 on page 1** | §5.7, p. 36 |
| Change a SAMPLER sound | press `[SAMPLER]`, press a Synth key, then Sound Design knob 1 on page 1 | §5.7, p. 36 |
| **Category jump** | hold Sound Design knob 1 (page 1) **+** press a Drum key → first sound of that category | §5.7.1, p. 37 |
| Save the current sound | hold `[ALL]` **+** press Sound Design knob 1. Global Meter flashes white; the copy is named `_editNN` and becomes a favourite | §9.5, p. 68 |
| Mute a track | hold `[MUTE]` **+** press a Track knob (LED green). Press again to unmute | §5.8.1, p. 38 |
| Unmute everything | hold `[MUTE]` **+** press `[ALL]` | §5.8.1, p. 38 |
| Solo a track | hold `[SOLO]` **+** press a Track knob (LED cyan blue) | §5.8.2, p. 38 |
| Bigger parameter jumps | **press and turn** a Sound Design knob | §9.1, p. 59 |
| Advanced sound pages | hold the Sound Design Page button **2 s or longer** (toggle) | §9.1.1, p. 60 |
| Undo / redo a parameter change | press `[UNDO/REDO]` — **not** sound or effect *selection* | §9.4, p. 68 |
| Effect parameter to minimum | press `[CLEAR FX]` | §10.3, p. 74 |
| Effect type | turn the `[FX]` knob; `[MASTER/SINGLE]` decides which effect | §10.2.2, p. 73 |

Solo wins over mute, and the mute state comes back when the solo is released
(§5.8.2). A sound registered as a favourite is reachable by a category jump to
FAVORITE, which stays dark when there is none (§5.7.1).

## 8. Drum tracks

| What | Gesture | Where |
|---|---|---|
| Step on / off | press a Drum key | §6.1, p. 40 |
| Switch step page | press `[PAGE]`, or hold `[PAGE]` **+** turn `[ALL]`. Current page flashes cyan on the Global Meter | §6.2, p. 40 |
| **Micro timing** | hold a **lit** Drum key **+** turn a Track knob. −60 to +59 ticks; index shows `MICRO TIMING` | §6.3, p. 41 |
| Micro timing on several steps | hold several lit Drum keys **+** turn a Track knob | §6.3, p. 41 |
| **Substep** | hold a **lit** Drum key **2 s or longer** → five keys light: off, ×2, ×3 (8th triplet), ×3 (16th triplet), ×4 | §6.4, p. 41 |
| **Trigger probability** | hold a **lit** Drum key **+** press `[MUTE]` → one level down of 8; wraps to maximum from minimum | §6.6, p. 43 |
| Real-time input mode | hold a **Drum** Track knob **+** press a Synth key (toggle; off at power-down) | §6.5, p. 42 |
| **Change the track type** | hold the Drum Track knob — keys 9, 10, 11 light = Drum, DrumKit, Synth — then, still holding, hold the type's key **5 s**, until it lights purple | §6.7, pp. 44-45 |

> **Re-typing a track deletes that track's sequence** (§6.7 NOTICE) and cannot
> be done during playback. The UI order here — Drum, DrumKit, Synth on keys 9,
> 10, 11 — is **not** the wire order; sending the UI index over SysEx gives a
> drum kit where a synth was meant.
> [13-track-types.md](13-track-types.md).

Substep lights its five keys on the **opposite** row from the key being edited
(§6.4). With several steps selected the Global Meter shows the **highest**
probability of them (§6.6).

## 9. Synth tracks and the SAMPLER

| What | Gesture | Where |
|---|---|---|
| Octave | press `[OCTAVE]`, or hold it **+** turn `[ALL]`. +2 to −3 | §7.3, p. 48 |
| Scale | press `[SCALE]`, or hold it **+** turn `[ALL]`. Eight per project | §7.4, p. 48 |
| Key, in half steps | press `[KEY]`, or hold it **+** turn `[ALL]` | §7.5, p. 49 |
| MONO / POLY / CHORD | turn **Sound Design knob 2 on page 1** | §7.6, p. 49 |
| **Edit a chord** | set CHORD, then hold `[ALL]` **+** press that Synth key; the notes appear on the Drum keys, up to four | §7.7, p. 50 |
| **Keyboard Input mode** | hold `[ALL]` **+** press `[KEY]`; the Drum keys light white as a keyboard | §7.8, p. 51 |
| **Step Input mode** | hold `[PAGE]` **+** press a Synth Track knob or `[SAMPLER]` (toggle; off at power-down) | §7.9, p. 51 |
| Add / remove a note on a step | hold a Drum key **+** press a Synth key | §7.9, p. 52 |
| Note length | hold a **lit** Drum key **+** turn `[ALL]`; for one note of a chord, hold the Drum **and** Synth key **+** turn `[ALL]` | §7.9, p. 52 |
| Quantize while recording, on / off | hold `[ALL]` **+** press the Record key | §7.2, p. 47 |
| Sampling source | hold `[REC SAMPLE]` **2 s or longer** **+** press the Drum key lit white — mic/AUDIO IN, USB audio, or resampling | §8.3, p. 54 |
| Start / stop sampling | press `[REC SAMPLE]`; 16 s maximum per sample | §8.2, p. 53 |
| **Cancel** sampling in progress | hold `[DELETE]` **+** press `[REC SAMPLE]` — restores the previous sound | §8.5, p. 54 |
| Count-in before sampling | hold `[ALL]` **+** press `[REC SAMPLE]` | §8.6, p. 55 |
| Monitoring mode (input level on the Global Meter) | hold `[REC SAMPLE]` **+** press `[VOL+]` (toggle) | §8.7, p. 55 |
| Delete one sample's pattern | hold `[DELETE]` **+** press its Synth key | §8.9, p. 56 |
| Mute one sample | hold `[MUTE]` **+** press its Synth key (lights green) | §8.11, p. 58 |

Note length is edited with `[ALL]`, not with a Track knob — the Track knob on a
held step is micro timing (§6.3). The two gestures are one knob apart.

Muting the SAMPLER track and muting a sample are independent, and unmuting all
tracks does **not** unmute a sample (§8.11).

Above G8 a note plays an octave lower (§7.7).

## 10. Per-step automation

| What | Gesture | Where |
|---|---|---|
| **Parameter Lock** | hold a **lit** Drum key **+** turn Sound Design knobs 1-4, or slide `[FX LEVEL]`. The step lights **purple** | §9.2, p. 64 |
| Parameter Lock on several steps | hold several Drum keys **+** the same | §9.2, p. 65 |
| **Motion Recording** | hold the Record key **+** turn Sound Design knobs 1-4, or slide a touch slider | §9.3, p. 67 |
| Delete one lock across the pattern | hold `[DELETE]` **+** press that Sound Design knob or the `[FX]` knob | §9.2.1, p. 65 |
| Delete one lock on one step | hold the Drum key **+** `[DELETE]` **+** press that knob | §9.2.1, p. 66 |
| Delete a Motion | hold `[DELETE]` **+** press that Sound Design knob or the `[FX]` knob | §9.3.1, p. 67 |
| Delete every lock on a step | **turn the step off** | §9.2.1, p. 66 |

Parameter Lock and Motion Recording write **the same data**, and a Motion over
a locked step overwrites it (§9.3). A lock on VOLUME changes the note's
velocity (§9.2).

Which parameters can be locked is per track type, in §9.1.2-9.1.5 (pp. 60-63):
SOUND SELECT, MONO/POLY/CHORD, ARPEGGIATOR TYPE and SPEED, and the SAMPLER's
START/END/LOOP cannot.

## 11. The four modes

Each is entered with the `[ALL]` knob and one button, and three of the four
leave the same way.

| Mode | Enter | Leave | Where |
|---|---|---|---|
| **Mixer** | hold `[ALL]` **+** press `[VOL+]` | same | §11.1, p. 75 |
| **Mute** | hold `[ALL]` **+** press `[MUTE]` — the `[ALL]` knob's three LEDs go green | press `[MUTE]` **alone** | §12.1, p. 78 |
| **Song** | hold `[ALL]` **+** press `[PROJECT↑]` | switch to Scene mode first, then the same combination | §13.1, p. 79 |
| **Scene** | from Song mode, hold `[ALL]` **+** press `[PROJECT↑]` | same | §13.1.1, p. 79 |

The index names the mode you are in. Entering Song mode stops playback;
*leaving* Song or Scene mode does not, and the pattern combination and
mute/solo state survive it (§13.1.1).

In **Mixer** mode, Sound Design knobs 1-4 select PAN, VOLUME, REVERB SEND and
DELAY SEND, the Track knobs set that parameter per track, and `[ALL]` sets the
project-wide value — or the send effect's RETURN LEVEL (§11.2, pp. 75-76). With
REVERB or DELAY SEND selected, the `[FX]` knob changes the send effect preset
(§11.3.1, p. 76).

In **Mute** mode a Track knob alone mutes; `[ALL]` unmutes everything; and
reserved pattern switching is unavailable (§12, p. 78).

### Song mode

| What | Gesture | Where |
|---|---|---|
| Play from the selected scene, or stop | press `[⏻/PLAY]` | §13.2, p. 80 |
| Select a scene | press its Drum key | §13.2.1, p. 80 |
| **Loop** a scene | **double-tap** its Drum key while it plays; it alternates purple and cyan | §13.2.2, p. 81 |
| Cancel the loop | press that Drum key, or select another scene | §13.2.2, p. 81 |
| Add a scene | press an **unlit** Drum key — the selected scene is copied into it; 16 maximum | §13.3, p. 82 |
| Delete a scene | hold `[DELETE]` **+** press the Drum key lit **red**. Later scenes move up | §13.4, p. 82 |
| Change a scene's patterns | turn the Track knobs, or `[ALL]` for all 11 | §13.5.1, p. 83 |
| **Scene length** | hold `[PAGE]` **+** turn `[ALL]`; press-and-turn for measures; **fully left = AUTO**, the longest pattern in the scene | §13.5.2, pp. 83-84 |

A scene currently playing cannot be deleted (§13.4). In Song mode a scene
change waits for the current scene to end; in Scene mode it lands on the next
Launch Quantize (§13.2.1). The wire form of all of this is
[14-song-mode.md](14-song-mode.md).

## 12. What the front panel cannot do

The guide names these as app-only — useful to know before hunting for a
combination that does not exist.

| Only in the SEQTRAK app | Where |
|---|---|
| Metronome sound (5 of them) and volume | §4.5.3, p. 28 |
| Quantize resolution — 1/32, 1/16T, 1/16, 1/8T, 1/8, off | §7.2, p. 47 |
| Editing a project's scales | §7.4, p. 48 |
| Deleting a saved sound; adding or removing favourites | §9.6, p. 68 |
| Importing sounds and samples (44.1 kHz, 16/24-bit WAV, ≤16 s) | §9.7, p. 69 |
| `HIGH PASS` and `REPEATER` effect types; COMPRESSOR and 5 BAND EQ | §10.1.3, p. 72 |
| Looping a whole song | §13.2.3, p. 81 |
| Track-knob sensitivity | §16.2, p. 93 |
| MIDI clock, MIDI output filters, MIDI Thru | §16.3, p. 93 |
| Auto Power Off **timeout** (the on/off is a gesture) | §3.2.3, p. 22 |
| Auto-normalize for sampling | §8.8, p. 56 |
| MANUAL / AUTO PLAYBACK mode under external MIDI clock | §4.1.1, p. 24 |

Most of these are reachable over SysEx without the app — the parameter tables
in [03a](03a-parameters-system.md)-[03g](03g-parameters-sequencer.md) are the
place to look. The "MIDI output filters" of §16.3.2 are the per-interface
transmit flags in the `00 00` block, and they matter over Bluetooth: the
published defaults are not what a used machine reads
([07-transports.md](07-transports.md),
[10-verified-behaviour.md](10-verified-behaviour.md)).
