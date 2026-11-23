# AWM elements and sampler (`41`, `42`, `50`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

249 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `41 ep 00` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Element Assign | 1 | 00 - 01 | 01 | Off, On | `` | Init value for Element 2 - 8 is Off | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Element Assign read 01 on part 7 elements 1 and 2 (41 07 00, 41 17 00); block surveyed read-only, see the document — also `from Yamaha Data List` |
| `41 ep 01` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Wave Select | 1 | 00 - 01 | 00 | 0=Preset, 1=User | `` | SAMPLER track is fixed to 1 (User) | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — part 8 (SYNTH 2) element 0 Wave Select read 01 = User after a WAV import, 4/4 attempts, with part 7 (41 07 01) and part 0 (41 00 01) reading 00 = Preset as witnesses in the same loop and the tempo as control: a non-SAMPLER element does reach user wave memory. Also on 2026-11-23: writable on a drum part -- part 0 element 0 written 01 (User) and read back 01, with part 1 and part 7 unmoved as witnesses and the tempo as control, then restored to 00. The field accepts the value and reports it; audibility was not tested — also `from Yamaha Data List` |
| `41 ep 02` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Element Group Number | 1 | 00 - 07 | 00 | 1 - 8 | `` |  | from Yamaha Data List |
| `41 ep 03` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Wave Number MSB Wave Number LSB | 2 | 00 - 1F 00 - 7F | 00 01 | 1 - 4096 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` | User Wave : | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Wave Number read as two data bytes (05 06) at the base address; 41 ep 04 is silent on four attempts, twice. Also on 2026-11-23: part 8 element 0 read 03 11 = 401 after a WAV import, 4/4 attempts, which equals the ContentNumber - 8192 of the waveform in the .Y3S exported from that same sound (8593 - 8192). Also on 2026-11-23: writable on a drum part -- part 0 element 0 written 03 11 (401) and read back, then restored to 07 7F (1023) — also `from Yamaha Data List` |
| `41 ep 05` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 06` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 07` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` | 1 - 2048 Init value for Synth/ SAMPLER track is 1 | from Yamaha Data List |
| `41 ep 08` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Trigger/Gate Mode | 1 | 00 - 01 | 00 | Trigger, Gate | `TriggerGateMode` |  | from Yamaha Data List |
| `41 ep 09` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 01 |  | `` |  | from Yamaha Data List |
| `41 ep 0A` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Alternate Group | 1 | 00 - 7F | 00 | 0=off, 1 - 127 | `AlternateGroup` |  | from Yamaha Data List |
| `41 ep 0B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Pan | 1 | 01 - 7F | 40 | L63 ... C ... R63 | `Pan` |  | from Yamaha Data List |
| `41 ep 0C` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Random Pan Depth | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 0D` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Alternate Pan Depth | 1 | 00 - 7F | 40 | L64 ... C ... R63 | `` |  | from Yamaha Data List |
| `41 ep 0E` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Scaling Pan Depth | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 0F` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | XA Control | 1 | 00 - 07 | 00 | Normal, Legato, Key Off, Cycle, Random | `` |  | from Yamaha Data List |
| `41 ep 10` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Note Limit Low | 1 | 00 - 7F | 00 | C-2 ... G8 | `` |  | from Yamaha Data List |
| `41 ep 11` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Note Limit High | 1 | 00 - 7F | 7F | C-2 ... G8 | `` |  | from Yamaha Data List |
| `41 ep 12` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Velocity Limit Low | 1 | 01 - 7F | 01 | 1 - 127 | `` |  | from Yamaha Data List |
| `41 ep 13` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Velocity Limit High | 1 | 01 - 7F | 7F | 1 - 127 | `` |  | from Yamaha Data List |
| `41 ep 14` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Velocity Cross Fade | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 15` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Key On Delay | 1 | 00 - 7F | 00 | 0 - 127 | `` | Available when Tempo Sync is Off | from Yamaha Data List |
| `41 ep 16` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Key On Delay Tempo Sync | 1 | 00 - 01 | 00 | Off, On | `` |  | from Yamaha Data List |
| `41 ep 17` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 18` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Insertion Effect Switch | 1 | 00 - 02 | 01 | Thru, InsA, InsB | `` |  | from Yamaha Data List |
| `41 ep 19` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Output Select | 1 | 00 | 00 | 0=MainL&R | `` |  | from Yamaha Data List |
| `41 ep 1A` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 1B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 5 |  | 00 00 00 00 | 00 | `` |  | from Yamaha Data List |
| `41 ep 20` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 5 |  | 00 00 00 00 | 00 | `` |  | from Yamaha Data List |
| `41 ep 25` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 26` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | LFO Speed Range | 1 | 00 - 01 | 00 | Normal, Extended | `` |  | from Yamaha Data List |
| `41 ep 27` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | LFO Extended Speed | 2 | 00 - 03 00 - 7F | 00 00 | 0 - 415 | `` | Available when | from Yamaha Data List |
| `41 ep 29` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 2A` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | LFO Box Switch | 1 | 00 - 07 | 07 | 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 bit6-3: reserved bit2: off,on box3 bit1: off,on box2 bit0: off,on box1 | `` | LFO Speed Range is Extended Available when | from Yamaha Data List |
| `41 ep 2B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Key On Delay Tempo | 1 | 05 - 15 | 0B | 16th, 8th/3, 16th., 8th, 4th/3, 8th., 4th, 2th/3, 4th., 2nd, Whole/3, 2nd., 4thX4, 4thX5, 4thX6, 4thX7, 4thX8 | `` | Tempo Sync is On | from Yamaha Data List |
| `41 ep 2C` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Half Damper Switch | 1 | 00 - 01 | 00 | Off, On | `` |  | from Yamaha Data List |
| `41 ep 2D` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 2E` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Element Level | 1 | 00 - 7F | 64 | 0 - 127 | `ElementLevel` |  | from Yamaha Data List |
| `41 ep 2F` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Velocity Sensitivity | 1 | 00 - 7F | 54 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 30` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Velocity Offset | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 31` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Sens Key Curve | 1 | 00 - 04 | 03 | 00 - 04 | `` |  | from Yamaha Data List |
| `41 ep 32` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 33` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Attack Time | 1 | 00 - 7F | 00 | 0 - 127 | `AEGAttackTime` |  | from Yamaha Data List |
| `41 ep 34` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Decay 1 Time | 1 | 00 - 7F | 40 | 0 - 127 | `AEGDecay1Time` |  | from Yamaha Data List |
| `41 ep 35` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Decay 2 Time | 1 | 00 - 7F | 40 | 0 - 127 | `AEGDecay2Time` |  | from Yamaha Data List |
| `41 ep 36` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Half Damper Time | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 37` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Release Time | 1 | 00 - 7F | 14 | 0 - 127 | `AEGReleaseTime` |  | from Yamaha Data List |
| `41 ep 38` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Init Level | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 39` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Attack Level | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 3A` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Decay 1 Level | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 3B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Decay 2 Level | 1 | 00 - 7F | 7F | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 3C` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 3D` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Time Velocity Segment | 1 | 00 - 04 | 04 | Attack, Atk+Dcy, Decay, Atk+Rls, All | `` |  | from Yamaha Data List |
| `41 ep 3E` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Time Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 3F` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Time Key Follow Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 40` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Time Key Follow Center Note | 1 | 00 - 7F | 18 | C-2 ... G8 | `` |  | from Yamaha Data List |
| `41 ep 41` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Break Point 1 | 1 | 00 - 7C | 24 | C-2 ... E8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `41 ep 42` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Break Point 2 | 1 | 01 - 7D | 30 | C#-2 ... F8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `41 ep 43` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Break Point 3 | 1 | 02 - 7E | 3C | D-2 ... F#8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `41 ep 44` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Break Point 4 | 1 | 03 - 7F | 48 | D#-2 ... G8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `41 ep 45` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Offset 1 MSB | 2 | 00 - 01 00 - 7F | 01 00 | -128 - +127 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | from Yamaha Data List |
| `41 ep 47` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Offset 1 LSB Level Scaling Offset 2 MSB Level Scaling Offset 2 LSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `` |  | from Yamaha Data List |
| `41 ep 49` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Offset 3 MSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `` |  | from Yamaha Data List |
| `41 ep 4B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Scaling Offset 3 LSB Level Scaling Offset 4 MSB Level Scaling Offset 4 LSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `` |  | from Yamaha Data List |
| `41 ep 4D` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Level Key Follow Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 4E` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | AEG Time Key Follow Sensitivity Release Adjustment | 1 | 00 - 7F | 40 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 4F` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Coarse Tune | 1 | 28 - 58 | 40 | -24 - +24 | `CoarseTune` |  | from Yamaha Data List |
| `41 ep 50` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Fine Tune | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 51` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Pitch Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 52` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `41 ep 53` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Random Pitch Depth | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 54` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Pitch Key Follow Sensitivity | 1 | 00 - 7F | 60 | -200 - +200[%] | `` |  | from Yamaha Data List |
| `41 ep 55` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Pitch Key Follow Sensitivity Center Note | 1 | 00 - 7F | 3C | C-2 ... G8 | `` |  | from Yamaha Data List |
| `41 ep 56` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | Pitch Fine Scaling Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 57` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Hold Time | 1 | 00 - 7F | 00 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 58` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Attack Time | 1 | 00 - 7F | 28 | 0 - 127 | `PEGAttackTime` |  | from Yamaha Data List |
| `41 ep 59` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Decay 1 Time | 1 | 00 - 7F | 40 | 0 - 127 | `PEGDecay1Time` |  | from Yamaha Data List |
| `41 ep 5A` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Decay 2 Time | 1 | 00 - 7F | 40 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 5B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Release Time | 1 | 00 - 7F | 40 | 0 - 127 | `` |  | from Yamaha Data List |
| `41 ep 5C` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Hold Level MSB | 2 | 00 - 01 00 - 7F | 01 00 | -128 - +127 (-4800 - +4800[cent]) 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | from Yamaha Data List |
| `41 ep 5E` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Hold Level LSB PEG Attack Level MSB PEG Attack Level LSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `PEGAttackLevel` |  | from Yamaha Data List |
| `41 ep 60` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Decay 1 Level MSB PEG Decay 1 Level LSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `PEGDecay1Level` |  | from Yamaha Data List |
| `41 ep 62` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Decay 2 Level MSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `PEGDecay2Level` |  | from Yamaha Data List |
| `41 ep 64` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Decay 2 Level LSB PEG Release Level MSB PEG Release Level LSB | 2 | 00 - 01 00 - 7F | 01 00 | ˶ | `PEGReleaseLevel` |  | from Yamaha Data List |
| `41 ep 66` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Depth | 1 | 00 - 7F | 54 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 67` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Time Velocity Sensitivity Segment | 1 | 00 - 04 | 04 | Attack, Atk+Dcy, Decay, Atk+Rls, All | `` |  | from Yamaha Data List |
| `41 ep 68` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Time Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 69` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Depth Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 6A` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Depth Velocity Sensitivity Curve | 1 | 00 - 04 | 02 | 0 - 4 | `` |  | from Yamaha Data List |
| `41 ep 6B` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Time Key Follow Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `41 ep 6C` | Sound Drum/Synth/SAMPLER / Oscillator/Amplitude/Pitch | PEG Time Key Follow Sensitivity Center Note | 1 | 00 - 7F | 3C | C-2 ... G8 | `` |  | from Yamaha Data List |
| `42 ep 00` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Type | 1 | 00 - 15 | 04 | LPF24D, LPF24A, LPF18, LPF18s, LPF12+HPF12, LPF6+HPF12, HPF24D, HPF12, BPF12D, (reserved), BPFw, BPF6, BEF12, BEF6, DualLPF, DualHPF, DualBPF, DualBEF, (reserved), | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Filter Type read 00 on part 7 elements 1 and 2; one data byte — also `from Yamaha Data List` |
| `42 ep 01` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Frequency MSB 0 Filter Cutoff Frequency LSB | 2 | 00 - 01 00 - 7F | 01 20 | LPF12+BPF6, (reserved), Thru - 255 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Filter Cutoff Frequency read as two data bytes (01 3E) at the base address; 42 ep 02 is silent on four attempts, twice — also `from Yamaha Data List` |
| `42 ep 03` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `42 ep 04` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | reserved | 1 |  | 02 |  | `` |  | from Yamaha Data List |
| `42 ep 05` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Resonance/Width 0 | 1 | 00 - 7F | 00 | - 127 | `` | Not available when Filter Type is LPF6/Thru | from Yamaha Data List |
| `42 ep 06` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Resonance Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `42 ep 07` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | HPF Cutoff Frequency MSB 0 HPF Cutoff Frequency LSB | 2 | 00 - 01 00 - 7F | 00 00 | - 255 | `` |  | from Yamaha Data List |
| `42 ep 09` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | reserved | 1 |  | 40 |  | `` |  | from Yamaha Data List |
| `42 ep 0A` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Distance MSB | 2 | 00 - 01 00 - 7F | 01 00 | 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 -128 - +127 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` | Available when Filter Type is DualLPF/HPF/ BPF/BEF | from Yamaha Data List |
| `42 ep 0C` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Distance LSB Filter Gain MSB 0 Filter Gain LSB | 2 | 00 - 01 00 - 7F | 01 66 | - 255 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | from Yamaha Data List |
| `42 ep 0E` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Hold Time 0 | 1 | 00 - 7F | 00 | - 127 | `` |  | from Yamaha Data List |
| `42 ep 0F` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Attack Time 0 | 1 | 00 - 7F | 00 | - 127 | `` |  | from Yamaha Data List |
| `42 ep 10` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Decay 1 Time 0 | 1 | 00 - 7F | 40 | - 127 | `` |  | from Yamaha Data List |
| `42 ep 11` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Decay 2 Time 0 | 1 | 00 - 7F | 40 | - 127 | `` |  | from Yamaha Data List |
| `42 ep 12` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Release Time 0 | 1 | 00 - 7F | 50 | - 127 | `` |  | from Yamaha Data List |
| `42 ep 13` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Hold Level MSB | 2 | 00 - 01 00 - 7F | 01 00 | -128 - +127 (-9600 - +9600[cent]) 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | from Yamaha Data List |
| `42 ep 15` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Hold Level LSB ˶ FEG Attack Level MSB FEG Attack Level LSB | 2 | 00 - 01 00 - 7F | 01 7F |  | `` |  | from Yamaha Data List |
| `42 ep 17` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | ˶ FEG Decay 1 Level MSB FEG Decay 1 Level LSB | 2 | 00 - 01 00 - 7F | 01 7F |  | `` |  | from Yamaha Data List |
| `42 ep 19` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | ˶ FEG Decay 2 Level MSB | 2 | 00 - 01 00 - 7F | 01 7F |  | `` |  | from Yamaha Data List |
| `42 ep 1B` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Decay 2 Level LSB ˶ FEG Release Level MSB FEG Release Level LSB | 2 | 00 - 01 00 - 7F | 01 00 |  | `` |  | from Yamaha Data List |
| `42 ep 1D` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Depth | 1 | 00 - 7F | 68 | -64 - +63 | `` |  | from Yamaha Data List |
| `42 ep 1E` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Time Velocity Sensitivity Segment | 1 | 00 - 04 | 04 | Attack, Atk+Dcy, Decay, Atk+Rls, All | `` |  | from Yamaha Data List |
| `42 ep 1F` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Time Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `42 ep 20` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Depth Velocity Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `42 ep 21` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Depth Velocity Sensitivity Curve 0 | 1 | 00 - 04 | 02 | - 4 | `` |  | from Yamaha Data List |
| `42 ep 22` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Time Key Follow Sensitivity | 1 | 00 - 7F | 40 | -64 - +63 | `` |  | from Yamaha Data List |
| `42 ep 23` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | FEG Time Key Follow Sensitivity Center Note | 1 | 00 - 7F | 18 | C-2 ... G8 | `` |  | from Yamaha Data List |
| `42 ep 24` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Break Point 1 | 1 | 00 - 7C | 24 | C-2 ... E8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `42 ep 25` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Break Point 2 | 1 | 01 - 7D | 30 | C#-2 ... F8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `42 ep 26` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Break Point 3 | 1 | 02 - 7E | 3C | D-2 ... F#8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `42 ep 27` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Break Point 4 | 1 | 03 - 7F | 48 | D#-2 ... G8 | `` | BP1<BP2 <BP3<BP4 | from Yamaha Data List |
| `42 ep 28` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Offset 1 MSB | 2 | 00 - 01 00 - 7F | 01 00 | -128 - +127 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `` |  | from Yamaha Data List |
| `42 ep 2A` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Offset 1 LSB ˶ Filter Cutoff Scaling Offset 2 MSB Filter Cutoff Scaling Offset 2 LSB | 2 | 00 - 01 00 - 7F | 01 00 |  | `` |  | from Yamaha Data List |
| `42 ep 2C` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | ˶ Filter Cutoff Scaling Offset 3 MSB | 2 | 00 - 01 00 - 7F | 01 00 |  | `` |  | from Yamaha Data List |
| `42 ep 2E` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Scaling Offset 3 LSB ˶ Filter Cutoff Scaling Offset 4 MSB Filter Cutoff Scaling Offset 4 LSB | 2 | 00 - 01 00 - 7F | 01 00 |  | `` |  | from Yamaha Data List |
| `42 ep 30` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Filter Cutoff Key Follow Sensitivity | 1 | 00 - 7F | 4A | -200 - +200[%] | `` |  | from Yamaha Data List |
| `42 ep 31` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | HPF Cutoff Key Follow Sensitivity | 1 | 00 - 7F | 40 | -200 - +200[%] | `` |  | from Yamaha Data List |
| `42 ep 32` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | EQ Type | 1 | 00 - 05 | 00 | 2-band, P.EQ, Boost6, Boost12, Boost18, Thru | `` |  | from Yamaha Data List |
| `42 ep 33` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | EQ Q 0 | 1 | 00 - 1F | 00 | - 31 (0.7 - 10.3) | `` | Available when | from Yamaha Data List |
| `42 ep 34` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | EQ 1 Frequency | 2 | 00 - 01 00 - 7F | 00 36 | 50.1 - 2.00k (2 Band) 139.7 - 12.9k (P.EQ) 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `EQ1Frequency` | EQ Type is P.EQ Available when EQ Type | from Yamaha Data List |
| `42 ep 36` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | EQ 1 Gain | 1 | 20 - 60 | 40 | -32 - +32 (-12.00 - +12.00[dB]) | `EQ1Gain` |  | from Yamaha Data List |
| `42 ep 37` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | EQ 2 Frequency | 2 | 01 03 - 71 | 01 67 | 503.8 - 10.1k 1st bit6-0 → bit13-7, 2nd bit6-0 → bit6-0 | `EQ2Frequency` | is 2-band/P.EQ Available when EQ Type is 2-band | from Yamaha Data List |
| `42 ep 39` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | EQ 2 Gain | 1 | 20 - 60 | 40 | -32 - +32 (-12.00 - +12.00[dB]) | `EQ2Gain` |  | from Yamaha Data List |
| `42 ep 3A` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO Wave | 1 | 00 - 02 | 01 | Saw, Triangle, Square | `LFOWave` |  | from Yamaha Data List |
| `42 ep 3B` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO Key On Sync | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `42 ep 3C` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO Key On Delay Time 0 | 1 | 00 - 7F | 00 | - 127 | `` |  | from Yamaha Data List |
| `42 ep 3D` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO Speed 0 | 1 | 00 - 3F | 26 | - 63 | `LFOSpeed` |  | from Yamaha Data List |
| `42 ep 3E` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO AMod Depth 0 | 1 | 00 - 7F | 00 | - 127 | `LFOAModDepth` |  | from Yamaha Data List |
| `42 ep 3F` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO PMod Depth 0 | 1 | 00 - 7F | 00 | - 127 | `LFOPModDepth` |  | from Yamaha Data List |
| `42 ep 40` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO FMod Depth 0 | 1 | 00 - 7F | 00 | - 127 | `LFOFModDepth` |  | from Yamaha Data List |
| `42 ep 41` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | LFO Fade In Time 0 | 1 | 00 - 7F | 00 | - 127 | `LFOFadeInTime` |  | from Yamaha Data List |
| `42 ep 42` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | reserved | 1 | 0 - 127 (decimal) | 00 | 0 - 2 | `LFODepthSelect` |  | from Yamaha Data List |
| `42 ep 43` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Common LFO Phase Offset | 1 | 00 - 05 | 00 | +0, +90, +120, +180, +240, +270 | `` |  | from Yamaha Data List |
| `42 ep 44` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Common LFO Box1 Depth Ratio 0 | 1 | 00 - 7F | 7F | - 127 | `` |  | from Yamaha Data List |
| `42 ep 45` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Common LFO Box2 Depth Ratio 0 | 1 | 00 - 7F | 7F | - 127 | `` |  | from Yamaha Data List |
| `42 ep 46` | Sound Drum/Synth/SAMPLER / Filter/EQ/LFO | Common LFO Box3 Depth Ratio 0 | 1 | 00 - 7F | 7F | - 127 | `` |  | from Yamaha Data List |
| `50 eA 00` | SAMPLER Sample / General | Sample Name 1 | 1 | 00 - 7F | 00 |  | `` | UTF8 (7-bit encoded) | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Sample name read on all seven slots and decoded 7-into-8 to readable UTF-8 (e.g. 'Bongo3 High 3'); 616 of 616 name addresses answered — also `from Yamaha Data List` |
| `50 eA 01` | SAMPLER Sample / General | Sample Name 2 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 02` | SAMPLER Sample / General | Sample Name 3 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 03` | SAMPLER Sample / General | Sample Name 4 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 04` | SAMPLER Sample / General | Sample Name 5 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 05` | SAMPLER Sample / General | Sample Name 6 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 06` | SAMPLER Sample / General | Sample Name 7 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 07` | SAMPLER Sample / General | Sample Name 8 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 08` | SAMPLER Sample / General | Sample Name 9 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 09` | SAMPLER Sample / General | Sample Name 10 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 0A` | SAMPLER Sample / General | Sample Name 11 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 0B` | SAMPLER Sample / General | Sample Name 12 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 0C` | SAMPLER Sample / General | Sample Name 13 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 0D` | SAMPLER Sample / General | Sample Name 14 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 0E` | SAMPLER Sample / General | Sample Name 15 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 0F` | SAMPLER Sample / General | Sample Name 16 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 10` | SAMPLER Sample / General | Sample Name 17 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 11` | SAMPLER Sample / General | Sample Name 18 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 12` | SAMPLER Sample / General | Sample Name 19 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 13` | SAMPLER Sample / General | Sample Name 20 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 14` | SAMPLER Sample / General | Sample Name 21 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 15` | SAMPLER Sample / General | Sample Name 22 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 16` | SAMPLER Sample / General | Sample Name 23 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 17` | SAMPLER Sample / General | Sample Name 24 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 18` | SAMPLER Sample / General | Sample Name 25 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 19` | SAMPLER Sample / General | Sample Name 26 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 1A` | SAMPLER Sample / General | Sample Name 27 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 1B` | SAMPLER Sample / General | Sample Name 28 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 1C` | SAMPLER Sample / General | Sample Name 29 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 1D` | SAMPLER Sample / General | Sample Name 30 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 1E` | SAMPLER Sample / General | Sample Name 31 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 1F` | SAMPLER Sample / General | Sample Name 32 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 20` | SAMPLER Sample / General | Sample Name 33 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 21` | SAMPLER Sample / General | Sample Name 34 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 22` | SAMPLER Sample / General | Sample Name 35 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 23` | SAMPLER Sample / General | Sample Name 36 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 24` | SAMPLER Sample / General | Sample Name 37 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 25` | SAMPLER Sample / General | Sample Name 38 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 26` | SAMPLER Sample / General | Sample Name 39 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 27` | SAMPLER Sample / General | Sample Name 40 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 28` | SAMPLER Sample / General | Sample Name 41 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 29` | SAMPLER Sample / General | Sample Name 42 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 2A` | SAMPLER Sample / General | Sample Name 43 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 2B` | SAMPLER Sample / General | Sample Name 44 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 2C` | SAMPLER Sample / General | Sample Name 45 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 2D` | SAMPLER Sample / General | Sample Name 46 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 2E` | SAMPLER Sample / General | Sample Name 47 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 2F` | SAMPLER Sample / General | Sample Name 48 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 30` | SAMPLER Sample / General | Sample Name 49 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 31` | SAMPLER Sample / General | Sample Name 50 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 32` | SAMPLER Sample / General | Sample Name 51 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 33` | SAMPLER Sample / General | Sample Name 52 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 34` | SAMPLER Sample / General | Sample Name 53 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 35` | SAMPLER Sample / General | Sample Name 54 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 36` | SAMPLER Sample / General | Sample Name 55 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 37` | SAMPLER Sample / General | Sample Name 56 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 38` | SAMPLER Sample / General | Sample Name 57 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 39` | SAMPLER Sample / General | Sample Name 58 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 3A` | SAMPLER Sample / General | Sample Name 59 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 3B` | SAMPLER Sample / General | Sample Name 60 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 3C` | SAMPLER Sample / General | Sample Name 61 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 3D` | SAMPLER Sample / General | Sample Name 62 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 3E` | SAMPLER Sample / General | Sample Name 63 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 3F` | SAMPLER Sample / General | Sample Name 64 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 40` | SAMPLER Sample / General | Sample Name 65 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 41` | SAMPLER Sample / General | Sample Name 66 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 42` | SAMPLER Sample / General | Sample Name 67 | 1 | 00 - 7F | 00 |  | `` | UTF8 (7-bit encoded) | from Yamaha Data List |
| `50 eA 43` | SAMPLER Sample / General | Sample Name 68 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 44` | SAMPLER Sample / General | Sample Name 69 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 45` | SAMPLER Sample / General | Sample Name 70 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 46` | SAMPLER Sample / General | Sample Name 71 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 47` | SAMPLER Sample / General | Sample Name 72 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 48` | SAMPLER Sample / General | Sample Name 73 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 49` | SAMPLER Sample / General | Sample Name 74 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 4A` | SAMPLER Sample / General | Sample Name 75 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 4B` | SAMPLER Sample / General | Sample Name 76 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 4C` | SAMPLER Sample / General | Sample Name 77 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 4D` | SAMPLER Sample / General | Sample Name 78 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 4E` | SAMPLER Sample / General | Sample Name 79 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 4F` | SAMPLER Sample / General | Sample Name 80 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 50` | SAMPLER Sample / General | Sample Name 81 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 51` | SAMPLER Sample / General | Sample Name 82 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 52` | SAMPLER Sample / General | Sample Name 83 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 53` | SAMPLER Sample / General | Sample Name 84 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 54` | SAMPLER Sample / General | Sample Name 85 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 55` | SAMPLER Sample / General | Sample Name 86 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 56` | SAMPLER Sample / General | Sample Name 87 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 57` | SAMPLER Sample / General | Sample Name 88 | 1 | 00 - 7F | 00 |  | `` | ˶ | from Yamaha Data List |
| `50 eA 58` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 59` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 5A` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 5B` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 5C` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 5D` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 5E` | SAMPLER Sample / General | reserved | 1 | 00 | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 5F` | SAMPLER Sample / General | Loop On/Off | 1 | 00 - 01 | 00 | Off, On | `LoopMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Loop On/Off read 00 on all seven slots, one data byte — also `from Yamaha Data List` |
| `50 eA 60` | SAMPLER Sample / General | - Loop Length | 4 | 00 00 00 | 00 00 00 00 | 0x00000050 - 0x00FFFFFF | `LoopLength` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Loop Length read as four data bytes at the base address on all seven slots — also `from Yamaha Data List` |
| `50 eA 64` | SAMPLER Sample / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 65` | SAMPLER Sample / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 66` | SAMPLER Sample / General | - Start Point | 4 | 00 00 00 | 00 00 00 00 | 0x00000000 - 0x00FFFFFF | `StartPoint` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — Start Point written 00 00 01 00 (128) on slot 7 and read back, End Point unmoved, restored to 00 00 00 00: a four-byte Parameter Change is accepted, 7-bit big-endian — also `from Yamaha Data List` |
| `50 eA 6A` | SAMPLER Sample / General | End Point | 4 | 00 00 00, | 00 00 00 00 | 0x00000000, 0x0000000F - 0x00FFFFFF | `EndPoint` | bit3-0 is | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — End Point read as four data bytes; decodes 7-bit big-endian to durations matching the sample names, under the documented 16 s ceiling — also `from Yamaha Data List` |
| `50 eA 6E` | SAMPLER Sample / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `50 eA 6F` | SAMPLER Sample / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
