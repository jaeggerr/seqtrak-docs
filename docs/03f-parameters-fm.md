# FM engine (`48`, `49`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

56 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `48 09 00` | Sound DX / Common | Algorithm | 1 | 00 - 0B | 00 | 1 - 12 | `Algorithm` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — DX Common block read in full on hardware: 14 of 14 controls answered (Algorithm read 09) — also `from Yamaha Data List` |
| `48 09 01` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `48 09 02` | Sound DX / Common | Pitch Bend Sensitivity | 1 | 28 - 58 | 42 | -24 - 0 - +24 [semitones] | `PitchBendSensitivity` |  | from Yamaha Data List |
| `48 09 03` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `48 09 04` | Sound DX / Common | LFO Wave | 1 | 00 - 06 | 00 | 0:Sin, 1:Tri, 2:Saw-Up, 3:Saw-Down, 4:Square, 5:S&H8, 6:S&H | `LFOWave` |  | from Yamaha Data List |
| `48 09 05` | Sound DX / Common | LFO Speed | 1 | 00 - 7F | 40 | 0 - 127 | `LFOSpeed` |  | from Yamaha Data List |
| `48 09 06` | Sound DX / Common | LFO Delay | 1 | 00 - 7F | 00 | 0 - 127 | `LFODelay` |  | from Yamaha Data List |
| `48 09 07` | Sound DX / Common | LFO PMD | 1 | 00 - 7F | 00 | 0 - 127 | `PMDDepth` |  | from Yamaha Data List |
| `48 09 08` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `48 09 09` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `48 09 0A` | Sound DX / Common | PEG Rate 1 | 1 | 00 - 7F | 40 | 0 - 127 | `PEGRate1` |  | from Yamaha Data List |
| `48 09 0B` | Sound DX / Common | PEG Rate 2 | 1 | 00 - 7F | 40 | 0 - 127 | `PEGRate2` |  | from Yamaha Data List |
| `48 09 0C` | Sound DX / Common | PEG Rate 3 | 1 | 00 - 7F | 40 | 0 - 127 | `PEGRate3` |  | from Yamaha Data List |
| `48 09 0D` | Sound DX / Common | PEG Rate 4 | 1 | 00 - 7F | 40 | 0 - 127 | `PEGRate4` |  | from Yamaha Data List |
| `48 09 0E` | Sound DX / Common | PEG Level 1 | 1 | 10 - 70 | 40 | -48 - 0 - 48 (16 - 64 - 112) +/- 4Oct | `PEGLevel1` |  | from Yamaha Data List |
| `48 09 0F` | Sound DX / Common | PEG Level 2 | 1 | 10 - 70 | 40 | -48 - 0 - 48 (16 - 64 - 112) +/- 4Oct | `PEGLevel2` |  | from Yamaha Data List |
| `48 09 10` | Sound DX / Common | PEG Level 3 | 1 | 10 - 70 | 40 | -48 - 0 - 48 (16 - 64 - 112) +/- 4Oct | `PEGLevel3` |  | from Yamaha Data List |
| `48 09 11` | Sound DX / Common | PEG Level 4 | 1 | 10 - 70 | 40 | -48 - 0 - 48 (16 - 64 - 112) +/- 4Oct | `PEGLevel4` |  | from Yamaha Data List |
| `48 09 12` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `48 09 13` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `48 09 14` | Sound DX / Common | reserved | 1 | 0 - 127 (decimal) | 00 | -64 - 63 | `ModAmount` |  | from Yamaha Data List |
| `48 09 15` | Sound DX / Common | reserved | 1 | 0 - 127 (decimal) | 00 | -64 - 63 | `ModFeedback` |  | from Yamaha Data List |
| `48 09 16` | Sound DX / Common | reserved | 1 | 0 - 127 (decimal) | 00 | -64 - 63 | `ModFrequencyRatio` |  | from Yamaha Data List |
| `48 09 17` | Sound DX / Common | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 00` | Sound DX / Operator | ON/OFF | 1 | 00 - 01 | 01 | Off, On | `IsOn` |  | from Yamaha Data List |
| `49 o9 01` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 02` | Sound DX / Operator | EG Rate 1 | 1 | 00 - 7F | 7F |  | `EGRate1` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — DX Operator block read in full on all four operators: 25 of 25 controls answered each, 100 replies — also `from Yamaha Data List` |
| `49 o9 03` | Sound DX / Operator | EG Rate 2 | 1 | 00 - 7F | 7F |  | `EGRate2` |  | from Yamaha Data List |
| `49 o9 04` | Sound DX / Operator | EG Rate 3 | 1 | 00 - 7F | 7F |  | `EGRate3` |  | from Yamaha Data List |
| `49 o9 05` | Sound DX / Operator | EG Rate 4 | 1 | 00 - 7F | 64 |  | `EGRate4` |  | from Yamaha Data List |
| `49 o9 06` | Sound DX / Operator | EG Level 1 | 1 | 00 - 7F | 7F | 0 - 127 | `EGLevel1` |  | from Yamaha Data List |
| `49 o9 07` | Sound DX / Operator | EG Level 2 | 1 | 00 - 7F | 7F | 0 - 127 | `EGLevel2` |  | from Yamaha Data List |
| `49 o9 08` | Sound DX / Operator | EG Level 3 | 1 | 00 - 7F | 7F | 0 - 127 | `EGLevel3` |  | from Yamaha Data List |
| `49 o9 09` | Sound DX / Operator | EG Level 4 | 1 | 00 - 7F | 00 | 0 - 127 | `EGLevel4` |  | from Yamaha Data List |
| `49 o9 0A` | Sound DX / Operator | EG Keyboard Rate Scaling | 1 | 00 - 7F | 00 | 0 - 127 | `KeyRateScaling` |  | from Yamaha Data List |
| `49 o9 0B` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 0C` | Sound DX / Operator | Keyboard Level Scaling Left Depth | 1 | 00 - 7F | 00 | -127 - 127 | `DepthKeyLevelScalingLeft` |  | from Yamaha Data List |
| `49 o9 0D` | Sound DX / Operator | Keyboard Level Scaling Right Depth | 1 | 00 - 7F | 00 | -127 - 127 | `DepthKeyLevelScalingRight` |  | from Yamaha Data List |
| `49 o9 0E` | Sound DX / Operator | Keyboard Level Scaling Left Curve | 1 | 00 - 03 | 00 | 0: -LIN, 1: -EXP, 2: +EXP, 3: +LIN | `CurveKeyLevelScalingLeft` |  | from Yamaha Data List |
| `49 o9 0F` | Sound DX / Operator | Keyboard Level Scaling Right Curve | 1 | 00 - 03 | 03 | 0: -LIN, 1: -EXP, 2: +EXP, 3: +LIN | `CurveKeyLevelScalingRight` |  | from Yamaha Data List |
| `49 o9 10` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 11` | Sound DX / Operator | LFO AMD Depth | 1 | 00 - 7F | 00 | 0 - 127 | `AMDDepth` |  | from Yamaha Data List |
| `49 o9 12` | Sound DX / Operator | Level Velocity Sensitivity | 1 | 00 - 7F | 00 | 0 - 127 | `VelocitySensitivity` |  | from Yamaha Data List |
| `49 o9 13` | Sound DX / Operator | Level Output Level | 1 | 00 - 7F | 64 | 0 - 127 | `OutputLevel` | Init value for Operator2/3 is 0 | from Yamaha Data List |
| `49 o9 14` | Sound DX / Operator | Level Feedback Level | 1 | 00 - 7F | 00 | 0 - 127 | `FeedbackLevel` |  | from Yamaha Data List |
| `49 o9 15` | Sound DX / Operator | Level Feedback Type | 1 | 00 - 01 | 00 | 0:SAW, 1:SQUARE | `FeedbackType` |  | from Yamaha Data List |
| `49 o9 16` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 17` | Sound DX / Operator | LFO PMD ON/OFF | 1 | 00 - 01 | 01 | Off, On | `IsOnPMD` |  | from Yamaha Data List |
| `49 o9 18` | Sound DX / Operator | PEG ON/OFF | 1 | 00 - 01 | 01 | Off, On | `IsOnPEG` |  | from Yamaha Data List |
| `49 o9 19` | Sound DX / Operator | Freq. Mode | 1 | 00 - 01 | 00 | 0:RATIO, 1:FIXED | `FreqMode` |  | from Yamaha Data List |
| `49 o9 1A` | Sound DX / Operator | Freq. Coarse | 1 | 00 - 1F | 01 | 0 - 31 | `FreqCoarse` |  | from Yamaha Data List |
| `49 o9 1B` | Sound DX / Operator | Freq. Fine | 1 | 00 - 63 | 00 | 0 - 99 | `FreqFine` |  | from Yamaha Data List |
| `49 o9 1C` | Sound DX / Operator | Freq. Detune | 1 | 00 - 7F | 40 | -64 - 0 - +63 (0 - 64 - 127) | `FreqDetune` |  | from Yamaha Data List |
| `49 o9 1D` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 1E` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `49 o9 1F` | Sound DX / Operator | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
