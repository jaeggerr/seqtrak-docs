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

**For writing a composition, use step record instead**:
[14-song-mode.md](14-song-mode.md#5-writing-a-whole-song-the-practical-route).

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
