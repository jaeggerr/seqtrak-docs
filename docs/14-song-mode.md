# 14 — Song mode (`71 xx xx`) and writing a whole song

Song mode chains **scenes**. A scene picks one pattern per track, plus mutes and
a length; playing the song walks the scenes. It is the only way to get a
structure longer than one pattern out of the machine without a host driving it
live.

This document also answers the practical question it leads to: **how do you get
an entire composition into a project?** Short answer in
[§5](#5-writing-a-whole-song-the-practical-route).

Everything is `from the official app, untested` unless marked
otherwise. The addresses are listed in
[03g-parameters-sequencer.md](03g-parameters-sequencer.md); this document adds
how they are composed, which the parameter table cannot show.

## 1. The address map

| Address | Name | Size | Declared range |
|---|---|---|---|
| `71 00 00` | `AddScene` | 1 | 0-15 |
| `71 20 00` | `RemoveScene` | 1 | 0-15 |
| `71 10 00` | `ChangeLength` | 3 | 0-245903 |
| `71 10 03` | `ChangeSoloTrack` | 2 | 0-1931 |
| `71 10 04` | `CurrentScene` | 1 | 0-15 |
| `71 10 05` | `ReserveChangeCurrentScene` | 1 | 0-15 |
| `71 10 06` | `ChangePlayMode` | 1 | 0-2 |
| `71 10 07` | `ChangeSceneLoop` | 1 | 0-1 |
| `71 50 00` | `ChangeSceneMode` | 1 | 0-1 |
| `71 1p 01` | `ChangePattern` | 2 | 0-1925 |
| `71 1p 02` | `ChangeMute` | 2 | 0-1921 |
| `71 1p 09` | `ChangeSamplerElementMute` | 2 | 0-1921 |
| `71 40 <scene>` | Scene Info request | — | scene in the address |

The last row is **not** in the parameter table: the app builds the address
from `0x71`, `0x40` and the scene number, and sends it as a Parameter Request:

```
F0 43 30 7F 1C 0C 71 40 <scene> F7
```

## 2. Sixteen scenes

`AddScene`, `RemoveScene`, `CurrentScene` and `ReserveChangeCurrentScene` are
all bounded 0-15. **Sixteen scenes per project.**

## 3. What a scene holds

Per scene: a length, a solo track, a play mode, a loop flag. **Per track within
the scene**: the chosen pattern, the mute, and the sampler element mute.

A scene is one column of a tracks × sections grid — exactly the shape needed to
chain sections of a composition.

`SongModel.Index`, the dictionary key, for reference: `AddScene` 0,
`ChangeLength` 1, `ChangePattern` 2, `ChangeMute` 3, `ChangeSoloTrack` 4,
`CurrentScene` 5, `ReserveChangeCurrentScene` 6, `ChangePlayMode` 7,
`ChangeSceneLoop` 8, `RemoveScene` 9, `ChangeSceneMode` 10, `SceneInfo` 11,
`ChangeSamplerElementMute` 12, `ChangeElementMute` 13.

## 4. The scene number travels in the data, not the address

This is the part the parameter table cannot express, and the easiest thing to
get wrong.

To set a track's pattern in a scene, the app takes the track's `ChangePattern`
address (`71 1p 01`) and sends two data bytes, `<scene> <pattern>`.

The address carries the **track**; the data carries the **scene**:

```
set a track's pattern in a scene   F0 43 10 7F 1C 0C 71 1p 01 <scene> <pattern> F7
set a track's mute in a scene      F0 43 10 7F 1C 0C 71 1p 02 <scene> <mute>    F7
set the scene's solo track         F0 43 10 7F 1C 0C 71 10 03 <scene> <track>   F7
```

Mute and solo track follow the same shape byte for byte.

### The composite maxima confirm it

The ranges in the parameter table are **composite values**, not scalar bounds —
[README.md](../README.md) already flags this for Song mode. Reading them as
`scene × 128 + x` makes every one of them land exactly:

| Parameter | Max | Decomposition | Reading |
|---|---|---|---|
| `ChangePattern` | 1925 | 15 × 128 + **5** | scene 0-15, **pattern 0-5** |
| `ChangeMute` | 1921 | 15 × 128 + 1 | scene 0-15, mute 0-1 |
| `ChangeSamplerElementMute` | 1921 | 15 × 128 + 1 | same |
| `ChangeSoloTrack` | 1931 | 15 × 128 + **11** | scene 0-15, **track 0-11** |
| `ChangeLength` | 245903 | 15 × 16384 + **143** | scene 0-15, length 0-143 |

The first four cross-check against facts established elsewhere — six patterns
per track, eleven tracks — which is what makes the fifth credible. **The unit of
scene length is unknown**; 143 is neither 128 nor 144 and no conversion appears
in the app.

### `AddScene` and `RemoveScene`, settled on hardware

`ChangePattern`, `ChangeMute` and `ChangeSoloTrack` are actually sent by the
official app, so their wire form is read, not guessed. `AddScene`
(`71 00 00`), `RemoveScene` (`71 20 00`) and `ChangeLength` (`71 10 00`) have
**no sender in the app**, so how a scene gets created could only be guessed
from the app's definitions.

`verified on hardware`: the guess was right for the first two. The scene
number goes in the **data**, exactly as for `ChangePattern`. The test used a
project that had three scenes, so scenes 3-15 answered a Scene Info request
with zero data bytes — a clean before/after instrument:

```
71 40 03  ->  0 data bytes          (scene 3 does not exist)
send      F0 43 10 7F 1C 0C 71 00 00 03 F7
71 40 03  ->  33 data bytes         (scene 3 exists)
send      F0 43 10 7F 1C 0C 71 20 00 03 F7
71 40 03  ->  0 data bytes          (back to the initial state)
```

Eleven scenes were then created in a row without incident, and a `RemoveScene`
on each unwanted one left exactly the intended count.

### `ChangeLength`, settled on hardware 2026-10-23

The last song message with no sender in the app and no test. Run on a scene
that **did not exist** before the test — scene 11 answered Scene Info with zero
data bytes — so it was created, written to, and removed, and nothing of the
project was touched. The tempo answered before and after.

```
71 40 0B  ->  0 data bytes            (scene 11 does not exist)
send      F0 43 10 7F 1C 0C 71 00 00 0B F7        AddScene
71 40 0B  ->  33 data bytes           (scene 11 exists, byte 1 = 00)
send      F0 43 10 7F 1C 0C 71 10 00 0B 00 40 F7  ChangeLength, 64
71 40 0B  ->  byte 1 = 40             (64)
send      F0 43 10 7F 1C 0C 71 10 00 0B 00 64 F7  ChangeLength, 100
71 40 0B  ->  byte 1 = 64             (100)
send      F0 43 10 7F 1C 0C 71 20 00 0B F7        RemoveScene
71 40 0B  ->  0 data bytes            (gone)
```

**The guessed wire form was right**: `71 10 00` with `<scene> <msb> <lsb>`, the
length 14-bit as the composite bound 245903 = 15 × 16384 + 143 implies.

**And byte 1 of a Scene Info reply is the scene's length.** It was `00` on a
freshly created scene, became `40` and then `64` as the length was set, and no
other byte of the 33 moved either time. Two different values tracked, which is
what tells a byte that *is* the length from a byte that merely changed.
`verified on hardware`.

That byte had no meaning in this document before. The Scene Info layout now
reads: byte 1 the length, offsets 2-12 the patterns, byte 13 still unexplained,
offsets 14-24 the mutes.

**The unit is still unknown**, and so is what happens above 127: a 14-bit field
with a documented maximum of 143 cannot hold 143 in the single byte the reply
uses, so either the reply truncates, the real maximum is lower, or the length
spills somewhere else in the 33 bytes. Nothing here settles that — the two
values tried were both under 127.

Reproduce with
[`../tools/hardware-probe/scene_length.py`](../tools/hardware-probe/scene_length.py).

### What a Scene Info reply contains

`verified on hardware`. `71 40 <scene>` answers **33 data bytes** for a scene
that exists and **zero** for one that does not. Comparing what was written to
what came back, across 11 scenes × 11 tracks of patterns and mutes:

| Offset | Size | Contents |
|---|---|---|
| 0-1 | 2 | unknown, `00` in everything observed |
| 2-12 | 11 | **pattern number**, one byte per track, tracks 0-10 |
| 13 | 1 | unknown, `00` in everything observed |
| 14-24 | 11 | **mute flag**, one byte per track, tracks 0-10 |
| 25-32 | 8 | unknown — plausibly the sampler element mutes, untested |

Byte 13 is the trap. Reading the mutes from offset 13 instead of 14 yields
eleven values shifted by one track, which looks exactly like a failed write
when the write was in fact correct.

A factory project made this layout easy to read: its scene 1 answered
`00 00` followed by eleven `01` bytes, and scene 2 the same with `02` —
every track pointed at pattern 1, then at pattern 2.

## 5. Writing a whole song: the practical route

### Use step record, one note per message

[04-sequencer-editing.md](04-sequencer-editing.md) has the message forms, and
the write/read-back/delete round trip there is `verified on hardware`. That is
the recommended route and the only one with a verified foundation.

The bulk route — handing the machine a complete project image — is **out of
reach today**. [08-bulk-and-files.md](08-bulk-and-files.md#sending-a-whole-project)
sets out why: the transport lives entirely in a native plugin, and the pattern
encoding inside a project image has not been decoded.

### Budget: the throughput is not the problem

The official app waits **2 ms after every MIDI message** — see
[07-transports.md](07-transports.md#send-pacing). So:

| Notes written | Messages | Time at 2 ms |
|---|---|---|
| 1 000 | 1 000 | 2 s |
| 4 000 | 4 000 | 8 s |
| 16 384 (every step of 8 tracks × 32 patterns × 64 steps) | 16 384 | 33 s |

Fixed overheads are negligible: one length message per (track, pattern) ≤ 66,
one `Pattern Select` per pattern switch ≤ 66, one re-type per converted track
≤ 7. Per-step velocity, micro-timing or retrigger each add one message per step
they touch, so they can double or triple the total — still under two minutes.

### Capacity: the structure *is* the problem

| Limit | Value | Where |
|---|---|---|
| Tracks | 11 | [01-overview.md](01-overview.md) |
| Patterns per track | **6** | `30 5p 0F`, range 0-5 |
| Steps per pattern | 1-128 | `30 5p 16` … `30 5p 20`, 2 bytes |
| Bars per pattern | 1-8 | `30 5p 10` … `30 5p 15` |
| Scenes | **16** | this document, §2 |

A composition with more than six distinct patterns on one track does not fit,
and no protocol trick changes that. Two ways to condense before you give up:

1. **Merge pairs.** Two consecutive 64-step patterns fit in one 128-step
   pattern. Thirty-two sections become sixteen — which is exactly the number of
   scenes.
2. **Deduplicate.** Trackers repeat heavily; identical patterns should collapse
   to one pattern reused across scenes. Where a track still needs more than six
   after deduplication, the decision is musical, not technical.

`77 01 20` / `77 01 21` (pattern copy and paste, see
[04-sequencer-editing.md](04-sequencer-editing.md#copying-a-pattern)) help when
patterns differ only slightly: copy once, paste, then edit the few steps.

### Suggested order

1. Select the project: Bank Select MSB 64, LSB 0, Program Change to the slot
   (see [08-bulk-and-files.md](08-bulk-and-files.md)). `01 10 15` is the
   read-back, not the command.
2. Check `01 10 20` (sequencer) reads `0` and `01 10 22` (sampling) reads `0`,
   and that the machine is not in Song mode.
3. Re-type the drum tracks you need as synths — **before** touching Song mode,
   because `MixerOrSongMode` is a refusal reason. One at a time, waiting for
   `01 33 01`. Then **assign each converted track's sound explicitly** with
   `01 1p 33`: the conversion replaces it with a default
   (`verified on hardware`). See [13-track-types.md](13-track-types.md).
4. Per track and pattern: `Pattern Select` `30 5p 0F`, length
   `30 5p 16+2n`, clear with `01 1p 37`, then the notes with `70 tt 00` at 2 ms.
5. Project settings: tempo `30 40 76`, master step `30 40 7A`, swing
   `30 40 7C`, scale `30 40 7E`, key `30 40 7F`.
6. Scenes: `71 1p 01` per (scene, track).
7. Save: `01 32 00` with data `01` (`MIDI.ContentsSender.SendProjectSave`).

> **Step record writes into the *selected* pattern.** `70 tt 00` has no pattern
> field, in the address or in the data. To fill more than one pattern on a
> track, change `Pattern Select` (`30 5p 0F`) between them.

## 6. Preconditions and interactions

| Condition | Address | Required value |
|---|---|---|
| **The project you think you are on** | `01 10 15` | the project you mean |
| Sequencer stopped | `01 10 20` | `0` |
| Not sampling | `01 10 22` | `0` |
| Not in content-management mode | `01 10 01` | `0` for editing, `1` for bulk content ops |
| Not in Song mode | — | required to re-type a track (`MixerOrSongMode`) |

### Read `CurrentProject` before writing — it is a precondition, not a detail

`verified on hardware`, the hard way. Nothing in the editing protocol carries a
project number: step record, both piano rolls, pattern lengths, scene writes
and `DeletePattern` all act on **the current project**, whichever that is. The
machine can be moved off it by a Bank Select + Program Change from any client,
or by hand on the front panel, and no reply to any of those messages mentions
which project they landed in.

This was met in practice. A whole project's worth of state read as damaged —
eight of eleven scenes missing, a tempo 26 BPM off, pattern lengths reset —
because the machine had been switched to project 7 while the song lived in
project 0. The song was intact. Writing the "repair" would have destroyed a
different project and reported success.

So: read `01 10 15` first. `CurrentProject` is a status read; to *move*
project, send Bank MSB 64, LSB 0, then the Program Change
([06-sounds-presets.md](06-sounds-presets.md#bank-select-and-program-change)).

#### Re-read the whole state and compare it, rather than picking a witness

What caught the wrong project was the **tempo**, reading 26 BPM off a value
that a track-type test cannot possibly move. But it was not a witness anyone
had chosen. It was in the diagnostic because that script re-reads *every*
project setting and compares each to the value it expects — a habit, with no
hypothesis about what was being looked for. The tempo spoke because it was
there, not because someone predicted it would.

That distinction bounds this repository's
[rule 3](../CLAUDE.md#talking-to-real-hardware) rather than contradicting it.
Rule 3 says to use witnesses **to prove what an address means**, and for that
they are exactly right: you change one thing and name what must not move, so
you control the only variable. They are the wrong instrument for finding out
*why something is broken*, because there you do not control the variable —
choosing a witness means guessing the failure mode in advance.

Here, guessing would have failed in the worst way. A repair of pattern
contents invites a witness among the pattern addresses — and on the wrong
project those *were* all wrong, so such a witness would have **confirmed** the
false diagnosis instead of breaking it. A witness correlated with the reported
cause cannot contradict it.

So, before repairing anything:

- **Re-read the full state and diff it against what you expect**, including
  everything the reported fault has no business touching. One value that cannot
  plausibly have changed is worth more than ten that confirm the story.
- A value that is wrong *in a way the diagnosis cannot explain* is the signal.
  Treat it as evidence that the diagnosis is wrong, not as extra damage.
- Keep witnesses for establishing meaning, where you control the one variable.

A systematic re-read catches the failure mode nobody anticipated, which is
exactly the one that does damage.

## 7. What to test on hardware, in order

Items 1, 2, 3 and 5 below are now `verified on hardware` — a complete song
(1320 notes, 11 parts, 11 scenes of 128 steps) was written to a real unit and
read back. What they established, and the two that remain:

1. ~~A burst at 2 ms over several hundred messages.~~ **Done**: 1320 note
   messages at 2 ms, read-back of 161 randomly chosen steps across all 41
   patterns, no loss. Note that `70 tt 00` only carried the three drum parts;
   the melodic parts went through the piano rolls, which were paced the same
   way — see [04-sequencer-editing.md](04-sequencer-editing.md).
2. ~~That `Pattern Select` really redirects.~~ **Done**, with a large caveat:
   it only reaches patterns 3-6 when `Pattern Select Mode` (`30 40 79`) is 1,
   and it fails silently otherwise.
3. ~~That `Pattern n Step` accepts 128.~~ **Done**: all 6 slots of all 11
   tracks set to 128 and read back.
4. **Still open**: the unit of `ChangeLength` (`71 10 00`), which has no sender
   in the app and was not exercised.
5. ~~Whether `71 1p 01` with a scene byte behaves as described.~~ **Done**:
   patterns and mutes written for 11 tracks × 11 scenes all read back exactly
   through `71 40 <scene>`.
6. **Still open**: whether the project actually plays as laid out. Scene
   contents were verified by read-back, not by listening.
