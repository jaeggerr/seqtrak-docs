# Project, tracks and master effects (`30 xx xx`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

917 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `30 00 00` | Track/Project | AddNoteEvent | 1 | 0 - 0 (decimal) |  | 0 - 8 | `AddNoteEvent` |  | from the official app, untested |
| `30 00 70` | Track/Project | DrumLockPitch | 1 | 0 - 127 (decimal) |  | -24 - 24 | `DrumLockPitch` |  | from the official app, untested |
| `30 00 71` | Track/Project | DrumLockSubStep | 1 | 0 - 127 (decimal) |  | 1 - 4 | `DrumLockSubStep` |  | from the official app, untested |
| `30 00 73` | Track/Project | DrumLockVelocity | 1 | 0 - 127 (decimal) |  | -10 - 10 | `DrumLockVelocity` |  | from the official app, untested |
| `30 40 00` | Project Common / General | Project Name 1 | 1 | 00 - 7F | 00 |  | `` | UTF8 (7-bit encoded) | from Yamaha Data List |
| `30 40 01` | Project Common / General | Project Name 2 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 02` | Project Common / General | Project Name 3 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 03` | Project Common / General | Project Name 4 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 04` | Project Common / General | Project Name 5 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 05` | Project Common / General | Project Name 6 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 06` | Project Common / General | Project Name 7 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 07` | Project Common / General | Project Name 8 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 08` | Project Common / General | Project Name 9 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 09` | Project Common / General | Project Name 10 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 0A` | Project Common / General | Project Name 11 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 0B` | Project Common / General | Project Name 12 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 0C` | Project Common / General | Project Name 13 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 0D` | Project Common / General | Project Name 14 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 0E` | Project Common / General | Project Name 15 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 0F` | Project Common / General | Project Name 16 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 10` | Project Common / General | Project Name 17 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 11` | Project Common / General | Project Name 18 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 12` | Project Common / General | Project Name 19 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 13` | Project Common / General | Project Name 20 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 14` | Project Common / General | Project Name 21 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 15` | Project Common / General | Project Name 22 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 16` | Project Common / General | Project Name 23 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 17` | Project Common / General | Project Name 24 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 18` | Project Common / General | Project Name 25 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 19` | Project Common / General | Project Name 26 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 1A` | Project Common / General | Project Name 27 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 1B` | Project Common / General | Project Name 28 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 1C` | Project Common / General | Project Name 29 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 1D` | Project Common / General | Project Name 30 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 1E` | Project Common / General | Project Name 31 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 1F` | Project Common / General | Project Name 32 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 20` | Project Common / General | Project Name 33 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 21` | Project Common / General | Project Name 34 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 22` | Project Common / General | Project Name 35 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 23` | Project Common / General | Project Name 36 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 24` | Project Common / General | Project Name 37 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 25` | Project Common / General | Project Name 38 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 26` | Project Common / General | Project Name 39 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 27` | Project Common / General | Project Name 40 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 28` | Project Common / General | Project Name 41 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 29` | Project Common / General | Project Name 42 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 2A` | Project Common / General | Project Name 43 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 2B` | Project Common / General | Project Name 44 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 2C` | Project Common / General | Project Name 45 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 2D` | Project Common / General | Project Name 46 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 2E` | Project Common / General | Project Name 47 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 2F` | Project Common / General | Project Name 48 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 30` | Project Common / General | Project Name 49 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 31` | Project Common / General | Project Name 50 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 32` | Project Common / General | Project Name 51 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 33` | Project Common / General | Project Name 52 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 34` | Project Common / General | Project Name 53 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 35` | Project Common / General | Project Name 54 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 36` | Project Common / General | Project Name 55 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 37` | Project Common / General | Project Name 56 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 38` | Project Common / General | Project Name 57 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 39` | Project Common / General | Project Name 58 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 3A` | Project Common / General | Project Name 59 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 3B` | Project Common / General | Project Name 60 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 3C` | Project Common / General | Project Name 61 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 3D` | Project Common / General | Project Name 62 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 3E` | Project Common / General | Project Name 63 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 3F` | Project Common / General | Project Name 64 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 40` | Project Common / General | Project Name 65 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 41` | Project Common / General | Project Name 66 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 42` | Project Common / General | Project Name 67 | 1 | 00 - 7F | 00 |  | `` | UTF8 (7-bit encoded) | from Yamaha Data List |
| `30 40 43` | Project Common / General | Project Name 68 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 44` | Project Common / General | Project Name 69 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 45` | Project Common / General | Project Name 70 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 46` | Project Common / General | Project Name 71 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 47` | Project Common / General | Project Name 72 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 48` | Project Common / General | Project Name 73 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 49` | Project Common / General | Project Name 74 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 4A` | Project Common / General | Project Name 75 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 4B` | Project Common / General | Project Name 76 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 4C` | Project Common / General | Project Name 77 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 4D` | Project Common / General | Project Name 78 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 4E` | Project Common / General | Project Name 79 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 4F` | Project Common / General | Project Name 80 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 50` | Project Common / General | Project Name 81 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 51` | Project Common / General | Project Name 82 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 52` | Project Common / General | Project Name 83 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 53` | Project Common / General | Project Name 84 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 54` | Project Common / General | Project Name 85 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 55` | Project Common / General | Project Name 86 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 56` | Project Common / General | Project Name 87 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 57` | Project Common / General | Project Name 88 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `30 40 58` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 59` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 5A` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 5B` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 5C` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 5D` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 5E` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 5F` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 60` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 61` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 62` | Project Common / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `30 40 63` | Project Common / General | Sampler Element Mute | 1 | 00 - 7F | 00 | bit6-0: element7-1 mute off,on | `SamplerElementMute` |  | from Yamaha Data List |
| `30 40 64` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 65` | Project Common / General | Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `` |  | from Yamaha Data List |
| `30 40 66` | Project Common / General | Volume | 1 | 00 - 7F | 7F | 0 - 127 | `Volume` |  | from Yamaha Data List |
| `30 40 67` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 68` | Project Common / General | Solo Track | 1 | 00 - 0B | 00 | Off, Track 1, ..., Track 11 | `SoloTrack` |  | from Yamaha Data List |
| `30 40 69` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 6A` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 6B` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 6C` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 6D` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 6E` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 6F` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 70` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 71` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 72` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 73` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 74` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 75` | Project Common / General | ARP Synchro Quantize Value | 1 | 05 | 05 | 240 | `` |  | from Yamaha Data List |
| `30 40 76` | Project Common / General | Tempo MSB Tempo LSB | 2 | 00 - 02 00 - 7F | 00 78 | 5 - 300 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `Tempo` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered through a long-lived client immediately after the USB cable was pulled and restored six minutes later: the transport reports LOST then CONNECTED and the link really works again — also `from Yamaha Data List` |
| `30 40 78` | Project Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 40 79` | Project Common / General | Pattern Select Mode | 1 | 00 - 01 | 00 | 0=normal, 1=advanced | `PatternSelectMode` |  | `verified on hardware` ([04-sequencer-editing.md](04-sequencer-editing.md)) — Pattern Select clamps at 2 while this reads 0, and reaches 5 when it reads 1 — also `from Yamaha Data List` |
| `30 40 7A` | Project Common / General | Pattern Master Step MSB | 2 | 00 - 01 00 - 7F | 00 10 | 1 - 128 | `PatternMasterStep` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered with 2 data bytes, 01 00 = 128 (Pattern Master Step); 30 40 7B does not answer separately, it is this field LSB; written 48 and read back on 2026-10-23 — also `from Yamaha Data List` |
| `30 40 7C` | Project Common / General | Pattern Master Step LSB Swing Offset MSB Swing Offset LSB | 2 | 00 - 01 00 - 7F | 01 00 | 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 -58 - 0 - +58 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `Swing` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Swing Offset alone, 2 data bytes; a write sweep with restore accepted 70 and 186 and clamped 69 and 187 to them, so the field is centred on 128 and display = value - 128 — also `from Yamaha Data List` |
| `30 40 7E` | Project Common / General | Scale | 1 | 00 - 07 | 00 | Scale 1, ..., Scale 8 | `Scale` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 00 (Scale 1) and read it back — also `from Yamaha Data List` |
| `30 40 7F` | Project Common / General | Key | 1 | 40 - 4B | 40 | 0 - +11 | `Key` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 40 (key C) and read it back — also `from Yamaha Data List` |
| `30 41 00` | Project Common / Send Reverb | Reverb Type MSB Reverb Type LSB | 2 | 00 - 7F 00 - 7F | 01 01 | Refer to Effect Parameter List | `ReverbType` | R3 Hall | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Send Reverb block read in full: 38 of 38 documented addresses answered; Reverb Type read 01 00 — also `from Yamaha Data List` |
| `30 41 02` | Project Common / Send Reverb | Reverb Template Number | 1 | 00 - 7F | 00 | ˶ | `` | Basic | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 (Basic) as the send reverb template after a type write — also `from Yamaha Data List` |
| `30 41 03` | Project Common / Send Reverb | Reverb Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 00 30 = 48 (Reverb Time) and read it back — the al = 01 | (k<<1) effect-parameter offset confirmed on a send block — also `from Yamaha Data List` |
| `30 41 05` | Project Common / Send Reverb | Reverb Parameter 1 LSB Reverb Parameter 2 MSB Reverb Parameter 2 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 07` | Project Common / Send Reverb | Reverb Parameter 3 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 09` | Project Common / Send Reverb | Reverb Parameter 3 LSB Reverb Parameter 4 MSB Reverb Parameter 4 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 0B` | Project Common / Send Reverb | Reverb Parameter 5 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — written 00 32 and read back, with witness 30 41 09 unmoved and restored to 00 2C: a two-byte Parameter Change is accepted. A one-byte write of 28 to the same address was ignored, leaving 00 2C — also `from Yamaha Data List` |
| `30 41 0D` | Project Common / Send Reverb | Reverb Parameter 5 LSB Reverb Parameter 6 MSB Reverb Parameter 6 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 0F` | Project Common / Send Reverb | Reverb Parameter 7 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 11` | Project Common / Send Reverb | Reverb Parameter 7 LSB Reverb Parameter 8 MSB Reverb Parameter 8 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 13` | Project Common / Send Reverb | Reverb Parameter 9 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 15` | Project Common / Send Reverb | Reverb Parameter 9 LSB Reverb Parameter 10 MSB Reverb Parameter 10 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 17` | Project Common / Send Reverb | Reverb Parameter 11 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 19` | Project Common / Send Reverb | Reverb Parameter 11 LSB Reverb Parameter 12 MSB Reverb Parameter 12 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 1B` | Project Common / Send Reverb | Reverb Parameter 13 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 1D` | Project Common / Send Reverb | Reverb Parameter 13 LSB Reverb Parameter 14 MSB Reverb Parameter 14 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 1F` | Project Common / Send Reverb | Reverb Parameter 15 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 21` | Project Common / Send Reverb | Reverb Parameter 15 LSB Reverb Parameter 16 MSB Reverb Parameter 16 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 23` | Project Common / Send Reverb | Reverb Parameter 17 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 25` | Project Common / Send Reverb | Reverb Parameter 17 LSB Reverb Parameter 18 MSB Reverb Parameter 18 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 27` | Project Common / Send Reverb | Reverb Parameter 19 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 29` | Project Common / Send Reverb | Reverb Parameter 19 LSB Reverb Parameter 20 MSB Reverb Parameter 20 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 2B` | Project Common / Send Reverb | Reverb Parameter 21 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 2D` | Project Common / Send Reverb | Reverb Parameter 21 LSB Reverb Parameter 22 MSB Reverb Parameter 22 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 2F` | Project Common / Send Reverb | Reverb Parameter 23 MSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | ˶ init | `` |  | from Yamaha Data List |
| `30 41 31` | Project Common / Send Reverb | Reverb Parameter 23 LSB Reverb Parameter 24 MSB Reverb Parameter 24 LSB | 2 | 00 - 7F 00 - 7F | value for Hall / Basic | Rev-X ˶ init Rev-X | `` |  | from Yamaha Data List |
| `30 41 33` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — reserved: answers one byte, not the documented two, and the address the table skips (30 41 34) answers one byte as well — a one-byte slot at a two-byte stride — also `from Yamaha Data List` |
| `30 41 35` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 37` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 39` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 3B` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 3D` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 3F` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 41` | Project Common / Send Reverb | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 43` | Project Common / Send Reverb | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 41 44` | Project Common / Send Reverb | Reverb Return | 1 | 00 - 7F | 2E | 0 - 127 | `ReverbReturn` |  | from Yamaha Data List |
| `30 41 45` | Project Common / Send Reverb | Reverb Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `` |  | from Yamaha Data List |
| `30 41 46` | Project Common / Send Reverb | Reverb On/Off | 1 | 00 - 7F | 01 | Off, On | `` |  | from Yamaha Data List |
| `30 42 00` | Project Common / Send Delay | Variation Type MSB Variation Type LSB | 2 | 00, 02 00 - 7F | 02 28 | Refer to Effect Parameter List | `VariationType` | Cross Delay | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Send Delay block read in full: 39 of 39 documented addresses answered — also `from Yamaha Data List` |
| `30 42 02` | Project Common / Send Delay | Variation Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `30 42 03` | Project Common / Send Delay | Variation Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 05` | Project Common / Send Delay | Variation Parameter 1 LSB Variation Parameter 2 MSB Variation Parameter 2 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 8 (Delay Time R>L, 8th) and read it back — also `from Yamaha Data List` |
| `30 42 07` | Project Common / Send Delay | Variation Parameter 3 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 92 (Feedback Level, 28 of 63) and read it back — also `from Yamaha Data List` |
| `30 42 09` | Project Common / Send Delay | Variation Parameter 3 LSB Variation Parameter 4 MSB Variation Parameter 4 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 0B` | Project Common / Send Delay | Variation Parameter 5 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 6 (Feedback High Damp) and read it back — also `from Yamaha Data List` |
| `30 42 0D` | Project Common / Send Delay | Variation Parameter 5 LSB Variation Parameter 6 MSB Variation Parameter 6 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 0F` | Project Common / Send Delay | Variation Parameter 7 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 11` | Project Common / Send Delay | Variation Parameter 7 LSB Variation Parameter 8 MSB Variation Parameter 8 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 13` | Project Common / Send Delay | Variation Parameter 9 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 15` | Project Common / Send Delay | Variation Parameter 9 LSB Variation Parameter 10 MSB Variation Parameter 10 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 90 (Dry/Wet Balance), read back 0 — bypassed on a send block while params 1, 2, 3 and 5 of the same block took — also `from Yamaha Data List` |
| `30 42 17` | Project Common / Send Delay | Variation Parameter 11 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 19` | Project Common / Send Delay | Variation Parameter 11 LSB Variation Parameter 12 MSB Variation Parameter 12 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 1B` | Project Common / Send Delay | Variation Parameter 13 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 1D` | Project Common / Send Delay | Variation Parameter 13 LSB Variation Parameter 14 MSB Variation Parameter 14 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 1F` | Project Common / Send Delay | Variation Parameter 15 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 21` | Project Common / Send Delay | Variation Parameter 15 LSB Variation Parameter 16 MSB Variation Parameter 16 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 23` | Project Common / Send Delay | Variation Parameter 17 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 25` | Project Common / Send Delay | Variation Parameter 17 LSB Variation Parameter 18 MSB Variation Parameter 18 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 27` | Project Common / Send Delay | Variation Parameter 19 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 29` | Project Common / Send Delay | Variation Parameter 19 LSB Variation Parameter 20 MSB Variation Parameter 20 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 2B` | Project Common / Send Delay | Variation Parameter 21 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 2D` | Project Common / Send Delay | Variation Parameter 21 LSB Variation Parameter 22 MSB Variation Parameter 22 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 2F` | Project Common / Send Delay | Variation Parameter 23 MSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | ˶ init | `` |  | from Yamaha Data List |
| `30 42 31` | Project Common / Send Delay | Variation Parameter 23 LSB Variation Parameter 24 MSB Variation Parameter 24 LSB | 2 | 00 - 7F 00 - 7F | value for Delay Cross Delay | / ˶ init / | `` |  | from Yamaha Data List |
| `30 42 33` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 35` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 37` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 39` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 3B` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 3D` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 3F` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 41` | Project Common / Send Delay | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 42 43` | Project Common / Send Delay | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 42 44` | Project Common / Send Delay | Variation Return | 1 | 00 - 7F | 60 | 0 - 127 | `VariationReturn` |  | from Yamaha Data List |
| `30 42 45` | Project Common / Send Delay | Variation Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `` |  | from Yamaha Data List |
| `30 42 46` | Project Common / Send Delay | Send Variation To Reverb | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `30 42 47` | Project Common / Send Delay | Variation On/Off | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `30 43 00` | Master Effect | Master Effect Type MSB Master Effect Type LSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | Refer to Effect Parameter List Refer | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Master Effect 1 type read 0C 28 = CONTROL FILTER; all five slots that type names read inside their documented ranges — also `from Yamaha Data List` |
| `30 43 02` | Master Effect | Master Effect Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `30 43 03` | Master Effect | Master Effect Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | ˶ Refer | `` |  | from Yamaha Data List |
| `30 43 05` | Master Effect | Master Effect Parameter 1 LSB Master Effect Parameter 2 MSB Master Effect Parameter 2 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 07` | Master Effect | Master Effect Parameter 3 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 09` | Master Effect | Master Effect Parameter 3 LSB Master Effect Parameter 4 MSB Master Effect Parameter 4 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 0B` | Master Effect | Master Effect Parameter 5 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 0D` | Master Effect | Master Effect Parameter 5 LSB Master Effect Parameter 6 MSB Master Effect Parameter 6 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 0F` | Master Effect | Master Effect Parameter 7 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 11` | Master Effect | Master Effect Parameter 7 LSB Master Effect Parameter 8 MSB Master Effect Parameter 8 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 13` | Master Effect | Master Effect Parameter 9 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 15` | Master Effect | Master Effect Parameter 9 LSB Master Effect Parameter 10 MSB Master Effect Parameter 10 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 17` | Master Effect | Master Effect Parameter 11 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 19` | Master Effect | Master Effect Parameter 11 LSB Master Effect Parameter 12 MSB Master Effect Parameter 12 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 1B` | Master Effect | Master Effect Parameter 13 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 1D` | Master Effect | Master Effect Parameter 13 LSB Master Effect Parameter 14 MSB Master Effect Parameter 14 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 1F` | Master Effect | Master Effect Parameter 15 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 21` | Master Effect | Master Effect Parameter 15 LSB Master Effect Parameter 16 MSB Master Effect Parameter 16 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 23` | Master Effect | Master Effect Parameter 17 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 25` | Master Effect | Master Effect Parameter 17 LSB Master Effect Parameter 18 MSB Master Effect Parameter 18 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 27` | Master Effect | Master Effect Parameter 19 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 29` | Master Effect | Master Effect Parameter 19 LSB Master Effect Parameter 20 MSB Master Effect Parameter 20 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 2B` | Master Effect | Master Effect Parameter 21 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 2D` | Master Effect | Master Effect Parameter 21 LSB Master Effect Parameter 22 MSB Master Effect Parameter 22 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 2F` | Master Effect | Master Effect Parameter 23 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 31` | Master Effect | Master Effect Parameter 23 LSB Master Effect Parameter 24 MSB Master Effect Parameter 24 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 43 33` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 35` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 37` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 39` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 3B` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 3D` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 3F` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 41` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 43 43` | Master Effect | Side Chain Part | 1 | 11, 7F | 7F | 17:Master, 127:Off | `` |  | from Yamaha Data List |
| `30 43 44` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 43 45` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 43 46` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 43 47` | Master Effect | Master Effect ON/OFF | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `30 44 00` | Master Effect | Master Effect Type MSB Master Effect Type LSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | Refer to Effect Parameter List Refer | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 02 10 (TEMPO CROSS DELAY) as Master Effect 2 and read it back — also `from Yamaha Data List` |
| `30 44 02` | Master Effect | Master Effect Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `30 44 03` | Master Effect | Master Effect Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | ˶ Refer | `` |  | from Yamaha Data List |
| `30 44 05` | Master Effect | Master Effect Parameter 1 LSB Master Effect Parameter 2 MSB Master Effect Parameter 2 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 07` | Master Effect | Master Effect Parameter 3 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 09` | Master Effect | Master Effect Parameter 3 LSB Master Effect Parameter 4 MSB Master Effect Parameter 4 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 0B` | Master Effect | Master Effect Parameter 5 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 0D` | Master Effect | Master Effect Parameter 5 LSB Master Effect Parameter 6 MSB Master Effect Parameter 6 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 0F` | Master Effect | Master Effect Parameter 7 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 11` | Master Effect | Master Effect Parameter 7 LSB Master Effect Parameter 8 MSB Master Effect Parameter 8 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 13` | Master Effect | Master Effect Parameter 9 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 15` | Master Effect | Master Effect Parameter 9 LSB Master Effect Parameter 10 MSB Master Effect Parameter 10 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 17` | Master Effect | Master Effect Parameter 11 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 19` | Master Effect | Master Effect Parameter 11 LSB Master Effect Parameter 12 MSB Master Effect Parameter 12 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 1B` | Master Effect | Master Effect Parameter 13 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 1D` | Master Effect | Master Effect Parameter 13 LSB Master Effect Parameter 14 MSB Master Effect Parameter 14 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 1F` | Master Effect | Master Effect Parameter 15 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 21` | Master Effect | Master Effect Parameter 15 LSB Master Effect Parameter 16 MSB Master Effect Parameter 16 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 23` | Master Effect | Master Effect Parameter 17 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 25` | Master Effect | Master Effect Parameter 17 LSB Master Effect Parameter 18 MSB Master Effect Parameter 18 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 27` | Master Effect | Master Effect Parameter 19 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 29` | Master Effect | Master Effect Parameter 19 LSB Master Effect Parameter 20 MSB Master Effect Parameter 20 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 2B` | Master Effect | Master Effect Parameter 21 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 2D` | Master Effect | Master Effect Parameter 21 LSB Master Effect Parameter 22 MSB Master Effect Parameter 22 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 2F` | Master Effect | Master Effect Parameter 23 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 31` | Master Effect | Master Effect Parameter 23 LSB Master Effect Parameter 24 MSB Master Effect Parameter 24 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 44 33` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 35` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 37` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 39` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 3B` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 3D` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 3F` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 41` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 44 43` | Master Effect | Side Chain Part | 1 | 11, 7F | 7F | 17:Master, 127:Off | `` |  | from Yamaha Data List |
| `30 44 44` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 44 45` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 44 46` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 44 47` | Master Effect | Master Effect ON/OFF | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `30 45 00` | Master Effect | Master Effect Type MSB Master Effect Type LSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | Refer to Effect Parameter List Refer | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote 0C 70 (VINYL BREAK) as Master Effect 3 and read it back — also `from Yamaha Data List` |
| `30 45 02` | Master Effect | Master Effect Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `30 45 03` | Master Effect | Master Effect Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | ˶ Refer | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — moved by an FX slider, reported in SysEx — also `from Yamaha Data List` |
| `30 45 05` | Master Effect | Master Effect Parameter 1 LSB Master Effect Parameter 2 MSB Master Effect Parameter 2 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | `verified on hardware` ([05-live-state.md](05-live-state.md)) — moved by an FX slider with no CC of its own — SysEx is the only report — also `from Yamaha Data List` |
| `30 45 07` | Master Effect | Master Effect Parameter 3 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 09` | Master Effect | Master Effect Parameter 3 LSB Master Effect Parameter 4 MSB Master Effect Parameter 4 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 0B` | Master Effect | Master Effect Parameter 5 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 0D` | Master Effect | Master Effect Parameter 5 LSB Master Effect Parameter 6 MSB Master Effect Parameter 6 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 0F` | Master Effect | Master Effect Parameter 7 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 11` | Master Effect | Master Effect Parameter 7 LSB Master Effect Parameter 8 MSB Master Effect Parameter 8 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 13` | Master Effect | Master Effect Parameter 9 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 15` | Master Effect | Master Effect Parameter 9 LSB Master Effect Parameter 10 MSB Master Effect Parameter 10 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 17` | Master Effect | Master Effect Parameter 11 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 19` | Master Effect | Master Effect Parameter 11 LSB Master Effect Parameter 12 MSB Master Effect Parameter 12 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 1B` | Master Effect | Master Effect Parameter 13 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 1D` | Master Effect | Master Effect Parameter 13 LSB Master Effect Parameter 14 MSB Master Effect Parameter 14 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 1F` | Master Effect | Master Effect Parameter 15 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 21` | Master Effect | Master Effect Parameter 15 LSB Master Effect Parameter 16 MSB Master Effect Parameter 16 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 23` | Master Effect | Master Effect Parameter 17 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 25` | Master Effect | Master Effect Parameter 17 LSB Master Effect Parameter 18 MSB Master Effect Parameter 18 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 27` | Master Effect | Master Effect Parameter 19 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 29` | Master Effect | Master Effect Parameter 19 LSB Master Effect Parameter 20 MSB Master Effect Parameter 20 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 2B` | Master Effect | Master Effect Parameter 21 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 2D` | Master Effect | Master Effect Parameter 21 LSB Master Effect Parameter 22 MSB Master Effect Parameter 22 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 2F` | Master Effect | Master Effect Parameter 23 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 31` | Master Effect | Master Effect Parameter 23 LSB Master Effect Parameter 24 MSB Master Effect Parameter 24 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 45 33` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 35` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 37` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 39` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 3B` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 3D` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 3F` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 41` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 45 43` | Master Effect | Side Chain Part | 1 | 11, 7F | 7F | 17:Master, 127:Off | `` |  | from Yamaha Data List |
| `30 45 44` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 45 45` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 45 46` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 45 47` | Master Effect | Master Effect ON/OFF | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `30 46 00` | Master Effect | Master Effect Type MSB Master Effect Type LSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | Refer to Effect Parameter List Refer | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Master Effect 4 type read 08 00 = VCM COMPRESSOR 376, a type effect-types.csv lists for Master 1 and Master 4 only — also `from Yamaha Data List` |
| `30 46 02` | Master Effect | Master Effect Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `30 46 03` | Master Effect | Master Effect Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | to Effect Parameter List | ˶ Refer | `` |  | from Yamaha Data List |
| `30 46 05` | Master Effect | Master Effect Parameter 1 LSB Master Effect Parameter 2 MSB Master Effect Parameter 2 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 07` | Master Effect | Master Effect Parameter 3 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 09` | Master Effect | Master Effect Parameter 3 LSB Master Effect Parameter 4 MSB Master Effect Parameter 4 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 0B` | Master Effect | Master Effect Parameter 5 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 0D` | Master Effect | Master Effect Parameter 5 LSB Master Effect Parameter 6 MSB Master Effect Parameter 6 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 0F` | Master Effect | Master Effect Parameter 7 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 11` | Master Effect | Master Effect Parameter 7 LSB Master Effect Parameter 8 MSB Master Effect Parameter 8 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 13` | Master Effect | Master Effect Parameter 9 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 15` | Master Effect | Master Effect Parameter 9 LSB Master Effect Parameter 10 MSB Master Effect Parameter 10 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 17` | Master Effect | Master Effect Parameter 11 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 19` | Master Effect | Master Effect Parameter 11 LSB Master Effect Parameter 12 MSB Master Effect Parameter 12 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 1B` | Master Effect | Master Effect Parameter 13 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 1D` | Master Effect | Master Effect Parameter 13 LSB Master Effect Parameter 14 MSB Master Effect Parameter 14 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 1F` | Master Effect | Master Effect Parameter 15 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 21` | Master Effect | Master Effect Parameter 15 LSB Master Effect Parameter 16 MSB Master Effect Parameter 16 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 23` | Master Effect | Master Effect Parameter 17 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 25` | Master Effect | Master Effect Parameter 17 LSB Master Effect Parameter 18 MSB Master Effect Parameter 18 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 27` | Master Effect | Master Effect Parameter 19 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 29` | Master Effect | Master Effect Parameter 19 LSB Master Effect Parameter 20 MSB Master Effect Parameter 20 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 2B` | Master Effect | Master Effect Parameter 21 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 2D` | Master Effect | Master Effect Parameter 21 LSB Master Effect Parameter 22 MSB Master Effect Parameter 22 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 2F` | Master Effect | Master Effect Parameter 23 MSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 31` | Master Effect | Master Effect Parameter 23 LSB Master Effect Parameter 24 MSB Master Effect Parameter 24 LSB | 2 | 00 - 7F 00 - 7F |  | ˶ ˶ | `` |  | from Yamaha Data List |
| `30 46 33` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 35` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 37` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 39` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 3B` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 3D` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 3F` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 41` | Master Effect | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 46 43` | Master Effect | Side Chain Part | 1 | 11, 7F | 7F | 17:Master, 127:Off | `` |  | from Yamaha Data List |
| `30 46 44` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 46 45` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 46 46` | Master Effect | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 46 47` | Master Effect | Master Effect ON/OFF | 1 | 00 - 01 | 01 | Off, On | `MasterEffectOnOff` |  | from Yamaha Data List |
| `30 47 00` | Project Common / Master EQ | EQ Gain 1 | 1 | 34 - 4C | 40 | -12 - +12[dB] | `EQGain1` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Master EQ block read in full: 21 of 21 documented addresses answered, every reply at its documented width — also `from Yamaha Data List` |
| `30 47 01` | Project Common / Master EQ | EQ Frequency 1 | 1 | 04 - 28 | 0C | 32 - 2000[Hz] | `EQFrequency1` |  | from Yamaha Data List |
| `30 47 02` | Project Common / Master EQ | EQ Q 1 | 1 | 01 - 78 | 07 | 0.1 - 12.0 | `EQQ1` | Not available when “shelving” is selected | from Yamaha Data List |
| `30 47 03` | Project Common / Master EQ | EQ Shape 1 | 1 | 00 - 01 | 00 | Shelf, Peak | `` |  | from Yamaha Data List |
| `30 47 04` | Project Common / Master EQ | EQ Gain 2 | 1 | 34 - 4C | 40 | -12 - +12[dB] | `EQGain2` |  | from Yamaha Data List |
| `30 47 05` | Project Common / Master EQ | EQ Frequency 2 | 1 | 0E - 36 | 14 | 100 - 10.0[kHz] | `EQFrequency2` |  | from Yamaha Data List |
| `30 47 06` | Project Common / Master EQ | EQ Q 2 | 1 | 01 - 78 | 07 | 0.1 - 12.0 | `EQQ2` |  | from Yamaha Data List |
| `30 47 07` | Project Common / Master EQ | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 47 08` | Project Common / Master EQ | EQ Gain 3 | 1 | 34 - 4C | 40 | -12 - +12[dB] | `EQGain3` |  | from Yamaha Data List |
| `30 47 09` | Project Common / Master EQ | EQ Frequency 3 | 1 | 0E - 36 | 1C | 100 - 10.0[kHz] | `EQFrequency3` |  | from Yamaha Data List |
| `30 47 0A` | Project Common / Master EQ | EQ Q 3 | 1 | 01 - 78 | 07 | 0.1- 12.0 | `EQQ3` |  | from Yamaha Data List |
| `30 47 0B` | Project Common / Master EQ | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 47 0C` | Project Common / Master EQ | EQ Gain 4 | 1 | 34 - 4C | 40 | -12 - +12[dB] | `EQGain4` |  | from Yamaha Data List |
| `30 47 0D` | Project Common / Master EQ | EQ Frequency 4 | 1 | 0E - 36 | 2C | 100 - 10.0[kHz] | `EQFrequency4` |  | from Yamaha Data List |
| `30 47 0E` | Project Common / Master EQ | EQ Q 4 | 1 | 01 - 78 | 07 | 0.1 - 12.0 | `EQQ4` |  | from Yamaha Data List |
| `30 47 0F` | Project Common / Master EQ | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 47 10` | Project Common / Master EQ | EQ Gain 5 | 1 | 34 - 4C | 40 | -12 - +12[dB] | `EQGain5` |  | from Yamaha Data List |
| `30 47 11` | Project Common / Master EQ | EQ Frequency 5 | 1 | 1C - 3A | 34 | 0.5 - 16.0[kHz] | `EQFrequency5` |  | from Yamaha Data List |
| `30 47 12` | Project Common / Master EQ | EQ Q 5 | 1 | 01 - 78 | 07 | 0.1 - 12.0 | `EQQ5` | Not available when “shelving” is selected | from Yamaha Data List |
| `30 47 13` | Project Common / Master EQ | EQ Shape 5 | 1 | 00 - 01 | 00 | Shelf, Peak | `` |  | from Yamaha Data List |
| `30 47 14` | Project Common / Master EQ | Master EQ On/Off | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `30 49 00` | Project Common / A/D Part Insertion A | Insertion-A Type MSB Insertion-A Type LSB | 2 | 00 - 7F 00 - 7F | 0D 70 | Refer to Effect Parameter List | `` | NOISE GATE+ COMP+EQ | from Yamaha Data List |
| `30 49 02` | Project Common / A/D Part Insertion A | Insertion-A Template Number | 1 | 00 - 7F | 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 03` | Project Common / A/D Part Insertion A | Insertion-A Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 05` | Project Common / A/D Part Insertion A | Insertion-A Parameter 1 LSB Insertion-A Parameter 2 MSB Insertion-A Parameter 2 LSB | 2 | 00 - 7F 00 - 7F | 00 0D | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 07` | Project Common / A/D Part Insertion A | Insertion-A Parameter 3 MSB | 2 | 00 - 7F 00 - 7F | 00 6D | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 09` | Project Common / A/D Part Insertion A | Insertion-A Parameter 3 LSB Insertion-A Parameter 4 MSB Insertion-A Parameter 4 LSB | 2 | 00 - 7F 00 - 7F | 00 03 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 0B` | Project Common / A/D Part Insertion A | Insertion-A Parameter 5 MSB | 2 | 00 - 7F 00 - 7F | 00 4B | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 0D` | Project Common / A/D Part Insertion A | Insertion-A Parameter 5 LSB Insertion-A Parameter 6 MSB Insertion-A Parameter 6 LSB | 2 | 00 - 7F 00 - 7F | 00 09 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 0F` | Project Common / A/D Part Insertion A | Insertion-A Parameter 7 MSB | 2 | 00 - 7F 00 - 7F | 00 40 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 11` | Project Common / A/D Part Insertion A | Insertion-A Parameter 7 LSB Insertion-A Parameter 8 MSB Insertion-A Parameter 8 LSB | 2 | 00 - 7F 00 - 7F | 00 36 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 13` | Project Common / A/D Part Insertion A | Insertion-A Parameter 9 MSB | 2 | 00 - 7F 00 - 7F | 00 40 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 15` | Project Common / A/D Part Insertion A | Insertion-A Parameter 9 LSB Insertion-A Parameter 10 MSB Insertion-A Parameter 10 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 17` | Project Common / A/D Part Insertion A | Insertion-A Parameter 11 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 19` | Project Common / A/D Part Insertion A | Insertion-A Parameter 11 LSB Insertion-A Parameter 12 MSB Insertion-A Parameter 12 LSB | 2 | 00 - 7F 00 - 7F | 00 0D | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 1B` | Project Common / A/D Part Insertion A | Insertion-A Parameter 13 MSB | 2 | 00 - 7F 00 - 7F | 00 39 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 1D` | Project Common / A/D Part Insertion A | Insertion-A Parameter 13 LSB Insertion-A Parameter 14 MSB Insertion-A Parameter 14 LSB | 2 | 00 - 7F 00 - 7F | 00 24 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 1F` | Project Common / A/D Part Insertion A | Insertion-A Parameter 15 MSB | 2 | 00 - 7F 00 - 7F | 00 40 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 21` | Project Common / A/D Part Insertion A | Insertion-A Parameter 15 LSB Insertion-A Parameter 16 MSB Insertion-A Parameter 16 LSB | 2 | 00 - 7F 00 - 7F | 00 0A | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 23` | Project Common / A/D Part Insertion A | Insertion-A Parameter 17 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 25` | Project Common / A/D Part Insertion A | Insertion-A Parameter 17 LSB Insertion-A Parameter 18 MSB Insertion-A Parameter 18 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 27` | Project Common / A/D Part Insertion A | Insertion-A Parameter 19 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 29` | Project Common / A/D Part Insertion A | Insertion-A Parameter 19 LSB Insertion-A Parameter 20 MSB Insertion-A Parameter 20 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 2B` | Project Common / A/D Part Insertion A | Insertion-A Parameter 21 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 2D` | Project Common / A/D Part Insertion A | Insertion-A Parameter 21 LSB Insertion-A Parameter 22 MSB Insertion-A Parameter 22 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 2F` | Project Common / A/D Part Insertion A | Insertion-A Parameter 23 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 31` | Project Common / A/D Part Insertion A | Insertion-A Parameter 23 LSB Insertion-A Parameter 24 MSB Insertion-A Parameter 24 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 49 33` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 35` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 37` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 39` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 3B` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 3D` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 3F` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 41` | Project Common / A/D Part Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 49 43` | Project Common / A/D Part Insertion A | Side Chain Part | 1 | - 11, 7F | 7F | 0:Part1, 1:Part2, ..., 10:Part11, 16:A/D, 17:Master, 127:Off | `` |  | from Yamaha Data List |
| `30 4A 00` | Project Common / A/D Part Insertion B | Insertion-B Type MSB Insertion-B Type LSB | 2 | 0D 2F | 0D 2F | Refer to Effect Parameter List | `` | LP-HP FILTER | from Yamaha Data List |
| `30 4A 02` | Project Common / A/D Part Insertion B | Insertion-B Template Number | 1 | 00 - 7F | 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 03` | Project Common / A/D Part Insertion B | Insertion-B Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | 02 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 05` | Project Common / A/D Part Insertion B | Insertion-B Parameter 1 LSB Insertion-B Parameter 2 MSB Insertion-B Parameter 2 LSB | 2 | 00 - 7F 00 - 7F | 00 10 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 07` | Project Common / A/D Part Insertion B | Insertion-B Parameter 3 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 09` | Project Common / A/D Part Insertion B | Insertion-B Parameter 3 LSB Insertion-B Parameter 4 MSB Insertion-B Parameter 4 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 0B` | Project Common / A/D Part Insertion B | Insertion-B Parameter 5 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 0D` | Project Common / A/D Part Insertion B | Insertion-B Parameter 5 LSB Insertion-B Parameter 6 MSB Insertion-B Parameter 6 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 0F` | Project Common / A/D Part Insertion B | Insertion-B Parameter 7 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 11` | Project Common / A/D Part Insertion B | Insertion-B Parameter 7 LSB Insertion-B Parameter 8 MSB Insertion-B Parameter 8 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 13` | Project Common / A/D Part Insertion B | Insertion-B Parameter 9 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 15` | Project Common / A/D Part Insertion B | Insertion-B Parameter 9 LSB Insertion-B Parameter 10 MSB Insertion-B Parameter 10 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 17` | Project Common / A/D Part Insertion B | Insertion-B Parameter 11 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 19` | Project Common / A/D Part Insertion B | Insertion-B Parameter 11 LSB Insertion-B Parameter 12 MSB Insertion-B Parameter 12 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 1B` | Project Common / A/D Part Insertion B | Insertion-B Parameter 13 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 1D` | Project Common / A/D Part Insertion B | Insertion-B Parameter 13 LSB Insertion-B Parameter 14 MSB Insertion-B Parameter 14 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 1F` | Project Common / A/D Part Insertion B | Insertion-B Parameter 15 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 21` | Project Common / A/D Part Insertion B | Insertion-B Parameter 15 LSB Insertion-B Parameter 16 MSB Insertion-B Parameter 16 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 23` | Project Common / A/D Part Insertion B | Insertion-B Parameter 17 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 25` | Project Common / A/D Part Insertion B | Insertion-B Parameter 17 LSB Insertion-B Parameter 18 MSB Insertion-B Parameter 18 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 27` | Project Common / A/D Part Insertion B | Insertion-B Parameter 19 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 29` | Project Common / A/D Part Insertion B | Insertion-B Parameter 19 LSB Insertion-B Parameter 20 MSB Insertion-B Parameter 20 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 2B` | Project Common / A/D Part Insertion B | Insertion-B Parameter 21 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 2D` | Project Common / A/D Part Insertion B | Insertion-B Parameter 21 LSB Insertion-B Parameter 22 MSB Insertion-B Parameter 22 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 2F` | Project Common / A/D Part Insertion B | Insertion-B Parameter 23 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 31` | Project Common / A/D Part Insertion B | Insertion-B Parameter 23 LSB Insertion-B Parameter 24 MSB Insertion-B Parameter 24 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` | ˶ | from Yamaha Data List |
| `30 4A 33` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 35` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 37` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 39` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 3B` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 3D` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 3F` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 41` | Project Common / A/D Part Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `30 4A 43` | Project Common / A/D Part Insertion B | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4B 00` | Project Common / A/D Part General | A/D Part Input Mode | 1 | 00 - 03 | 03 | L Mono, R Mono, L+R Mono, Stereo | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — A/D Part General block read in full: 22 of 22 documented addresses answered — also `from Yamaha Data List` |
| `30 4B 01` | Project Common / A/D Part General | A/D Part Volume | 1 | 00 - 7F | 64 | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4B 02` | Project Common / A/D Part General | A/D Part Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `` |  | from Yamaha Data List |
| `30 4B 03` | Project Common / A/D Part General | A/D Part Reverb Send | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 — A/D Part Reverb Send at its default, ruling the built-in mic out as a reverb source — also `from Yamaha Data List` |
| `30 4B 04` | Project Common / A/D Part General | A/D Part Variation Send | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4B 05` | Project Common / A/D Part General | A/D Part Insertion Connect Type | 1 | 01 | 01 | Ins A->B | `` |  | from Yamaha Data List |
| `30 4B 06` | Project Common / A/D Part General | A/D Part Insertion FX Switch | 1 | 02 - 03 | 02 | Bit0:Insertion A Off/On, Bit1:Insertion B Off/On, Bit2-6:reserved | `ADPartInsertionFXSwitch` | Bit1 is fixed to "On" | from Yamaha Data List |
| `30 4B 07` | Project Common / A/D Part General | A/D Part Dry Level | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4B 08` | Project Common / A/D Part General | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4B 09` | Project Common / A/D Part General | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4B 0A` | Project Common / A/D Part General | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4B 0B` | Project Common / A/D Part General | A/D Part 2bandEQ Low Type | 1 | 00 - 05 | 00 | Thru, LPF, HPF, Low Shelf Hi Shelf, Peak/Dip | `` |  | from Yamaha Data List |
| `30 4B 0C` | Project Common / A/D Part General | A/D Part 2bandEQ Low Frequency MSB A/D Part 2bandEQ Low Frequency LSB | 2 | 00 - 01 00 - 7F | 00 30 | → 1st bit6-0 bit13-7, 2nd bit6-0 → bit6-0 63.0 - 18.0k | `` |  | from Yamaha Data List |
| `30 4B 0E` | Project Common / A/D Part General | A/D Part 2bandEQ Low Gain | 1 | 28 - 58 | 40 | 40 - 64 - 88 (-12.00 - +12.00[dB]) | `` |  | from Yamaha Data List |
| `30 4B 0F` | Project Common / A/D Part General | A/D Part 2bandEQ Low Q | 1 | 01 - 78 | 01 | 0.1 - 12.0 | `` |  | from Yamaha Data List |
| `30 4B 10` | Project Common / A/D Part General | A/D Part 2bandEQ High Type | 1 | 00 - 05 | 00 | Thru, LPF, HPF, Low Shelf Hi Shelf, Peak/Dip | `` |  | from Yamaha Data List |
| `30 4B 11` | Project Common / A/D Part General | A/D Part 2bandEQ High Frequency MSB A/D Part 2bandEQ High Frequency LSB | 2 | 00 - 01 00 - 7F | 00 30 | → 1st bit6-0 bit13-7, 2nd bit6-0 → bit6-0 63.0 - 18.0k | `` |  | from Yamaha Data List |
| `30 4B 13` | Project Common / A/D Part General | A/D Part 2bandEQ High Gain | 1 | 28 - 58 | 40 | 40 - 64 - 88 (-12.00 - +12.00[dB]) | `` |  | from Yamaha Data List |
| `30 4B 14` | Project Common / A/D Part General | A/D Part 2bandEQ High Q | 1 | 01 - 78 | 01 | 0.1 - 12.0 | `` |  | from Yamaha Data List |
| `30 4B 15` | Project Common / A/D Part General | A/D Part 2bandEQ Output Gain | 1 | 28 - 58 | 40 | 40 - 64 - 88 (-12.00 - +12.00[dB]) | `` |  | from Yamaha Data List |
| `30 4B 16` | Project Common / A/D Part General | A/D Part Output Select | 1 | - 01, 7D | 00 | 0:MainL&R, 1:Direct Out, 125:Off | `ADPartOutputSelect` |  | from Yamaha Data List |
| `30 4B 17` | Project Common / A/D Part General | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 00` | Project Common / USB Audio Input | USB Part Input Mode | 1 | 00 - 03 | 03 | L Mono, R Mono, L+R Mono, Stereo | `` |  | from Yamaha Data List |
| `30 4C 01` | Project Common / USB Audio Input | USB Part Volume | 1 | 00 - 7F | 64 | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4C 02` | Project Common / USB Audio Input | USB Part Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `` |  | from Yamaha Data List |
| `30 4C 03` | Project Common / USB Audio Input | USB Part Reverb Send | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4C 04` | Project Common / USB Audio Input | USB Part Variation Send | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4C 05` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 06` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 07` | Project Common / USB Audio Input | USB Part Dry Level | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `30 4C 08` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 09` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 0A` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 0B` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 0C` | Project Common / USB Audio Input | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 0E` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 0F` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 10` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 11` | Project Common / USB Audio Input | reserved | 2 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 13` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 14` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 15` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4C 16` | Project Common / USB Audio Input | USB Part Output Select | 1 | - 01, 7D | 00 | 0:MainL&R, 1:Direct Out, 125:Off | `USBPartOutputSelect` |  | from Yamaha Data List |
| `30 4C 17` | Project Common / USB Audio Input | reserved | 1 |  |  |  | `` |  | from Yamaha Data List |
| `30 4D 00` | Project Common / Scale | Scale 1 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale1NoteOfPad1` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — reversible write verified; also per-project rather than global — also `from Yamaha Data List` |
| `30 4D 01` | Project Common / Scale | Scale 1 Note of Pad 2 | 1 | 24 - 60 | 3E | C1 ... C6 | `Scale1NoteOfPad2` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the user-scale sweep — also `from Yamaha Data List` |
| `30 4D 02` | Project Common / Scale | Scale 1 Note of Pad 3 | 1 | 24 - 60 | 3F | C1 ... C6 | `Scale1NoteOfPad3` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote note 50 and read it back (scale 1 pad 3) — also `from Yamaha Data List` |
| `30 4D 03` | Project Common / Scale | Scale 1 Note of Pad 4 | 1 | 24 - 60 | 41 | C1 ... C6 | `Scale1NoteOfPad4` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote note 52 and read it back (scale 1 pad 4) — also `from Yamaha Data List` |
| `30 4D 04` | Project Common / Scale | Scale 1 Note of Pad 5 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale1NoteOfPad5` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote note 55 and read it back (scale 1 pad 5) — also `from Yamaha Data List` |
| `30 4D 05` | Project Common / Scale | Scale 1 Note of Pad 6 | 1 | 24 - 60 | 44 | C1 ... C6 | `Scale1NoteOfPad6` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote note 57 and read it back (scale 1 pad 6) — also `from Yamaha Data List` |
| `30 4D 06` | Project Common / Scale | Scale 1 Note of Pad 7 | 1 | 24 - 60 | 46 | C1 ... C6 | `Scale1NoteOfPad7` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote note 60 and read it back (scale 1 pad 7) — also `from Yamaha Data List` |
| `30 4D 07` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 08` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 09` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 0A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 0B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 0C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 0D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 0E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 0F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 10` | Project Common / Scale | Scale 2 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale2NoteOfPad1` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the user-scale sweep — also `from Yamaha Data List` |
| `30 4D 11` | Project Common / Scale | Scale 2 Note of Pad 2 | 1 | 24 - 60 | 3E | C1 ... C6 | `Scale2NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 12` | Project Common / Scale | Scale 2 Note of Pad 3 | 1 | 24 - 60 | 40 | C1 ... C6 | `Scale2NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 13` | Project Common / Scale | Scale 2 Note of Pad 4 | 1 | 24 - 60 | 41 | C1 ... C6 | `Scale2NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 14` | Project Common / Scale | Scale 2 Note of Pad 5 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale2NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 15` | Project Common / Scale | Scale 2 Note of Pad 6 | 1 | 24 - 60 | 45 | C1 ... C6 | `Scale2NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 16` | Project Common / Scale | Scale 2 Note of Pad 7 | 1 | 24 - 60 | 47 | C1 ... C6 | `Scale2NoteOfPad7` |  | from Yamaha Data List |
| `30 4D 17` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 18` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 19` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 1A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 1B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 1C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 1D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 1E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 1F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 20` | Project Common / Scale | Scale 3 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale3NoteOfPad1` |  | from Yamaha Data List |
| `30 4D 21` | Project Common / Scale | Scale 3 Note of Pad 2 | 1 | 24 - 60 | 3F | C1 ... C6 | `Scale3NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 22` | Project Common / Scale | Scale 3 Note of Pad 3 | 1 | 24 - 60 | 41 | C1 ... C6 | `Scale3NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 23` | Project Common / Scale | Scale 3 Note of Pad 4 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale3NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 24` | Project Common / Scale | Scale 3 Note of Pad 5 | 1 | 24 - 60 | 46 | C1 ... C6 | `Scale3NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 25` | Project Common / Scale | Scale 3 Note of Pad 6 | 1 | 24 - 60 | 48 | C1 ... C6 | `Scale3NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 26` | Project Common / Scale | Scale 3 Note of Pad 7 | 1 | 24 - 60 | 4B | C1 ... C6 | `Scale3NoteOfPad7` |  | from Yamaha Data List |
| `30 4D 27` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 28` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 29` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 2A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 2B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 2C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 2D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 2E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 2F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 30` | Project Common / Scale | Scale 4 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale4NoteOfPad1` |  | from Yamaha Data List |
| `30 4D 31` | Project Common / Scale | Scale 4 Note of Pad 2 | 1 | 24 - 60 | 3E | C1 ... C6 | `Scale4NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 32` | Project Common / Scale | Scale 4 Note of Pad 3 | 1 | 24 - 60 | 40 | C1 ... C6 | `Scale4NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 33` | Project Common / Scale | Scale 4 Note of Pad 4 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale4NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 34` | Project Common / Scale | Scale 4 Note of Pad 5 | 1 | 24 - 60 | 45 | C1 ... C6 | `Scale4NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 35` | Project Common / Scale | Scale 4 Note of Pad 6 | 1 | 24 - 60 | 48 | C1 ... C6 | `Scale4NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 36` | Project Common / Scale | Scale 4 Note of Pad 7 | 1 | 24 - 60 | 4A | C1 ... C6 | `Scale4NoteOfPad7` |  | from Yamaha Data List |
| `30 4D 37` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 38` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 39` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 3A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 3B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 3C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 3D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 3E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 3F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 40` | Project Common / Scale | Scale 5 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale5NoteOfPad1` |  | from Yamaha Data List |
| `30 4D 41` | Project Common / Scale | Scale 5 Note of Pad 2 | 1 | 24 - 60 | 3E | C1 ... C6 | `Scale5NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 42` | Project Common / Scale | Scale 5 Note of Pad 3 | 1 | 24 - 60 | 40 | C1 ... C6 | `Scale5NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 43` | Project Common / Scale | Scale 5 Note of Pad 4 | 1 | 24 - 60 | 42 | C1 ... C6 | `Scale5NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 44` | Project Common / Scale | Scale 5 Note of Pad 5 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale5NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 45` | Project Common / Scale | Scale 5 Note of Pad 6 | 1 | 24 - 60 | 45 | C1 ... C6 | `Scale5NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 46` | Project Common / Scale | Scale 5 Note of Pad 7 | 1 | 24 - 60 | 47 | C1 ... C6 | `Scale5NoteOfPad7` |  | from Yamaha Data List |
| `30 4D 47` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 48` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 49` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 4A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 4B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 4C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 4D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 4E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 4F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 50` | Project Common / Scale | Scale 6 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale6NoteOfPad1` |  | from Yamaha Data List |
| `30 4D 51` | Project Common / Scale | Scale 6 Note of Pad 2 | 1 | 24 - 60 | 3E | C1 ... C6 | `Scale6NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 52` | Project Common / Scale | Scale 6 Note of Pad 3 | 1 | 24 - 60 | 3F | C1 ... C6 | `Scale6NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 53` | Project Common / Scale | Scale 6 Note of Pad 4 | 1 | 24 - 60 | 41 | C1 ... C6 | `Scale6NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 54` | Project Common / Scale | Scale 6 Note of Pad 5 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale6NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 55` | Project Common / Scale | Scale 6 Note of Pad 6 | 1 | 24 - 60 | 45 | C1 ... C6 | `Scale6NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 56` | Project Common / Scale | Scale 6 Note of Pad 7 | 1 | 24 - 60 | 46 | C1 ... C6 | `Scale6NoteOfPad7` |  | from Yamaha Data List |
| `30 4D 57` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 58` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 59` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 5A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 5B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 5C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 5D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 5E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 5F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 60` | Project Common / Scale | Scale 7 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale7NoteOfPad1` |  | from Yamaha Data List |
| `30 4D 61` | Project Common / Scale | Scale 7 Note of Pad 2 | 1 | 24 - 60 | 3E | C1 ... C6 | `Scale7NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 62` | Project Common / Scale | Scale 7 Note of Pad 3 | 1 | 24 - 60 | 40 | C1 ... C6 | `Scale7NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 63` | Project Common / Scale | Scale 7 Note of Pad 4 | 1 | 24 - 60 | 41 | C1 ... C6 | `Scale7NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 64` | Project Common / Scale | Scale 7 Note of Pad 5 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale7NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 65` | Project Common / Scale | Scale 7 Note of Pad 6 | 1 | 24 - 60 | 45 | C1 ... C6 | `Scale7NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 66` | Project Common / Scale | Scale 7 Note of Pad 7 | 1 | 24 - 60 | 46 | C1 ... C6 | `Scale7NoteOfPad7` |  | from Yamaha Data List |
| `30 4D 67` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 68` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 69` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 6A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 6B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 6C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 6D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 6E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 6F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 70` | Project Common / Scale | Scale 8 Note of Pad 1 | 1 | 24 - 60 | 3C | C1 ... C6 | `Scale8NoteOfPad1` |  | from Yamaha Data List |
| `30 4D 71` | Project Common / Scale | Scale 8 Note of Pad 2 | 1 | 24 - 60 | 3D | C1 ... C6 | `Scale8NoteOfPad2` |  | from Yamaha Data List |
| `30 4D 72` | Project Common / Scale | Scale 8 Note of Pad 3 | 1 | 24 - 60 | 3F | C1 ... C6 | `Scale8NoteOfPad3` |  | from Yamaha Data List |
| `30 4D 73` | Project Common / Scale | Scale 8 Note of Pad 4 | 1 | 24 - 60 | 41 | C1 ... C6 | `Scale8NoteOfPad4` |  | from Yamaha Data List |
| `30 4D 74` | Project Common / Scale | Scale 8 Note of Pad 5 | 1 | 24 - 60 | 43 | C1 ... C6 | `Scale8NoteOfPad5` |  | from Yamaha Data List |
| `30 4D 75` | Project Common / Scale | Scale 8 Note of Pad 6 | 1 | 24 - 60 | 44 | C1 ... C6 | `Scale8NoteOfPad6` |  | from Yamaha Data List |
| `30 4D 76` | Project Common / Scale | Scale 8 Note of Pad 7 | 1 | 24 - 60 | 46 | C1 ... C6 | `Scale8NoteOfPad7` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the user-scale sweep — also `from Yamaha Data List` |
| `30 4D 77` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 78` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 79` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 7A` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 7B` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 7C` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 7D` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 7E` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 4D 7F` | Project Common / Scale | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 00` | Project Track / General | Volume | 1 | 00 - 7F | 64 | 0 - 127 | `Volume` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — written 100 on part 7 where it read 0 and read back, with parts 0 and 6 as witnesses unmoved at 100: this is the track volume that silences a track, distinct from the Mute flag at 30 5p 29 — also `from Yamaha Data List` |
| `30 5p 01` | Project Track / General | Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `Pan` |  | from Yamaha Data List |
| `30 5p 02` | Project Track / General | Velocity Limit Low | 1 | 01 - 7F | 01 | 1 - 127 | `` | Not available for DX track | from Yamaha Data List |
| `30 5p 03` | Project Track / General | Velocity Limit High | 1 | 01 - 7F | 7F | 1 - 127 | `` | Not available for DX track | from Yamaha Data List |
| `30 5p 04` | Project Track / General | Note Limit Low | 1 | 00 - 7F | 00 | C-2 ... G8 | `` | Not available for DX track | from Yamaha Data List |
| `30 5p 05` | Project Track / General | Note Limit High | 1 | 00 - 7F | 7F | C-2 ... G8 | `` | Not available for DX track | from Yamaha Data List |
| `30 5p 06` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 07` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 08` | Project Track / General | Group Number | 1 | 00 - 7F | 00 | Off, Group1, ..., Group127 | `GroupNumber` |  | from Yamaha Data List |
| `30 5p 09` | Project Track / General | reserved | 1 | 0 - 1 (decimal) | 00 | 0 - 0 | `ChordSwitch` |  | from Yamaha Data List |
| `30 5p 0A` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 0B` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 0C` | Project Track / General | Octave | 1 | 3E - 42 | 40 | -2 - 0 - +2 | `Octave` | Not available for Drum/ SAMPLER Track | from Yamaha Data List |
| `30 5p 0D` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 0E` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 0F` | Project Track / General | Pattern Select | 1 | 00 - 05 | 00 | 1 - 6 | `PatternSelect` |  | `verified on hardware` ([04-sequencer-editing.md](04-sequencer-editing.md)) — written and read back; clamps at 2 unless Pattern Select Mode is 1 — also `from Yamaha Data List` |
| `30 5p 10` | Project Track / General | reserved | 1 | 1 - 8 (decimal) | 00 | 0 - 8 | `Pattern1BarLength` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — written 3 on all eleven parts and read back 0 on parts 0 and 7, while 30 5p 16 written in the same loop read back 48 on all eleven: the write does not take. Not read before the write, so an ignored write and a write landing as 0 are indistinguishable — also `from Yamaha Data List` |
| `30 5p 11` | Project Track / General | reserved | 1 | 1 - 8 (decimal) | 00 | 0 - 8 | `Pattern2BarLength` |  | from Yamaha Data List |
| `30 5p 12` | Project Track / General | reserved | 1 | 1 - 8 (decimal) | 00 | 0 - 8 | `Pattern3BarLength` |  | from Yamaha Data List |
| `30 5p 13` | Project Track / General | reserved | 1 | 1 - 8 (decimal) | 00 | 0 - 8 | `Pattern4BarLength` |  | from Yamaha Data List |
| `30 5p 14` | Project Track / General | reserved | 1 | 1 - 8 (decimal) | 00 | 0 - 8 | `Pattern5BarLength` |  | from Yamaha Data List |
| `30 5p 15` | Project Track / General | reserved | 1 | 1 - 8 (decimal) | 00 | 0 - 8 | `Pattern6BarLength` |  | from Yamaha Data List |
| `30 5p 16` | Project Track / General | Pattern 1 Step MSB | 2 | 00 - 01 00 - 7F | 00 10 | 1 - 128 → 1st bit6-0 bit13-7, 2nd bit6-0 → bit6-0 | `Pattern1Step` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote pattern 1 step length on all eleven parts (12, 14, 16, 32 and 48) and read each back — also `from Yamaha Data List` |
| `30 5p 18` | Project Track / General | Pattern 1 Step LSB Pattern 2 Step MSB Pattern 2 Step LSB | 2 | 00 - 01 00 - 7F | 00 10 | ˶ | `Pattern2Step` |  | from Yamaha Data List |
| `30 5p 1A` | Project Track / General | Pattern 3 Step MSB | 2 | 00 - 01 00 - 7F | 00 10 | ˶ | `Pattern3Step` |  | from Yamaha Data List |
| `30 5p 1C` | Project Track / General | Pattern 3 Step LSB Pattern 4 Step MSB Pattern 4 Step LSB | 2 | 00 - 01 00 - 7F | 00 10 | ˶ | `Pattern4Step` |  | from Yamaha Data List |
| `30 5p 1E` | Project Track / General | Pattern 5 Step MSB | 2 | 00 - 01 00 - 7F | 00 10 | ˶ | `Pattern5Step` |  | from Yamaha Data List |
| `30 5p 20` | Project Track / General | Pattern 5 Step LSB Pattern 6 Step MSB Pattern 6 Step LSB | 2 | 00 - 01 00 - 7F | 00 10 | ˶ | `Pattern6Step` |  | from Yamaha Data List |
| `30 5p 22` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 23` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 24` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 25` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 26` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 27` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 28` | Project Track / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 5p 29` | Project Track / General | Mute | 1 | 00,7D | 00 | 0:off, 125:on | `OutputSelect` |  | from Yamaha Data List |
| `30 6p 00` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 01` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 02` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 03` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 04` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 05` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 06` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 07` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 08` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 09` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 0A` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 0B` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 0C` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 0D` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 0E` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 0F` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 4B | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 10` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 11` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 12` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 13` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 14` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 15` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 16` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 4B | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 17` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 4F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 18` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 1 of Scale 1 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 19` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 2 of Scale 1 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 1A` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 3 of Scale 1 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 1B` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 4 of Scale 1 | 1 | 00, 24 - 60 | 50 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 1C` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 1D` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 1E` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 1F` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 20` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 21` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 22` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 23` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 24` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 25` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 26` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 27` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 28` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 29` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 2A` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 2B` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 2C` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 2D` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 2E` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 2F` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 4C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 30` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 31` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 32` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 33` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 34` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 35` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 36` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 4C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 37` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 4F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 38` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 1 of Scale 2 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 39` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 2 of Scale 2 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 3A` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 3 of Scale 2 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 3B` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 4 of Scale 2 | 1 | 00, 24 - 60 | 51 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 3C` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 3D` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 3E` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 3F` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 40` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 41` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 42` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 43` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 44` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 45` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 46` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 47` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 48` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 49` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 4A` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 4B` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 4C` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 4D` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 4E` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 4F` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 4B | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 50` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 51` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 52` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 53` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 54` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 55` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 56` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 4B | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 57` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 4F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 58` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 1 of Scale 3 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 59` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 2 of Scale 3 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 5A` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 3 of Scale 3 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 5B` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 4 of Scale 3 | 1 | 00, 24 - 60 | 50 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 5C` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 5D` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 5E` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 5F` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 60` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 61` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 62` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 63` | Project Track / Chord Notes of Scale 1-4 | Pad 1 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 64` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 65` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 66` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 67` | Project Track / Chord Notes of Scale 1-4 | Pad 2 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 68` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 69` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 6A` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 6B` | Project Track / Chord Notes of Scale 1-4 | Pad 3 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 6C` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 6D` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 6E` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 6F` | Project Track / Chord Notes of Scale 1-4 | Pad 4 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 4C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 70` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 71` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 72` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 73` | Project Track / Chord Notes of Scale 1-4 | Pad 5 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 74` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 75` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 48 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 76` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 4C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 77` | Project Track / Chord Notes of Scale 1-4 | Pad 6 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 4F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 78` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 1 of Scale 4 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 79` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 2 of Scale 4 | 1 | 00, 24 - 60 | 4A | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 7A` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 3 of Scale 4 | 1 | 00, 24 - 60 | 4D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 7B` | Project Track / Chord Notes of Scale 1-4 | Pad 7 Chord Note 4 of Scale 4 | 1 | 00, 24 - 60 | 51 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 6p 7C` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 7D` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 7E` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 6p 7F` | Project Track / Chord Notes of Scale 1-4 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 00` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 01` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 02` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 03` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 04` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 05` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 42 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 06` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 07` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 00 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 08` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 09` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 0A` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 0B` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 0C` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 0D` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 0E` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 0F` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 10` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 11` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 42 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 12` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 13` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 14` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 15` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 16` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 17` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 18` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 1 of Scale 5 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 19` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 2 of Scale 5 | 1 | 00, 24 - 60 | 42 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 1A` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 3 of Scale 5 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 1B` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 4 of Scale 5 | 1 | 00, 24 - 60 | 47 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 1C` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 1D` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 1E` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 1F` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 20` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 21` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 22` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 23` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 24` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 25` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 26` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 27` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 28` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 29` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 2A` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 2B` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 2C` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 2D` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 2E` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 2F` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 00 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 30` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 31` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 32` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 33` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 34` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 35` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 36` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 37` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 38` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 1 of Scale 6 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 39` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 2 of Scale 6 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 3A` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 3 of Scale 6 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 3B` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 4 of Scale 6 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 3C` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 3D` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 3E` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 3F` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 40` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 41` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 42` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 43` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 00 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 44` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 45` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 46` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 47` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 48` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 49` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 4A` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 4B` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 4C` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 4D` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 4E` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 4F` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 50` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 51` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 52` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 53` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 54` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 55` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 40 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 56` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 57` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 58` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 1 of Scale 7 | 1 | 00, 24 - 60 | 3E | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 59` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 2 of Scale 7 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 5A` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 3 of Scale 7 | 1 | 00, 24 - 60 | 45 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 5B` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 4 of Scale 7 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 5C` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 5D` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 5E` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 5F` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 60` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 61` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 62` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 63` | Project Track / Chord Notes of Scale 5-8 | Pad 1 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 64` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 65` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 3D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 66` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 67` | Project Track / Chord Notes of Scale 5-8 | Pad 2 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 68` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 69` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 6A` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 6B` | Project Track / Chord Notes of Scale 5-8 | Pad 3 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 00 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 6C` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 6D` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 6E` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 6F` | Project Track / Chord Notes of Scale 5-8 | Pad 4 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 70` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 71` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 72` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 73` | Project Track / Chord Notes of Scale 5-8 | Pad 5 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 74` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3C | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 75` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 3F | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 76` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 43 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 77` | Project Track / Chord Notes of Scale 5-8 | Pad 6 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 78` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 1 of Scale 8 | 1 | 00, 24 - 60 | 3D | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 79` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 2 of Scale 8 | 1 | 00, 24 - 60 | 41 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 7A` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 3 of Scale 8 | 1 | 00, 24 - 60 | 44 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 7B` | Project Track / Chord Notes of Scale 5-8 | Pad 7 Chord Note 4 of Scale 8 | 1 | 00, 24 - 60 | 46 | 0:off, 24 - 60:C1 ... C6 | `` |  | from Yamaha Data List |
| `30 7p 7C` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 7D` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 7E` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `30 7p 7F` | Project Track / Chord Notes of Scale 5-8 | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
