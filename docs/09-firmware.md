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

**A block is sent window by window, 256 KiB at a time, and each window is one
create cycle.** `-[MidiFirmwareUpdater sendingDataSize]`:

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
| Window, one per create cycle | `0x40000` = 262,144 bytes |
| Image bytes per packet | ≤ **3500** |
| Packets in a full window | 74 × 3500 + 1 × 3144 = **75** |
| SysEx data bytes per full packet | 3500 × 8/7 = **4000** exactly |
| Full packet message length | 4000 + 17 = **4017** bytes |

That 4000 is the design constraint, and it is what makes the 3500 look
arbitrary until you apply the 7-into-8 packing described in
[02-sysex-format.md](02-sysex-format.md#dividable-bulk-split-transfers).

Applied to the OS 2.00 file:

| Block | Payload in the file | Create cycles | Packets |
|---|---|---|---|
| `Installer` | 1,048,576 | 4 | 300 |
| `Program` | 10,780,511 | 42 | 3,085 |

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

### Strings in the `Program` image cannot be cross-referenced

`from firmware image (static analysis)`. Worth knowing before anyone spends
days on it: **the ordinary way into an unknown binary — find a meaningful
string, then find the code that uses it — does not work on the `Program`
image.** The strings are there in the clear; nothing points at them.

The instrument is a base-address sweep. For every one of the 4096 possible
1 MiB-aligned base addresses `B`, count how many NUL-terminated strings of
≥ 6 printable characters, at image offset `off`, have the 32-bit value
`B + off` present as a 4-byte-aligned little-endian word anywhere in the image.
A binary whose pointers are stored as data shows a sharp peak at its real base.

| Block | Declared load address | Peak found by the sweep | Strings with a stored pointer | Aligned words that are in-image pointers |
|---|---|---|---|---|
| `Installer` | `0x10000000` | **`0x10000000`**, sharply | 60 / 311 (**19.3 %**) | 1.095 % |
| `Program` | `0x20040000` | **none** | 12 / 23,590 (**0.1 %**) | 0.078 % |

The `Installer` is the control, and it validates the method: the sweep recovers
its documented load address against a noise floor of 1/311, a signal of about
60×. The `Program`'s best candidate is `0xE5300000` at 64/2000 — which is not
an address at all but the ARM encoding bucket for `ldr` with the
always-condition `0xE`, i.e. instruction words miscounted as pointers. **There
is no base address at which the `Program`'s strings are pointed to.** Searching
for a bare image offset, or for the offset less the 1024-byte prologue, finds
nothing either (3 and 7 hits out of 2000).

Two mechanisms would each produce this, and the measurement does not separate
them — *inferred*:

- **`movw` / `movt` immediate pairs.** On ARMv7 a 32-bit constant is normally
  materialised by two instructions carrying 16 bits each, so the address exists
  nowhere in the file as a 32-bit word. The `Installer` demonstrates the
  pattern: `movw r1,#0x4780 ; movt r1,#0x1006` builds `0x10064780`, the address
  of the `#8Z33` tag. A tool that does not fold these pairs reports no
  cross-reference even when the base is right.
- **An offset table plus a runtime base register**, which is what a relocated
  or position-independent image would use.

**Practical consequence.** Approach the `Installer` — 1 MiB, uncompressed, base
recovered, a fifth of its strings directly referenced — and treat the
`Program`'s 15.75 MiB code section as reachable only by control flow from the
reset vector and the exception table, not by string search. The sweep is
`seqtrak-firmware-analysis/tools/string_xref_base_sweep.py`.

### Architecture and SoC

**ARMv7-A, 32-bit, little-endian.** Both blocks open with the characteristic
8-entry ARM exception vector table built from `ldr pc, [pc, #0x18]`
instructions — a Cortex-M would use a table of addresses, not instructions,
which rules out the M profile.

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

### The version string decodes `FirmwareVersion`

The plaintext `2.00.2` at `+0x18` corresponds exactly to the four bytes
`02 00 00 02` that the machine returns for `FirmwareVersion` at `01 00 00`
(`verified on hardware`). So that parameter is a **version triple plus a build
number**: `2`, `00`, `0`, `2` → "2.00.2". The correspondence is reproduced; the
reading of the third byte is *inferred*, since it is `0` in both blocks here and
therefore unconstrained.

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

## What is now established

`from firmware image (static analysis)` unless noted:

1. **The container is fully understood and reproducible.** A syntactically valid
   `.PGM` with correct checksums can be built from a modified image.
2. **The `Program` image is a flat ARMv7-A memory image** loaded at
   `0x20040000`, in the clear, with a plaintext section table. It is modifiable
   in principle.
3. **Nothing in the file is encrypted.** The high entropy measured before the
   file was parsed came entirely from LZSS compression and audio sample data —
   which is exactly the ambiguity the earlier version of this document warned
   about, resolved in the benign direction.
4. The SoC is a **Yamaha SWX09** (*inferred* from a build path), running an
   **eForce** RTOS. This document previously said there was no hint of the
   silicon anywhere.
5. The update channel itself is fully documented above, so **a third-party
   updater is writable** — one that pushes an official Yamaha file without the
   app. `from the official app, untested`.
6. **The `Installer`'s block-receive path has been analysed**, and it checks
   *less* than the file carries. See the subsection below.
7. **The write chain is closed and verified, entirely off the machine.** The
   container can be synthesised from named field values instead of copied: a
   rebuild from fields reproduces the official file **byte for byte**
   (sha256 `1a87fb5a…13bcf63`). An LZSS compressor exists and round-trips the
   63.75 MiB image exactly, and one script takes a modified image through to a
   coherent `.PGM`. So producing a modified update file is no longer a question
   mark; whether the machine would accept one is a separate question, and it is
   the open one. `from firmware image (static analysis)`.

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
| `+0x40` | **additive sum** | **no — never read** |
| `+0x6E` | index / flag | **yes** — range check |
| `+0x7C` | payload length | **yes** — must be non-zero; drives the transfer |

So the receiver's whole validation of an incoming block is: the ordinary 7-bit
Yamaha checksum **per message**, the packet sequence number (out of order →
error 15), bounds on the name, version and index fields, and a **5-byte
`memcmp` against the plaintext tag `#8Z33`** (mismatch → `UpdateResult` 9,
`InvalidData`). The block-data handler accumulates no 32-bit sum over what it
receives, and finalisation at `0x4004` is a flash-commit retry loop with no
integrity check at all.

> **The `#8Z33` tag: where it is, and what it is not compared against.** It is
> in **neither** block header — both were dumped byte for byte to check.
> `Installer` holds the name `Installer` at `+0x00` and `Program` holds
> `Program`; the tag appears nowhere in those 128 bytes. It is the first five
> bytes of the **decompressed** `Program` image, which opens
> `#8Z33 Copyright(C)2021 YAMAHA Co.,Ltd.`, and it is also a string constant
> in the `Installer`'s own data at image `0x64800`, beside `Wave` and `Data` —
> that constant is the comparison target.
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

**Consequence.** The additive sum at `+0x40` is a check the *producer* of the
file applies — and a useful control for this analysis — not a barrier enforced
on reception. Nothing in this path would stand in the way of a modified
`Program` image, provided the `#8Z33` tag, the string lengths, the packet
numbers and the 7-bit checksums are right, all of which are trivial to
reproduce.

**What this does not touch.** This is the loader→`Installer` step already
passed and the `Installer`→`Program` step. The **resident loader**, which
receives and writes the `Installer` itself, is still not in this file. If it
demands a signature on the `Installer`, that applies upstream of everything
traced here.

## What is still blocking

> The component that **validates and writes** is not in this file.

Being precise about this matters more than the headline. The file contains an
`Installer` and a `Program`; the resident loader receives and writes the
`Installer`, and the freshly written `Installer` then receives and writes the
`Program`. Therefore:

- The `Installer` **receives no signature for the `Program`** — there is none in
  the file. Established.
- The `Installer` **checks nothing beyond a plaintext tag** — not even the
  additive sum. Established by analysis;
  [see above](#what-the-installers-receive-path-actually-checks). So the
  `Installer`→`Program` step is no longer a candidate barrier.
- **Nothing at all can be said about the resident loader.** Its code is not in
  this file. If it requires a signature on the `Installer`, everything stops
  there, and this file cannot reveal that. Hardware has since confirmed it is
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

## A sender exists, and it has been exercised against a simulated receiver

`from firmware image (static analysis)` for what it validates,
`from the official app, untested` for the sizing it reproduces.
Three tools in the sibling analysis project:

| Tool | What it is |
|---|---|
| `tools/fw_sysex.py` | the framing: 7-into-8 packing, the 14-bit byte count, the 7-bit checksum, the window and chunk arithmetic, the `.PGM` parser |
| `tools/installer_sim.py` | a stand-in for the receiver, implementing the checks traced in the subsection above |
| `tools/sysex_updater.py` | builds the whole stream and drives it at the simulator, then compares what arrived against the file |
| `tools/fw_midi.py` | the MIDI transport, with the guard rails below |

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

**One thing in the sender is still a guess, and it is marked as such in the
code:** the order of the create/acknowledge handshake around each window.
`64 01 00`, `64 02 00` and `64 01 03` are all documented device messages, but
which one closes a window — and whether the block header draws a reply at all —
is not established, and the app's state machine waits for a create confirmation
*after* the data rather than after the header. The flow-control wait therefore
accepts any of the three and fails only on silence, so a wrong guess about
which arrives cannot abort a transfer that is going fine. A real transfer is
what settles it.

The full OS 2.00 file goes through intact:

| Block | Payload | Create cycles | Packets | Messages | Arrived intact |
|---|---|---|---|---|---|
| `Installer` | 1,048,576 | 4 | 300 | 304 | yes |
| `Program` | 10,780,511 | 42 | 3,085 | 3,127 | yes |

**What that does and does not prove.** It establishes the framing, the byte
count, the checksum, the packing, the window split, the chunk sizing, the
packet numbering against a one-byte counter, the create/ack flow control, and
that the bytes leaving the sender are the bytes in the file. It cannot
establish that the *reading* of the receiver is right: if the firmware was
misread, the sender and the simulator agree and are both wrong. Only hardware
settles that.

### There is no `SendingStart` command

The state machine's `SendingStartForInstaller` / `…ForProgram` states suggest a
distinct "arm the transfer" message. **There is none.** Resolving the
the indirect calls in the plug-in and then enumerating every
call site of
`-[FirmwareUpdater sendSysExWithCategory:command:data:dataLength:]` gives the
complete inventory of what the app ever sends into the `0x64` space. It is four
call sites:

| Call site | Message | Meaning |
|---|---|---|
| `sendRebootRequest:` | `64 00 06 <n>` | reboot — `01` to the loader, `00` to normal |
| `handleIdentityReply:` | `64 00 00 01` | enter update mode |
| `startUpdatingAsLoader` | `64 00 00 01` | the same, on the loader path |
| `sendNextBlock:` | `64 00 00 00` | **leave** update mode, sent once everything has been sent |

That is all. `64 00 00` is the mode command and the data byte is the mode, and
the receiver masks it: `and r0, r0, #1`, so **only bit 0 matters**. On hardware
the `01` form is acknowledged by `64 00 02 01` after about seven seconds.

So **the block header message `64 02 01` is what arms a transfer.** That is
also what the receiver says: the data handler at `0x3380` refuses unless the
context holds the armed state, the header handler at `0x36ac` is what
establishes it, and the teardown at `0x3284` — category 1 command `04`, which
requires the armed state, clears it and returns code 14 — is the cancel. Every
other slot in the three dispatch tables is a `bx lr` stub.

The sequence a sender must follow is therefore fully determined:

```
F0 7E 7F 06 01 F7                    identity, expect mm = 0A
64 00 06 01                          reboot to the loader; re-enumerates
F0 7E 7F 06 01 F7                    identity, expect byte 11 = 00
64 00 00 01                          enter update mode; 64 00 02 01 at 7.04 s
  64 02 01  <packed 128-byte header>   per 256 KiB window
  64 02 02  <packet 0 .. 74>            flow-controlled by 64 01 00
  ...                                   window ends with 64 02 00
64 00 00 00                          leave update mode
64 00 06 00                          reboot to normal
```

> **`0x4004` is the reply emitter, not a commit loop.** An earlier reading of
> this material called it "finalisation: a flash-commit retry loop". It is
> reached from the mode handler, the data handler and the cancel alike, and the
> mode handler tail-calls it after staging a buffer with `mov r1, #0xb` —
> eleven bytes, exactly the length of a `64 00 02 xx` Parameter Change. It is
> how the device answers.

## Next steps, ordered by information per unit of risk

Only the first two are free of hardware risk.

1. **Write a third-party updater** that replays the SysEx protocol with the
   **official, unmodified** file. Real risk from the first write onward.
2. Only then, a minimally patched `Program` image. Note before planning any
   such patch: the `Program` image cannot be navigated by string
   cross-reference — see
   [above](#strings-in-the-program-image-cannot-be-cross-referenced).

Both steps that used to open this list are **done**: the `Installer`'s
block-receive path has been analysed, which moved the `Installer`→`Program`
step off the blocking list, and the container rebuild came back byte-identical,
which closed the write chain. What is left on the risk-free side is one probe,
below.

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
block, with the `Installer` fully written. The unit answered no SysEx for two
minutes and would not power off with `[⏻/PLAY]`. **Forced termination —
`[⏻/PLAY]` + `[PROJECT↑]`, User Guide §3.2.2 — brought it back**, and after
about thirty seconds of apparent hang on the next start it booted normally,
with `FirmwareVersion` unchanged and the owner's projects intact.
`verified on hardware`, written up in
[10-verified-behaviour.md](10-verified-behaviour.md#2026-11-05-hardware-session-an-interrupted-firmware-write-and-the-machine-came-back).

Read that bound narrowly. The file was the **same version the unit was already
running**, so a partially rewritten region received its own content: the mildest
partial write there is. It says nothing about surviving a partial write of a
modified image, which is the case custom firmware depends on. And the
interruption fell in the `Program` phase — the `Installer` phase, the first
1.6 % of a transfer, whose destination in flash is still unknown, was not
interrupted and remains the untested sliver.

Entering loader mode is reversible on one unit, five cycles — that is a bound on
the risk of *looking*, not of writing. Yamaha's own release notes say that "if
the unit becomes inoperable by accident, run the updater again", which suggests
a robust resident loader; the unit recovered without the updater being re-run,
which is better than the notice promises, but it is still one observation and
it probably does not cover an arbitrary `Program` image.

**And a warning worth more than the reassurance.** The interruption was not the
residual unknown this document had been flagging for weeks. It was a timeout in
the sender set to 5 seconds, in code written hours after this same session
measured a 7.04-second latency on this unit twice and made a point of it. The
dangerous part of this exercise turned out not to be the device.

For most of what people want from this machine, the **SysEx + external display +
third-party app** route gives far more result for far less risk. The protocol
documented in this repository already covers pattern editing — now
`verified on hardware`, writes included — live editing state, user scales, song
mode and Wi-Fi configuration: a very large control surface, with the firmware
untouched.
