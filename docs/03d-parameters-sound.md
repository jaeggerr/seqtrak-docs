# Sound, per track (`31 xx xx`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

316 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `31 0p 00` | Sound Common / Name | Sound Name 1 | 1 | 00 - 7F | 00 |  | `` | UTF8 (7-bit encoded) | `verified on hardware` ([06-sounds-presets.md](06-sounds-presets.md)) — 88 bytes, 7-bit packed in 11 groups of 8, dumped per part — also `from Yamaha Data List` |
| `31 0p 01` | Sound Common / Name | Sound Name 2 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 02` | Sound Common / Name | Sound Name 3 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 03` | Sound Common / Name | Sound Name 4 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 04` | Sound Common / Name | Sound Name 5 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 05` | Sound Common / Name | Sound Name 6 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 06` | Sound Common / Name | Sound Name 7 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 07` | Sound Common / Name | Sound Name 8 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 08` | Sound Common / Name | Sound Name 9 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 09` | Sound Common / Name | Sound Name 10 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 0A` | Sound Common / Name | Sound Name 11 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 0B` | Sound Common / Name | Sound Name 12 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 0C` | Sound Common / Name | Sound Name 13 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 0D` | Sound Common / Name | Sound Name 14 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 0E` | Sound Common / Name | Sound Name 15 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 0F` | Sound Common / Name | Sound Name 16 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 10` | Sound Common / Name | Sound Name 17 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 11` | Sound Common / Name | Sound Name 18 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 12` | Sound Common / Name | Sound Name 19 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 13` | Sound Common / Name | Sound Name 20 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 14` | Sound Common / Name | Sound Name 21 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 15` | Sound Common / Name | Sound Name 22 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 16` | Sound Common / Name | Sound Name 23 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 17` | Sound Common / Name | Sound Name 24 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 18` | Sound Common / Name | Sound Name 25 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 19` | Sound Common / Name | Sound Name 26 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 1A` | Sound Common / Name | Sound Name 27 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 1B` | Sound Common / Name | Sound Name 28 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 1C` | Sound Common / Name | Sound Name 29 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 1D` | Sound Common / Name | Sound Name 30 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 1E` | Sound Common / Name | Sound Name 31 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 1F` | Sound Common / Name | Sound Name 32 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 20` | Sound Common / Name | Sound Name 33 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 21` | Sound Common / Name | Sound Name 34 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 22` | Sound Common / Name | Sound Name 35 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 23` | Sound Common / Name | Sound Name 36 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 24` | Sound Common / Name | Sound Name 37 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 25` | Sound Common / Name | Sound Name 38 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 26` | Sound Common / Name | Sound Name 39 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 27` | Sound Common / Name | Sound Name 40 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 28` | Sound Common / Name | Sound Name 41 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 29` | Sound Common / Name | Sound Name 42 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 2A` | Sound Common / Name | Sound Name 43 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 2B` | Sound Common / Name | Sound Name 44 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 2C` | Sound Common / Name | Sound Name 45 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 2D` | Sound Common / Name | Sound Name 46 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 2E` | Sound Common / Name | Sound Name 47 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 2F` | Sound Common / Name | Sound Name 48 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 30` | Sound Common / Name | Sound Name 49 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 31` | Sound Common / Name | Sound Name 50 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 32` | Sound Common / Name | Sound Name 51 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 33` | Sound Common / Name | Sound Name 52 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 34` | Sound Common / Name | Sound Name 53 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 35` | Sound Common / Name | Sound Name 54 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 36` | Sound Common / Name | Sound Name 55 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 37` | Sound Common / Name | Sound Name 56 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 38` | Sound Common / Name | Sound Name 57 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 39` | Sound Common / Name | Sound Name 58 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 3A` | Sound Common / Name | Sound Name 59 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 3B` | Sound Common / Name | Sound Name 60 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 3C` | Sound Common / Name | Sound Name 61 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 3D` | Sound Common / Name | Sound Name 62 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 3E` | Sound Common / Name | Sound Name 63 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 3F` | Sound Common / Name | Sound Name 64 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 40` | Sound Common / Name | Sound Name 65 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 41` | Sound Common / Name | Sound Name 66 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 42` | Sound Common / Name | Sound Name 67 | 1 | 00 - 7F | 00 |  | `` | UTF8 (7-bit encoded) | from Yamaha Data List |
| `31 0p 43` | Sound Common / Name | Sound Name 68 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 44` | Sound Common / Name | Sound Name 69 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 45` | Sound Common / Name | Sound Name 70 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 46` | Sound Common / Name | Sound Name 71 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 47` | Sound Common / Name | Sound Name 72 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 48` | Sound Common / Name | Sound Name 73 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 49` | Sound Common / Name | Sound Name 74 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 4A` | Sound Common / Name | Sound Name 75 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 4B` | Sound Common / Name | Sound Name 76 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 4C` | Sound Common / Name | Sound Name 77 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 4D` | Sound Common / Name | Sound Name 78 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 4E` | Sound Common / Name | Sound Name 79 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 4F` | Sound Common / Name | Sound Name 80 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 50` | Sound Common / Name | Sound Name 81 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 51` | Sound Common / Name | Sound Name 82 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 52` | Sound Common / Name | Sound Name 83 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 53` | Sound Common / Name | Sound Name 84 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 54` | Sound Common / Name | Sound Name 85 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 55` | Sound Common / Name | Sound Name 86 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 56` | Sound Common / Name | Sound Name 87 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 57` | Sound Common / Name | Sound Name 88 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 58` | Sound Common / Name | Sound Name 89 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 59` | Sound Common / Name | Sound Name 90 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 5A` | Sound Common / Name | Sound Name 91 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 5B` | Sound Common / Name | Sound Name 92 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 5C` | Sound Common / Name | Sound Name 93 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 5D` | Sound Common / Name | Sound Name 94 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 5E` | Sound Common / Name | Sound Name 95 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 5F` | Sound Common / Name | Sound Name 96 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 60` | Sound Common / Name | Sound Name 97 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 61` | Sound Common / Name | Sound Name 98 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 62` | Sound Common / Name | Sound Name 99 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 63` | Sound Common / Name | Sound Name 100 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `31 0p 64` | Sound Common / Name | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 0p 65` | Sound Common / Name | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 0p 66` | Sound Common / Name | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 0p 67` | Sound Common / Name | reserved | 1 | 0 - 15 (decimal) | 00 | 0 - 15 | `SubCategory` |  | from Yamaha Data List |
| `31 0p 68` | Sound Common / Name | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 0p 69` | Sound Common / Name | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 00` | Sound Common / General | AEG Decay/Release Offset | 1 | 00 - 7F | 40 | -64 - +63 | `AEGDecayReleaseOffset` | Available for Synth track | from Yamaha Data List |
| `31 1p 01` | Sound Common / General | Carrier Attack Offset | 1 | 00 - 7F | 40 | -64 - +63 | `CarrierAttackOffset` | Available for DX track | from Yamaha Data List |
| `31 1p 02` | Sound Common / General | Carrier Decay Offset | 1 | 00 - 7F | 40 | -64 - +63 | `CarrierDecayOffset` | Available for DX track | from Yamaha Data List |
| `31 1p 03` | Sound Common / General | Mod Amount Offset | 1 | 00 - 7F | 40 | -64 - +63 | `ModAmountOffset` | Available for DX track | from Yamaha Data List |
| `31 1p 04` | Sound Common / General | Freq Ratio Offset | 1 | 00 - 7F | 40 | -64 - +63 | `FreqRatioOffset` | Available for DX track | from Yamaha Data List |
| `31 1p 05` | Sound Common / General | Feedback Offset | 1 | 00 - 7F | 40 | -64 - +63 | `FeedbackOffset` | Available for DX track | from Yamaha Data List |
| `31 1p 06` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 07` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 08` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 09` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 0A` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 0B` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 0C` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 0D` | Sound Common / General | Trigger/Gate Mode | 1 | 00 - 02 | 02 | Trigger, Gate, Depend on Voice | `TriggerGateMode` | Not available for DX track | from Yamaha Data List |
| `31 1p 0E` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 0F` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 10` | Sound Common / General | Pitch Bend Range Upper | 1 | 10 - 58 | 42 | -48 - +24 | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 11` | Sound Common / General | Pitch Bend Range Lower | 1 | 10 - 58 | 3E | -48 - +24 | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 12` | Sound Common / General | Velocity Sense Depth | 1 | 00 - 7F | 40 | 0 - 127 | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 13` | Sound Common / General | Velocity Sense Offset | 1 | 00 - 7F | 40 | 0 - 127 | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 14` | Sound Common / General | Volume | 1 | 00 - 7F | 64 | 0 - 127 | `Volume` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote Volume on all eleven parts and read each back — also `from Yamaha Data List` |
| `31 1p 15` | Sound Common / General | Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `` |  | from Yamaha Data List |
| `31 1p 16` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 17` | Sound Common / General | Detune MSB Detune LSB | 2 | 00 - 0F 00 - 0F | 08 00 (80) | -12.8 - +12.7[Hz] 1st bit3-0 → bit7-4, 2nd bit3-0 → bit3-0 | `` | Not available for DX track | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Detune read as two data bytes (08 00) at the base address on part 7; 31 1p 18 is silent on four attempts — also `from Yamaha Data List` |
| `31 1p 19` | Sound Common / General | Reverb Send | 1 | 00 - 7F | 00 | 0 - 127 | `ReverbSend` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote Reverb Send on all eleven parts and read each back — also `from Yamaha Data List` |
| `31 1p 1A` | Sound Common / General | Variation Send | 1 | 00 - 7F | 00 | 0 - 127 | `VariationSend` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote Variation Send on all eleven parts and read each back — also `from Yamaha Data List` |
| `31 1p 1B` | Sound Common / General | Dry Level | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `31 1p 1C` | Sound Common / General | Note Shift | 1 | 28 - 58 | 40 | -24 - +24[semitones] | `NoteShift` |  | from Yamaha Data List |
| `31 1p 1D` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 1E` | Sound Common / General | Portamento Switch | 1 | 00 - 01 | 00 | Off, On | `PortamentoSwitch` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 1F` | Sound Common / General | Portamento Time | 1 | 00 - 7F | 40 | 0 - 127 | `PortamentoTime` |  | from Yamaha Data List |
| `31 1p 20` | Sound Common / General | Portamento Mode | 1 | 00 - 01 | 01 | Fingered, Full-time | `PortamentoMode` |  | from Yamaha Data List |
| `31 1p 21` | Sound Common / General | Portamento Time Mode | 1 | 00 - 03 | 00 | Rate 1, Time 1, Rate 2, Time 2 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 22` | Sound Common / General | Key Assign Mode | 1 | 00 - 01 | 01 | Single, Multi | `KeyAssignMode` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 23` | Sound Common / General | Mono/Poly Mode | 1 | 00 - 02 | 01 | Mono, Poly, Chord | `MonoPolyChordMode` | Chord is not available for Drum/ SAMPLER track | from Yamaha Data List |
| `31 1p 24` | Sound Common / General | Micro Tuning Scale | 2 | 00 - 0C | 00 00 (00) | Equal Temperament, Pure Major, Pure Minor, Werckmeister, Kirnberger, Valloti&Young, 1/4 Shift, 1/4 tone, 1/8 tone, Indian, Arabic 1, Arabic 2, Arabic 3 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 26` | Sound Common / General | Micro Tuning Root | 1 | 00 - 0B | 00 | C, C#, …, B | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 27` | Sound Common / General | Legato Slope | 1 | 00 - 07 | 00 | 0 - 7 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 28` | Sound Common / General | Insertion Connect Type | 1 | 01 | 01 | Ins A->B | `` |  | from Yamaha Data List |
| `31 1p 29` | Sound Common / General | Insertion FX Switch | 1 | 02 - 03 | 03 | bit0: Insertion A Off/On, bit1:Insertion B Off/On, bit2-6:reserved | `` | bit1 is fixed to On | from Yamaha Data List |
| `31 1p 2A` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 2B` | Sound Common / General | Element Pan on/off | 1 | 00 - 01 | 01 | Off, On | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 2C` | Sound Common / General | AEG Attack Time | 1 | 00 - 7F | 40 | -64 - +63 | `<key=13>` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered on part 7, reading 40 (the documented default); the address is reachable, its meaning was not proven by physical action — also `from Yamaha Data List` |
| `31 1p 2D` | Sound Common / General | AEG Decay Time | 1 | 00 - 7F | 40 | -64 - +63 | `AEGDecayTime` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered on part 7, reading 40 (the documented default); the address is reachable, its meaning was not proven by physical action — also `from Yamaha Data List` |
| `31 1p 2E` | Sound Common / General | AEG Sustain Level | 1 | 00 - 7F | 40 | -64 - +63 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 2F` | Sound Common / General | AEG Release Time | 1 | 00 - 7F | 40 | -64 - +63 | `ReleaseTime` |  | from Yamaha Data List |
| `31 1p 30` | Sound Common / General | FEG Attack Time | 1 | 00 - 7F | 40 | -64 - +63 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 31` | Sound Common / General | FEG Decay Time | 1 | 00 - 7F | 40 | -64 - +63 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 32` | Sound Common / General | FEG Sustain Level | 1 | 00 - 7F | 40 | -64 - +63 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 33` | Sound Common / General | FEG Release Time | 1 | 00 - 7F | 40 | -64 - +63 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 34` | Sound Common / General | FEG Depth | 1 | 00 - 7F | 40 | -64 - +63 | `` | Not available for Drum/DX track | from Yamaha Data List |
| `31 1p 35` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 36` | Sound Common / General | Filter Cutoff Frequency | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — wrote Filter Cutoff Frequency on all eleven parts and read each back — also `from Yamaha Data List` |
| `31 1p 37` | Sound Common / General | Filter Resonance/Width | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered on part 7, reading 40 (the documented default); the address is reachable, its meaning was not proven by physical action — also `from Yamaha Data List` |
| `31 1p 38` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 39` | Sound Common / General | 3bandEQ Low Frequency MSB 3bandEQ Low Frequency LSB | 2 | 00 - 01 00 - 7F | 00 6F | 50.1 - 2.00k 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` | Not available for DX track Not available for DX track | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — 3bandEQ Low Frequency read as two data bytes (00 76) on part 7; 31 1p 3A is silent on four attempts — also `from Yamaha Data List` |
| `31 1p 3B` | Sound Common / General | 3bandEQ Low Gain | 1 | 20 - 60 | 40 | -32 - +32 (12.00 - +12.00[dB]) | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 3C` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 3D` | Sound Common / General | 3bandEQ Mid Frequency MSB 3bandEQ Mid Frequency LSB | 2 | 00 - 01 00 - 7F | 01 0D | 139.7 - 10.1k 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` | Not available for | from Yamaha Data List |
| `31 1p 3F` | Sound Common / General | 3bandEQ Mid Gain | 1 | 20 - 60 | 40 | -32 - +32 (-12.00 - +12.00[dB]) | `` | DX track Not available for DX track Not available for | from Yamaha Data List |
| `31 1p 40` | Sound Common / General | 3bandEQ Mid Q | 1 | 00 - 1F | 00 | 0 - 31 (0.7 - 10.3) | `` |  | from Yamaha Data List |
| `31 1p 41` | Sound Common / General | 3bandEQ High Frequency MSB 3bandEQ High Frequency LSB | 2 | 01 03 - 7F | 01 1D | 503.8 - 14.0k 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` | DX track Not available for DX track | from Yamaha Data List |
| `31 1p 43` | Sound Common / General | 3bandEQ High Gain | 1 | 20 - 60 | 40 | -32 - +32 (-12.00 - +12.00[dB]) | `` | Not available for DX track | from Yamaha Data List |
| `31 1p 44` | Sound Common / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 1p 45` | Sound Common / General | 2bandEQ Low Type | 1 | 00 - 05 | 03 | Thru, LPF, HPF, Low Shelf, Hi Shelf, Peak/Dip | `` |  | from Yamaha Data List |
| `31 1p 46` | Sound Common / General | 2bandEQ Low Frequency MSB 2bandEQ Low Frequency LSB | 2 | 00 - 01 00 - 7F | 00 66 | 63.0 - 18.0k 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `EQ2BandLowFrequency` |  | from Yamaha Data List |
| `31 1p 48` | Sound Common / General | 2bandEQ Low Gain | 1 | 28 - 58 | 40 | 40 - 64 - 88 (-12.00 - +12.00[dB]) | `EQ2BandLowGain` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered on part 7, reading 40 (the documented default, +0.00 dB); reachable, meaning not proven by physical action — also `from Yamaha Data List` |
| `31 1p 49` | Sound Common / General | 2bandEQ Low Q | 1 | 01 - 78 | 01 | 0.1 - 12.0 | `` |  | from Yamaha Data List |
| `31 1p 4A` | Sound Common / General | 2bandEQ High Type | 1 | 00 - 05 | 04 | Thru, LPF, HPF, Low Shelf, Hi Shelf, Peak/Dip | `` |  | from Yamaha Data List |
| `31 1p 4B` | Sound Common / General | 2bandEQ High Frequency MSB 2bandEQ High Frequency LSB | 2 | 00 - 01 00 - 7F | 01 10 | 63.0 - 18.0k 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `EQ2BandHighFrequency` |  | from Yamaha Data List |
| `31 1p 4D` | Sound Common / General | 2bandEQ High Gain | 1 | 28 - 58 | 40 | 40 - 64 - 88 (-12.00 - +12.00[dB]) | `EQ2BandHighGain` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — answered on part 7, reading 40 (the documented default, +0.00 dB); reachable, meaning not proven by physical action — also `from Yamaha Data List` |
| `31 1p 4E` | Sound Common / General | 2bandEQ High Q | 1 | 01 - 78 | 01 | 0.1 - 12.0 | `` |  | from Yamaha Data List |
| `31 1p 4F` | Sound Common / General | 2bandEQ Output Gain | 1 | 28 - 58 | 40 | 40 - 64 - 88 (-12.00 - +12.00[dB]) | `` |  | from Yamaha Data List |
| `31 2p 00` | Sound Common / Insertion A | Insertion-A Type MSB Insertion-A Type LSB | 2 | 00 - 7F 00 - 7F | 00 00 | Refer to Effect Parameter List | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — insertion A block: all 27 readable addresses answered on part 8, and all were restored by write; on 2026-10-23 part 7 was changed to a different type (08 10 CLASSIC COMPRESSOR -> 01 02 SPX HALL), reported back correctly and restored — also `from Yamaha Data List` |
| `31 2p 02` | Sound Common / Insertion A | Insertion-A Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 03` | Sound Common / Insertion A | Insertion-A Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 05` | Sound Common / Insertion A | Insertion-A Parameter 1 LSB Insertion-A Parameter 2 MSB Insertion-A Parameter 2 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 07` | Sound Common / Insertion A | Insertion-A Parameter3 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 09` | Sound Common / Insertion A | Insertion-A Parameter3 LSB Insertion-A Parameter4 MSB Insertion-A Parameter4 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 0B` | Sound Common / Insertion A | Insertion-A Parameter5 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 0D` | Sound Common / Insertion A | Insertion-A Parameter5 LSB Insertion-A Parameter6 MSB Insertion-A Parameter6 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 0F` | Sound Common / Insertion A | Insertion-A Parameter7 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 11` | Sound Common / Insertion A | Insertion-A Parameter7 LSB Insertion-A Parameter8 MSB Insertion-A Parameter8 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 13` | Sound Common / Insertion A | Insertion-A Parameter9 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 15` | Sound Common / Insertion A | Insertion-A Parameter9 LSB Insertion-A Parameter 10 MSB Insertion-A Parameter 10 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 17` | Sound Common / Insertion A | Insertion-A Parameter 11 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 19` | Sound Common / Insertion A | Insertion-A Parameter 11 LSB Insertion-A Parameter 12 MSB Insertion-A Parameter 12 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 1B` | Sound Common / Insertion A | Insertion-A Parameter 13 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 1D` | Sound Common / Insertion A | Insertion-A Parameter 13 LSB Insertion-A Parameter 14 MSB Insertion-A Parameter 14 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 1F` | Sound Common / Insertion A | Insertion-A Parameter 15 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 21` | Sound Common / Insertion A | Insertion-A Parameter 15 LSB Insertion-A Parameter 16 MSB Insertion-A Parameter 16 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 23` | Sound Common / Insertion A | Insertion-A Parameter 17 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 25` | Sound Common / Insertion A | Insertion-A Parameter 17 LSB Insertion-A Parameter 18 MSB Insertion-A Parameter 18 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 27` | Sound Common / Insertion A | Insertion-A Parameter 19 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 29` | Sound Common / Insertion A | Insertion-A Parameter 19 LSB Insertion-A Parameter 20 MSB Insertion-A Parameter 20 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 2B` | Sound Common / Insertion A | Insertion-A Parameter 21 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 2D` | Sound Common / Insertion A | Insertion-A Parameter 21 LSB Insertion-A Parameter 22 MSB Insertion-A Parameter 22 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 2F` | Sound Common / Insertion A | Insertion-A Parameter 23 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 31` | Sound Common / Insertion A | Insertion-A Parameter 23 LSB Insertion-A Parameter 24 MSB Insertion-A Parameter 24 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 2p 33` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 35` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 37` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 39` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 3B` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 3D` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 3F` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 41` | Sound Common / Insertion A | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 2p 43` | Sound Common / Insertion A | Side Chain Part | 1 | 11, 7F | 7F | 0:part1, …, 10:part11, 16:A/D, 17:Master, 127: Off | `` |  | from Yamaha Data List |
| `31 3p 00` | Sound Common / Insertion B | Insertion-B Type MSB Insertion-B Type LSB | 2 | 0D 2F | 0D 2F | Refer to Effect Parameter List | `` | LP-HP FILTER | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — insertion B block: all 26 readable addresses answered on part 8, and all were restored by write — also `from Yamaha Data List` |
| `31 3p 02` | Sound Common / Insertion B | Insertion-B Template Number | 1 | 00 - 7F | 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 03` | Sound Common / Insertion B | Insertion-B Parameter 1 MSB | 2 | 00 - 7F 00 - 7F | 02 00 | ˶ | `Frequency` |  | from Yamaha Data List |
| `31 3p 05` | Sound Common / Insertion B | Insertion-B Parameter 1 LSB Insertion-B Parameter 2 MSB Insertion-B Parameter 2 LSB | 2 | 00 - 7F 00 - 7F | 00 10 | ˶ | `Resonance` |  | from Yamaha Data List |
| `31 3p 07` | Sound Common / Insertion B | Insertion-B Parameter 3 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 09` | Sound Common / Insertion B | Insertion-B Parameter 3 LSB Insertion-B Parameter 4 MSB Insertion-B Parameter 4 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 0B` | Sound Common / Insertion B | Insertion-B Parameter 5 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 0D` | Sound Common / Insertion B | Insertion-B Parameter 5 LSB Insertion-B Parameter 6 MSB Insertion-B Parameter 6 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 0F` | Sound Common / Insertion B | Insertion-B Parameter 7 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 11` | Sound Common / Insertion B | Insertion-B Parameter 7 LSB Insertion-B Parameter 8 MSB Insertion-B Parameter 8 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 13` | Sound Common / Insertion B | Insertion-B Parameter 9 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 15` | Sound Common / Insertion B | Insertion-B Parameter 9 LSB Insertion-B Parameter 10 MSB Insertion-B Parameter 10 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 17` | Sound Common / Insertion B | Insertion-B Parameter 11 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 19` | Sound Common / Insertion B | Insertion-B Parameter 11 LSB Insertion-B Parameter 12 MSB Insertion-B Parameter 12 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 1B` | Sound Common / Insertion B | Insertion-B Parameter 13 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 1D` | Sound Common / Insertion B | Insertion-B Parameter 13 LSB Insertion-B Parameter 14 MSB Insertion-B Parameter 14 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 1F` | Sound Common / Insertion B | Insertion-B Parameter 15 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 21` | Sound Common / Insertion B | Insertion-B Parameter 15 LSB Insertion-B Parameter 16 MSB Insertion-B Parameter 16 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 23` | Sound Common / Insertion B | Insertion-B Parameter 17 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 25` | Sound Common / Insertion B | Insertion-B Parameter 17 LSB Insertion-B Parameter 18 MSB Insertion-B Parameter 18 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 27` | Sound Common / Insertion B | Insertion-B Parameter 19 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 29` | Sound Common / Insertion B | Insertion-B Parameter 19 LSB Insertion-B Parameter 20 MSB Insertion-B Parameter 20 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 2B` | Sound Common / Insertion B | Insertion-B Parameter 21 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 2D` | Sound Common / Insertion B | Insertion-B Parameter 21 LSB Insertion-B Parameter 22 MSB Insertion-B Parameter 22 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 2F` | Sound Common / Insertion B | Insertion-B Parameter 23 MSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 31` | Sound Common / Insertion B | Insertion-B Parameter 23 LSB Insertion-B Parameter 24 MSB Insertion-B Parameter 24 LSB | 2 | 00 - 7F 00 - 7F | 00 00 | ˶ | `` |  | from Yamaha Data List |
| `31 3p 33` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 35` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 37` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 39` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 3B` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 3D` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 3F` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 41` | Sound Common / Insertion B | reserved | 2 |  | 00 00 |  | `` |  | from Yamaha Data List |
| `31 3p 43` | Sound Common / Insertion B | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 4p 00` | Sound Common / LFO | LFO Phase | 1 | 00 - 05 | 00 | 0, 90, 120, 180, 240, 270 | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Sound Common LFO block surveyed read-only on part 7: every documented address answered at its documented width — also `from Yamaha Data List` |
| `31 4p 01` | Sound Common / LFO | LFO Wave | 1 | 00 - 0C | 00 | Triangle, Triangle+, Saw Up, Saw Down, Squ1/4, Squ1/3, Square, Squ2/3, Squ3/4, Trapezoid, S/H1, S/H2, User | `LFOWaveSound` |  | from Yamaha Data List |
| `31 4p 02` | Sound Common / LFO | LFO Speed | 1 | 00 - 3F | 20 | 0 - 63 | `LFOSpeed` | Available when Tempo Sync is Off | from Yamaha Data List |
| `31 4p 03` | Sound Common / LFO | LFO Tempo Speed | 1 | 05 - 18 | 0B | 5 - 24 (16th, 8th/3, 16th., 8th, 4th/3, 8th., 4th, 2th/3, 4th., 2nd, Whole/3, 2nd., 4thX4, 4thX5, 4thX6, 4thX7, 4thX8, 4thX16,4thX32, 4thX64) | `LFOTempoSpeed` | Available when Tempo Sync is On | `verified on hardware` ([12-open-questions.md](12-open-questions.md)) — write sweep on part 7 accepted 24 and clamped 25, 30, 40, 52 and 60 to 24 — also `from Yamaha Data List` |
| `31 4p 04` | Sound Common / LFO | LFO Tempo Sync | 1 | 00 - 01 | 00 | Off, On | `LFOTempoSync` | Default value for Drum track is 00 (Off) | from Yamaha Data List |
| `31 4p 05` | Sound Common / LFO | LFO Delay Time | 1 | 00 - 7F | 00 | 0 - 127 | `LFODelayTime` |  | from Yamaha Data List |
| `31 4p 06` | Sound Common / LFO | LFO Fade In Time | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `31 4p 07` | Sound Common / LFO | LFO Hold Time | 1 | 00 - 7F | 7F | 0 - 126, Hold | `` |  | from Yamaha Data List |
| `31 4p 08` | Sound Common / LFO | LFO Fade Out Time | 1 | 00 - 7F | 40 | 0 - 127 | `` |  | from Yamaha Data List |
| `31 4p 09` | Sound Common / LFO | LFO Key On Reset | 1 | 00 - 02 | 02 | Off, Each-On, 1st-On | `` | Default value for Drum track is 00 (Off) | from Yamaha Data List |
| `31 4p 0A` | Sound Common / LFO | LFO Play Mode | 1 | 00 - 01 | 00 | Loop, One-shot | `` |  | from Yamaha Data List |
| `31 4p 0B` | Sound Common / LFO | LFO Box1 Destination | 1 | 00 - 44 | 40 | 0 - 68 | `LFOBox1Destination` |  | from Yamaha Data List |
| `31 4p 0C` | Sound Common / LFO | LFO Box1 Depth | 1 | 00 - 7F | 00 | 0 - 127 | `LFOBox1Depth` |  | from Yamaha Data List |
| `31 4p 0D` | Sound Common / LFO | reserved | 1 |  | 0F |  | `` |  | from Yamaha Data List |
| `31 4p 0E` | Sound Common / LFO | LFO Box2 Destination | 1 | 00 - 45 | 41 | 0 - 68 | `` |  | from Yamaha Data List |
| `31 4p 0F` | Sound Common / LFO | LFO Box2 Depth | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `31 4p 10` | Sound Common / LFO | reserved | 1 |  | 0F |  | `` |  | from Yamaha Data List |
| `31 4p 11` | Sound Common / LFO | LFO Box3 Destination | 1 | 00 - 45 | 42 | 0 - 68 | `` |  | from Yamaha Data List |
| `31 4p 12` | Sound Common / LFO | LFO Box3 Depth | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `31 4p 13` | Sound Common / LFO | reserved | 1 |  | 0F |  | `` |  | from Yamaha Data List |
| `31 4p 14` | Sound Common / LFO | User Wave Total Step | 1 | 00 - 06 | 06 | 2 steps, 3 steps, 4 steps, 6 steps, 8 steps, 12 steps, 16 steps | `` |  | from Yamaha Data List |
| `31 4p 15` | Sound Common / LFO | User Wave Slope | 1 | 00 - 03 | 00 | Off, Up, Down, Up&Down | `` |  | from Yamaha Data List |
| `31 4p 16` | Sound Common / LFO | User Wave Step Value 1 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 17` | Sound Common / LFO | User Wave Step Value 2 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 18` | Sound Common / LFO | User Wave Step Value 3 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 19` | Sound Common / LFO | User Wave Step Value 4 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 1A` | Sound Common / LFO | User Wave Step Value 5 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 1B` | Sound Common / LFO | User Wave Step Value 6 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 1C` | Sound Common / LFO | User Wave Step Value 7 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 1D` | Sound Common / LFO | User Wave Step Value 8 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 1E` | Sound Common / LFO | User Wave Step Value 9 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 1F` | Sound Common / LFO | User Wave Step Value 10 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 20` | Sound Common / LFO | User Wave Step Value 11 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 21` | Sound Common / LFO | User Wave Step Value 12 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 22` | Sound Common / LFO | User Wave Step Value 13 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 23` | Sound Common / LFO | User Wave Step Value 14 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 24` | Sound Common / LFO | User Wave Step Value 15 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 25` | Sound Common / LFO | User Wave Step Value 16 | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `31 4p 26` | Sound Common / LFO | LFO Random Speed Depth | 1 | 00 - 7F | 00 | 0 - 127 | `` | Available when Tempo Sync is Off | from Yamaha Data List |
| `31 5p 00` | Sound Common / Arpeggiator | ARP Template | 1 | 00 - 0F | 00 | Off, Up, Up 2Oct, Down, Down 2Oct, Random, Random 2Oct, Up/Down A, Up/Down A 2Oct, Up/Down B, Up/Down B 2Oct, Thumb Up, Unison, Chord Trigger1, Chord Trigger2, As Played | `ArpTemplate` | Affects ARP Switch / Key Mode / Octave Range / Type | from Yamaha Data List |
| `31 5p 01` | Sound Common / Arpeggiator | ARP Switch | 1 | 00 - 01 | 00 | Off, On | `ArpSwitch` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 (ARP Switch off) on parts 8 and 9 — also `from Yamaha Data List` |
| `31 5p 02` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 03` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 04` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 05` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 06` | Sound Common / Arpeggiator | ARP Loop | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `31 5p 07` | Sound Common / Arpeggiator | ARP Hold | 1 | 00 - 02 | 01 | Sync-Off, Off, On | `` |  | from Yamaha Data List |
| `31 5p 08` | Sound Common / Arpeggiator | ARP Unit Multiply | 1 | 00 - 09 | 03 | 50%, 66%, 75%, 100%, 133%, 150%, 200%, 266%, 300%, 400% | `ArpUnit` |  | from Yamaha Data List |
| `31 5p 09` | Sound Common / Arpeggiator | ARP Note Limit Low | 1 | 00 - 7F | 00 | C-2 ... G8 | `` |  | from Yamaha Data List |
| `31 5p 0A` | Sound Common / Arpeggiator | ARP Note Limit High | 1 | 00 - 7F | 7F | C-2 ... G8 | `` |  | from Yamaha Data List |
| `31 5p 0B` | Sound Common / Arpeggiator | ARP Velocity Limit Low | 1 | 01 - 7F | 01 | 1 - 127 | `` |  | from Yamaha Data List |
| `31 5p 0C` | Sound Common / Arpeggiator | ARP Velocity Limit High | 1 | 01 - 7F | 7F | 1 - 127 | `` |  | from Yamaha Data List |
| `31 5p 0D` | Sound Common / Arpeggiator | ARP Key Mode | 1 | 00 - 04 | 00 | Sort, Thru, Direct, Sort+Drct, Thru+Drct | `ArpKeyMode` |  | from Yamaha Data List |
| `31 5p 0E` | Sound Common / Arpeggiator | ARP Vel Mode | 1 | 00 - 01 | 01 | Original, Thru | `` |  | from Yamaha Data List |
| `31 5p 0F` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 10` | Sound Common / Arpeggiator | ARP Quantize Value | 1 | 03 | 03 | 120 | `` |  | from Yamaha Data List |
| `31 5p 11` | Sound Common / Arpeggiator | ARP Quantize Strength | 1 | 00 - 64 | 00 | 0 - 100[%] | `` |  | from Yamaha Data List |
| `31 5p 12` | Sound Common / Arpeggiator | ARP Velocity Rate MSB ARP Velocity Rate LSB | 2 | 00 - 01 00 - 7F | 00 64 | 0 - 200[%] 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | from Yamaha Data List |
| `31 5p 14` | Sound Common / Arpeggiator | ARP Gate Time Rate MSB | 2 | 00 - 01 00 - 7F | 00 64 | 0 - 200[%] | `ArpGateTimeRate` |  | from Yamaha Data List |
| `31 5p 16` | Sound Common / Arpeggiator | ARP Gate Time Rate LSB Swing Offset MSB Swing Offset LSB | 2 | 00 - 01 00 - 7F | 01 00 | 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 -60 - 0 - +60 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `SwingOffset` |  | from Yamaha Data List |
| `31 5p 18` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 19` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 1A` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 1B` | Sound Common / Arpeggiator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 1C` | Sound Common / Arpeggiator | ARP Octave Range | 1 | 3D - 43 | 40 | -3 - 0 - +3 | `ArpOctaveRange` |  | from Yamaha Data List |
| `31 5p 1D` | Sound Common / Arpeggiator | Reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `31 5p 1E` | Sound Common / Arpeggiator | ARP Type MSB | 2 | 00 - 00 00 - 08 | 00 00 | Up, Down, Random, Up Down 1, Up Down 2, Slap & Pop, Unison, Rhythm 1, Rhythm 2 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `ArpAssignType` |  | from Yamaha Data List |
