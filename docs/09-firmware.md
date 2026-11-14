# 09 — Firmware update protocol, and custom firmware

The complete update channel, and an honest assessment of whether a custom
firmware is reachable.

Two independent bodies of evidence are in play here, and they are marked
differently:

- the **update protocol** comes from the official app, so
  `from the official app, untested` — except the Identity Reply and
  what [the `0x64` probes](#what-the-hardware-has-actually-said-about-0x64)
  established, which are `verified on hardware`;
- the **update file** comes from the official OS 2.00 image, so
  `from firmware image (static analysis)`. Those facts were checked byte for
  byte against the artefact and are reproducible, but they say nothing about
  runtime behaviour.

In the official app, the firmware protocol lives in a native plug-in (classes
`FirmwareUpdater` / `MidiFirmwareUpdater` / `WiFiFirmwareUpdater`).

## Entry points on the app side

```csharp
StartUpdatingViaMidi(string filePath, int blocks, UpdateInfoDelegate callback)
StartUpdatingViaWiFi(string filePath, int blocks, string ipAddress,
                     int portNumber, int wifiMode, UpdateInfoDelegate callback)
CancelUpdating()
ResumeUpdating()
```

`blocks` is a bitmask of `BlockType`:

| Bit | Block |
|---|---|
| `1` | Boot |
| `2` | Program |
| `4` | Wave |

So the app can push only part of an image. There is also a `skipBlock:`, so a
block can be skipped mid-transfer.

> **The bitmask does not describe the file.** The OS 2.00 update file contains
> only **two** blocks, `Installer` and `Program` — there is no block named
> `Boot` and none named `Wave`, and the waveform data lives *inside* the
> `Program` image. `from firmware image (static analysis)`. So for that update
> the state machine's Boot and Wave stages have nothing to push, which is
> plausibly what `skipBlock:` is for — an inference, not an observed app
> behaviour. See [the file format](#the-update-file-os-200).

## The frame

Firmware update uses **address-high `0x64`** inside the ordinary SysEx space. It
is not a separate protocol.

```
F0 43 10 7F 1C 0C 64 <category> <command> [data] F7
```

In Parameter Change terms: `ah = 64`, `am = category`, `al = command`. The total
length is 10 plus the data size, and the app only ever sends 0 or 1 data bytes.

### Checksum

`checkSumValueFromMessage:size:` sums the bytes at indices **7 to size-3**
inclusive, then returns `(0x80 - (sum & 0x7F)) & 0x7F`, or `0` when
`sum & 0x7F == 0`. That is the ordinary Yamaha checksum applied from the Model
ID to the last data byte — the same range this repository verified against a
captured message in
[02-sysex-format.md](02-sysex-format.md#bulk-dump).

## Detecting the device

A standard Universal Identity Request / Reply. The plug-in's
`isIdentityReply:length:correctness:` requires a reply of exactly **15 bytes**:

```
F0 7E 7F 06 02 43 00 41 64 06 mm 00 00 7F F7
```

- byte 11 must be `00`
- bytes 13-14 must be `7F F7`
- `64 06` is the SEQTRAK's device family / code
- `mm = (version − 1.0) × 10`

A real unit answered `F0 7E 7F 06 02 43 00 41 64 06 0A 00 00 7F F7`, so
`mm = 0x0A` → version 2.0, matching the OS V2.00 it was running.
`verified on hardware`. The pattern derived from the official app is exact.

The same function also accepts a proprietary reply of the form
`F0 43 10 7F 1C 0C … F7`, at least 10 bytes long, which is what the device sends
once it is already in loader mode.

## Device-to-host messages

From the dispatcher `handleSysExMessage:withSize:`:

| Address | Meaning | Handler |
|---|---|---|
| `64 00 02` | mode reply, 1 data byte | `handleModeReply:` |
| `64 00 07` | reboot reply, 1 data byte | `handleRebootReply:` |
| `64 01 00` | request for the next packet (flow control) | `handlePacketRequest` |
| `64 01 03` | block-creation confirmation | `handleCreateConfirm` |
| `64 01 05` | terminate with error → `ErrorFromHardware` (13) | `terminateWithResult:` |
| `64 02 00` | block acknowledgement | advance to the next header |

## The data: bulk dumps

Blocks go out as **Bulk Dumps**, not Parameter Changes. The common header, read
from the plug-in's literal pool:

```
F0 43 00 7F 1C bh bl 0C 64 02 al … cc F7
```

| `al` | Contents |
|---|---|
| `01` | **block header**: 4 metadata bytes (`00 01 00 00`) then the payload |
| `02` | **block data**: a 14-bit packet number then the payload |

`bh bl` is the byte count from the Model ID to the last data byte; the message
ends with the checksum and `F7`. A block message is `payload + 17` bytes total.

### How a block is cut into packets

`from the official app, untested`, read out of
`MidiFirmwareUpdater`'s own implementations — `FirmwareUpdater` is an abstract
base class whose `sendingDataSize` and `updateTotalPacketCount` are assertion
stubs, so the base class tells you nothing.

**A block is sent with one header, then packets, then one create request.**
The 256 KiB window only governs packet sizing and numbering. Corrected
2026-11-14: this section used to call each window a create cycle with its own
header, and a sender built on that reading failed on hardware
([below](#there-is-no-sendingstart-command)). `-[MidiFirmwareUpdater sendingDataSize]`:

```
and  w20, w0, #0xfffc0000      ; sent, rounded down to a multiple of 0x40000
sub  w8, w20, w0
add  w8, w8, #0x40, lsl #12    ; w8 = 0x40000 - (sent mod 0x40000)
mov  w9, #0xdac                ; 3500
cmp  w8, #0xdac
csel w20, w8, w9, lo           ; min(rest of the window, 3500)
                               ; then clamped again to total - sent
```

So each packet carries **at most 3500 bytes of image**, and a packet never
crosses a 256 KiB boundary. `-[MidiFirmwareUpdater updateTotalPacketCount]`
agrees from the other side: while more than 256 KiB remains it returns a
literal `75` (`mov w2, #0x4b`), and for the last window
`ceil(remaining / 3500.0)`, the divisor being the double `3500.0` at `0x9db8`.

| | |
|---|---|
| Window: packet numbers restart at each boundary | `0x40000` = 262,144 bytes |
| Image bytes per packet | ≤ **3500** |
| Packets in a full window | 74 × 3500 + 1 × 3144 = **75** |
| SysEx data bytes per full packet | 3500 × 8/7 = **4000** exactly |
| Full packet message length | 4000 + 17 = **4017** bytes |

That 4000 is the design constraint, and it is what makes the 3500 look
arbitrary until you apply the 7-into-8 packing described in
[02-sysex-format.md](02-sysex-format.md#dividable-bulk-split-transfers).

Applied to the OS 2.00 file:

| Block | Payload in the file | Headers | Windows | Packets | Create requests |
|---|---|---|---|---|---|
| `Installer` | 1,048,576 | 1 | 4 | 300 | 1 |
| `Program` | 10,780,511 | 1 | 42 | 3,085 | 1 |

Packet numbers therefore run `0`-`74` inside a window, which is why the
receiver can hold its expected number in a single byte, and why the 14-bit
packet-count field is never strained. **The earlier reading of this document —
"payloads of 128 bytes (`mov w0, #0x80`)" — was wrong**: that `0x80` is the
128-byte block header size. A 128-byte data payload would have made the
`Program` block need about 96,000 packets, which neither field can express,
and that contradiction is what sent anyone looking here in the first place.

This is exactly the "dividable bulk" format from
[02-sysex-format.md](02-sysex-format.md#dividable-bulk-split-transfers): packet
count and packet number at offset 11, data from offset 15.

## The state machine

`UpdateState` has 35 states and reveals that an update runs in **four
successive stages, each with its own reboot**:

```
Idling
└─ CheckingIdentityAtBegining            identity request in normal mode
└─ RebootingAsLoader                     reboot into the loader
   WaitingForConnectionForLoader
   WaitingForStabilizationForLoader
   CheckingIdentityAsLoader
   ChangingModeForLoader
└─ INSTALLER   SendingStartForInstaller → SendingInstallerHeader
               → SendingInstallerData → WaitingForCreateConfirmForInstaller
└─ RebootingAsUpdater                    reboot into the freshly written updater
   WaitingForConnectionForUpdater
   CheckingIdentityAsUpdater
   ChangingModeForUpdater
└─ BOOT        SendingStartForBoot → SendingBootHeader
               → SendingBootData → WaitingForCreateConfirmForBoot
└─ PROGRAM     SendingStartForProgram → SendingProgramHeader
               → SendingProgramData → WaitingForRequestForProgram
               → WaitingForCreateConfirmForProgram
└─ WAVE        SendingStartForWave → SendingWaveHeader
               → SendingWaveData → WaitingForRequestForWave
               → WaitingForCreateConfirmForWave
└─ RebootingAsNormal
   WaitingForConnectionForNormal
   CheckingIdentityAsNormal
   End
```

**The notable part**: the first thing the host sends is not firmware, it is an
**installer**, which the loader writes and then executes after a reboot. That
installer is what receives Boot, Program and Wave. The logic that validates and
writes the image is itself delivered by the update.

## Result codes

`UpdateResult`:

| Code | Meaning |
|---|---|
| 0 | `Success` |
| 1 | `AlreadyUpdating` |
| 2 | `FileNotFound` |
| 3 | `DisconnectedPort` |
| 4 | `SetupFailure` |
| 5 | `ReceivingFailure` |
| 6 | `SendingFailure` |
| 7 | `Timeout` |
| 8 | `DeviceNotFound` |
| 9 | `InvalidData` |
| 10 | `UnknownError` |
| 11 | `CancelByApp` |
| 12 | `CancelByHardware` |
| 13 | `ErrorFromHardware` |
| 14 | `RebootFailure` |

`InvalidData` is checked **app-side** (a malformed file); `ErrorFromHardware`
comes from the machine via `64 01 05`.

## The update file (OS 2.00)

Everything in this section is `from firmware image (static analysis)`: derived
from the official `8Z33OS_.PGM` for OS 2.00 (11,829,343 bytes, sha256
`1a87fb5a…13bcf63`) by static analysis only. Nothing was executed and no machine
was touched. Values described as reproduced were checked byte for byte and can
be replayed with the tools in the sibling `seqtrak-firmware-analysis` project;
interpretations are marked *inferred*.

### Container

Two blocks concatenated, with no global index. Each is a 128-byte header
followed by its payload, and the next block starts immediately after.

```
offset       size          contents
0x00000000   128           "Installer" block header
0x00000080   0x00100000    Installer payload: raw ARM image, loaded at 0x10000000
0x00100080   128           "Program" block header
0x00100100   0x00a47f5f    Program payload: u32 big-endian length + LZSS stream
                           -> 0x03fc0000 (63.75 MiB) flat image, loaded at 0x20040000
0x00b4805f   -             end of file, no trailing bytes
```

`128 + 0x100000 + 128 + 0xa47f5f` is exactly the file size, so the block chain
accounts for the whole file: there is no hidden block and no trailing field.

### Block header, 128 bytes

| Offset | Size | Type | `Installer` | `Program` | Meaning |
|---|---|---|---|---|---|
| `+0x00` | 24 | ASCII, NUL | `Installer` | `Program` | block name |
| `+0x18` | 40 | ASCII, NUL | `2.00.2` | `2.00.2` | version |
| `+0x40` | 4 | u32 LE | `0x0C1566FF` | `0x592A6F35` | **additive sum** |
| `+0x44` | 28 | ASCII, NUL | ` (C)2021 YAMAHA ` | same | copyright |
| `+0x60` | 14 | — | zeros | zeros | reserved |
| `+0x6E` | 2 | u16 LE | `0xFFFF` | `0x0001` | block index — *inferred* |
| `+0x70` | 4 | u32 LE | `0` | `0` | reserved |
| `+0x74` | 2 | u16 LE | `0x0000` | `0x0055` | compression flag — *inferred* |
| `+0x76` | 2 | u16 LE | `0x0055` | `0x0055` | validity flag — *inferred* |
| `+0x78` | 4 | u32 LE | `0x10000000` | `0x20040000` | load address |
| `+0x7C` | 4 | u32 LE | `0x00100000` | `0x00A47F5F` | payload length **in the file** |

`+0x7C` is the length *in the file*, so the compressed size for `Program`. The
decompressed size is stored nowhere in the header; it is implicit in the stream.

The three *inferred* fields are inferred because two blocks are not enough to
tell a flag from a coincidence. `+0x74` is the strongest of them: it is `0x55`
for the one compressed block and `0` for the one raw block.

### Integrity: a single additive sum per block

The `+0x40` field is **the arithmetic sum of the payload bytes**, truncated to
32 bits. Both were reproduced exactly:

| Block | Field at `+0x40` | Sum of |
|---|---|---|
| `Installer` | `0x0C1566FF` | its 1,048,576 payload bytes |
| `Program` | `0x592A6F35` | its 66,846,720 **decompressed** bytes |

The field was tested against byte sum, u16 LE sum, u32 LE sum, u32 LE XOR,
CRC-32, complemented CRC-32 and Adler-32, each over the payload alone, over
header + payload, and over the header with the field zeroed. **Only the byte sum
matches**, and it matches both blocks.

An additive sum has no cryptographic property: anyone can recompute it after
modifying the image.

### Compression

The `Program` payload is **Okumura-style LZSS**, fully reconstructed and
verified. The payload begins with a u32 **big-endian** length for the stream
that follows; the stream is a sequence of a flag byte followed by eight tokens.

### What is in the blocks

**`Installer`** — 1 MiB, uncompressed, in the clear, mean entropy 2.287
bits/byte. An 8-entry ARM exception vector table at `+0x00`, a literal pool at
`+0x20`, an identification area at `+0x200` reading
`" Boot Program #8Z33 Copyright(C) 2021 Yamaha Corporation."`, a reset handler at
`+0x280`, then mostly GCC-compiled Thumb-2 with libstdc++ (exceptions, RTTI,
demangler), the **eForce** RTOS, a NAND driver and a FAT12 stack.

That identification string is the origin of a mistake worth recording: the
`Boot` and `Wave` strings in this file are **code strings inside the Installer**,
not block headers. Reading a cluster of neighbouring strings as a table of
contents is what produced the four-block model this document used to carry.

**`Program`** — a 63.75 MiB flat image at `0x20040000`, in the clear. The first
1024 bytes are a plaintext prologue: 128 bytes of copyright, then a **section
table** of 14 sixteen-byte records, then `0xFF` padding, then the ARM vector
table and code at `+0x400`.

Section record layout: `u8` id, `u8` flag (always `0x01`), 6 zero bytes,
`u32` LE address, `u32` LE length. The first eight records **tile
`0x20000000`-`0x24000000` exactly** — 64 MiB, each address being the previous
one plus its length, with the 1024-byte prologue as the only hole — which is
what makes the interpretation more than a guess.

| # | id | Address | Length | Contents |
|---|---|---|---|---|
| 0 | `0x04` | `0x20000000` | 256 KiB | reserved window, absent from the image — *inferred* |
| 1 | `0x05` | `0x20040400` | 15.75 MiB | **code**: ARM then Thumb-2 |
| 2 | `0x11` | `0x21000000` | 7.94 MiB | **factory sample data** — *inferred* |
| 3 | `0x18` | `0x217F0000` | 16 KiB | data |
| 4 | `0x19` | `0x217F4000` | 4 KiB | data |
| 5 | `0x1A` | `0x217F5000` | 44 KiB | data |
| 6 | `0x20` | `0x21800000` | 20 MiB | preformatted storage area |
| 7 | `0x21` | `0x22C00000` | 20 MiB | the same, a near-identical copy |

Six further records form a second, non-contiguous list whose role is not
established.

Only **19.00 MiB** of the 63.75 MiB holds anything other than pure `0x00` or
`0xFF`. The two 20 MiB areas are nearly empty and differ in just **36 bytes out
of 20,971,520** — section `0x20` starts with the magic `DE AD FA CE` and ends
with a boot record containing the ASCII `170055`, while `0x21` starts and ends
erased. That is the signature of an A/B pair with only the first initialised at
the factory (*inferred*).

### Strings in the `Program` image are reached through a RAM alias

`from firmware image (static analysis)`. **This section used to say the
opposite**: that the `Program`'s strings could not be cross-referenced at any
base address. That was wrong, and the reason is worth more than the
correction. The idea came from a third-party analysis (see
[below](#the-program-image-from-inside-a-third-party-analysis-2026-11)), and
the measurements here were re-run on this repository's own copy of the image.

**Most of the code does not run where it sits in the image.** The reset
handler calls a RAM-init routine at `0x2004091C`. It makes five calls to a copy
routine at `0x200407D4` (source, destination, destination end) and one call
to a zero-fill at `0x200407E0`. Read as `movw`/`movt` pairs:

| Source (image VA) | Destination | Destination end | What it is |
|---|---|---|---|
| `0x20040400` | `0x00000000` | `0x000002F8` | vectors |
| `0x20060400` | `0x000002F8` | `0x0001EBF0` | low RAM |
| `0x20080400` | `0x00020000` | `0x00028038` | low RAM |
| *zero-fill* | `0x11000000` | `0x11B607C0` | `.bss`, about 11.4 MiB, no source in the image |
| `0x2068DEF8` | `0x105FDAF8` | `0x10613B60` | data |
| `0x20090400` | `0x10000000` | `0x105FDAF8` | **code and data, about 6 MiB** |

The last two are contiguous at both ends, so one mapping covers
`0x10000000`-`0x10613B60`:

```
image VA    = RAM - 0x10000000 + 0x20090400
file offset = RAM - 0x10000000 + 0x50400     (offset in the decompressed image)
```

Code in this range is called, and points at its strings, **at its RAM
address**. The measurement that proves it: of the **8,827** NUL-terminated
strings of 6 or more printable characters in the mirrored range, **8,001
(90.6 %)** have their RAM address stored as an aligned little-endian word
somewhere in the image. Only **3** have their image address stored that way.

**Why the old sweep missed it.** The sweep tried every 1 MiB-aligned base. As
a base for the whole image, this alias is `0x10000000 - 0x50400 =
0x0FFAFC00`, which is not 1 MiB-aligned, so the sweep never tried it. And it
only holds for one region of the image, not for all of it. The sweep was
measuring correctly; it was asking the wrong question. The `Installer` control
worked because the `Installer` really is flat.

**Practical consequence.** In Ghidra, add a byte-mapped block named
`RAM_MIRROR` at `0x10000000`, length `0x613B60`, mapped from `0x20090400`.
Strings, jump tables and vtables then resolve. **To patch code seen at a RAM
address `R`, edit the image at `R - 0x10000000 + 0x20090400`**: the RAM copy
is made at boot.

A second trap, also from the third-party analysis and consistent with what
was read here: the image **mixes ARM and Thumb-2 by address region**. A caller
search run in the wrong mode finds nothing, and then "zero callers" means
nothing.

### Architecture and SoC

**ARMv7, R profile, 32-bit, little-endian.** Both blocks open with the characteristic
8-entry ARM exception vector table built from `ldr pc, [pc, #0x18]`
instructions — a Cortex-M would use a table of addresses, not instructions,
which rules out the M profile.

Corrected 2026-11-14: this section used to say ARMv7-**A**. The `Program`'s
start-up code programs a **memory protection unit**, which only the R profile
has: it reads `MPUIR` (`mrc p15, 0, r1, c0, c0, 4`), writes the region
registers `c6, c2, 0` / `c6, c1, 0` / `c6, c1, 2` / `c6, c1, 4` in a loop at
`0x20040A00`, and sets `SCTLR.BR` (bit 17, the background region). No
translation-table write (`c2, c0`) exists. `from firmware image (static analysis)`.
The core is therefore a Cortex-R class part (*inferred* which one).

| MPU region (table at `0x200407F8`) | Base | Size | Access | Cache |
|---|---|---|---|---|
| 0 | `0x10000000` | 128 MiB | AP=3, full read/write, executable | write-back |
| 1 | `0x16C00000` | 4 MiB | AP=3 | TEX=1, uncached normal |
| 2 | `0x17000000` | 16 MiB | AP=3 | TEX=1, uncached normal |
| 3 | `0x20000000` | 64 MiB | **AP=6, read-only** | write-back |
| 4 | `0x22C00000` | 4 MiB | AP=3 | strongly ordered |
| 5 | `0x23000000` | 16 MiB | AP=3 | strongly ordered |
| 6 | `0x80000000` | 2 GiB | AP=3 | strongly ordered |

Region 0 holds the RAM copy the code runs from (the `0x10000000` alias), and it
is writable. That is what lets a patch keep a data word inside its own code
cave. Region 3, the image at its load address, is read-only.

Build paths survive in both blocks:

```
/home/ngs/workspace/mode-b_fullbuild/build_dir/mode-b/de-21mode-b-tg/src/...
/home/ngs/workspace/mode-b_fullbuild/build_dir/mode-b/swx09-platform/platform/...
```

- **`swx09-platform`** — the SoC is a **Yamaha SWX09**, from their in-house
  audio silicon family. *Inferred*, but a named platform path is a strong
  indicator, and it is the first concrete fact about the silicon: this document
  previously said there was no hint of it anywhere.
- **`eForce Co., Ltd.`** in the Installer — the Japanese vendor of the
  μC3/μITRON RTOS and the μNet stack. *Inferred* as to which product.
- Subtrees present: `src/ndd` (NAND driver: ONFI, ECC, bad blocks, wear
  levelling), `src/sytg` (tone generator: `player`, `tone_generator`,
  `transporter`), `src/uef`, `src/vtg`, `src/rtg`, `src/wad`,
  `platform/emidos/driver/fmdc` (flash driver), `platform/bluetooth`,
  `test/swx09`.
- **The `Program` carries a FAT file system that knows FAT32.** In the code
  section, the boot-sector templates of a file system calling itself
  `EMI-DOS` appear from image address `0x20687032`, with the type strings
  `FAT12` (13 occurrences), `FAT16` (7) and `FAT32` (2, first at
  `0x206880AC`). `from firmware image (static analysis)`. The strings prove
  the code exists, not that the running OS mounts a USB stick with it: no
  mass-storage or SCSI string was found next to it. That matters for a
  third-party report of custom firmware loaded at boot from a FAT32 stick.

### The version string decodes `FirmwareVersion`

The plaintext `2.00.2` at `+0x18` corresponds exactly to the four bytes
`02 00 00 02` that the machine returns for `FirmwareVersion` at `01 00 00`
(`verified on hardware`). So that parameter is a **version triple plus a build
number**: `2`, `00`, `0`, `2` → "2.00.2". The correspondence is reproduced; the
reading of the third byte is *inferred*, since it is `0` in both blocks here and
therefore unconstrained.

## The `Program` image from inside: a third-party analysis (2026-11)

An independent analyst — `giddycadet` on Reddit, `rexendevar` on GitHub, the same person according to the owner of this repository — published a working notebook at
<https://justpaste.it/g3gtl> ("SEQTRAK Firmware Notes", session 4). They went
further than this repository: they **flashed a modified `Program` and the
machine accepted it**. Their goal is a tap-tempo patch, and no patch code had
been written when the notes were published. It has since been written and
reported working: see
[the SLOPTRAK follow-up](#follow-up-a-working-code-patch-published-as-sloptrak-2026-11-13).

**Read the markers in this section carefully. They are the point.**

- *Reported by a third party, not reproduced here* is a claim about **their**
  unit, in their words. None of the four markers can carry it, so none is
  used. In particular, nothing here is `verified on hardware`.
- `from firmware image (static analysis)` marks what was **re-checked**
  against this repository's copy of the OS 2.00 image (sha256 `1a87fb5a…13bcf63`),
  independently of their tooling.
- **Rule 2 applies.** Their notes cite this repository for the load address,
  the SoC and the absence of a signature. Where they agree with us on those
  points, it may be inheritance, not corroboration. What they found that we
  did not have — the flash result, the RAM alias, the parameter table and the
  BPM handler — is their own.

### What they report on hardware

| Claim | Status here |
|---|---|
| A `Program` image patched by two bytes, re-compressed and repacked into a `.PGM`, **was accepted and booted**. The USB product name changed from `SEQTRAK` to `SEQTRAX` | reported by a third party, not reproduced here |
| The update went through the **USB-stick** route, not SysEx | reported; *inferred* from their description of the Installer reading the file through FAT12 |
| The same image with a **stale** `+0x40` sum was **rejected** (red LED about 2 s after the first progress LEDs lit). With the sum written **big-endian**, it was rejected the same way. Written little-endian, it was accepted | reported by a third party, not reproduced here |
| The USB `iProduct` string comes from image address `0x203ED400`. A second `SEQTRAK_` at `0x2068DF84` is not it | reported. The bytes `SEQTRAK\0` at `0x203ED400` are `from firmware image (static analysis)` |
| Pressing `[BPM−]` emits a Tempo Parameter Change at `30 40 76`, one step per press | reported. It matches [10-verified-behaviour.md](10-verified-behaviour.md) |
| `[REC]` emits `01 10 21` `RecordingStatus`: `01` on press, `00` on release, one message per edge | reported by a third party, not reproduced here. This repository has the address only `from the official app, untested` |
| The USB descriptor carries a **second configuration**: four vendor-specific (`0xFF`) interfaces that reuse the MIDI bulk endpoints | reported by a third party, not reproduced here |

**What the flash result changes.** It is one report from one unit, and it has
not been reproduced. If it holds, it answers the question this document kept
open: the machine accepts a modified `Program` image, with **no signature**,
through the stick route. It does not touch the resident loader: they modified
the `Program` only and kept the official `Installer`. So "does the loader
check the `Installer`'s signature" stays open, and for a `Program`-only patch
it no longer matters.

### What was re-checked against the image

`from firmware image (static analysis)`, each read in ARM mode:

| Item | Address | What the image shows |
|---|---|---|
| RAM-init routine | `0x2004091C` | the copy table above, six calls, exactly as they list it |
| Exception vectors | `0x20040400` | `ldr pc, [pc, #0x18]`; the sixth slot is a `nop` |
| Installer checksum | `0x10001FD4` | adds up every byte of each chunk, then compares the total with header `+0x40` and returns **`2`** on mismatch. See [the correction below](#what-the-installers-receive-path-actually-checks) |
| Installer per-type table | `0x1006D570` | six pointers. Type `1` points to `0x1006476C`: name `Main`, then `0x1000211C` (the `#8Z33` check, then the sum) and `0x1000203C` |
| `#8Z33` check | `0x1000211C` | `memcmp(ctx+8, 0x10064780, 5)` → returns **`9`** on mismatch |
| Parameter index table, built at boot | writer `0x20194B4C`, table RAM `0x11128DB0` | 4-byte rows `{ah, am, al, size}`, 1,160 bytes stored. **Row `0x29` = `30 40 76`, size 2: Tempo.** It was recovered here by tracking the `mov`/`strb` immediates, not by emulation |
| Neighbours of Tempo | rows `0x27`, `0x28`, `0x2A`, `0x2B` | `30 40 7A`/2, `30 40 7C`/2, `30 40 7F`/1, `30 40 7E`/1 |
| `set_param` | `0x200A8C50` | `cmp r1, #0xE9; bxhi lr; b 0x200A870C`: a thunk that ignores indices above `0xE9` |
| BPM step (`bump`) | `0x200BCBA4` | reads the current BPM at `this+0x40`, clamps to min `+0x46` and max `+0x44`, and if it changed calls `set_param(this->mgr, 0x29, new)` at `0x200BCBE8` |

### What they report from static analysis, not re-checked here

Each item is theirs, *inferred* or better in their own grading, and not
re-checked against the image here.

- **The tempo path** from the front panel: listener `0x200BCE24` →
  `on_button` `0x200BCCC0` → 1000 ms hold timer, then 50 ms auto-repeat →
  `bump` → `set_param`. Pressing both BPM buttons together restores a saved
  value kept at `+0x48`.
- **Control offsets** in the panel object: `page` `+0x450`, `bpm+` `+0x658`,
  `bpm-` `+0x680`, `master` `+0x180`. The seven synth pads are an array of
  `0x28`-byte controls. A held-state query sits at `0x200B1CF8`.
- **Inbound SysEx**: the router is `0x20135F84` and the engine parser is
  `0x20147F0C`. The parser does **not** consume Tempo (`am = 0x40` maps to
  `0xFF`), and where an incoming Tempo is acted on is still unknown.
- **Open, by their own account**: whether `set_param` changes the sequencer's
  tempo or only broadcasts it. Their cheapest next step is a hardware test of
  exactly that.
- The preset table at image offset `0xFBFFFF`, 2032 records of `0x700` bytes,
  the `sound.bin` layout of a `.Y3S` with one extra leading byte. The wave
  table at `0x3E8B20`, 64-byte records, sample rate as a u32 at `+0x28`.

### Where they and this repository disagree

| Point | This repository | Them | Settled by |
|---|---|---|---|
| Does the Installer check `+0x40`? | said **no**, from the SysEx receive path | **yes**, from the stick path, and refused twice on hardware | the image: it is checked at `0x10001FD4`. **We were wrong**; corrected below |
| `Program` strings and cross-references | said unreachable | reached through the RAM alias | the image: 8,001 / 8,827. **We were wrong**; corrected above |
| Does the Installer code run as Thumb-2? | "mostly Thumb-2" | ARM32 | partly. Every Installer routine read for this section decodes cleanly as ARM. The claim about the whole block was not re-measured |
| LZSS re-encoding | not byte-identical to Yamaha's | their C encoder is **byte-identical** | not checked. If they are right, it is a better encoder than ours. Either way the receiver decompresses, so it does not matter |

### Follow-up: a working code patch, published as SLOPTRAK (2026-11-13)

The same analyst later published their notes and a builder as a repository,
<https://github.com/rexendevar/SLOPTRAK>. It goes one step past the
`SEQTRAX` test: a **code patch** — new ARM routines hooked into the OS — that
adds tap tempo, and which they report **working on their unit**. That is the
first report of custom behaviour, not just a changed string, running on a
SEQTRAK.

The same marker rules as above apply. Rule 2 still applies too: their
documentation cites this repository as a layout model, and agreement on the
container is not independent.

#### What they report

| Claim | Status here |
|---|---|
| A `.PGM` carrying the tap-tempo code patch was accepted, booted, and the tap gesture sets the tempo | reported by a third party, not reproduced here |
| Calling `bump` (`0x200BCBA4`), and through it `set_param(mgr, 0x29, bpm)`, changes the **audible** tempo, not only the broadcast | reported; they grade it *inferred* (it is the path the physical BPM buttons run). It closes the question listed as open above |
| The stick route is the official one: format with `[DX]` + `[UNDO/REDO]` at power-on, `8Z33OS_.PGM` at the root, then `[KICK]` + `[BAR LENGTH]` at power-on. Top knob row flashes green, bottom row shows progress, an all-red column means refused | reported. The two gestures match [15-front-panel.md](15-front-panel.md) (Owner's Manual §17.1) |
| The UI manager's `update` runs every **10 ms** (`mgr[2] = 10`), which is the only clock they found fine enough to timestamp taps. No free-running tick getter was found | reported, *inferred* by them |
| There is **no zero padding** usable as a code cave inside the code range `0x20090400`–`0x203C8000` | reported, not re-measured here |

#### The patch technique, re-checked against the image

`from firmware image (static analysis)`, against this repository's copy of the
OS 2.00 image, read in ARM mode. This is the reusable part: it is how
any future code patch can be built.

| Piece | Address (image VA) | What the image shows |
|---|---|---|
| Hook: manager `update` (10 ms) | `0x200A7DF0` | first word `push {r4, lr}`, as their builder expects |
| Hook: `[PAGE]` handler | `0x200D890C` | first word `push {r4-r7, lr}` |
| Hook: BPM `on_button` | `0x200BCCC0` | first word `cmp r1, #0` |
| Hook: synth-pad handler `on_pad` | `0x200D6DC8` | first word `cmp r1, #6` (seven pads, `k = 0…6`) |
| Patch state storage | `0x200A7844`, in the manager factory `0x200A783C` | `movw r0, #0xA3C` then `blx` malloc. They enlarge it to `0xA80` and keep 64 bytes of patch state in the new tail, zero-filled lazily behind a magic word since malloc does not clear |
| Code cave | manager destructor D1, `0x200AD5D8`–`0x200ADE47` (2,160 bytes) | referenced only by one vtable slot (`0x203C7710`, holding the RAM-alias address `0x1001D1D8`) and by the sibling destructor D0's `bl` at `0x200ADE50`. A full scan of the RAM-alias code range found no other branch into it (one apparent hit, at `0x2067AA3C`, decodes as a table of descending 16-bit values, not code). They overwrite D1's first word with `bx lr` and put their code after it |

Two conventions their builder depends on, both consistent with the RAM alias
documented above:

- New code is **assembled at its RAM-alias address**
  (`ROM − 0x20090400 + 0x10000000`) and written at the ROM address, because
  that is where it runs.
- Each hook replaces the function's first instruction with a `b` to the cave;
  the cave routine saves `r0-r12, lr`, does its work, restores, replays the
  displaced instruction and branches back to the original function plus 4. The
  original behaviour is kept: pads still sound, BPM still steps.

What this does **not** cover: they report 35 checks run in an emulator
(Unicorn) on the patched routines and one working unit. Nothing here was
flashed, and the D1 cave is only safe as long as the manager is never
destroyed — which they argue (it lives for the whole session), and the image
does not contradict, but cannot prove.

### Toward a "play from the current page" patch (static, 2026-11-14)

The owner wants `[PLAY]` to start from the step page on screen, not from step
1. An earlier pass in the sibling analysis project concluded the transport code
could not be located. That verdict predates the RAM alias and is withdrawn:
the Play handler is reachable the same way the BPM handler was.

`from firmware image (static analysis)`, read in ARM mode against this
repository's copy of the image. Nothing was run or flashed.

| Item | Address (image VA) | What the image shows |
|---|---|---|
| Parameter index table, rebuilt by tracking the `mov`/`strb` immediates of the writer `0x20194B4C` | RAM `0x11128DB0` | all 290 rows filled before the first call; row `0x29` = `30 40 76`/2 (Tempo), rows `0x37`, `0x38`, `0xEC`, `0xFA` match the third party's Page captures |
| `SequencerStatus` `01 10 20` | table row **`0x1D`** | |
| `NotifyResetPlayCurrentStepCount` `01 10 29` | table row **`0x33`** | not written through `set_param`; it is written from the engine side, see the next table |
| `DrumPatternPage` `01 1p 36` | table row **`0xEC`** | emitted per part by the Page handler at `0x200D8390` (third party's finding, re-found here) |
| Panel listener for button category **8** | `0x200BA490` | the usual shape (`0x200B05D4(mgr, 8, pressed)` gate, then `0x200B0FD0`); when the event byte is **1** it tail-calls `0x200B9F04`, otherwise `0x200BA3C4`. Corrected 2026-11-14: an earlier reading of this row had the two swapped. If 1 means press, the toggle runs on **release**, and `0x200B9F04` only arms the flag `+0x3F` that makes the release skip the toggle (*inferred*: a held-`[PLAY]` combination) |
| **Play toggle** | `0x200BA3C4` | after two state checks, reads "is the sequencer running" through `0x20170850` and calls **`set_param(mgr, 0x1D, !running)`** at `0x200BA434`. Category 8 is therefore *inferred* to be `[PLAY]`; the control-to-category map was not decoded for it |
| Other writers of `0x1D` = 0 (stop) | `0x200A9F9C`, `0x200AA020`, `0x200B0F10` | each calls `0x200A9E9C` first, then the emitter `0x200A870C(mgr, 0x1D, 0)` |

**What this means.** Starting playback is a **property write**, not a direct
call into the sequencer: `[PLAY]` sets `SequencerStatus`, and whatever starts
the step clock is an observer downstream of the model. So the hook point for
the patch is known and is the same kind as the tap-tempo hooks. What is **not**
known is the one piece the patch needs: **where the sequencer sets its step
position when playback starts, and whether that position can be set to
anything other than zero.** Finding that means following the
`SequencerStatus` property (`0x20170798` returns the object, value through
`vtbl+0xA8` at `+0x74`) to its observers and into the engine. The next
subsection does this from the engine side.

#### Down to the engine: where the play position is reset (static, 2026-11-14)

`from firmware image (static analysis)`, same method. The trace entered the
engine from two ends: the MIDI clock **sender** (the only code that emits
`FA`/`FC`), and the one place the image writes row `0x33`. Both lead to the
same object, a sequencer player with eleven tracks.

| Item | Address (image VA) | What the image shows |
|---|---|---|
| Engine-side parameter setter | `0x20136668` | `cmp r1, #0xE9; bxhi lr; b 0x2013663C`: the same shape as `set_param`, on the engine's own model (`ctrl+0x10`) |
| MIDI clock sender, "set running" | `0x2014B0FC` | on a change of the running byte `+0x54`, sends `FA` (with `+0x44` and `+0x6C` cleared) or `FC` through `0x20137D48`; `0x2014B2F0`, `0x2014B310`, `0x2014B324` send `F8`, `FA`, `FC` alone |
| Transport controller | `0x2014211C` and neighbours | calls the clock sender, holds ten player pointers at `+0x18`…`+0x3C`, and writes row `0x1D` through `0x20136668` (`0x2014290C`… see below) |
| Writes row `0x1D` (`SequencerStatus`) on the engine side | `0x201428F8` | `0x20136668(ctrl+0x10, 0x1D, v, 0)` |
| Writes row `0x33` (`NotifyResetPlayCurrentStepCount`) | `0x2014290C` | `0x20136668(ctrl+0x10, 0x33, 0, 0)`; its only caller is `0x2016ADCC` |
| **Step-count reset** | `0x2016AD98` | `(player, flag)`: clears `+0x94`/`+0x95`, sets `+0x98 = 0x3C01`, sets `+0x90` to 1 and sends the `0x33` notification when `flag = 0`, or to 0 silently otherwise |
| Sequencer player vtable | `0x203CCB80` (alias `0x1033C780`) | `+0x24` tick `0x2016B8F4`, `+0x28` **start** `0x2016B344`, `+0x2C` seek `0x2016A0B4`, `+0x30` **rewind** `0x2016A270`, `+0x34` stop request `0x2016A1FC`. `0x2016AB1C` loops over **11** tracks through `0x20169944(player, i)` |
| Per-tick step boundary | `0x2016B83C` | reads the position in ticks (`0x2017A400` on `player+0xC`), divides by 120 with the `0x88888889` reciprocal, and acts only on exact multiples. At 480 ticks per quarter note, **120 ticks is one 16th step** (*inferred*) |
| Loop wrap | `0x2016B780` | when the position reaches the limit `+0x98`, computes a new position from the loop start at `+0x40` through the timeline (`vtbl+0x3C`), stores it (`0x2016AA04`) and resets the step count |
| **Start** | `0x2016B344` | reads the current tick, reports it to the controller (`0x20142A08`), sets state `+0x2C = 1` and `+0x3C = 1`. **It does not move the position**: with `flag = 0` it only sets `+0x8C`, with `flag ≠ 0` it calls seek (`vtbl+0x2C`), which hands the *current* position to every track (`+0x118`) |
| **Rewind** | `0x2016A270` | sets state `+0x2C = 0`, clears the step count (`+0x90 = 0`, `+0x98 = 0x3C01`), **builds a position from the start position stored at `+0x40`…`+0x54`** (`0x2017B7BC`), **sets it** (timeline `vtbl+0x10` = `0x2017B5BC`), tells the controller "no position" (`0x20142A08(ctrl, -1)`), then relocates each track (`+0x11C`, `+0x154`, `+0x110`) |
| Who calls start and rewind | scheduler `0x2013E34C` / `0x2013E3A8` | the first sets a job's countdown and calls `vtbl+0x28`; the second runs `vtbl+0x24` each period and, when it returns −1, calls `vtbl+0x34` then `vtbl+0x30` |
| Position format | 24 bytes | byte 0 is a mode (1 or 2), five words follow; `0x2017B5BC` converts between the two modes. The fields were **not** decoded |

**What this means for the patch** (*inferred*). The position goes back to zero at
**stop**, not at play: rewind replaces it with the start position kept at
`player+0x40`. Play then starts from wherever the position is. So
"play from the current page" does not need a new mechanism. It needs one
extra step, before start or at the end of rewind: replace the position with
*start + page × 16 steps × 120 ticks*, using the primitives the image already
uses for its own loop wrap (timeline `vtbl+0x3C` to advance, `vtbl+0x10` to
set, then seek `vtbl+0x2C` to hand the position to the tracks).

The position belongs to the whole player, not to one track. Whether each track
folds a global position back into its own length is **not established**. That
is the open design question about tracks of different lengths, now in a precise
form. Do **not** patch `+0x40` itself: the loop wrap reads it too, so the
pattern would loop back to the page instead of to step 1.

Still missing: the field layout of the 24-byte position, and how the current
page reaches the engine (row `0xEC` per part is the candidate).

#### The three pieces a patch needs (static, 2026-11-14, continued)

`from firmware image (static analysis)` unless marked otherwise.

| Piece | Where | What the image shows |
|---|---|---|
| **Current track**, UI side | UI state, index `4` | `0x200B2D00(ui, 4)`. The getter reads byte `ui + 0x6C + index` (indices up to `0xD2`; index `0x15` is special-cased). This is a UI mirror, not the parameter table |
| **Current page** of track `p`, UI side | UI state, index `0x39 + p` | `0x200B2D50(ui, 0x39, p)`, which bounds `p ≤ 10` and returns index `0xD3` (always 0) when out of range |
| **Last page** of track `p` | UI state, index `0x2E + p` | the `[PAGE]` step `0x200D8328` computes the new page as `0x200A8A5C(cur = [0x39+p], max = [0x2E+p], min = 0, delta, wrap)`: a clamp, or wrap to 0 past `max`, and emits it as row `0xEC` (`DrumPatternPage`) for part `p` |
| UI state seen from the Play handler | `0x200BA3C4`, `r0+8` | the same object class the `[PAGE]` handler holds at `+4` (both call `0x200B2DD4`/`0x200B2DE8` on it). So a hook at the Play toggle can read the current track and its page with two existing calls |
| Track class (seek side) | vtable `0x203CC998` | `+0x118` = `0x201697D0`: clears `+0x158`, then `0x20164414` takes the position, moves it back by the track's own offset (`vtbl+0x14C`), and hands it to every reader in the list at `+0x90` (`vtbl+0x10`). No modulo by the track's length happens at this level |
| **Move a position by an integer** | timeline `vtbl+0x38` = `0x2017A36C` | `(out, timeline, delta, position by value)`: picks the sub-timeline from the position's mode byte and delegates to its `+0x38`. The track seek uses it with a negative delta. The unit is *inferred* to be sequencer ticks |
| Position layout | 24 bytes | byte 0 = mode (`1` or `2`). Mode 1 is built from a single 8-byte value (`0x2017B430`); mode 2 is converted through a sorted map of 32-byte entries carrying a 16-bit value at `+4` and two bytes at `+0x1C`/`+0x1D`, combined as `(v × 4) >> b` (a time-signature map: *inferred*). Field-by-field layout **not decoded**, and **not needed** if the patch only moves a position with `vtbl+0x38` |
| Swing, not length | `0x201644F4` | a nearby modulo routine divides by 100 (`0x51EB851F`) and indexes a 12-byte table at `0x1037C304` of grid divisions (`16/4`, `12/6`, `8/4`, `6/6`, …): swing or groove, **not** the per-track length fold |

**Per-track length.** Each track has its own pattern length
(`30 5p 10`–`15`, 1–8 bars), and tracks of different lengths loop
independently (`verified on hardware`, see
[04](04-sequencer-editing.md#pattern-length) and
[10](10-verified-behaviour.md)). The player keeps **one** position for all
eleven tracks. So the fold into each track's own length has to happen below the
track seek, in the readers at `+0x90` (*inferred*; that code was not read).

**What a patch would look like** (*inferred*, nothing built). A page is one bar
of 16 steps, so 16 × 120 = **1,920 ticks**.

1. **UI side, hook the Play toggle `0x200BA3C4`.** On a stopped-to-playing
   edge, read `p = [ui 4]` and `page = [ui 0x39+p]`, and leave
   `page × 1920` in the patch state block, the way the tap-tempo patch keeps
   its state.
2. **Engine side, hook start `0x2016B344`.** If an offset is pending, move the
   position with timeline `vtbl+0x38`, set it with `vtbl+0x10`, consume the
   offset, and let start run with its seek (`vtbl+0x2C`) so that every track
   is relocated.

The other tracks then start at the same global position folded into their own
lengths: a 1-bar track starts on its only bar, and a 4-bar track on page 3
starts on its bar 3. Whether that is the behaviour the owner wants for tracks
shorter than the current page is a design choice, not an obstacle.

Not established: the tick unit of `vtbl+0x38`'s delta; whether the UI task and
the engine task can share the state block without a lock (a single aligned word
is the safe minimum); the readers' fold; and whether start is ever entered with
a pending seek from somewhere other than Play (Song mode, external `FA`).

#### A play-from-page patch, built and then flashed (2026-11-14)

> **Flashed over SysEx on 2026-11-14, and it works** (owner's report:
> `[PLAY]` on page 2 starts at page 2). The first attempts failed on sender
> defects, not on the patch. See
> [10](10-verified-behaviour.md#2026-11-14-hardware-session-the-first-complete-sysex-update-and-the-play-from-page-patch-works).

`seqtrak-firmware-analysis/tools/play_from_page.py` patches a decompressed
OS 2.00.2 `Program` image; `tools/make_custom_pgm.py` then turns it into an
updater. Every claim in this subsection is `from firmware image (static
analysis)` except where marked. It was written before flashing; the patch was
then flashed over SysEx and **works** (owner's report, see the note above).

| Change | Image VA | Before | After |
|---|---|---|---|
| Dead destructor D1 made a no-op | `0x200AD5D8` | first word of D1 | `bx lr` |
| Code cave and mailbox | `0x200ADD08`–`0x200ADE47` (320 bytes, the **end** of D1) | D1's body | cave A, cave B, a zeroed mailbox word at `0x200ADE44` (RAM `0x1001DA44`) |
| Play toggle | `0x200BA434` | `bl 0x200A8C50` (`set_param`) | `bl` cave A |
| Sequencer player start | `0x2016B344` | `push {r4, r5, r6, lr}` | `b` cave B |

**Cave A** (UI side, 23 instructions). On a start edge (`r2 = 1`) it reads the
current track from UI state index 4 and its page from index `0x39 + track`
(handler object `[r4 + 8]`), and if both are in range (track ≤ 10, page ≤ 7)
stores `page × 1920` in the mailbox. On a stop edge, or out of range, it stores 0.
It then tail-calls `set_param` with the original arguments, so the firmware's
own path is untouched.

**Cave B** (engine side, 41 instructions). If the mailbox is non-zero it
clears it, gets the player's position (timeline `player + 0xC`, `vtbl+0x0C`),
moves it by the mailbox value (`vtbl+0x38`), and sets it (`vtbl+0x10`). It then
replays the displaced `push` and continues into start, which seeks every track
to the current position.

**Checks run on the build:**

| Check | Result |
|---|---|
| Every encoded word decodes back to the intended instruction | yes, 64 of 64 |
| Branch targets: `0x200B2D00`, `0x200B2D50`, `set_param`, start + 4 | all four exact |
| Original words at both hook sites before patching | as expected (`bl set_param`; `push {r4, r5, r6, lr}`) |
| Bytes changed in the whole image | 330, all in the four rows above |
| Program-counter-relative loads into the cave from outside D1, ±8 KiB | none |
| Other references to start `0x2016B344` | only its vtable slot (`0x203CCBA8`); no other class shares it |
| Stack alignment at every call from the caves | 8 bytes |
| `.PGM` built: `Installer` identical, `+0x40` = sum of the patched image (`0x592A4CF2`), re-decompressed `Program` = patched image | yes; image sha256 `55efa411…a4568` |

**Assumptions the build cannot check** (*inferred*, each one a way it could fail):

| Assumption | If wrong |
|---|---|
| One page = 16 steps × 120 ticks, and `vtbl+0x38` moves by ticks | playback starts at the wrong place, or on a fraction of a step |
| UI state index 4 is the current track and `0x39 + track` its page, as the `[PAGE]` handler uses them | the offset is taken from the wrong track, or is always 0 (no visible change) |
| The UI task and the engine task see the mailbox word coherently (one aligned word, write-back cache on both sides) | an offset is missed or applied late |
| No other path enters start while the mailbox holds a value | a later start (external `FA`, Song mode) could jump once to a stale page |
| The cave's tail of D1 stays unused if combined with the third-party tap-tempo patch, which fills D1 from its start | combining the two would need a fit check |

**Known side effect.** The MIDI clock output still sends `FA` (start from the
top) when playback starts mid-pattern, so a slaved device starts at bar 1.

**Going back** is the stock updater, `8Z33OS_.PGM`, flashed the same way:
`[KICK]` + `[BAR LENGTH]` at power-on, with the file at the stick's root
(reported by a third party).

**A route that is closed:** injecting a MIDI Song Position Pointer (`F2`)
followed by Continue (`FB`) internally. Yamaha's MIDI Implementation Chart
marks Song Position as neither transmitted nor recognised
(appendix I) `from Yamaha Data List`. It could still be tried from the host,
which is cheap and needs no flashing, but the chart predicts no effect.

## What the hardware has actually said about `0x64`

Everything above about the protocol comes from the official app. Read-only probe
sessions on the real unit tested the one thing that binary cannot answer:
whether the `0x64` space is reachable at all from outside an update. **It is
not**, and that is now a firm negative in both modes.

The marker differs between the two halves of this section, and the difference is
the point:

| Claim | Marker |
|---|---|
| `0x64` answers no read in **normal** mode | `verified on hardware` — instrumented negative, control in the loop |
| The loader's Identity Reply, byte 11 = `00` | `verified on hardware` |
| Entering and leaving loader mode is reversible on this unit | `verified on hardware`, one unit, four cycles |
| The change-mode `64 00 00 01` **is** acknowledged in loader mode, at **7.04 s** — reproduced by two tools on two runs | `verified on hardware` |
| `0x64` answers no read in **loader** mode, change-mode acknowledged | `verified on hardware` — instrumented negative, control after every probe |

**In normal mode, there is no SysEx read path into `0x64`.** Parameter Requests
to `64 00 00`, `64 01 00`, `64 02 00` and `64 06 00`, six loops each, returned
nothing — 24 attempts, not one reply. A `FirmwareVersion` control at `01 00 00`
sat in the same loop and answered 5 times out of 6, so the link and the read
primitive were working while `0x64` stayed silent. The single control miss is
the ~1-in-10 drop documented in
[10-verified-behaviour.md](10-verified-behaviour.md); it is why the control
belongs in the loop.

**In loader mode, `0x64` is silent too, and the reserve is now lifted.** The
machine was rebooted into the loader with `F0 43 10 7F 1C 0C 64 00 06 01 F7`,
re-enumerated as a MIDI port, and answered the Universal Identity Request:

```
← F0 7E 7F 06 02 43 00 41 64 06 00 00 01 7F F7
```

Byte 11 is `00` here against `0A` in normal mode, which is how you tell the two
apart: that byte is `mm = (version − 1.0) × 10` for the application firmware and
reads `00` for the loader.

**The change-mode is acknowledged — it just takes about seven seconds.** This
is what three earlier runs missed, and the reason they could not settle
anything:

```
→ F0 43 10 7F 1C 0C 64 00 00 01 F7          change-mode
← F0 43 10 7F 1C 0C 64 00 02 01 F7          +7.04 s
```

With the mode entered and acknowledged, all seven read addresses tried —
`64 00 00`, `64 00 01`, `64 00 02`, `64 01 00`, `64 01 03`, `64 02 00`,
`64 06 00` — returned **nothing** in a 2.5-second window each, while an
Identity Request sent immediately after every one of them answered in **0.01 s,
seven times out of seven**. So the link was demonstrably alive and fast at each
measurement point while `0x64` stayed silent. That is the instrumented negative
the earlier runs could not produce. Session in
[10-verified-behaviour.md](10-verified-behaviour.md#2026-11-05-hardware-session-the-loader-takes-seven-seconds-to-acknowledge-and-0x64-is-silent-anyway).

> **The instrument was the whole problem, for the third time in this
> repository.** The earlier probers used 0.25-second windows, so the
> acknowledgement at +7 s was invisible, and one run caught it inside the
> window of an unrelated request and briefly looked like `64 06 00` answering.
> A reply attributed to whichever request happened to be in flight is not a
> measurement. Long windows, a drain before every send, and the arrival time
> printed for every message: `tools/loader_probe_timed.py` in the sibling
> analysis project does that, and it is the one to use for anything in this
> space.

One behavioural detail, worth knowing before writing a client: **while a
change-mode is pending, the loader answers nothing else.** In the run that sent
eight change-modes about 0.65 s apart, the Identity control was silent all
eight times and only started answering once the acknowledgement had landed.
Identity is otherwise instant in loader mode.

**Entering and leaving loader mode is reversible on this unit.** Normal →
loader → identity → reboot → normal, with the machine back in its initial state
and nothing written: no `SendingStart`, no block. Four cycles now, including one
where the prober crashed in loader mode on a port-enumeration race and the unit
was brought back by sending the exit by hand. That is real de-risking — the
"entry might erase something" hypothesis has not materialised — but it is one
unit, and it says nothing about what a *write* in loader mode would do.

What this does **not** establish: that the resident loader checks no signature.
Its code is still not readable by any route available here, which is the
blocking item below. A silent address proves there is no read path, not that
there is nothing behind it.

---

# Is custom firmware feasible?

**The file lifts one lock, but not the one that counts.**

There is no cryptographic signature in the update file. That removes the
objection most people expect to stop them — and it is a **necessary** condition
for custom firmware, not a **sufficient** one. The component that validates and
writes is not in the file.

## The defensible statement

This is the wording to quote, and it is deliberately narrower than "there is no
signature":

> The SEQTRAK OS 2.00 update file contains no cryptographic signature, no
> certificate and no cryptographic primitive constants; its only integrity check
> is a 32-bit additive sum per block, verified exactly. It remains possible that
> the update mechanism verifies a short digest that was not spotted, or that
> verification happens in a component absent from this file.
>
> And, since 2026-11-14: a `Program` modified with real code, with that sum
> recomputed, was accepted over SysEx and runs (`verified on hardware`).
> Whatever the resident loader checks, it does not stand in the way of a
> modified `Program`.

## What is now established

`from firmware image (static analysis)` unless noted:

1. **The container is fully understood and reproducible.** A syntactically valid
   `.PGM` with correct checksums can be built from a modified image.
2. **The `Program` image is a flat ARMv7 (R profile) memory image** loaded at
   `0x20040000`, in the clear, with a plaintext section table. It is modifiable
   in principle.
3. **Nothing in the file is encrypted.** The high entropy measured before the
   file was parsed came entirely from LZSS compression and audio sample data —
   which is exactly the ambiguity the earlier version of this document warned
   about, resolved in the benign direction.
4. The SoC is a **Yamaha SWX09** (*inferred* from a build path), running an
   **eForce** RTOS. This document previously said there was no hint of the
   silicon anywhere.
5. The update channel itself is fully documented above, and **a third-party
   updater exists and works**: on 2026-11-14 this repository's sender pushed a
   complete update over USB MIDI, without the app, and the machine came back
   on it. `verified on hardware`
   ([10](10-verified-behaviour.md#2026-11-14-hardware-session-the-first-complete-sysex-update-and-the-play-from-page-patch-works)).
6. **The `Installer`'s block-receive path has been analysed**, and it checks
   *less* than the file carries. See the subsection below.
7. **The write chain is closed and verified, entirely off the machine.** The
   container can be synthesised from named field values instead of copied: a
   rebuild from fields reproduces the official file **byte for byte**
   (sha256 `1a87fb5a…13bcf63`). An LZSS compressor exists and round-trips the
   63.75 MiB image exactly, and one script takes a modified image through to a
   coherent `.PGM`. So producing a modified update file is no longer a question
   mark. Whether the machine would accept one was the open question. A third
   party reported that it does, for a `Program`-only change through the stick
   route ([see above](#what-they-report-on-hardware)), and this repository has
   since **reproduced it over SysEx**: a `Program` carrying a 330-byte code
   patch was accepted, runs, and does what it was written to do
   ([the play-from-page patch](#a-play-from-page-patch-built-and-then-flashed-2026-11-14)).
   `verified on hardware`.

   **One trap worth carrying over.** The `+0x40` semantics differ between the
   two blocks: `Installer` stores the sum of its payload **as stored**, while
   `Program` stores the sum of its **decompressed** image, not of the LZSS
   stream that is actually in the file. Summing the compressed payload gets you
   a field that is wrong in its low byte alone, which is a slow thing to debug.

   The regenerated LZSS stream is **valid but not byte-identical** to Yamaha's,
   because LZSS output is not canonical — it depends on the compressor's
   match-finding. That has no consequence: the receiver never compares the
   compressed stream, it decompresses it and writes the result.

### What the `Installer`'s receive path actually checks

`from firmware image (static analysis)`. The 1 MiB `Installer` block was
analysed at its load address `0x10000000`; the write-up, with
every address, is in the sibling project's
`seqtrak-firmware-analysis/INSTALLER-RECEIVE-PATH.md`. The control flow was
reconstructed by reading — nothing was executed, and the called leaf functions
(`memcmp`, `strlen`, the flash write) are identified by prologue and use rather
than proved.

The SysEx dispatcher sits at `0x3e1c`: it requires `ah = 0x64`, bounds the
category at `<= 2`, and jumps through a 3-entry table at `0x6489c`. Category 2
re-dispatches on `al` — `01` to the block-header handler at `0x36ac`, `02` to
the block-data handler at `0x3380`, which is exactly the `64 02 01` / `64 02 02`
split documented above.

Which of the 128 header bytes the receiver actually consumes:

| Header offset | Field | Read by the `Installer`? |
|---|---|---|
| `+0x00` | block name, 24 bytes | **yes** — bounded to ≤ 23 chars |
| `+0x18` | version | **yes** — bounded to ≤ 11 chars |
| `+0x40` | **additive sum** | **yes** — by the per-type handler at `0x10001FD4`, not by the SysEx handlers. This table said "no" until 2026-11-10 |
| `+0x6E` | index / flag | **yes** — range check |
| `+0x7C` | payload length | **yes** — must be non-zero; drives the transfer |

So the receiver's whole validation of an incoming block is: the ordinary 7-bit
Yamaha checksum **per message**, the packet sequence number (out of order →
error 15), bounds on the name, version and index fields, a **5-byte `memcmp`
against the plaintext tag `#8Z33`** (mismatch → `UpdateResult` 9,
`InvalidData`), and **the additive sum at `+0x40`** (mismatch → `2`).

> **Corrected 2026-11-10.** This paragraph used to say that no 32-bit sum is
> accumulated over what is received. The SysEx handlers at `0x3380` and
> `0x36AC` indeed accumulate none. But the Installer has a second layer the
> first reading missed: a table of per-type handlers at `0x1006D570`, indexed
> by header `+0x6E`. Type `1` is `Main`, and its chunk handler `0x1000211C`
> does the `#8Z33` check on the first chunk, then tail-calls `0x10001FD4`.
> That routine adds every byte of the chunk to a running total at `ctx+0x14`.
> Once the received count at `ctx+0x10` reaches header `+0x7C`, it compares the
> total with header `+0x40` and returns `2` if they differ.
> `from firmware image (static analysis)`. A third party reports that the
> hardware enforces it: a stale sum was refused, and so was a sum written
> big-endian ([above](#what-they-report-on-hardware)). Whether the SysEx path
> reaches this table as well was not traced; assume it does.

> **The `#8Z33` tag: where it is, and what it is not compared against.** It is
> in **neither** block header — both were dumped byte for byte to check.
> `Installer` holds the name `Installer` at `+0x00` and `Program` holds
> `Program`; the tag appears nowhere in those 128 bytes. It is the first five
> bytes of the **decompressed** `Program` image, which opens
> `#8Z33 Copyright(C)2021 YAMAHA Co.,Ltd.`, and it is also a string constant
> in the `Installer`'s own data at image `0x64800`, beside `Wave` and `Data` —
> that constant is the comparison target.
>
> **Now answered (2026-11-10):** `0x1000211C` compares the tag against
> `ctx+8`, the first chunk of the **decompressed** image, and the running sum
> is also taken over decompressed bytes. So decompression happens upstream of
> the per-type handler. Where exactly is still not traced (candidates named by
> the third party: `0x10002A6C`, `0x1005879A`). The reasoning below, kept for
> the record, was right that the tag is not compared against the compressed
> payload.
>
> What the received side is, though, is **not established**, and two facts rule
> out the obvious guess. The comparison sits in the header path, which runs
> before any payload has arrived; and the `Program` payload as carried in the
> file is the **LZSS stream**, which opens with compressed data, not with the
> tag. So the check cannot be reading the head of the received payload. A
> simulator that assumed it did refused the official file, which is how this
> was caught. The validator reaches its operand through a pointer at `+8` of a
> context structure and that is as far as the reading goes.
>
> Practical consequence, unchanged and cheap: keep `#8Z33` as the first five
> bytes of any modified image.

**Consequence.** The additive sum at `+0x40` **is** enforced on reception.
But it is an additive sum: the rebuild tools already recompute it, so it is no
barrier to a modified image, only a trap. **Write it little-endian, over the
decompressed image.** Nothing in this path would stand in the way of a
modified `Program` image, provided the `#8Z33` tag, the sum, the string
lengths, the packet numbers and the 7-bit checksums are right. All of these are
trivial to reproduce, and a third party reports exactly that on hardware.

**What this does not touch.** This is the loader→`Installer` step already
passed and the `Installer`→`Program` step. The **resident loader**, which
receives and writes the `Installer` itself, is still not in this file. It has
accepted Yamaha's own `Installer` on hardware; whether it would accept a
**modified** `Installer` is unknown, and no one has needed to try: a
`Program`-only change goes through the unmodified `Installer`.

## What is still blocking

> The component that **validates and writes** is not in this file.

Being precise about this matters more than the headline. The file contains an
`Installer` and a `Program`; the resident loader receives and writes the
`Installer`, and the freshly written `Installer` then receives and writes the
`Program`. Therefore:

- The `Installer` **receives no signature for the `Program`** — there is none in
  the file. Established.
- The `Installer` **checks a plaintext tag and an additive sum**, and nothing
  cryptographic. Established by analysis;
  [see above](#what-the-installers-receive-path-actually-checks). So the
  `Installer`→`Program` step is no longer a candidate barrier. A third party
  reports a modified `Program` accepted on hardware through the stick route
  ([see above](#what-they-report-on-hardware)); not reproduced here.
- **Nothing at all can be said about the resident loader's checks.** Its code
  is not in this file. For a `Program`-only change this no longer matters: the
  loader only ever receives Yamaha's own `Installer`, and a modified `Program`
  was accepted on hardware over SysEx on 2026-11-14. It would matter for a
  modified `Installer`, and this file cannot reveal it. Hardware has since confirmed it is
  not readable by SysEx either, in normal or loader mode — see
  [above](#what-the-hardware-has-actually-said-about-0x64). What hardware *did*
  settle is cheaper and still useful: switching into loader mode and back is
  reversible on this unit.

## What the signature search could not have detected

Read this before quoting any conclusion. Each item is a real limit of the
method, not a stylistic hedge.

1. **A bare 32-byte digest.** A SHA-256 stored as-is is too short for entropy
   analysis and has no recognisable structure; at a 32-byte window the false
   positive rate is 2.6 %, which is noise. If the image carries a digest
   somewhere, the search could not have seen it. Same for a 16-byte MAC.
2. **A signature outside this file.** USB-stick updates go through a FAT volume
   and only the `.PGM` was analysed. A detached signature in a second file on
   the volume, or carried as a message field in the SysEx stream, is out of
   scope.
3. **Verification in the resident loader or mask ROM.** The fundamental limit:
   the code that validates the `Installer` is not in this file, and no
   measurement on this file can speak about it.
4. **A hand-rolled bignum verifier.** An in-house RSA or EC implementation with
   no OID table, no named curve constant and a derived rather than stored public
   key would pass every constant filter. Unlikely for an industrial vendor, not
   excluded.
5. **Non-standard or obfuscated cryptography** whose constants resemble nothing
   known.
6. **It says nothing about the resident loader.** The claim proved is *the file
   carries no signature*, and the `Installer`'s receive path has since been read
   and enforces nothing cryptographic — but both are statements about this file
   and the software it delivers, never about the code already on the machine
   that receives the `Installer`.

## A sender exists, and it has updated the machine

It was first exercised against a simulated receiver, then, after three defects
found on hardware, it completed a full update on 2026-11-14.
`verified on hardware` for the run; the protocol it follows is the one read out
of the official plug-in ([below](#there-is-no-sendingstart-command)).
Four tools in the sibling analysis project:

| Tool | What it is |
|---|---|
| `tools/fw_sysex.py` | the framing: 7-into-8 packing, the 14-bit byte count, the 7-bit checksum, the window and chunk arithmetic, the `.PGM` parser |
| `tools/installer_sim.py` | a stand-in for the receiver, implementing the checks traced in the subsection above |
| `tools/sysex_updater.py` | builds the whole stream and drives it at the simulator, then compares what arrived against the file; `--write --i-mean-it` drives the machine |
| `tools/fw_midi.py` | the MIDI transport, with the guard rails below, the hand-over to the `Installer`, and one header and one create request per block |

The transport has two hardware modes. `--rehearse` enters loader mode, enters
update mode, waits for the acknowledgement and stops — no header, no block, so
no write path is opened; that is the part already exercised and found
reversible — five cycles, the last of them driven by this transport, with the
acknowledgement landing at 7.04 s exactly as the probe had measured it. `--write` additionally requires `--i-mean-it`, reads the battery at
`01 10 02` and **refuses below 80 %**, because losing power during a flash
write is the one failure this protocol has no answer for. Messages are paced at
2 ms, the exit to normal mode is in a `finally`, and port lookup tolerates the
re-enumeration race that killed one probe run after its reboot had already gone
out.

**The handshake is no longer a guess.** It was, and guessing it cost four
failed runs. Each run wrote nothing to flash, which is why each one was
survived:

| Defect in the sender | What the machine did | Run |
|---|---|---|
| Per-packet timeout of 5 s | blamed for the first stop; wrongly, see the next row | 2026-11-05 |
| No hand-over to the `Installer`: the `Program` went to the loader | stopped answering after 1,062,576 bytes, twice | 2026-11-05, 2026-11-14 |
| No create request `64 01 02` at the end of a block | buffered without writing; the hand-over then found the loader still running | 2026-11-14 |
| A header every 256 KiB instead of one per block | `64 01 05` (error) | 2026-11-14 |

With all four fixed, the run went through: one header and `64 01 00`; a
`64 01 00` after every packet; `64 01 02` once, answered by `64 01 03` at once;
then the hand-over, and the same for the `Program`. Details in
[10](10-verified-behaviour.md#2026-11-14-hardware-session-the-first-complete-sysex-update-and-the-play-from-page-patch-works).

The simulator now models the same exchange, and the full OS 2.00 file goes
through it intact:

| Block | Payload | Headers | Packets | Create requests | Messages | Arrived intact |
|---|---|---|---|---|---|---|
| `Installer` | 1,048,576 | 1 | 300 | 1 | 302 | yes |
| `Program` | 10,780,511 | 1 | 3,085 | 1 | 3,087 | yes |

**What the simulator does and does not prove.** It checks the framing, the byte
count, the checksum, the packing, the chunk sizing, the packet numbering and
that the bytes leaving the sender are the bytes in the file. Its model of the
replies was **wrong** until hardware corrected it: it agreed with a sender that
the machine refused. A simulator written from the same reading as the sender
is not an independent check of that reading.

### There is no `SendingStart` command

The state machine's `SendingStartForInstaller` / `…ForProgram` states suggest a
distinct "arm the transfer" message. **There is none.** Resolving the
the indirect calls in the plug-in and then enumerating every
call site of
`-[FirmwareUpdater sendSysExWithCategory:command:data:dataLength:]` gives the
inventory of what the app sends into the `0x64` space. Corrected 2026-11-14:
this said "four call sites, that is all", and it missed the create request,
sent from `-[MidiFirmwareUpdater sendNextPacket]` through the same method:

| Call site | Message | Meaning |
|---|---|---|
| `sendRebootRequest:` | `64 00 06 <n>` | reboot — `01` to the loader, `00` to normal |
| `handleIdentityReply:` | `64 00 00 01` | enter update mode |
| `startUpdatingAsLoader` | `64 00 00 01` | the same, on the loader path |
| `sendNextBlock:` | `64 00 00 00` | **leave** update mode, sent once everything has been sent |
| `handleCreateConfirm` | `64 00 00 00` | **leave** update mode after the `Installer`: the unit reboots into it |
| `-[MidiFirmwareUpdater sendNextPacket]` | `64 01 02`, no data | **create request**, once the whole block is sent; answered by `64 01 03` |

The block messages `64 02 01` (header) and `64 02 02` (data) go out through
`sendMessage:withLength:` directly, not through this method. `64 00 00` is the mode command and the data byte is the mode, and
the receiver masks it: `and r0, r0, #1`, so **only bit 0 matters**. On hardware
the `01` form is acknowledged by `64 00 02 01` after about seven seconds.

So **the block header message `64 02 01` is what arms a transfer.** That is
also what the receiver says: the data handler at `0x3380` refuses unless the
context holds the armed state, the header handler at `0x36ac` is what
establishes it, and the teardown at `0x3284` — category 1 command `04`, which
requires the armed state, clears it and returns code 14 — is the cancel. Every
other slot in the three dispatch tables is a `bx lr` stub.

The sequence a sender must follow, with the hand-over this section first missed:

```
F0 7E 7F 06 01 F7                    identity, expect mm = 0A
64 00 06 01                          reboot to the loader; re-enumerates
F0 7E 7F 06 01 F7                    identity, expect byte 11 = 00, byte 12 = 01
64 00 00 01                          enter update mode; 64 00 02 01 at 7.04 s
  Installer block, as below            the LOADER receives it
64 00 00 00                          leave update mode: the unit reboots
                                     into the Installer (64 02 00, or the
                                     port re-enumerates)
F0 7E 7F 06 01 F7                    identity, byte 12 must be 02
64 00 00 01                          enter update mode on the Installer;
                                     64 00 02 with non-zero data
  64 02 01  <packed 128-byte header>   ONCE per block; 64 01 00
  64 02 02  <packet 0 .. 74>            each answered by 64 01 00; the
  ...                                   number restarts every 256 KiB
  64 01 02                              create request, no data, once
                                        at the end of the block; 64 01 03
64 00 00 00                          leave update mode; the unit reboots
```

> **Corrected 2026-11-14.** This block used to go straight from the
> `Installer` to the `Program` without the hand-over, and called the sequence
> "fully determined". It was not: the app's own state machine above has a
> `RebootingAsUpdater` stage, and this repository's sender skipped it. Read
> out of the official app's firmware-update plug-in,
> `from official app`:
>
> | Method | What it does |
> |---|---|
> | `handleCreateConfirm` | in state 9 or 10 (`Installer` data, waiting for the create confirmation): state 11 `RebootingAsUpdater`, sends `64 00 00 00`, starts the reboot timer. In the `Boot`, `Program` and `Wave` states it calls `sendNextBlock:` instead |
> | `handleSysExMessage:withSize:` | `64 02 00` received in state 11: state 13 `CheckingIdentityAsUpdater`, sends Identity |
> | `handleConnectionChange:` | port back in state 12: state 13, sends Identity |
> | `handleIdentityReply:` | its argument is **byte 12** of the Identity Reply. State 1 and `01`: already in the loader. State 5 and `01`: enter update mode on the loader. State 13 and **`02`**: state 14, sends `64 00 00 01` |
> | `handleModeReply:` | in state 14 with non-zero data: `startSendingBlocks:` continues with the next block of the file |
> | `sendNextBlock:` | when the whole file is sent: `64 00 00 00`, state 29 `RebootingAsNormal` |
>
> So byte 12 of the Identity Reply names the running code: `00` the normal
> firmware, `01` the resident loader, `02` the `Installer` (all three
> `verified on hardware`, the last on 2026-11-14).
>
> Two more pieces, from the same binary: `sendBlockHeader` sends **one**
> header per block and takes the block length from its `+0x7C`, and
> `sendNextPacket` sends the **create request `64 01 02`** (category 1,
> command 2, no data) once the whole block is out. The earlier inventory of
> "four call sites" missed it. The full sequence went through on hardware on
> 2026-11-14 ([10](10-verified-behaviour.md#2026-11-14-hardware-session-the-first-complete-sysex-update-and-the-play-from-page-patch-works)). Skipping the hand-over sent the
> `Program` to the loader, which stopped answering after 1,062,576 bytes, twice
> ([10](10-verified-behaviour.md#2026-11-14-hardware-session-the-sysex-transfer-stops-at-the-same-byte-every-time)).

> **`0x4004` is the reply emitter, not a commit loop.** An earlier reading of
> this material called it "finalisation: a flash-commit retry loop". It is
> reached from the mode handler, the data handler and the cancel alike, and the
> mode handler tail-calls it after staging a buffer with `mov r1, #0xb` —
> eleven bytes, exactly the length of a `64 00 02 xx` Parameter Change. It is
> how the device answers.

## Next steps, ordered by information per unit of risk

The two steps that used to open this list are **done**, both on 2026-11-14:

1. **A third-party updater** pushes an update over SysEx, without the app.
2. **A patched `Program`**, carrying real code rather than a string change,
   was flashed that way and works
   ([above](#a-play-from-page-patch-built-and-then-flashed-2026-11-14)).

What is left, roughly in order:

1. **Flash the stock `8Z33OS_.PGM` back over SysEx** once, to establish that
   the way back works by the same route. Expected to work (it is Yamaha's own
   file through a protocol now verified), not yet done.
2. The play-from-page patch's untested cases: a track shorter than the current
   page, Song mode, an external `FA`
   ([12](12-open-questions.md)).
3. Any further patch: load the RAM alias first
   ([above](#strings-in-the-program-image-are-reached-through-a-ram-alias)),
   keep the cave plan of the existing patches in mind (both use the dead
   destructor D1: the tap-tempo patch from its start, play-from-page from its
   end), and remember that the code RAM is writable
   ([MPU table](#architecture-and-soc)).

Also free and already done: **query the identity** in normal mode
(`F0 7E 7F 06 01 F7`). `mm = 0x0A` decoded to version 2.0 and matched the
machine. Repeat it after any firmware change to read the new version. The same
request in loader mode returns `mm = 00`, which is the cheap way to confirm
which mode the machine is in.

The probe that used to be owed here — the loader-mode read sweep with an
acknowledged change-mode — has been **run, and it came back a firm negative**.
There is no SysEx read path into `0x64` in either mode. So nothing risk-free is
left to try: every remaining step writes to the machine, or needs a hardware
dump of the flash.

## Risks, stated plainly

Writing to a machine's loader can brick it permanently, and no accessible JTAG
is documented.

**One recovery path is now verified, for one failure mode.** This section used
to say that no recovery path could be verified to exist. That is no longer
true, and it was settled the expensive way: a real transfer of the official
file was interrupted by a defect in the sender, at 9.9 % of the `Program`
block, with the `Installer` fully sent (but, as found later, never written). The unit answered no SysEx for two
minutes and would not power off with `[⏻/PLAY]`. **Forced termination —
`[⏻/PLAY]` + `[PROJECT↑]`, User Guide §3.2.2 — brought it back**, and after
about thirty seconds of apparent hang on the next start it booted normally,
with `FirmwareVersion` unchanged and the owner's projects intact.
`verified on hardware`, written up in
[10-verified-behaviour.md](10-verified-behaviour.md#2026-11-05-hardware-session-an-interrupted-firmware-write-and-the-machine-came-back).

Read that bound narrowly, and more narrowly than first written. *Corrected
2026-11-14:* that run, and the next one, never wrote anything. The sender never
sent the create request `64 01 02` and never handed over to the `Installer`,
so the loader buffered the data and stopped answering
([10](10-verified-behaviour.md#2026-11-14-hardware-session-the-sysex-transfer-stops-at-the-same-byte-every-time)).
What was survived is a **stalled transfer before any flash write**, not a
partial write. Surviving an interrupted write, of either block, is still
untested.

Entering loader mode is reversible on one unit, five cycles — that is a bound on
the risk of *looking*, not of writing. Yamaha's own release notes say that "if
the unit becomes inoperable by accident, run the updater again", which suggests
a robust resident loader; the unit recovered without the updater being re-run,
which is better than the notice promises, but it is still one observation and
it probably does not cover an arbitrary `Program` image.

**And a warning worth more than the reassurance.** Every failure in this
exercise came from the sender, not the device. The first was blamed on a
5-second timeout, which was a real defect but not the cause: the cause was
three missing pieces of the protocol, which a careful reading of the official
plug-in would have shown before the first write. Reading the code that works
is cheaper than probing the machine.

For most of what people want from this machine, the **SysEx + external display +
third-party app** route gives far more result for far less risk. The protocol
documented in this repository already covers pattern editing — now
`verified on hardware`, writes included — live editing state, user scales, song
mode and Wi-Fi configuration: a very large control surface, with the firmware
untouched.
