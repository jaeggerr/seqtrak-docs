# 04 — Writing into the sequencer

How to put a note into a pattern, edit it, delete it and read it back. None of
this is in the Yamaha Data List; it is the capability that lets an external host
compose on the SEQTRAK rather than only mix it.

**The step-record read and write path is `verified on hardware`, end to end:**
write a note, read it back, delete it, confirm the step is empty again. That is
the headline capability of this whole reference — it means a pattern can be
composed, read and edited from outside, without the Yamaha app. The worked round
trip is [below](#the-verified-round-trip).

The rest is `from the official app, untested`. A second reading of the piano-roll address
exists in a sibling project, but it is **not** independent corroboration — see
[the piano-roll section](#the-compact-step-list-a-second-reading-of-ah--75).

> **The sequencer must be stopped.** Check `01 10 20` (`SequencerStatus`) reads
> `0` before writing to a pattern; the reference script refuses to run
> otherwise.

> **Read before you write.** The read forms change nothing, so they are the
> right way to validate your address arithmetic before committing to a write.

> **Pace at 2 ms.** The official app sleeps 2 ms after every MIDI message, on
> every transport — read out of its MIDI plugin, see
> [07-transports.md](07-transports.md#send-pacing--the-official-app-waits-2-ms-between-messages).
> Writing a whole pattern means hundreds of messages back to back; use the same
> interval.

For writing a *whole composition* rather than a single pattern — how many
messages that is, what the capacity limits are, and how scenes chain patterns
into a song — see [14-song-mode.md](14-song-mode.md).

## Two editing models

The SEQTRAK represents a pattern in two ways and the app uses both.

- **Step record** (`ah = 70`) — a grid. You address a *step* and put a note in
  it. This is the model of the drum tracks and of step-input mode.
- **Piano roll** (`ah = 72`-`76` for synth parts, `22`-`27` for drum parts) — a
  list of dated *events*, addressed by index. It allows several notes at the
  same instant, plus CC and SysEx events inside the sequence.

### Which model a track accepts is not a choice — it follows the track type

`verified on hardware`. The two models are not two ways of reaching the same
tracks. `70` answers **only on a part whose `PartAwmType` (`01 1p 3C`) reads
1 (DRUM)**; everything else is reached through a piano roll.

Measured by sweeping the read address `70 (0x40|t) ss` over t = 0-11 and
steps 0-3, four attempts per address, on a machine whose parts 0-5 were DRUM,
part 6 had just been re-typed to SYNTH, and 7-10 are the native synth, FM and
sampler tracks:

| Track | Type | Reply to `70 (0x40\|t) ss` |
|---|---|---|
| 0-5 | DRUM | 6 data bytes when the step is occupied, **0 data bytes** when empty |
| 6 | SYNTH | **no reply**, 4 steps × 4 attempts |
| 7-10 | native SYNTH / DX / SAMPLER | **no reply**, 4 steps × 4 attempts |
| 11 | — | **no reply** |

The boundary follows the **type**, not the index: part 6 replied before it was
re-typed and stopped replying afterwards, with the other six parts read in the
same loop as witnesses, all still replying. That is what licenses reading the
silence as a boundary rather than as dropped messages — a bare absence after
four tries would not (see
[CLAUDE.md](../CLAUDE.md#talking-to-real-hardware), rule 1).

This **does not contradict** the verified round trip below: that test wrote,
read back and deleted a note on part 0, a DRUM part, which is exactly where
`70` works. Both results are true in their own domain, and neither one is a
statement about the other. The scope of each hardware claim in this document is
the track type it was measured on.

**Practical consequence.** A melodic part cannot be written with step record at
all. Re-typing a drum part to SYNTH ([13-track-types.md](13-track-types.md))
moves it from the `70` space to the `22` space, silently — nothing announces
the change, and `70` writes sent afterwards are simply not acknowledged.

## Step record — `ah = 70`

```
am = <mode> | part
al = <event type, attribute, or step number>
```

### Modes, in the high nibble of `am`

| `am` | Mode |
|---|---|
| `0x00 \| part` | add an event |
| `0x10 \| part` | change one attribute of a step |
| `0x20 \| part` | delete |
| `0x40 \| part` | request: note info for a step |
| `0x50 \| part` | request: parameter info for a step |
| `0x60 \| part` | request: conditional lock for a step |

### Add — `am = 0x00 | part`

| `al` | Event | Data bytes |
|---|---|---|
| `00` | Note | `step, note, velocity, gateMsb, gateLsb` |
| `01` | Control Change | `step, ccNumber, value` |
| `03` | SysEx, 1 byte | `step, …` (4 bytes) |
| `04` | SysEx, 2 bytes | `step, …` (5 bytes) |

**Putting a note in a step** — the single most useful message in this document:

```
F0 43 10 7F 1C 0C 70 tt 00 ss nn vv gh gl F7
                        │     │  │  │  └──┴─ gate time, 14-bit, MSB first
                        │     │  │  └─ velocity
                        │     │  └─ MIDI note number
                        │     └─ step number
                        └─ part number
```

The app's own defaults are `note = 60, velocity = 100, gateMsb = 0,
gateLsb = 120` — middle C at velocity 100 with a gate of 120 ticks, which is
exactly one 16th step (see [ticks](#ticks)).

Middle C on step 0 of part 0 (KICK):

```
F0 43 10 7F 1C 0C 70 00 00 00 3C 64 00 78 F7
```

**The add message carries only step, note, velocity and gate.** The machine
fills in the other two fields itself: `retrigger = 0` and `microTiming = 60`.
So **60 is the neutral micro-timing value**, which also tells you that the
`70 (10|tt) 00` change-micro-timing command works on a scale centred on 60
rather than on 0. `verified on hardware`.

### The verified round trip

Part 0 (KICK), **a DRUM part** — step record is not reachable on any other
track type, see [above](#which-model-a-track-accepts-is-not-a-choice--it-follows-the-track-type).
Step 3, sequencer stopped. `verified on hardware`; the script is
[`../tools/hardware-probe/step_write_test.py`](../tools/hardware-probe/step_write_test.py),
which picks an empty step itself and deletes in a `finally`.

```
write    F0 43 10 7F 1C 0C 70 00 00 03 3C 64 00 78 F7
                            │  │  │  │  │  │  └──┴─ gate 120, 14-bit
                            │  │  │  │  │  └─ velocity 100
                            │  │  │  │  └─ note 60
                            │  │  │  └─ step 3
                            │  │  └─ al = 00 (Note)
                            │  └─ am = 0x00 | track  (add)
                            └─ ah = 70 (step record)

read     F0 43 30 7F 1C 0C 70 40 03 F7
reply    3C 64 00 3C 00 78
         60 100  0  60  0 120    note, velocity, retrigger, micro timing, gate

delete   F0 43 10 7F 1C 0C 70 20 00 03 F7
                            │  │  └─ step 3
                            │  └─ al = 00
                            └─ am = 0x20 | track  (delete)

read     F0 43 30 7F 1C 0C 70 40 03 F7
reply    (zero data bytes — the step is empty again)
```

Three things this establishes:

1. **Note, velocity and gate round-trip exactly**, gate included — so the 14-bit
   MSB/LSB split behaves as documented.
2. **The write is localised.** A neighbouring empty step, read as a witness, was
   untouched.
3. **Add and delete are a matched pair**, which makes this a safe
   write / verify / restore cycle for exploring the rest of the zone.

### Dumping a whole pattern

Because an empty step answers with zero data bytes, scanning the read address
across a pattern reads the pattern out. Scanning `70 40 00` through `70 40 0F`
on a factory kick track returned:

```
step  0  #   step  4  #   step  8  .   step 12  #
step  1  #   step  5  .   step  9  .   step 13  .
step  2  #   step  6  .   step 10  #   step 14  .
step  3  .   step  7  .   step 11  .   step 15  .
```

Every occupied step held identical contents, `3C 64 00 3C 00 78` — which is what
you would expect on a drum track, where the note number is fixed and only the
on/off pattern varies. `verified on hardware`.

```python
def dump_pattern(link, part, steps=16):
    """Read a drum pattern out step by step. Empty steps reply with no data."""
    out = []
    for step in range(steps):
        ok, data = link.read((0x70, 0x40 | part, step))
        out.append(None if (not ok or not data) else {
            "note": data[0], "velocity": data[1], "retrigger": data[2],
            "micro_timing": data[3], "gate": (data[4] << 7) | data[5],
        })
    return out
```

Remember that a missing reply and an empty step look alike at the transport
level. Retry before concluding a step is empty — see
[10-verified-behaviour.md](10-verified-behaviour.md#transport-reliability).

### Change — `am = 0x10 | part`

| `al` | Attribute | Data |
|---|---|---|
| `00` | micro timing | `step, microTiming` |
| `01` | velocity | `step, velocity` |
| `03` | retrigger (substep) | `step, retrigger` |
| `04` | conditional lock (probability) | `step, conditionalLock` |

### Delete — `am = 0x20 | part`

A one-byte Parameter Change whose data is the step number:

```
F0 43 10 7F 1C 0C 70 (20|tt) 00 ss F7
```

This is the undo for an added note, which makes add/delete a safe
write/verify/restore cycle. `verified on hardware` — see
[the verified round trip](#the-verified-round-trip).

### Read a step

Parameter Requests; `al` is the step number.

```
F0 43 30 7F 1C 0C 70 (40|tt) ss F7     note info
F0 43 30 7F 1C 0C 70 (50|tt) ss F7     parameter info
F0 43 30 7F 1C 0C 70 (60|tt) ss F7     conditional lock
```

**The note-info reply carries six data bytes, not eight** — `verified on
hardware`. The part and step are in the *address*, not in the data:

```
noteNumber  velocity  retrigger  microTiming  gateTimeMsb  gateTimeLsb
```

Read from a real unit, part 0 step 0:

```
→ F0 43 30 7F 1C 0C 70 40 00 F7
← data: 3C 64 00 3C 00 78
        60 100   0  60    0 120    = middle C, velocity 100, micro timing 60,
                                     gate 120 ticks
```

**An empty step replies with zero data bytes.** That is the marker to test for,
and it corresponds to `IsNoteNothing()` in `MIDI.StepNoteInfoMessage`.
`verified on hardware`.

> Do not confuse an empty step with a lost request. An isolated Parameter
> Request is *occasionally* dropped on the wire — measured at roughly 1 in 10
> for two different addresses. A missing reply is never information; retry.
> See [10-verified-behaviour.md](10-verified-behaviour.md#transport-reliability).

A request for parameter info on a step with no parameter lock also replies with
zero data bytes; conditional lock replies with one byte (`00` observed).

### Drum parameter locks

Three drum lock parameters sit outside the `70` zone, in an undocumented corner
of the project space. `from the official app, untested`.

| Address | Parameter | Range |
|---|---|---|
| `30 00 00` | `AddNoteEvent` | trigger |
| `30 00 70` | `DrumLockPitch` | 0-127 |
| `30 00 71` | `DrumLockSubStep` | 0-127 |
| `30 00 73` | `DrumLockVelocity` | 0-127 |

Which parameters can be locked or motion-recorded at all is tabulated in
[appendix-h-sound-design-parameters.md](appendix-h-sound-design-parameters.md).

## Synth piano roll — `ah = 72`-`76`

A part's events are an indexed list. The index is **11 bits**, split across the
address:

```
am = (part << 4) | (eventIndex >> 7)
al = eventIndex & 0x7F
```

14-bit values inside the payload (`eventTime`, `gateTime`) are MSB then LSB.

### The synth block is indexed locally, 0-3

`verified on hardware`, and it is a trap worth stating plainly: the `part` in
`am = (part << 4) | …` above is **not** the global part number. Sweeping the
read address `75 (n<<4) idx` over n = 0-11:

| `n` | Replies | Track |
|---|---|---|
| 0 | yes | SYNTH 1 — global part 7 |
| 1 | yes | SYNTH 2 — global part 8 |
| 2 | yes | DX — global part 9 |
| 3 | yes | SAMPLER — global part 10 |
| 4-11 | **no reply**, 6 indices × 2 attempts | — |

So the synth block counts its own four tracks from zero, while the drum block
(`22`-`27`) uses the global part number 0-6. Addressing SYNTH 1 as `n = 7`
reaches nothing at all.

### Add an event — `ah = 72`

`am = part << 4`, `al = 00`. The payload starts with the event time, then an
event type (`PianoRoll.EventType`):

| Type | Value |
|---|---|
| Note | `0` |
| Control Change | `1` |
| Pitch Bend | `2` |
| SysEx, 1 byte | `3` |
| SysEx, 2 bytes | `4` |
| SysEx data | `5` |

A **note** is 8 data bytes:

```
F0 43 10 7F 1C 0C 72 (t<<4) 00  eh el 00 nn vv ov gh gl  F7
                                 │  │  │  │  │  │  └──┴─ gate time, 14-bit
                                 │  │  │  │  │  └─ note-off velocity
                                 │  │  │  │  └─ note-on velocity
                                 │  │  │  └─ note number
                                 │  │  └─ event type 00 = Note
                                 └──┴─ event time in ticks, 14-bit
```

A **Control Change** is also 8 bytes:

```
… 72 (t<<4) 00  eh el 01 cc vv 00 00 00  F7
```

### Change an event — `ah = 73`

Same payload as an add, but the address carries the event index. The message
rewrites the whole event, even though `MIDI.PianoRoll.NoteChangeEventType`
enumerates `EventTime (0)`, `GateTime (1)`, `NoteNumber (2)` and
`NoteVelocity (3)`.

```
F0 43 10 7F 1C 0C 73 ((t<<4)|(idx>>7)) (idx&7F)  eh el 00 nn vv ov gh gl  F7
```

### Delete an event — `ah = 74`

A Parameter Change with no data:

```
F0 43 10 7F 1C 0C 74 ((t<<4)|(idx>>7)) (idx&7F) F7
```

### Read an event — `ah = 75`

```
F0 43 30 7F 1C 0C 75 ((t<<4)|(idx>>7)) (idx&7F) F7
```

**The reply is eight bytes and is the add payload verbatim** —
`eh el tt nn vv ov gh gl` — `verified on hardware` 2026-10-23. A twenty-event
melody on SYNTH 1 round-tripped exactly through this pair, with velocities 90 to
110 and gate times of 120, 240, 360, 480 and 600 ticks — so the 14-bit split
holds for a `gateTime` longer than one step, and velocity is stored per event.
Index 20 answered with zero data bytes, which is what established the end of the
list. There is no
part number in it and the event type is the **third** byte.

The official app describes it as `eventType,
partNumber, eventTime (16 bits), note, onVelocity, offVelocity, gateTime
(16 bits)`, nine bytes with the type first. That is what the app's own
definition describes; it is not what the wire carries. A client written to it reads the
event time as a type and the note as a velocity.

An index with no event answers with **zero** data bytes, which is how you find
the end of the list.

### Find an event's index — `ah = 76`

The mandatory step before changing or deleting: describe the event, get its
index back.

```
am = 00
al = part
```

| Looking for | 6 data bytes |
|---|---|
| a note | `eh el 00 nn 00 00` |
| a Control Change | `eh el 01 cc 00 00` |
| a 1-byte SysEx | `eh el 03 … ` |
| a 2-byte SysEx | `eh el 04 … ` |

```
F0 43 10 7F 1C 0C 76 00 tt  eh el 00 nn 00 00  F7
```

**The index comes back on `76`, not on `77`** — `verified on hardware`
2026-10-23. The reply is addressed `76 01 00` (`am = 01` marks it as a reply)
and carries the query echoed with **the index appended as a 14-bit pair**:

| Looking for | Reply body | Index |
|---|---|---|
| tick 0, note 60 | `00 00 00 3C 00 00` + `00 00` | 0 |
| tick 12, note 67 | `00 0C 00 43 00 00` + `00 01` | 1 |
| tick 24, note 72 | `00 18 00 48 00 00` + `00 02` | 2 |

**A note that is not in the list is answered with the pair omitted** — six
bytes instead of eight. Check the length: a trailing `00 00` meaning index 0 is
otherwise indistinguishable from "not found".

`ah = 77` (`StepRecAndPianoRollIndex`) carries pattern copy/paste:

| Address | Function | Data |
|---|---|---|
| `77 01 20` | copy pattern | `part, pattern` |
| `77 01 21` | paste pattern | `part, pattern` |

`reverse-engineered from app traffic`.

### The compact step list: a second reading of `ah = 75`

A second interpretation of the same `75` address exists in one of the sibling
projects in this tree (`SeqtrakDemo`). Both readings are recorded here because
they genuinely disagree, and the disagreement is listed in
[12-open-questions.md](12-open-questions.md).

> **This is not independent corroboration, and an earlier version of this
> document wrongly presented it as such** — as "a working third-party iOS app",
> which implied an outside source. It is the user's own code, written from the
> same documentation lineage as this repository. Where it agrees with the
> official app, that agreement may be inheritance rather than confirmation; where it
> disagrees, it is a hypothesis about the hardware, not a measurement of it.
> Neither reading below has been tested on a machine.

That code's model:

- the address is `75 (p << 4) | 0` with `al` = an **internal index**, not an
  event index split across two bytes;
- `p` is counted over the **melodic tracks only** — Synth 1 = 0, Synth 2 = 1,
  DX = 2, Sampler = 3 — not the global part number;
- the SEQTRAK stores only **active** steps, packed with no gaps, so index 0 is
  the first active step, index 1 the second, and so on;
- you stop reading when the reply is short or empty;
- the real musical position comes from the tick value in the payload, not from
  the request index.

Its payload layout, which matches the official app's note-event layout byte for byte
— though for the reason above, that match is weak evidence:

```
[0] position MSB   ┐ absolute tick position, 14-bit
[1] position LSB   ┘
[2] event type     (0 for a note; the app ignores it)
[3] note number    0-127
[4] velocity       0-127
[5] note-off velocity  (observed always 0)
[6] gate MSB       ┐ gate time, 14-bit
[7] gate LSB       ┘
```

The two readings agree on the payload and on `72 (p<<4) 00` for writing. They
disagree on what `p` counts and on whether `al` is an event index or a compact
list index. **Resolve it on hardware before relying on either** — neither
reading has any hardware behind it.

## Drum piano roll — `ah = 22`-`27`

Identical structure, a different block of address-high values.

| `ah` | Role |
|---|---|
| `22` | add |
| `23` | change |
| `24` | remove |
| `25` | get an event |
| `26` | find an index |
| `27` | parameterised remove with acknowledgement |

The index is composed from the **drum part number**:
`(drumPart << 4) | (eventIndex >> 7)`.

### Verified on hardware

`verified on hardware`. `25` (read) answers for **n = 0-6 and no further**;
n = 7-11 give no reply over 6 indices × 2 attempts each. So this block really
is the seven drum parts, addressed by their global part number — unlike the
synth block, whose index is local (see
[below](#the-synth-block-is-indexed-locally-0-3)).

It works on a drum part **whether or not that part has been re-typed**: part 6,
converted to SYNTH, answers here and not on `70`.

**The event payload is 8 bytes, the same layout reading and writing:**

```
tMsb tLsb type note velocity ?? gateMsb gateLsb
```

`type` 0 = note. Both 14-bit fields are MSB first: writing `eventTime = 960`
reads back as `07 40`. Byte 5 read as `00` in everything observed; its role is
unknown.

```
write   F0 43 10 7F 1C 0C 22 (p<<4) 00  th tl 00 nn vv 00 gh gl  F7
read    F0 43 30 7F 1C 0C 25 ((p<<4)|(idx>>7)) (idx&7F) F7
```

**A chord fits in one instant.** Four notes written at the same `eventTime` on
a re-typed part 6, then read back one index at a time:

```
evt 0  t=60  note=61      evt 2  t=60  note=68      evt 4  t=180 note=48
evt 1  t=60  note=64      evt 3  t=60  note=71          (witness, next step)
```

All four survive. This is the only route to a chord on the SEQTRAK sequencer —
step record holds one note per step.

**The index space differs by track type.** On the re-typed part the indices are
**dense and in time order** (0,1,2,3 for the chord, 4 for the witness). On a
DRUM part they are **spaced like steps**: a factory kick track answered at
indices 0, 1, 2, 4 and 10 with empty replies in between, and those indices
match the occupied steps exactly. `verified on hardware` for both
observations; the reading that a DRUM part is one event per step and keys its
index on the step, while a SYNTH part keeps a true event list, is the
straightforward explanation but has not been tested further.

**The machine does not quantise `eventTime`.** Three notes of one chord written
20 ticks apart read back as `300, 320, 340` — the full 1/120-of-a-step
resolution is preserved.

## Copying a pattern

`from the official app, untested`. Address-high `0x77` copies a whole pattern into a clipboard and pastes it
back somewhere else. Useful when several patterns differ only in a few steps:
copy once, paste, then edit.

| Operation | Address | Data bytes |
|---|---|---|
| Pattern Copy | `77 01 20` | `trackIndex, patternIndex` |
| Pattern Paste | `77 01 21` | `trackIndex, patternIndex` |

These two addresses are also listed in [02-sysex-format.md](02-sysex-format.md);
they are repeated here with their payloads.

Whether the clipboard survives a project change, and whether paste across
tracks of different types is allowed, are both untested.

## Clearing a pattern

`01 1p 37` (`DeletePattern`, 0-5) clears one pattern of one part in a single
message, rather than 128 step deletions. `verified on hardware`: sent with the
pattern number currently selected on a re-typed part holding five events, it
left indices 0-23 all answering empty. `01 1p 48`
(`DeletePatternElement`, 0-6) is the drum-kit element equivalent.

**The slot number is in the data, so clearing does not need a `PatternSelect`
write** — unlike the writes above, which all land in the *selected* pattern.
Sent 66 times in one run, six slots on each of the eleven parts with no
selection touched, it left every part's selected pattern empty: steps 0-15 at
`70 (40|p) ss` on the five DRUM parts and index 0 of the piano roll on the other
six, each read with retries so that a zero-byte reply could be told from a
silence. That run is the first to exercise it on the **native** synth parts
(7-10). `verified on hardware`, see
[10-verified-behaviour.md](10-verified-behaviour.md#2026-10-23-hardware-session-a-sung-melody-written-to-synth-1-and-three-single-shot-verifications-broadened).

**Clearing every pattern of a project does not make it a blank project.**
`01 1p 37` touches the notes and nothing else: the track volumes (`30 5p 00`),
the mutes (`30 5p 29`) and the scene mute bytes reached by `71 1p 02` all
survive it. A slot reused for a new song can therefore hold a correct pattern
and stay completely silent — which is what happened, and what cost the most time
in that run. `verified on hardware`, see
[10-verified-behaviour.md](10-verified-behaviour.md#2026-10-23-hardware-session-why-a-freshly-written-track-was-silent-and-two-writes-settled-on-the-way).

It says nothing about the five slots that were *not* selected: those were
cleared but never read back, so clearing an unselected slot is still
`from the official app, untested`.

## Ticks

One 16th-note step is **120 ticks** (`0x78`). So:

```
gridIndex       = positionTicks // 120
gridPositionTicks = gridIndex * 120
microOffsetTicks  = positionTicks - gridPositionTicks
```

`reverse-engineered from app traffic`. This is consistent with the step-record
default gate of 120 and with the micro-timing range of -60 to +59 (half a step
either way).

**Confirmed on hardware, and the origin is the step centre.** `verified on
hardware`. A factory kick track holds notes on steps 0, 1, 2, 4 and 10, read
independently through step record. The same notes read through the drum piano
roll (`25`) carry:

| step | 0 | 1 | 2 | 4 | 10 |
|---|---|---|---|---|---|
| `eventTime` | 60 | 180 | 300 | 540 | 1260 |

Five points on `eventTime = step × 120 + 60`. The offset of 60 is not
arbitrary: step record reads `microTiming = 60` on each of those steps, so

```
eventTime = step × 120 + microTiming      microTiming 60 = dead centre
```

A writer placing notes on the grid must therefore use `step × 120 + 60`, not
`step × 120`. Writing a 128-step pattern needs `eventTime` up to 15 300, well
inside the 14-bit field.

MIDI clock, when enabled, runs at 24 ppqn — **6 clock ticks per 16th step** —
which is a different tick unit from the 120-tick sequencer resolution. Both are
`verified on hardware`.

## Pattern length

A step number must stay inside the length of the pattern you are writing to, and
**each track has its own length**.

| Parameter | Address | Range |
|---|---|---|
| `Pattern Select` | `30 5p 0F` | 0-5 → pattern 1-6 |
| `Pattern 1-6 Bar Length` | `30 5p 10` … `30 5p 15` | 1-8 bars |
| `Pattern 1-6 Step` | `30 5p 16`, `18`, `1A`, `1C`, `1E`, `20` | 2 bytes, 1-128 |
| `Pattern Master Step` | `30 40 7A` | 2 bytes, 1-128 |

`from Yamaha Data List`. A global playhead cursor is only correct when every
track shares the master length.

### `Pattern Select` only reaches patterns 3-6 when `Pattern Select Mode` is 1

`verified on hardware`, and this is the failure that costs the most, because
**it is completely silent**: no acknowledgement, no error code, just a value
that does not move.

`Pattern Select Mode` (`30 40 79`, range 0-1) was listed in
[03c-parameters-project.md](03c-parameters-project.md) with no stated meaning.
It gates how many of the six pattern slots are reachable. Writing `30 5t 0F`
with 0-5 in turn and reading it back after each write, on track 0:

| value written | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| read back, mode **0** | 0 | 1 | 2 | **2** | **2** | **2** |
| read back, mode **1** | 0 | 1 | 2 | 3 | 4 | 5 |

The mode was restored to its original value afterwards. The consequence was
observed before the cause: writing eleven tracks' worth of patterns in mode 0
left slots 2, 3 and 4 of each track holding **the same** content, because every
write aimed at 3 or 4 landed on 2 and overwrote it. Nothing in the exchange
said so; it surfaced only on read-back.

So, for any client that uses more than three patterns per track:

1. Write `30 40 79 = 1` first.
2. **Read `30 5t 0F` back after every selection** and refuse to continue if it
   does not match. A pattern write aimed at an unreachable slot destroys the
   content of slot 2.

What the mode means on the machine's own front panel is not established here —
only its effect on the reachable range.

> **Step record writes into the *selected* pattern.** `70 tt 00` carries no
> pattern number, in the address or in the data — only a step. To fill more
> than one pattern on a track, change `Pattern Select` (`30 5p 0F`) between
> them. `verified on hardware`: with the mode set as described below, selecting
> each slot in turn and reading the events back returned a different pattern
> each time. The same is true of the two piano rolls — `22` and `72` carry no
> pattern number either, and write into the selected pattern.

## Suggested order of work

Steps 1 to 3 are all `verified on hardware`, so they are a known-good path
rather than a guess.

1. Check `01 10 20` reads `0` — the sequencer must be stopped.
2. Parameter Request on `70 (40|tt) ss` to read what is in a step. Nothing is
   modified, so this validates your address arithmetic for free.
3. Add a note with `70 tt 00`, read the step back, then delete it again with
   `70 (20|tt) 00` to restore the pattern.
4. Only then move to the piano roll, which is more capable but requires index
   bookkeeping and whose addressing is still
   [disputed](12-open-questions.md).

Keep a known-good control address in the same loop (the tempo at `30 40 76` is
ideal) so that a dropped reply cannot be mistaken for a result.
