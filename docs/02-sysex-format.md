# 02 — SysEx message format

How to build and parse every SEQTRAK System Exclusive message: framing, the
five message forms, the address map, the value encodings, the checksum, and the
bulk-dump variants.

Framing is `from Yamaha Data List` and confirmed `from the official app, untested` in `MIDI.Common`; the two agree exactly. Message exchange
over USB MIDI is `verified on hardware`.

## Framing constants

```
Manufacturer ID : 43        Yamaha
Group ID        : 7F 1C     high, low
Model ID        : 0C        SEQTRAK
Device Number   : n         the app transmits n = 0
```

The device number lives in the low nibble of byte 2. On reception the official
app **masks that nibble off before comparing** (`MaskDeviceNumber()` /
`CheckDeviceNumber()`), so a device answers whatever device number you used, and
a parser should do the same: compare `byte2 & 0xF0`, not `byte2`.

## The five message forms

| Form | Frame | Direction |
|---|---|---|
| Parameter Change | `F0 43 1n 7F 1C 0C ah am al dd … F7` | both |
| Parameter Change, no data | `F0 43 1n 7F 1C 0C ah am al F7` | host → device (a trigger) |
| Parameter Request | `F0 43 3n 7F 1C 0C ah am al F7` | host → device |
| Bulk Dump Request | `F0 43 2n 7F 1C 0C ah am al F7` | host → device |
| Bulk Dump | `F0 43 0n 7F 1C bh bl 0C ah am al dd … cc F7` | both |

A Parameter Request is answered with a Parameter Change at the same address. A
Bulk Dump Request is answered with one or more Bulk Dumps. Both are
`verified on hardware` over USB MIDI in device-to-host direction, with the
SEQTRAK acting as the USB host.

`ah am al` is the three-byte address. Every byte is 7-bit, as in all MIDI data.

### Reading a single parameter

```
F0 43 30 7F 1C 0C 30 40 76 F7        request the tempo
F0 43 10 7F 1C 0C 30 40 76 00 77 F7  reply: 0x00 << 7 | 0x77 = 119 BPM
```

### Writing a single parameter

```
F0 43 10 7F 1C 0C 30 40 76 00 78 F7  set the tempo to 120 BPM
```

### Byte offsets in a Parameter Change — not the Bulk Dump offsets

The two forms do not share an offset table, because the bulk frame carries a
14-bit byte count that this one does not. Parsing a Parameter Change with the
Bulk Dump offsets is off by one and matches **nothing**, silently.

```
F0  43  1n  7F  1C  0C  ah  am  al  dd ... F7
 0   1   2   3   4   5   6   7   8   9
```

| Offset | Field |
|---|---|
| 0 | `F0` |
| 1 | manufacturer ID, `43` |
| 2 | `1n` — compare `byte2 & 0xF0`, not `byte2` |
| 3, 4 | group ID, `7F 1C` |
| **5** | **model ID, `0C`** |
| **6, 7, 8** | **address high, mid, low** |
| 9 … | data, up to the closing `F7` |

Against the bulk frame, where the model ID is at 7 and the address at 8-10
([below](#bulk-dump)). A reader that confuses the two drops every reply while
appearing to work, since the receive loop simply never matches —
`verified on hardware`, having happened.

## Address map

The complete set of address-high values the official app can address, taken
from the `ParameterInfo.AddressHighType` enumeration, merged with the zones
Yamaha documents and the zones found by watching app traffic.

| `ah` | Internal name | Contents | Source |
|---|---|---|---|
| `00` | System | Global settings; Wi-Fi at `00 60`-`00 62` | `from Yamaha Data List` (`00 00`), `from the official app, untested` (`00 60`-`00 62`, since `verified on hardware` for `00 60`) |
| `01` | PCApp | Live session and editing state — see [05-live-state.md](05-live-state.md) | `from the official app, untested`, several addresses now `verified on hardware` |
| `0B` | *(not in the enum)* | Project list bulk dump (all 8 slots) | `reverse-engineered from app traffic` |
| `0C` | *(not in the enum)* | Sound browser: category lists and favourites | `reverse-engineered from app traffic` |
| `10` | *(not in the enum)* | Content attributes: UUID at `10 00 02`, rename at `10 00 04`, favourite toggle at `10 01 xx` | `reverse-engineered from app traffic` **and** `from the official app, untested` — found twice, independently |
| `11` | Bulk Header | `11 mm nn`, opens a bulk transfer | `from Yamaha Data List` |
| `12` | Bulk Footer | `12 mm nn`, closes it | `from Yamaha Data List` |
| `18` | PCAppDrumKitStatus | Current drum-kit element state | `from the official app, untested` |
| `22`-`27` | DrumPartPianoRoll… | Drum piano-roll add / change / remove / get / find-index / parameterised remove | `from the official app, untested` |
| `30` | Track / Project | Project common, send effects, master effects, master EQ, A/D and USB audio input, scales, chords, per-track settings | `from Yamaha Data List` |
| `31` | Sound | Per-part sound: name, general, insertion A/B, LFO, arpeggiator | `from Yamaha Data List` |
| `41` | Element | AWM element oscillator / amplitude / pitch | `from Yamaha Data List` |
| `42` | ElementFilter | AWM element filter / EQ / LFO | `from Yamaha Data List` |
| `48` | FMSound | FM common (algorithm, PEG, LFO) | `from Yamaha Data List` |
| `49` | Operator | FM operators | `from Yamaha Data List` |
| `50` | SampleElement | Sampler sample: name, loop and playback points | `from Yamaha Data List` |
| `64` | *(unnamed in the enum)* | Firmware update — see [09-firmware.md](09-firmware.md) | `from the official app, untested` |
| `70` | StepRec | Step record: write, edit, delete and read a step | `from the official app, untested`; the three read forms are `verified on hardware` |
| `71` | Song | Song mode: scenes, length, play mode | `from the official app, untested`; three addresses `verified on hardware` |
| `72`-`76` | PianoRoll… | Synth piano-roll add / change / remove / get / find-index | `from the official app, untested` |
| `77` | StepRecAndPianoRollIndex / SoundPatternCopyPaste | Index replies; pattern copy at `77 01 20`, paste at `77 01 21` | `from the official app, untested` |

Zones `0B`, `0C` and `10` are not in the app's address-high enumeration because
the app builds them elsewhere (`MIDI.Bulk`, `ContentsSender`). They are no less
real: `10 00 04` was found independently by traffic sniffing and by static
analysis, which is the strongest kind of agreement available short of hardware.

### Base addresses, as Yamaha publishes them

| Block | Top address | Data bytes |
|---|---|---|
| System General | `00 00 00` | 48 |
| Format Version | `00 7F 00` | 4 |
| Bulk Header | `11 mm nn` | — |
| Bulk Footer | `12 mm nn` | — |
| Project Common General | `30 40 00` | 128 |
| Send Reverb | `30 41 00` | 71 |
| Send Delay | `30 42 00` | 72 |
| Master Effect 1-4 | `30 43 00` - `30 46 00` | 72 each |
| Master EQ | `30 47 00` | 21 |
| A/D Part Insertion A | `30 49 00` | 68 |
| A/D Part Insertion B | `30 4A 00` | 68 |
| A/D Part General | `30 4B 00` | 24 |
| USB Audio Input | `30 4C 00` | 24 |
| Scale | `30 4D 00` | 128 |
| Project Track General | `30 5p 00` | 42 |
| Chord Notes of Scale 1-4 | `30 6p 00` | 128 |
| Chord Notes of Scale 5-8 | `30 7p 00` | 128 |
| Sound Common Name | `31 0p 00` | 106 |
| Sound Common General | `31 1p 00` | 80 |
| Sound Insertion A | `31 2p 00` | 68 |
| Sound Insertion B | `31 3p 00` | 68 |
| Sound LFO | `31 4p 00` | 39 |
| Sound Arpeggiator | `31 5p 00` | 32 |
| AWM Oscillator / Amplitude / Pitch | `41 ep 00` | 109 |
| AWM Filter / EQ / LFO | `42 ep 00` | 71 |
| FM Common | `48 09 00` | 24 |
| FM Operator | `49 o9 00` | 32 |
| SAMPLER Sample General | `50 eA 00` | 112 |

Yamaha publishes a **byte count** for each block, which is the data size plus
four — one Model ID byte and three address bytes. For example System General is
listed as 52 (`0x0034`) for 48 bytes of data. The table above gives the data
size, which is what you index into.

## Composing the address-mid byte

Many addresses carry a part, element or operator index inside the mid byte. The
official app composes them at run time; Yamaha writes the variable nibble as a
letter. Both notations mean the same thing.

| Family | Composition | Result | Letter |
|---|---|---|---|
| Project track | `0x50 \| part` | `30 50`-`30 5A` | `30 5p` |
| Chord notes | `0x60 \| part`, `0x70 \| part` | `30 67`-`30 69`, `30 77`-`30 79` | `30 6p`, `30 7p` |
| Sound name | `0x00 \| part` | `31 00`-`31 0A` | `31 0p` |
| Sound general | `0x10 \| part` | `31 10`-`31 1A` | `31 1p` |
| Insertion A / B | `0x20 \| part`, `0x30 \| part` | `31 20`-, `31 30`- | `31 2p`, `31 3p` |
| Sound LFO | `0x40 \| part` | `31 40`- | `31 4p` |
| Sound arpeggiator | `0x50 \| part` | `31 57`-`31 59` | `31 5p` |
| AWM element | `(element << 4) \| part` | `41 07` = element 0 part 7 | `41 ep` |
| FM operator | `(operator << 4) \| 0x9` | `49 09`, `49 19`, `49 29`, `49 39` | `49 o9` |
| SAMPLER element | `(element << 4) \| 0x0A` | `50 0A`-`50 6A` | `50 eA` |
| Live app state, per part | `0x10 \| part` | `01 10`-`01 1A` | `01 1p` |
| Master effect | `0x40 \| (2 + effect)` | `30 43`-`30 46` | `30 4n`, n = 3-6 |

The app's own helper is literally `parameter.AddressMid | track`
(`SoundModel.GetAddressMid`).

> **Watch out for the `01 1p` overlap.** Address-high `01` uses mid `0x10` for
> both the global session block *and* part 0's per-part block. They are
> distinguished by the low byte: `al < 0x30` (plus `0x70`) is global, `al >=
> 0x30` is per-part. So `01 10 15` is `CurrentProject` (global) while
> `01 10 33` is part 0's `CurrentSound`. `verified on hardware` — both were read
> back from a real unit in the same session.

### Effect parameters inside an effect block

An effect block exposes up to 16 parameters, each two bytes. Parameter *k*
(1-based) sits at

```
al = 0x01 | (k << 1)
```

so parameter 1 is at offset `03`, parameter 2 at `05`, … parameter 16 at `21`.
This came out of `ParameterFactory.CreateEffectParameter` and is
`verified on hardware`: live traffic showed Master Effect 3 parameters 1 and 2
at `30 45 03` and `30 45 05`, and Insertion Effect A parameter 4 of part 7 at
`31 27 09`. Offsets `00`-`01` hold the effect type (MSB, LSB) and `02` the
template number. See [appendix-a-effect-types.md](appendix-a-effect-types.md)
and [appendix-b-effect-parameters.md](appendix-b-effect-parameters.md).

## Value encodings

### One byte

Most parameters are a single 7-bit byte, 0-127. Signed parameters are offset:
centre 64 for a `-64 … +63` display, centre 64 for `-24 … +24` (range `0x28`-
`0x58`), and so on. Each parameter document gives both the transmitted range and
the displayed range.

### Multi-byte integers: 7 bits per byte, big-endian

A parameter whose size is 2, 3 or 4 bytes carries 7 usable bits per byte, most
significant first.

```
2 bytes → 14 bits (0 … 16383)
3 bytes → 21 bits
4 bytes → 28 bits
```

Tempo (`30 40 76`, 2 bytes, 5-300) at 120 BPM:

```
MSB = (120 >> 7) & 0x7F = 0x00
LSB =  120       & 0x7F = 0x78

F0 43 10 7F 1C 0C 30 40 76 00 78 F7
```

At 140 BPM it is `01 0C`. The app's helper is
`EncodeIntegerTo7BitArray(value, size)`.

### Multi-byte nibble values

A few parameters pack **4 bits per byte** instead, which the Data List spells
out in its Description column. Master Tune (`00 00 02`, 4 bytes) is
`1st bit3-0 → bit15-12, 2nd → bit11-8, 3rd → bit7-4, 4th → bit3-0`; its default
`00 04 00 00` is therefore 0x4000, the centre of a `-102.4 … +102.3` range.
Sample points (`50 eA 60`, `66`, `6A`) use 3 bits in the first byte then 7 in
each of the next three, giving 24 usable bits.

Always read the Description column before assuming an encoding: Yamaha mixes
7-bit-per-byte and nibble packing in the same table.

### Strings and blobs: 7-into-8 packing

Names and sample blobs are packed in **blocks of 7 data bytes into 8 MIDI
bytes** (`EncodingBlockSize = 7`). The first byte of each group carries bit 7 of
each of the seven bytes that follow; the next seven carry the low 7 bits.

A name field of 88 MIDI bytes is therefore **11 groups of 8**, holding 77 bytes
of UTF-8 — and that is exactly the "88 bytes, 11 groups of 8" shape seen in
project, sound and element names. For plain ASCII every group's first byte is
`00`, which is why a name often reads straight out of the dump.

`"hello world"` as an 88-byte name field:

```
00 68 65 6C 6C 6F 20 77    "hello w"
00 6F 72 6C 64 00 00 00    "orld" + padding
00 00 00 00 00 00 00 00    groups 3-11, all zero
… 72 more zero bytes
```

The app's helpers are `EncodeByteArrayTo7BitByteArray` and
`Decode7BitArrayTo8BitArray`.

## Bulk Dump

```
F0 43 0n 7F 1C bh bl 0C ah am al dd … dd cc F7
       │        │  │  │  └──┴──┴─ address
       │        │  │  └─ model ID
       │        └──┴─ byte count, 14-bit (bh = MSB)
       └─ device number
```

Offsets, from `MIDI.Bulk`:

| Offset | Field |
|---|---|
| 3 | group number high |
| 5 | byte count (14-bit, bytes 5 and 6) |
| 7 | model ID (`0C`) |
| 8, 9, 10 | address high, mid, low |
| 11 | first data byte (plain bulk) |

**Byte count** counts from the Model ID to the last data byte inclusive — so
`4 + data_size`.

**Checksum** is the 7-bit two's complement of the sum of every byte from the
**Model ID** to the last data byte — that is, model ID + address + data +
checksum ≡ 0 (mod 128). In code:

```python
checksum = (-sum(message[7:-2])) & 0x7F
```

The firmware plug-in spells out the same rule as
`(0x80 - (total & 0x7F)) & 0x7F`, or `0` when `total & 0x7F == 0`
(`from the official app, untested`).

> **A conflict, resolved.** The Data List's prose says the checksum covers
> "the Byte Count, Start Address, Data and Check-sum itself". That does not add
> up on a real message, and it is worth showing all three candidate ranges
> rather than one, because **neither** reading of Yamaha's wording reaches zero.
>
> Take the project-rename bulk dump captured from the official app
> (`reverse-engineered from app traffic`), which ends in checksum `0x55`:
>
> | Range summed | Sum | `+ 0x55` | mod 128 |
> |---|---|---|---|
> | Model ID → last data byte | 683 | 768 | **0** ✓ |
> | the published wording taken literally: byte count + address + data, **without** the Model ID | 777 | 862 | 94 |
> | Model ID → last data byte, **plus** the two byte-count bytes | 789 | 874 | 106 |
>
> **Exclude the byte count; include the Model ID.** Each of the two failing rows
> is arithmetically correct for its own range — they are different ways of
> reading the same loose sentence, and neither lands on zero. Both other sources
> (the official app and the firmware plug-in) describe the range that checks out.

### Bulk Header and Footer

A bulk transfer of a whole project, sound or sampler element is bracketed by a
header and a footer at `11 mm nn` and `12 mm nn`:

| `mm` | Target | `nn` |
|---|---|---|
| `00` | Project edit buffer | 0 |
| `01` | Project user 1 | 0-7 (slot) |
| `02` | Sound edit buffer, part `nn` | 0-10 (part) |
| `03`-`12` | Sound user bank 1-16 | 0-127 |
| `13` | Sampler element edit buffer, element `nn` | 0-6 |
| `14`-`1B` | Sampler element user 1-8 | 0-127 |

To request one project, sound or sampler element, send a Bulk Dump Request to
its **header** address. The blocks between header and footer may arrive in any
order and need not all be present, but a transfer containing an irrelevant
block is rejected.

### Dividable bulk: split transfers

Not documented by Yamaha. When a payload does not fit in one message, the
header grows by four bytes:

| Offset | Field |
|---|---|
| 11, 12 | packet count (14-bit) |
| 13, 14 | packet number (14-bit) |
| 15 | first data byte |

This is the format the firmware update uses, and the reason the app's
`AckDataIndex` is 11: the device acknowledges each packet.
`from the official app, untested`.

Two corrections to that picture, both read out of the `Installer`'s own
receive path rather than the app, and both needed before anyone writes a
sender. `from firmware image (static analysis)`.

**The packet number is matched against an 8-bit counter that wraps.** The field
is 14 bits on the wire, but the receiver holds its expected value in a single
byte and truncates on every increment:

```
ldrb r2, [r4, #5]        ; expected packet number -- one byte of context
ldrh r3, [r0, #0xe]      ; received packet number, decoded
cmp  r3, r2
bne  -> 15               ; out of sequence
...
ldrb r3, [r4, #5]
add  r3, r3, #1
uxtb r3, r3              ; wraps at 256, and the truncation is explicit
```

So a sender must transmit `index & 0xFF`, not a running 14-bit index. The
`uxtb` makes the wrap deliberate rather than incidental, which matters: a block
of more than 16,383 packets is expressible, and the `Program` block needs far
more than that.

**The payload is 7-into-8 packed.** The routine at `0x31cc`, reached before the
flash write, is not a length check: it walks the data a byte at a time, shifts
each one left by one, tests bit `0x80` and reassembles through
`mvn … lsl #25` / `mvn … lsr #25`, consuming **8 bytes at a time**. That is the
ordinary Yamaha 7-into-8 unpack. A message carrying 128 SysEx data bytes
therefore delivers **112** image bytes, not 128.

## Identity Request and Reply

Standard universal non-realtime messages. Request is receive-only, reply is
transmit-only.

```
→ F0 7E 0n 06 01 F7                                     n ignored
← F0 7E 7F 06 02 43 00 41 64 06 mm 00 00 7F F7
                        │  │  │  └─ version
                        └──┴──┴─ device family / code: SEQTRAK is 64 06
```

`mm = (version − 1.0) × 10`, so version 1.0 gives `00` and version 1.5 gives
`05`. `from Yamaha Data List`.

A real unit answered with `mm = 0x0A`, which decodes to **version 2.0** and
matches the OS V2.00 it was running — `verified on hardware`:

```
F0 7E 7F 06 02 43 00 41 64 06 0A 00 00 7F F7
```

The firmware plug-in validates the reply by length (15 bytes), by byte 11 being
`00` and by bytes 13-14 being `7F F7`; it also accepts a proprietary
`F0 43 10 7F 1C 0C … F7` reply of at least 10 bytes, used when the device is
already in loader mode. `from the official app, untested`.

## What gates transmission

Yamaha's transmit and receive flows gate each message class behind a System
parameter. This is why a correct message can produce no reply.

| Gate | Parameter | Blocks |
|---|---|---|
| MIDI In/Out, per interface | `00 00 09` (TRS), `00 00 0D` (USB), `00 00 11` (Bluetooth) | everything on that interface |
| Transmit Channel Message | `00 00 0A`, `00 00 0E`, `00 00 12` | notes, CC, Program Change, pitch bend |
| Transmit CC / Bank Select / Program Change | `00 00 0B`, `00 00 0F`, `00 00 13` | bit 6 = CC, bit 5 = Bank Select, bit 4 = Program Change; range `00`-`70` |
| Transmit System Exclusive | `00 00 0C`, `00 00 10`, `00 00 14` | Bulk Dump and Parameter Change out |
| Receive/Transmit Bank Select | `00 00 07` | Bank Select in and out |
| Receive/Transmit Program Change | `00 00 08` | Program Change in and out |
| MIDI Clock Out | `00 00 2D` | `F8` timing clock |
| Transmit Sequencer Control | `00 00 2B` | `FA` start, `FC` stop |
| MIDI Sync | `00 00 2A` | whether incoming `F8` is followed |

Two System Exclusive messages are **not** gated by any of these, which makes
them a recovery path: `Legacy/USB MIDI In/Out` itself and `Sink Current
Setting`. `from Yamaha Data List`.

Active Sensing (`FE`) is transmitted every 250 ms and is not gated. On a legacy
MIDI interface, once sensing has started, a gap of about 500 ms clears the
receive buffer and forces notes off.

## Worked examples

```
Set the tempo to 120 BPM
F0 43 10 7F 1C 0C 30 40 76 00 78 F7

Read the tempo
F0 43 30 7F 1C 0C 30 40 76 F7

Set the KICK track volume to 100
F0 43 10 7F 1C 0C 30 50 00 64 F7

Mute the SNARE track          (0x7D = on, 0x00 = off)
F0 43 10 7F 1C 0C 30 51 29 7D F7

Select pattern 3 on SYNTH 1   (0-indexed, so 02)
F0 43 10 7F 1C 0C 30 57 0F 02 F7

Turn the send reverb off
F0 43 10 7F 1C 0C 30 41 46 00 F7

Set the speaker volume to 80
F0 43 10 7F 1C 0C 00 00 00 50 F7

Set user scale 1, pad 1 to G3 (MIDI note 67)
F0 43 10 7F 1C 0C 30 4D 00 43 F7

Request the project edit buffer (a burst of bulk dumps comes back)
F0 43 20 7F 1C 0C 11 00 00 F7

Request the sound block of part 2 only
F0 43 20 7F 1C 0C 11 02 02 F7

Ask the machine who it is
F0 7E 7F 06 01 F7
```

The scale write and the tempo read above are `verified on hardware`; the rest
are `from Yamaha Data List`.

## Reference code

```python
MFR, GROUP, MODEL = 0x43, (0x7F, 0x1C), 0x0C


def parameter_change(address, data, device=0):
    return bytes([0xF0, MFR, 0x10 | device, *GROUP, MODEL, *address, *data, 0xF7])


def parameter_request(address, device=0):
    return bytes([0xF0, MFR, 0x30 | device, *GROUP, MODEL, *address, 0xF7])


def bulk_request(address, device=0):
    return bytes([0xF0, MFR, 0x20 | device, *GROUP, MODEL, *address, 0xF7])


def encode_int(value, size):
    """Big-endian, 7 usable bits per byte."""
    return [(value >> (7 * (size - 1 - i))) & 0x7F for i in range(size)]


def decode_int(data):
    out = 0
    for byte in data:
        out = (out << 7) | (byte & 0x7F)
    return out


def decode_name(packed):
    """Undo the 7-into-8 packing: 8 MIDI bytes carry 7 data bytes."""
    out = bytearray()
    for block in range(0, len(packed), 8):
        high, body = packed[block], packed[block + 1:block + 8]
        for i, byte in enumerate(body):
            out.append(byte | (((high >> i) & 1) << 7))
    return bytes(out).split(b"\x00")[0].decode("utf-8", "replace")


def bulk_dump(address, data, device=0):
    body = [MODEL, *address, *data]        # byte count covers exactly this run
    count = len(body)
    checksum = (-sum(body)) & 0x7F         # and so does the checksum
    return bytes([0xF0, MFR, 0x00 | device, *GROUP,
                  (count >> 7) & 0x7F, count & 0x7F, *body, checksum, 0xF7])
```
