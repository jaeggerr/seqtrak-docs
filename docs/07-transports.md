# 07 — Transports

Four ways to carry the same SysEx: USB MIDI, Bluetooth LE MIDI, MIDI TRS, and
Wi-Fi. At the message level they are interchangeable (`MIDI.MidiPluginInterface`
abstracts all four in the official app). What differs is who initiates, what the
defaults are, and how much you can push through.

## Send pacing

**The official app waits 2 ms after every MIDI message it sends**
(`sendIntervalTime`). `from the official app, untested`.

That single number is the one every sender needs, because almost everything
interesting here is a burst rather than a message: a pattern write is one
message per note, a bulk transfer is one per packet, and a firmware update is
hundreds of thousands. At 2 ms the budget is 500 messages per second, so:

| Work | Messages | Time at 2 ms |
|---|---|---|
| Write 16 notes into a pattern | 16 | 32 ms |
| Read a 64-step pattern | 64 | 128 ms |
| Fill 11 tracks × 64 steps | 704 | 1.4 s |

Yamaha's own pacing is the safest default: it is what the hardware is known to
cope with. Going faster has not been tested, and the device's flow control does
not cover Parameter Changes — only bulk transfers acknowledge. Note that a
Parameter **Request** round trip takes about 250 ms
(`verified on hardware`, [below](#latency)), which is a separate budget: pacing
limits how fast you can *write*, latency limits how fast you can *ask*.

## USB MIDI

The USB-C port does both roles.

| `00 00 17` `USB Role` | Meaning |
|---|---|
| `0` | **To Host** — the SEQTRAK is a USB *device*; a computer is the host |
| `1` | **To Device** — the SEQTRAK is the USB *host*; it powers and drives a class-compliant MIDI device |

`from Yamaha Data List`.

### SEQTRAK as host ("To Device")

This is the mode in which the SEQTRAK powers an attached controller or display.
It supplies **up to 500 mA**, and **nothing at all** when its own battery is at
2 Global-Meter LEDs or fewer (User Guide §15.2.1).

What a device attached this way actually receives, `verified on hardware` over
a 2026-08 session with an ESP32-S3 running TinyUSB:

- **Notes** on each track's own MIDI channel: yes.
- **SysEx**, including live-state Parameter Changes from the `01 10 xx` zone:
  yes — despite `00 00 10` `USB MIDI TX SysEx` being documented as `Off` by
  default. **But two negative conclusions drawn in this session were later
  disproved** (Bank Select, and the FX sliders) — not because of a parsing
  fault, but because they were read off a nine-line scrolling log while bursts
  of ~105 messages arrived in ~1.2 seconds. If you are going to claim the
  machine never sends something, count messages cumulatively or capture the
  whole stream; a live scrolling view cannot support a negative claim. See
  [10-verified-behaviour.md](10-verified-behaviour.md#the-august-no-sysex-claim-falls--and-why).
- **Transport** `FA` / `FB` / `FC`: yes.
- **Program Change**: yes. **Bank Select** was not seen in this session, even
  across a bank boundary — but that observation has since been overturned; the
  machine does transmit it, and the fault was most likely on the receiving
  side. See
  [10-verified-behaviour.md](10-verified-behaviour.md#bank-select-is-transmitted--a-documented-conclusion-reversed).
- **MIDI clock `F8`: not received** — but only because `00 00 2D`
  `MIDI Clock Out` was `Off` on that unit. Reading the setting back confirmed
  it; turning it on makes the clock arrive, at 24 ppqn.
- The SEQTRAK **answers Parameter Requests** in this direction, so a host-mode
  peripheral can read the tempo, the system settings and the live state without
  the app.
- It **answers Bulk Dump Requests** too: a single-track request `11 02 pp`
  returns the burst of blocks described in
  [06-sounds-presets.md](06-sounds-presets.md).

> **About 95 % of the USB traffic is padding.** Transfers are fixed-size and
> filled out with null USB-MIDI packets (code index number `0x0`). Filter them
> or they will drown everything else.

### SEQTRAK as device ("To Host")

The ordinary case: a computer sees a CoreMIDI / ALSA / Windows MIDI endpoint
whose name contains `SEQTRAK`. Discovery is a substring match on the endpoint
name in every implementation here. Both an input and an output endpoint appear.

USB also carries **24-bit / 44.1 kHz audio**, 2 in and 2 out, over the same
cable. A computer supplies at most 500 mA, which can drain the SEQTRAK's battery
while playing.

### Latency

A Parameter Request round trip takes **about 250 ms** over USB MIDI
(`verified on hardware`). Fast enough that filling a display from cold reads as
a transition rather than a wait, and fast enough to follow preset scrolling at
the knob — including the ~30-block single-track bulk dump used to read a preset
name — with no perceptible lag.

### Send pacing — the official app waits 2 ms between messages

`from the official app, untested`. The app does not stream messages
back to back: it sleeps **2 ms** on the sending thread after every message,
over USB and over BLE alike. The interval is configurable in the app, but it
is never changed from its default, so 2 ms is what the official app actually
uses.

**Practical consequence.** A host writing a whole pattern or a whole song
should pace at 2 ms as well: it is the rate the hardware is known to tolerate,
and it still allows ~500 messages per second, which is far more than any
realistic write needs. See
[14-song-mode.md](14-song-mode.md#budget-the-throughput-is-not-the-problem).

### Transport reliability

An isolated Parameter Request is **occasionally lost**: measured at roughly
1 in 10 over USB MIDI, on two different addresses, uncorrelated.
`verified on hardware`. Never read a missing reply as information — retry (four
attempts was enough) and keep a known-good control address in any test loop.
Details in
[10-verified-behaviour.md](10-verified-behaviour.md#transport-reliability).

## Bluetooth LE MIDI

The SEQTRAK advertises as a **BLE MIDI peripheral**; the host connects as
central. It uses the standard MMA/AMEI MIDI-over-BLE service, with no
proprietary extension.

| | |
|---|---|
| Service UUID | `03B80E5A-EDE8-4B33-A751-6CE34EC4C700` |
| Data I/O characteristic UUID | `7772E5DB-3868-4112-A1A9-F2669D106BF3` |
| Local name | starts with `SEQTRAK` |
| Characteristic properties | `notify`, `writeWithoutResponse`, `read` — **no plain `write`** on the unit measured 2026-10-22, so `.withoutResponse` is the only output path |

**The UUIDs are the MMA/AMEI standard ones**, not SEQTRAK-specific, which is
what makes them trustworthy here: they are fixed by the BLE-MIDI specification
rather than discovered. They were read out of a Swift package in this tree
(`seqtrak-lib`) — a consumer of this documentation, so not an independent
source, and note that package's own receive parser is marked as non-working.
The service and characteristic identifiers themselves stand on the
specification.

### Discovery and connection

1. Scan for peripherals advertising the MIDI service UUID; accept the one whose
   `CBAdvertisementDataLocalNameKey` starts with `SEQTRAK`.
2. Once a peripheral is known, reconnect by identifier —
   `retrieveConnectedPeripherals(withServices:)` first, then
   `retrievePeripherals(withIdentifiers:)` — which is far faster than scanning
   again. Sub-second reconnection is achievable from a cached identifier.
3. Discover the service and characteristic, then `setNotifyValue(true)` on the
   data I/O characteristic.
4. Write with `.withoutResponse` when the characteristic advertises that
   property, otherwise `.withResponse`.

### Pairing on the hardware

Press `[ALL]` + `[SWING]`; the SEQTRAK then waits **30 seconds** for a
connection, and the Global Meter indicates the state. Only **one BLE central at
a time** — connecting a second host takes the link from the first.
From the User Guide, §15.1.2, p. 90.

### BLE MIDI packet framing

> **This section was wrong until 2026-10-22.** It described a two-byte
> running timestamp and said you could tell a timestamp from a status byte by
> position. Both are false, and the description was taken from a Swift package
> in this tree that nothing imports and that provably emits **zero** events for
> any conformant packet — I cited a consumer as though it were a measurement.
> See [evidence discipline](../AGENTS.md). What follows traces back to the MMA
> specification and the official Yamaha plug-in — see
> [provenance](#provenance-of-this-section), which says exactly whose reading of
> them this is.

**A BLE packet is a container, not a message.** Several messages can share one
packet, a message can be cut anywhere between two packets, and running status
carries across packets.

```
byte 0        10tttttt   header: bits 12-7 of a 13-bit millisecond timestamp
byte 1        1ttttttt   timestamp low: bits 6-0
bytes 2…      MIDI data, with single-byte timestamps interleaved
```

Note the two details that are easy to get wrong:

- The header carries **six** timestamp bits (`header & 0x3F`), not seven.
- Within a packet a timestamp is **one** byte, `0x80 | (time & 0x7F)`. The
  two-byte form appears **once**, at the start of the packet. Consuming two
  bytes for an interleaved timestamp eats the status byte after it.

**Measured on hardware, 2026-10-22.** A tempo reply over BLE, whole packet:

```
B1 89 F0 43 10 7F 1C 0C 30 40 76 00 7B 89 F7
└─ header
   └─ timestamp, ONE byte
                                           └─ timestamp again, then F7
```

The terminator is preceded by its own timestamp, repeating the value used at the
start of the message. Two SysEx captured, two timestamped terminators, zero
un-timestamped. So **a decoder must expect a timestamp in front of `F7`** — and
the two-byte running timestamp this section once described would have
mis-parsed this packet.

**The hard part: a byte with bit 7 set is ambiguous.** A timestamp byte is
`0x80 | (time & 0x7F)`, so by value alone it is indistinguishable from any
status byte, `F8`-`FF` included. The answer is never in the byte — it is in what
was expected next. That is why this needs a **state machine**, not a filter: any
stateless pass has to guess, and every guess has a counter-example that
silently drops a message.

Three disambiguation rules that matter:

- Inside a SysEx, the only bit-7 bytes are `F7`, a System Real-Time byte, or a
  timestamp introducing one of those. Recognising `F7` here is what stops an
  un-timestamped terminator from being eaten as a timestamp.
- The **last byte of a packet** cannot be a timestamp — there is nothing left
  for it to stamp — so it is a status byte.
- A long SysEx is split across packets, so reassembly must span them: accumulate
  from `F0` until `F7`, with a length cap to bound a malformed stream.

Message lengths, status byte included — the **effective** lengths, which is not
the same as the bytes of the plug-in's table:

| Status | Length |
|---|---|
| `0x80`-`0xBF` (note off/on, aftertouch, CC) | 3 |
| `0xC0`-`0xDF` (program change, channel pressure) | 2 |
| `0xE0`-`0xEF` (pitch bend) | 3 |
| `0xF0` | variable — read to `0xF7` |
| `0xF1` (MTC quarter frame) | 2 |
| `0xF2` (song position pointer) | 3 |
| `0xF3` (song select) | 2 |
| `0xF6` (tune request) | 1 |
| `0xF4`, `0xF5`, `0xF9`, `0xFD` | **0 — undefined, ignore, do not emit** |
| `0xF8`, `0xFA`, `0xFB`, `0xFC`, `0xFE`, `0xFF` (system real-time) | 1 |

> **Do not derive this table from the official app's raw length table.** Read
> literally, that table gives `F4`, `F5`, `F9` and `FD` a length of **1** —
> "emit them" — which is wrong, and wrong in exactly the direction that
> produces phantom messages. The app masks those status bytes out before the
> lookup and returns 0 for them. The table above is the post-mask result.
> `from the official app, untested`.

The official plug-in uses a nine-state machine for this (`BLE_HANDLER_STATE`),
which is a useful sanity check on the shape of any implementation.

### Provenance of this section

Worth being exact about, because getting it wrong once is what made the previous
version of this section unusable.

- The **independent witness** is the official app's own BLE-MIDI handling,
  plus the MMA BLE-MIDI specification. Both were read by the session that wrote
  the implementation below.
- **This section derives from that implementation**, at
  `seqtrak-apple/Packages/SeqtrakConnect/Sources/SeqtrakConnect/BLE/`
  (`BLEMIDIParser.swift` for receive, `BLEMIDIFraming.swift` for send) — some
  of the reasoning above is paraphrased from its comments. So agreement between
  this document and that code is **inheritance, not confirmation**, and neither
  corroborates the other. Both trace back to the official app and the specification.

That implementation is the one to port or consult. The parser in the
`seqtrak-lib` package in this tree is **not** — it is unused and emits no events
for any conformant packet, and it is where this section's earlier errors came
from.

### Bluetooth defaults are hostile

**Every Bluetooth transmit flag is off by default.** Over BLE, a freshly
unboxed SEQTRAK sends nothing useful.

| Address | Parameter | Default | Needed for a mirror |
|---|---|---|---|
| `00 00 11` | Bluetooth MIDI In/Out | `00` (off) | `01` |
| `00 00 13` | BT MIDI TX CC / Bank Select / Program Change | `00` (nothing) | `0x70` (all three bits) |
| `00 00 14` | BT MIDI TX SysEx | `00` (off) | `01` |
| `00 00 2D` | MIDI Clock Out | `01` | keep on |

`from Yamaha Data List`. Without `00 00 13` a host never sees a knob move;
without `00 00 14` it never sees the live-state broadcasts.

#### What a machine in use actually reads — `verified on hardware`

The defaults above are the Data List's. They are **not** what this unit reads
(2026-10-22, read over USB, four attempts each, tempo interleaved as a live
control, 4/4 on every address):

| Address | Parameter | Data List default | Read on this unit |
|---|---|---|---|
| `00 00 11` | Bluetooth MIDI In/Out | `00` | **`00`** — off |
| `00 00 13` | BT MIDI TX CC / BS / PC | `00` | **`70`** — all three bits already set |
| `00 00 14` | BT MIDI TX SysEx | `00` | **`01`** — already on |

So "every Bluetooth transmit flag is off by default" does not describe a
machine that has been used: the two **transmit** flags were already on. A
client that blindly writes all three is writing two values that were already
correct.

> **Do not read `00 00 11` = `00` as "Bluetooth is off".** Later the same day a
> CoreBluetooth central was connected to this unit and carried Control Change,
> Program Change, clock and active sensing, while `00 00 11` still read `00` on
> four consecutive requests. An earlier revision of this section called it the
> master switch that had to be turned on; that is **contradicted**. See
> [the BLE measurement](10-verified-behaviour.md#two-readings-of-the-bluetooth-flags-are-contradicted).

**Read all three before writing any of them** — the repository's standing rule
9 (*read the settings; do not assume the defaults*), confirmed again here.

Writing these changes the user's device settings, so a client should do it as an
explicit, reversible action: snapshot the previous values first and offer to
restore them.

## MIDI TRS ("legacy")

MIDI IN and OUT on 3.5 mm jacks, via the converter cable included in the box —
**only that cable works**. Gated by `00 00 09` (In/Out), `00 00 0A` (channel
messages), `00 00 0B` (CC / Bank Select / Program Change bitmask) and
`00 00 0C` (SysEx). MIDI Thru for this interface is **off** by default.

Active Sensing (`FE`) matters here: once sensing has started, a gap of about
500 ms clears the receive buffer and forces playing notes off.
`from Yamaha Data List`.

## Wi-Fi

Wi-Fi is a **proprietary transport over IP**, used by the official app for bulk
content transfer and for audio streaming. It is not a MIDI transport in the
usual sense, and the audio stream is a separate protocol this repository does
not document.

What *is* documented: **the SEQTRAK's Wi-Fi can be configured entirely over
SysEx.** No app is needed to put it on a network. `from the official app, untested`, except `00 60 00`, `00 60 01` and `00 00 16`, which are
`verified on hardware` (all read `0` on a unit with Wi-Fi off).

### `00 60 xx` — general

| `al` | Parameter | Size | Range |
|---|---|---|---|
| `00` | `WiFiMode` | 1 | 0-1 |
| `01` | `WiFiReady` | 1 | 0-1 |
| `02` | `WiFiAudio` | 1 | 0-1 |
| `06` | `CountryCode` | 2 | string |
| `08` | `PortNumber` | 8 | string |

The app's own UI writes `00 00 16` (`Wireless LAN`, the global switch) **and
then** `00 60 01` (`WiFiReady`). The order matters: bring the radio up, then
signal that it is ready.

### `00 61 xx` — station mode (join an existing network)

| `al` | Parameter | Size |
|---|---|---|
| `00` | `SecurityProtocolSTA` (0-7) | 1 |
| `01` | `DHCPClientSwitch` (0-1) | 1 |
| `02` | `Connection` (0-1) | 1 |
| `10` | `SSID_STA` | 32 |
| `30` | `SecurityKeySTA` | 64 |
| `70` | `IPAddressSTA` | 16 |

### `00 62 xx` — access-point mode

| `al` | Parameter | Size |
|---|---|---|
| `00` | `SecurityProtocolAP` (0-7) | 1 |
| `10` | `SSID_AP` | 32 |
| `30` | `SecurityKeyAP` | 64 |
| `70` | `IPAddressAP` | 16 |

Text fields use the 7-into-8 packing from
[02-sysex-format.md](02-sysex-format.md#strings-and-blobs-7-into-8-packing).
`WiFiStartupResult` (`01 10 06`, 0-7) reports the outcome of a connection
attempt.

> **A Wi-Fi key written over SysEx travels in clear text on the MIDI link.**
> Harmless over a direct USB cable; worth remembering if you are logging
> traffic to a file.

### Host side

The official app's Wi-Fi plug-in does the rest on the computer:
`WiFiPluginRequestSSID`, `WiFiPluginGetSecurityType`,
`WiFiPluginSearchIPAddress` (finds the machine on the network),
`WiFiPluginStartRecording` / `StopRecording` (**audio over Wi-Fi**), plus the
callbacks `SetReceivingCallback`, `SetReceivedHeaderCallback` and
`SetSamplingCallback`. `from the official app, untested`.

Bluetooth pairing is required before Wi-Fi can be used with the app.

## Choosing a transport

| Need | Use |
|---|---|
| Bus power for a companion device | USB, SEQTRAK as host — mind the 500 mA and 2-LED limits |
| Lowest-friction development | USB, SEQTRAK as device |
| Audio in or out | USB (24-bit, 44.1 kHz) |
| No cable, wearable or phone host | BLE MIDI — but write the three transmit flags first |
| Bulk content, samples, firmware over the air | Wi-Fi, after BLE pairing |
| Hardware sequencer sync to other gear | MIDI TRS, with `00 00 2D` on |

Not supported: Bluetooth and Wi-Fi on Windows.
