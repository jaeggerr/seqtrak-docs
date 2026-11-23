# 08 — Bulk dumps, content management and file transfer

How to read and write whole projects, sounds and sampler elements; how the
device reports success or refusal; and what an exported project actually looks
like.

Framing is in [02-sysex-format.md](02-sysex-format.md#bulk-dump). This document
covers the control addresses, the structure sizes, the result codes and the
file-transfer channel.

## Requesting a dump

Send a Bulk Dump Request to a **Bulk Header** address, `11 mm nn`:

```
F0 43 20 7F 1C 0C 11 mm nn F7
```

| `mm` | Target | `nn` |
|---|---|---|
| `00` | project edit buffer | 0 |
| `01` | project user slot | 0-7 |
| `02` | sound edit buffer of part `nn` | 0-10 |
| `03`-`12` | sound user bank 1-16 | 0-127 |
| `13` | sampler element edit buffer, element `nn` | 0-6 |
| `14`-`1B` | sampler element user 1-8 | 0-127 |

`from Yamaha Data List`. `verified on hardware` for `11 02 pp`.

The reply is a **burst of bulk dumps**, bracketed by the matching header and
footer (`12 mm nn`), one message per block of the base-address map. For a single
part this is about thirty blocks: the name, the sound settings, then the eight
AWM elements. **Filter on the address of each block** or later blocks will
overwrite what you just parsed. `verified on hardware`.

The blocks between header and footer may arrive in any order, and not all of
them need be present — but a transfer that includes an irrelevant block is
rejected outright.

## Content management mode

Three preconditions are visible in the result codes: content operations fail if
the machine is **not in content-management mode** (set `01 10 01 = 1`), if the
**sequencer is playing** (stop it), or if it is **sampling**.
`from the official app, untested`.

## Control addresses

As the official app defines them. `from the official app, untested`.

| Field | Address |
|---|---|
| `AcknowledgeAddress` | `01 20 00` |
| `InfoAckAddress` | `01 22 00` |
| `RemoveProjectAddress` | `01 40 00` |
| `RemoveSoundAddress` | `01 41 00` |
| `RemoveElementAddress` | `01 42 00` |
| `AttributeProjectUUIDAddress` | `10 00 02` |
| `AttributeProjectNameAddress` | `10 00 04` |
| `FavoriteAddress` | `10 01 03` |
| `FavoriteElementAddress` | `10 02 03` |
| `AttributeSoundUUIDAddress` | `10 01 02` |
| `AttributeElementUUIDAddress` | `10 02 02` |
| `AttributeSoundNameAddress` | `10 01 04` |
| `AttributeElementNameAddress` | `10 02 04` |

The whole set is regular, which is a check on it:

```
10 <cc> <ff>     cc = 00 project, 01 sound, 02 element
                 ff = 02 UUID, 03 favourite, 04 name
01 4c 00         c  = 0 project, 1 sound, 2 element  (remove)
```

`10 01 03` and `10 02 03` corroborate the `10 01 xx` favourite addresses found
independently by traffic sniffing and documented in
[06-sounds-presets.md](06-sounds-presets.md) — a second independent agreement
between the app's definitions and observed traffic, after `10 00 04`.

**`10 00 04` is a double find.** It was located independently by watching app
traffic *and* in the official app's own definitions, which is the strongest
corroboration available short of hardware.

## Renaming a project — `10 00 04`

`reverse-engineered from app traffic`. Writes a project name straight into a
slot. The data prefix targets the slot, so no Bank Select + Program Change is
needed first.

```
F0 43 00 7F 1C 00 6A 0C 10 00 04 00 ss 00 [88-byte name] [12 zero bytes] cc F7
```

Byte count `00 6A` = 106 = 1 model + 3 address + 102 data.

| Offset | Size | Field |
|---|---|---|
| 0 | 1 | flag, always `00` |
| 1 | 1 | target slot, 0-7 |
| 2 | 88 | project name, 7-bit packed (11 groups of 8) |
| 90 | 12 | reserved, always `00` |

The first byte of the name field (group 1's MSB byte) lands on data offset 2 and
is `00` for ASCII names.

Rename slot 1 to `"doowap"`:

```
F0 43 00 7F 1C 00 6A 0C 10 00 04 00 01 00 64 6F 6F 77 61 70 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 55 F7
```

That `0x55` checksum is the message this repository used to settle how the
checksum range is defined — see
[02-sysex-format.md](02-sysex-format.md#bulk-dump).

### What the official app wraps around it

1. Bank Select MSB 64 / LSB 0 plus a Program Change to the target slot, which
   loads it into the edit buffer.
2. A wait of about 12 ms, for the SEQTRAK's `01 10 15` acknowledgement.
3. The rename dump above.
4. A second Bank Select + Program Change, usually back to the slot that was
   active before.

Step 1 is **not required** — the dump's slot prefix targets the slot directly
and the rename persists. Step 4 is an app-side courtesy, restoring the user's
selection.

## Listing all projects — `0B 00 00`

`reverse-engineered from app traffic`. Returns all eight user project slots,
names and metadata, in one response.

```
→ F0 43 20 7F 1C 0C 0B 00 00 F7
← F0 43 00 7F 1C 0E 28 0C 0B 00 00 dd … dd cc F7
```

Byte count `0E 28` = 1832, so 1828 data bytes = a 4-byte header plus
8 slots × 228 bytes.

Header:

| Offset | Size | Field |
|---|---|---|
| 0 | 1 | reserved, always `00` |
| 1 | 1 | reserved, observed constant `01` — **not** the active slot |
| 2 | 2 | reserved, `00 00` |

Slot structure, 228 bytes each, starting at data offset 4:

| Offset | Size | Field | Notes |
|---|---|---|---|
| 0 | 1 | reserved | always `00` |
| 1 | 1 | slot index | 0-7 |
| 2 | 22 | reserved | mostly zeros |
| 24 | 1 | unknown | 0-0x7F, varies per slot |
| 25 | 88 | project name | 7-bit packed — **starts at 25, not 26** |
| 113 | 113 | reserved | mostly zeros |
| 226 | 2 | tempo | 14-bit (`01 1F` = 159, `00 78` = 120) |

**The dump does not carry the active slot index.** Read `01 10 15`
(`CurrentProject`) separately for that — see
[05-live-state.md](05-live-state.md).

> **Offset 25, not 26 — this one bites.** Offset 25 is the first group's **MSB
> carrier byte**, which is `00` for ASCII names, so the characters *look* like
> they begin at 26. Read from 26 and stop at the first `00` and you land on the
> next group's carrier byte at offset 33, truncating **every name to seven
> characters**. That was a real bug in a client built from this documentation.
> The field is 88 bytes of 7-into-8 packing like every other name field; decode
> it as such rather than reading it as raw text. See
> [02-sysex-format.md](02-sysex-format.md#strings-and-blobs-7-into-8-packing).

Parsing it:

```python
HEADER, SLOT = 4, 228

for slot in range(8):
    base = HEADER + slot * SLOT
    index = data[base + 1]
    name = decode_name(data[base + 25: base + 25 + 88])   # 25, not 26
    tempo = (data[base + 226] << 7) | data[base + 227]
```

The 228-byte slot size matches `SoundInfoSize = 228` from the official app, which
is the same record shape reused for projects, sounds and browser entries.

## Structure sizes

As the official app defines them. Needed to parse replies.
`from the official app, untested`.

| Constant | Bytes |
|---|---|
| `SoundInfoSize` | 228 |
| `SoundUUIDInfoSize` | 21 |
| `WaveformInfoSize` | 226 |
| `ElementInfoSize` | 230 |
| `ElementUUIDInfoSize` | 21 |
| `ProjectNameSize` | 88 |
| `ProjectReservedAreaSize` | 11 |
| `ElementNameSize` | 88 |
| `ElementReservedAreaSize` | 7 |
| `InfoNameSize` | 100 |
| `InfoTagSize` | 100 (2 × 50) |
| `InfoUuidSize` | 19 |
| `InfoOrderSize` | 4 |
| `InfoTempoSize` | 2 |
| `InfoAckByteCount` | 12 |
| `FavoriteByteCount` | 7 |
| `RenameContentsByteCount` | 106 |
| `RemoveSingleContentByteCount` | 6 |
| `AttributeContentUUIDByteCount` | 25 |
| `MaxRemoveContentsDataAreaSize` | 3000 (so at most 1500 contents at once) |
| `InfoTimeoutInterval` | 5000 ms |

`RenameContentsByteCount = 106` matches the observed project-rename byte count
exactly, and `InfoNameSize = 100` matches the 100-byte name field of a browser
entry — two more independent agreements between the traffic captures and the
official app.

## Result codes

The device answers on `AcknowledgeAddress` (`01 20 00`). `Bulk.Result`, `from
official app, untested`.

| Code | Meaning |
|---|---|
| 0 | `Success` |
| 1 | `Cancel` |
| 2 | `SoundFull` |
| 3 | `ElementFull` |
| 4 | `WaveformFull` |
| 5 | `KeybankFull` |
| 6 | `SampleFull` |
| 7 | `PacketLoss` |
| 8 | `CheckSumError` |
| 9 | `NotContentManagementMode` |
| 10 | `SequencerPlaying` |
| 11 | `Sampling` |
| 32 | `CancelBySender` |
| 33 | `CancelByReceiver` |
| 48 | `Timeout` |
| 49 | `DirectoryPathInvalid` |
| 50 | `DisconnectedPort` |
| 51 | `SendingFailure` |
| 52 | `XmlParseError` |
| 53 | `ContentIndexOutOfRange` |
| 54 | `BinaryGetError` |
| 55 | `XmlWriteError` |
| 64 | `AlreadySending` |
| 65 | `DirectoryNotFound` |
| 80 | `AlreadyReceiving` |
| 81 | `InvalidPacketNumber` |
| 82 | `InvalidPacketCount` |
| 83 | `DirectoryUncreated` |
| 84 | `DirectoryUnrenamed` |
| 85 | `TooManyContentData` |
| 86 | `NotEnoughContentData` |
| 87 | `InvalidRequest` |
| 127 | `UnknownError` |

Codes 9, 10 and 11 are the three preconditions named above. Code 52
(`XmlParseError`) is the hint that project metadata is XML.

## File transfer over MIDI (FTOM)

The official app's file-transfer plug-in. Its API, `from the official app, untested`:

```
FTOMPluginPrepareToSendFiles      FTOMPluginPrepareToReceiveFiles
FTOMPluginSendFiles               FTOMPluginRequestFiles
FTOMPluginCancelSendingFiles      FTOMPluginCancelReceivingFiles
FTOMPluginSetFileSendCallback     FTOMPluginSetFileReceiveCallback
FTOMPluginResetFileSendCallback   FTOMPluginResetFileReceiveCallback
```

Every function has a `…ViaWiFi` twin: same protocol, different transport.

Internal classes: `FileTransferBase`, `FileSender`, `FileReceiver` (plus Wi-Fi
variants), `ProjectInfo` (with `_soundNumbers` and `_sampleNumbers`),
`SampleInfo`, and `GDataXMLDocument` / `GDataXMLElement` / `GDataXMLNode`.

**Project metadata travels as XML.** The app's own resources show the shape:
`StreamingAssets/Projects/<uuid>/project.xml` plus `project.bin`, with
`app-system-model.xml` and `stub-sound-database.xml` in the metadata. The
`XmlParseError` result code confirms it. So an exported project is a directory
named by a UUID containing a descriptive XML file and a binary.

For extracting samples, this is the channel to follow: samples go through it,
and `SampleInfo` together with `WaveformInfoSize = 226` describes their
metadata.

## Sending a whole project

`from the official app, untested`. The app can write a complete
project into a slot, and read one back. `SendProject(uuid | directoryPath,
targetIndex, …)` drives it; in order, it:

1. calls `GetSoundAttribute()` and `GetElementAttribute()` — an inventory of
   what the target machine already holds;
2. runs `FileIO.SendingProjectPreprocessor` over a copy in a `Tmp` directory,
   rewriting content numbers inside the project binary to match that inventory;
3. reads `ContentFileManager.GetProjectInfo(...)` for the four counts;
4. calls `MidiPluginInterface.SendProjectFile(number, directoryPath,
   soundCount, elementCount, waveformCount, sampleCount)`.

The reverse exists as `RequestFiles(type, number, parentDirectoryPath,
projectUUID)`.

### Why a host cannot do this today

Step 4 is a pass-through into the app's native file-transfer plug-in, and
**the protocol lives entirely inside it.** The operations that carry it are
`sendContentsDumpHeader`, `sendProjectDataAtPacketIndex:`, `sendSoundData`,
`sendElementData`, `sendWaveformData`, `sendSampleDataAtPacketIndex:`,
`handleSysExMessage:withSize:`, `waitingAcknowledgeAddress`,
`terminateWithResult:contentNumber:`, `checkSendabilityWithDirectoryPath:`,
`restartTimer`, `timedOut:`.

Reimplementing it means rebuilding packet numbering, checksums, the
acknowledgement state machine and the timeouts — and then still needing a valid
project image, whose pattern encoding is undecoded (below).

### What has since been recovered — `from the official app, untested`

That verdict is now partly out of date. The **contents dump header** is fully
decoded, and with it the channel's frame, its addressing, its acknowledgement
and its size accounting.

#### The frame

A content dump is an ordinary **Bulk Dump**, on the same skeleton as the
firmware channel's:

```
F0 43 00 7F 1C bh bl 0C  ah am al  00 01 00 00  <payload…>  cc F7
```

| Field | What it is |
|---|---|
| `bh bl` | the Yamaha byte count, as a 16-bit value in two 7-bit bytes |
| `ah` | **the content kind** — see the table below |
| `am al` | **the content number, 14 bits**: `am = number >> 7`, `al = number & 0x7F` |
| `00 01 00 00` | the same four metadata bytes the firmware channel's block header carries |
| `cc` | checksum, then `F7` |

#### The content kinds — `ah`

Read off the branches on the app's own `FileType` (`Project` 0, `Sound` 1,
`Element` 2, `Waveform` 3):

| `ah` | Content kind |
|---|---|
| `02` | Project |
| `03` | Sound |
| `04` | Element (a sampler element) |
| `05` | Waveform |

Samples have no kind of their own: they travel under a waveform, which is how
a [`.Y3S`](06-sounds-presets.md#the-y3s-content-package--how-a-sound-of-your-own-gets-in)
packages them too.

#### The header's payload

Every field is 7-bit encoded. Offsets are from the start of the message.

| Offset | Size | Contents |
|---|---|---|
| `0x0B` | 4 | `00 01 00 00` |
| `0x0F` | 2 | sound count — **0 when the kind is Sound** |
| `0x11` | 2 | element count — **0 when the kind is Element** |
| `0x13` | 2 | waveform count — **0 when the kind is Waveform** |
| `0x15` | 4 | sample count |
| `0x19` | 4 × *n* | one entry per sample, built by reading each `sample<i>.xml` of the directory and taking its waveform and keybank numbers |

So the kind being sent is excluded from its own count, and the rest declare
what accompanies it.

| Quantity | Value |
|---|---|
| Yamaha byte count (`bh bl`) | `0x12 + 4n` = 18 + 4 × samples |
| Whole message length | **27 + 4 × samples** |

Those two agree only if the byte count runs from the **Model ID through the
last data byte** — which is what [02-sysex-format.md](02-sysex-format.md#bulk-dump)
says and the Data List's wording does not. A third independent confirmation of
that reading.

#### The checksum, read again on this channel

It sums the bytes from index 7 up to `size - 3` inclusive, then returns
`(0x80 - (sum & 0x7F)) & 0x7F`, or `0` when `sum & 0x7F` is zero. Byte for byte
the firmware channel's function ([09-firmware.md](09-firmware.md#checksum)).
The checksum goes at `size - 2` and `F7` at `size - 1`.

#### The acknowledgement

After sending, the plug-in sets the address it waits on to the **21-bit packing
of the address it just sent**:

```
waitingAcknowledgeAddress = (ah << 14) | (am << 7) | al
```

So a content dump is acknowledged at its own address. The receive side also
masks and checks a device number.

#### Size accounting, and a cross-check

The sender adds **1792 bytes per sound** to the transfer's total — exactly the
size of a `.Y3S`'s `sound.bin`, measured independently on a real export. For a
project it adds `0x10D001` (1,101,825) bytes.

#### The 7-bit conversions

| Conversion | Use |
|---|---|
| 16-bit integer ↔ 7-bit array | byte counts, the three content counts |
| 32-bit integer ↔ 7-bit array | sample counts, sizes, positions |
| binary ↔ 7-bit array | file data, with an encoded/decoded byte-count pair giving the ratio |
| string ↔ 7-bit array | names |

#### The bodies have their own addresses

The dump header's `ah` names the **kind being announced**. Each body then
travels at an `ah` of its own, and the two spaces do not overlap:

| `ah` | Body | Sent |
|---|---|---|
| `06` | project data | by packet index |
| `07` | sound data | one message |
| `08` | element data | one message |
| `09` | waveform data | one message |
| `0A` | sample data | by packet index |

For the one-message bodies, `am al` carry the content number as in the header.
For project data `am` is **0** and `al` is the packet index.

#### A body's size is declared, and the three sizes check out

Each one-message body copies a fixed-size file into the message:

| Body | Bytes | What it is, measured independently |
|---|---|---|
| sound | `0x700` = **1792** | the size of a `.Y3S`'s `sound.bin`, measured on a real export |
| element | `0x200` = **512** | the 512-byte `element.bin` of a sampler export, as a third party measured it |
| waveform | `0x84` = **132** | `4 + 64 × 2` — a **stereo** `waveform0.bin`, exactly the layout of [§the keybank record](06-sounds-presets.md#the-rest-of-the-record) |

Three numbers recovered from the app that match three files measured without
it. That is the strongest internal check this section has.

#### Packet cutting

The two packet-index paths carry **`0xBB8` = 3000 raw bytes per packet**. At
the 7-into-8 ratio that is 3429 encoded bytes, which sits inside the
`0xF98` = 3992-byte payload area with room for the header.

#### A body's message layout, taking waveform data as the worked case

| Offset | Size | Contents |
|---|---|---|
| `0x0B` | 4 | `00 01 00 00` |
| `0x0F` | 19 | the content's **UUID**, 16 raw bytes through the binary conversion |
| `0x22` | 4 | a 32-bit value, 7-bit encoded |
| `0x26` | 50 | a name, string-encoded |
| `0x58` | 50 | a second string — the tag |
| `0x8A` | 3 | three single bytes (the category pair and one more) |
| `0x8D` | *n* | the file's bytes, binary-encoded |

Message length is *n* + `0x8F`. Sound data ends at *n* + `0x8E`, element and
waveform data at *n* + `0x8F`.

The 19 bytes for a 16-byte UUID are the 7-into-8 ratio made visible:
⌈128 / 7⌉ = 19.

#### Those fields come straight from the content's XML

The sender parses the kind's `.xml` beside the `.bin` and walks its tags. For a
waveform, `waveform<i>.xml` ([its shape](06-sounds-presets.md#7-xml-files)) maps
onto the message like this:

| XML tag | Where it lands | How sure |
|---|---|---|
| `UUID` | `0x0F`, 16 raw bytes → 19 | **certain** — it is parsed as a UUID and its bytes taken |
| `ContentNumber` | split into the message's own `am al` | **certain** — the value is shifted and masked into the address |
| `Order` | `0x22`, 32-bit encoded | by elimination among the integer tags |
| `Tag1`, `Tag2` | `0x26` and `0x58`, 50 bytes each | by elimination among the string tags |
| `MainCategory` | `0x8A` | by position in the tag chain |
| `SubCategory` | `0x8B` | by position in the tag chain |
| `Commercial` | `0x8C` | **certain** — it is the only tag read as a boolean |

So a host does not invent this metadata: it carries the same fields a `.Y3S`
already ships, and the content number in the body's address is the one written
in the file — not one the host chooses.

#### How a content number becomes `am al` — the exact rule

The sender does not split the number naively. Reading the arithmetic:

```
am = ((contentNumber >> 7) | 0x40) & 0x7F
al =   contentNumber & 0x7F
```

The `| 0x40` is applied **only when the number is below 8192**, but it changes
nothing above it: for 8192 ≤ *n* < 16384 the shift already lands in
`0x40`-`0x7F`. So the one rule above holds throughout, and **bit 6 of `am` is
always set**.

Two consequences a host must know:

- **The address does not distinguish a factory content number from a user
  one.** *n* and *n* + 8192 produce the same `am al` — 100 and 8292 both give
  `am = 0x40`, `al = 0x64`. That is consistent with the `.Y3S`, where an
  element refers to a user waveform as `ContentNumber − 8192`: on the wire the
  number is the index within its space, and which space is carried elsewhere.
- **16384 is a hard ceiling.** At or above it the shift leaves bit 7 set and the
  byte is no longer valid SysEx data. Nothing in the send path checks for it.

This retires a warning an earlier pass left here, which read the nine-bit
extract as a danger: the value always fits seven bits below 16384, and nothing
is narrowed or refused.

#### The acknowledgement addresses

| After sending | It waits on |
|---|---|
| the contents dump header | the address it just sent, packed `(ah << 14) \| (am << 7) \| al` |
| sound data | `(0x07 << 14) \| content number` |
| element data | `(0x08 << 14) \| content number` |
| waveform data | `(0x09 << 14) \| content number` |
| sample data | **`0A 00 00`** flat — not its own content number |

#### The acknowledgement a host must send back

Every message the machine acknowledges carries:

| Offset | Size | Contents |
|---|---|---|
| `0x0B` | 1 | **status** — `0` means go on |
| `0x0C`-`0x0E` | 3 | the `ah am al` being acknowledged |
| `0x0F`-`0x10` | 2 | the **packet index**, 7-bit encoded, on the two packet-index paths |
| `0x11`-`0x12` | 2 | the **content number the machine assigned**, as `(msg[0x11] << 7) | msg[0x12]` |
| `size - 2` | 1 | checksum |

The sender checks three things in order, and each failure is distinct:

| Check | On failure |
|---|---|
| the packed `(ah << 14) \| (am << 7) \| al` equals the address it is waiting on | the message is **ignored silently** — no error, no retry |
| `msg[0x0B]` is zero | terminate with that byte as the result, except that **`1` `Cancel` is reported as `33` `CancelByReceiver`** |
| `msg[size-2]` equals the checksum it computes | terminate with **`7` `PacketLoss`** — *not* `8` `CheckSumError` |

Those last two are worth reading twice against the
[result-code table](#result-codes). A bad checksum is reported as
**`PacketLoss`**, and `CheckSumError` is never what the sender raises for one;
and the machine's bare `Cancel` is translated on the way to the caller, so the
code a host sees is not always the code that travelled.

That split runs through the whole table: the codes **below 32** are conditions
the machine reports on the wire — a full memory, the three mode preconditions —
while **32 and above** are raised locally and never travel. That reading fits
every name but has not been checked against a machine.

#### The timeout is 36 seconds

Each send arms a single timer for that long, invalidating the previous one, and
its expiry is the only thing that ends a stalled transfer. Combined with the
silent drop above: a host that acknowledges on the wrong address waits **36
seconds** and then gets `48` `Timeout`, with nothing to say which of the two
mistakes it made.

That silent drop on an address mismatch matters: a host that answers on the
wrong address does not get an error, it gets a stall until the timeout.

#### The send order, and it is a dependency order

The whole transfer is driven by acknowledgements — one message out, one
acknowledgement in, the next message chosen by **which address was
acknowledged**:

| Acknowledged | What goes out next |
|---|---|
| `02`-`05` (the dump header) | counters reset, then **sample** data, packet 0 |
| `0A` (sample data) | the next packet; when the packets run out, the next sample at packet 0; when the samples run out, **waveform** data |
| `09` (waveform data) | the next waveform; when they run out: for a Waveform transfer **done**, otherwise **element** or **sound** data |
| `08` (element data) | the next element; when they run out: for an Element transfer **done**, otherwise **sound** data |
| `07` (sound data) | the next sound; when they run out: for a Sound transfer **done**, otherwise **project** data, packet 0 |
| `06` (project data) | the next packet; when they run out, **done** |

So the order is **samples → waveforms → elements → sounds → project**: the
audio first, then each thing that references it. A sound cannot arrive before
the waveform it points at, which is the same constraint the `.Y3S`'s own
`ContentNumber − 8192` reference implies.

A transfer ends at the stage matching its own kind. For a Sound or an Element
the sender signals completion with the **content number the machine assigned**,
taken from `0x11`-`0x12` of the last acknowledgement — which is how a host
learns where its sound landed.

#### Pulling content out: the request

This is the direction that matters for getting a sample off the machine, and it
is **not** the `11 mm nn` route of [§Requesting a dump](#requesting-a-dump).
That one asks the parameter zone for a sound's blocks; this one asks the content
channel for the **files** — the XML metadata and the PCM.

The request is a plain 10-byte Bulk Dump Request, with no checksum:

```
F0 43 20 7F 1C 0C  ah am al  F7
```

| Field | Value |
|---|---|
| `ah` | the content kind: `02` Project, `03` Sound, `04` Element, `05` Waveform — the same kinds as the dump header |
| `am al` | the content number, by the [rule above](#how-a-content-number-becomes-am-al--the-exact-rule) |

The requester then waits on `(ah << 14) | (am << 7) | al`, exactly as the
sender does.

#### Pulling content out: the acknowledgement a host must send

Every message the machine sends has to be acknowledged, and the acknowledgement
is a **21-byte bulk message at address `01 21 00`** — not `01 20 00`, which is
the direction the machine answers on:

```
F0 43 00 7F 1C 00 0C  0C 01 21 00  rr  ah am al  e1 e2  00 00  cc F7
```

| Offset | Size | Contents |
|---|---|---|
| `0x00`-`0x06` | 7 | the bulk prefix, with the byte count fixed at **`00 0C`** = 12 |
| `0x07`-`0x0A` | 4 | `0C 01 21 00` — the Model ID and the address |
| `0x0B` | 1 | `rr`, the result code: `0` to ask for the next message |
| `0x0C`-`0x0E` | 3 | the `ah am al` **of the message being acknowledged**, copied from its bytes 8-10 |
| `0x0F`-`0x10` | 2 | two bytes copied from the incoming message's bytes `0x0D`-`0x0E` |
| `0x11`-`0x12` | 2 | zero |
| `0x13`-`0x14` | 2 | checksum, then `F7` |

The byte count of 12 covers the Model ID through `0x12`, which is both what the
checksum sums and what the app's own `InfoAckByteCount = 12` says — three
independent statements of the same number.

Each acknowledgement **re-arms the 36-second timer**, so a host that answers
promptly never sees a timeout, and one that stops answering ends the transfer
by itself.

The receiver also writes the XML back out as it goes, adding string, integer
and boolean elements to a root — so the metadata a host must reconstruct is the
same set the [body layout](#those-fields-come-straight-from-the-contents-xml)
carries.

#### What is still missing

- the per-kind receive handlers' field offsets, which should mirror the send
  side but have not been read;
- the restart behaviour on a timeout, and the full result-code vocabulary
  beyond `0` (go on), `7` (bad checksum) and `0x21`;
- the exact meaning of each body's metadata fields — the 32-bit value at
  `0x22` and the three bytes at `0x8A`;
- the project body's own layout, which is built differently from the other
  four;
- the whole **receiving** direction, for reading content out of the machine.

> Marked `from the official app, untested` throughout: none of this has been
> sent to a machine. The audio path in particular has never been exercised, and
> a wrong byte count or checksum on a content write is not a harmless mistake.

## What a project looks like on disk

The app ships **three complete demo projects** under
`Contents/Resources/Data/StreamingAssets/Projects/<uuid>/`, each a `project.xml`
and a `project.bin`. That is a real sample of the format, analysable without
hardware.

### `project.xml`

```xml
<ProjectData>
  <UUID>…</UUID> <Order>17</Order> <Tag1/> <Tag2/> <Commercial>false</Commercial>
  <Part01SoundNumber>33</Part01SoundNumber> … <Part11SoundNumber>0</Part11SoundNumber>
  <Element1SampleNumber>242</Element1SampleNumber> … <Element8SampleNumber>0</Element8SampleNumber>
  <Name>Yamaha Demo Project 3</Name>
  <CompatibleVersion>1</CompatibleVersion>
  <CreatedDate>2024-01-16T00:00:00</CreatedDate>
</ProjectData>
```

Eleven parts, eight elements. These are the numbers
`SendingProjectPreprocessor` rewrites to match the target machine's content
inventory.

### `project.bin` — structure observed, meaning not

Measured across the three demo images:

| Observation | Value |
|---|---|
| Size | **1 101 825 bytes**, identical for all three |
| Filler byte | `0xFF` (1 020 543 of 1 101 825 bytes) — a flash image, not a packed format |
| Byte-identical between the three | 97.5 % |
| Record stride | **16 384 bytes** (`0x4000`), boundaries at `0x1000 + k × 0x4000` |
| Data per record | up to ~9 216 bytes, then `0xFF` filler |
| Record count | 67, plus one trailing byte |
| First 4 096 bytes | header; the project name in 7-into-8 packing starts at offset 4 (`00 00 00 A8 \| 00 "Yamaha " \| 00 "Demo Pr" …`), consistent with `HeaderSize = 4` and `ProjectNameSize = 88` |

The arithmetic suggests 66 of the 67 records are 11 tracks × 6 patterns and the
67th is the song data. **That is a guess from the record count alone and should
not be relied on.** The note encoding inside a record has not been decoded.

The constants the app itself knows about the format
(`FileIO.SendingProjectPreprocessor`) cover only the head of the image:
`HeaderSize = 4`, `PerformanceCommonDataSize = 581`, `AllPartsDataSize = 2851`,
`PART_DATA_SIZE = 245`, `AwmSoundDataSize = 1477`, `SoundDataSize = 341`,
`AwmElementDataSize = 141`, `FmSoundDataSize = 483`, `NUMBER_OF_ELEMENTS = 7`,
`PERFORMANCE_DATA_INDEX_SCALE1 = 606`, `PAD_OFFSET = 4`, `SCALE_OFFSET = 28`,
`MIDI_NOTE_NUMBER_C1 = 36`. **The app never touches pattern data** — it only
remaps sound and sample numbers.

Anyone who wants to decode the pattern encoding has a good starting point:
three reference images on disk, and a differential method (write one known note
with step record, pull the project back with `RequestFiles`, diff). That needs
hardware and is a project of its own.

## The app's cloud, for completeness

The official app embeds AWS Cognito and S3, plus the NHN **Gpm** SDK, for the
content catalogue and firmware downloads. No firmware URL appears in clear text
in the app — it is built at run time. None of this touches
communication with the machine. `from the official app, untested`.
