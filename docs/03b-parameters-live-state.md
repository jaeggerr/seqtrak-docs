# Live app state (`01 xx xx`, `18 xx xx`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

86 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `01 00 00` | PCApp | FirmwareVersion | 4 | 0 - 268435455 (decimal) |  |  | `FirmwareVersion` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 02 00 00 02 on a unit running OS V2.00 |
| `01 00 04` | PCApp | CompatibleVersion | 1 | 0 - 127 (decimal) |  |  | `CompatibleVersion` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 01 |
| `01 10 00` | PCApp | SystemStatus | 1 | 0 - 1 (decimal) |  |  | `SystemStatus` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 (SystemStatus) |
| `01 10 01` | PCApp | ContentsManagementMode | 1 | 0 - 1 (decimal) |  |  | `ContentsManagementMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00; a write of 1 did not suspend Parameter Requests and a write of 0 did not restore them, so the silence seen on 2026-11-21/23 was the measuring instrument, not this mode |
| `01 10 02` | PCApp | Battery | 1 | 0 - 100 (decimal) |  |  | `Battery` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 46 = 70 and 64 = 100 (battery percentage) |
| `01 10 03` | PCApp | AutoPowerOffTime | 1 | 0 - 6 (decimal) |  |  | `AutoPowerOffTime` |  | from the official app, untested |
| `01 10 06` | PCApp | WiFiStartupResult | 1 | 0 - 7 (decimal) |  |  | `WiFiStartupResult` |  | from the official app, untested |
| `01 10 07` | PCApp | HeadphonePlugStatus | 1 | 0 - 1 (decimal) |  |  | `HeadphonePlugStatus` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00, headphones unplugged |
| `01 10 08` | PCApp | ResumeTrigger | 1 | 0 - 2 (decimal) |  |  | `ResumeTrigger` |  | from the official app, untested |
| `01 10 09` | PCApp | UserSoundEmptyContentCount | 2 | 0 - 2175 (decimal) |  |  | `UserSoundEmptyContentCount` |  | from the official app, untested |
| `01 10 0B` | PCApp | UserElementEmptyContentCount | 2 | 0 - 1151 (decimal) |  |  | `UserElementEmptyContentCount` |  | from the official app, untested |
| `01 10 0D` | PCApp | UserWaveformEmptyContentCount | 2 | 0 - 16383 (decimal) |  |  | `UserWaveformEmptyContentCount` |  | from the official app, untested |
| `01 10 0F` | PCApp | UserWaveformTotalContentCount | 2 | 0 - 16383 (decimal) |  |  | `UserWaveformTotalContentCount` |  | from the official app, untested |
| `01 10 11` | PCApp | SampleMemoryUsedSize | 2 | 0 - 16383 (decimal) |  |  | `SampleMemoryUsedSize` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 0B = 11 (sample memory used) |
| `01 10 13` | PCApp | SampleMemoryTotalSize | 2 | 0 - 16383 (decimal) |  |  | `SampleMemoryTotalSize` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 03 7E = 510 (sample memory total) |
| `01 10 15` | PCApp | CurrentProject | 1 | 0 - 7 (decimal) |  |  | `CurrentProject` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00; also the precondition that caught a false failure report |
| `01 10 16` | PCApp | CurrentProjectName | 87 |  |  |  | `CurrentProjectName` |  | from the official app, untested |
| `01 10 17` | PCApp | GeneralMode | 1 | 0 - 3 (decimal) |  |  | `GeneralMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — 00 outside Song mode and 02 inside, over three entries and three exits |
| `01 10 18` | PCApp | DrumPadMode | 1 | 0 - 20 (decimal) |  |  | `DrumPadMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — 00 outside Song mode and 13 inside — values measured, meaning inferred |
| `01 10 19` | PCApp | SynthPadMode | 1 | 0 - 2 (decimal) |  |  | `SynthPadMode` |  | from the official app, untested |
| `01 10 1A` | PCApp | MasterEffectSliderMode | 1 | 0 - 1 (decimal) |  |  | `MasterEffectSliderMode` |  | from the official app, untested |
| `01 10 1B` | PCApp | ReverbSliderMode | 1 | 0 - 1 (decimal) |  |  | `ReverbSliderMode` |  | from the official app, untested |
| `01 10 1C` | PCApp | VariationSliderMode | 1 | 0 - 1 (decimal) |  |  | `VariationSliderMode` |  | from the official app, untested |
| `01 10 1D` | PCApp | ClearEffect | 1 | 1 - 1 (decimal) |  |  | `ClearEffect` |  | from the official app, untested |
| `01 10 1E` | PCApp | EffectModeSelect | 1 | 0 - 1 (decimal) |  |  | `EffectModeSelect` |  | from the official app, untested |
| `01 10 1F` | PCApp | UndoRedo | 1 | 1 - 1 (decimal) |  |  | `UndoRedo` |  | from the official app, untested |
| `01 10 20` | PCApp | SequencerStatus | 1 | 0 - 1 (decimal) |  |  | `SequencerStatus` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — 01 playing and 00 stopped, alongside FA/FC, over eight transitions; and the machine starts and stops when the HOST sends FA/FC, broadcasting 01 10 20 unsolicited on each; the broadcasts were seen again over Bluetooth on 2026-10-23. Also on 2026-11-23: read 00 while the machine emitted MIDI clock continuously at about 48 F8 a second, so clock runs with the sequencer stopped |
| `01 10 21` | PCApp | RecordingStatus | 1 | 0 - 1 (decimal) |  |  | `RecordingStatus` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — writable while the sequencer plays: written 1 it reads back 1, written 0 it reads back 0, twice over; written 1 while stopped it still reads 0; the write is not echoed. Whether notes are then recorded was not tested |
| `01 10 22` | PCApp | SamplingStatus | 1 | 0 - 2 (decimal) |  |  | `SamplingStatus` |  | from the official app, untested |
| `01 10 23` | PCApp | MonitoringStatus | 1 | 0 - 1 (decimal) |  |  | `MonitoringStatus` |  | from the official app, untested |
| `01 10 24` | PCApp | CategoryJumpFavoriteFiltering | 1 | 0 - 1 (decimal) |  |  | `CategoryJumpFavoriteFiltering` |  | from the official app, untested |
| `01 10 27` | PCApp | CurrentPart | 1 | 0 - 10 (decimal) |  |  | `CurrentPart` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00; broadcast on every track change |
| `01 10 28` | PCApp | SamplerCurrentElement | 1 | 0 - 6 (decimal) |  |  | `SamplerCurrentElement` |  | from the official app, untested |
| `01 10 29` | PCApp | NotifyResetPlayCurrentStepCount | 1 | 0 - 0 (decimal) |  |  | `NotifyResetPlayCurrentStepCount` |  | from the official app, untested |
| `01 10 2A` | PCApp | NotifyAllPatternChange | 1 | 0 - 6 (decimal) |  |  | `NotifyAllPatternChange` |  | from the official app, untested |
| `01 10 2B` | PCApp | NotifyBarLengthChange | 1 | 0 - 1 (decimal) |  |  | `NotifyBarLengthChange` |  | from the official app, untested |
| `01 10 2C` | PCApp | NotifySynthPadNoteOn | 1 | 0 - 6 (decimal) |  |  | `NotifySynthPadNoteOn` |  | from the official app, untested |
| `01 10 2D` | PCApp | MasterKnobMode | 2 | 0 - 16262 (decimal) |  |  | `MasterKnobMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00; replies with one data byte but broadcasts two |
| `01 10 2E` | PCApp | ParameterLedMode | 1 | 0 - 43 (decimal) |  |  | `ParameterLedMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 01; broadcast with sound changes, knob moves and FX-block changes |
| `01 10 2F` | PCApp | DeviceID | 1 | 0 - 1 (decimal) |  |  | `DeviceID` |  | from the official app, untested |
| `01 10 70` | PCApp | NotifyChangeProjectWithResume | 1 | 0 - 1 (decimal) |  |  | `NotifyChangeProjectWithResume` |  | from the official app, untested |
| `01 1p 30` | PCApp | SoundDesignPage | 1 | 0 - 5 (decimal) |  |  | `SoundDesignPage` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 on part 0 (SoundDesignPage) |
| `01 1p 31` | PCApp | InsertionEffectSliderMode | 1 | 0 - 1 (decimal) |  |  | `InsertionEffectSliderMode` |  | from the official app, untested |
| `01 1p 32` | PCApp | ReserveChangePattern | 1 | 0 - 6 (decimal) |  |  | `ReserveChangePattern` |  | from the official app, untested |
| `01 1p 33` | PCApp | CurrentSound | 2 | 0 - 6143 (decimal) |  |  | `CurrentSound` |  | `verified on hardware` ([06-sounds-presets.md](06-sounds-presets.md)) — catalogue number minus one — ten presets loaded by Bank/PC and read back; re-read on parts 0-9 on 2026-10-23 and resolved to the right preset each time, but silent on part 10 (SAMPLER) in eight attempts across two clients. Also on 2026-11-23: part 8 read 20 04 = 4100, 4/4 attempts, equal to the <ContentNumber> of that sound's exported .Y3S -- but a content dump request for sound 4100 finds nothing, so the two numbers being equal is not evidence that they are the same namespace |
| `01 1p 35` | PCApp | CurrentSoundName | 87 |  |  |  | `CurrentSoundName` |  | from the official app, untested |
| `01 1p 36` | PCApp | DrumPatternPage | 1 | 0 - 7 (decimal) |  |  | `DrumPatternPage` |  | from the official app, untested |
| `01 1p 37` | PCApp | DeletePattern | 1 | 0 - 5 (decimal) |  |  | `DeletePattern` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — cleared a pattern of five events on a re-typed part in one message; broadened 2026-10-23 to 66 messages (6 slots x 11 parts) with no PatternSelect write, each part's selected pattern then read back empty, native synth parts 7-10 included |
| `01 1p 38` | PCApp | WritingMotionRecord | 1 | 0 - 1 (decimal) |  |  | `WritingMotionRecord` |  | from the official app, untested |
| `01 1p 39` | PCApp | PatternKnobMode | 2 | 0 - 903 (decimal) |  |  | `PatternKnobMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 on part 0; observed broadcasting two data bytes |
| `01 1p 3C` | PCApp | PartAwmType | 1 | 0 - 5 (decimal) |  |  | `PartAwmType` |  | `verified on hardware` ([13-track-types.md](13-track-types.md)) — answered on all eleven parts, 44 replies out of 44; 1/2/4/5 observed |
| `01 1p 3D` | PCApp | DrumKitCurrentElement | 1 | 0 - 6 (decimal) |  |  | `DrumKitCurrentElement` |  | from the official app, untested |
| `01 1p 40` | PCApp | SamplingPadSampleSize | 4 | 0 - 16777215 (decimal) |  | 0 - 16777215 | `SamplingPadSampleSize` |  | from the official app, untested |
| `01 1p 44` | PCApp | CurrentElement | 2 | 0 - 1535 (decimal) |  |  | `CurrentElement` |  | from the official app, untested |
| `01 1p 46` | PCApp | CurrentElementName | 87 |  |  |  | `CurrentElementName` |  | from the official app, untested |
| `01 1p 47` | PCApp | CurrentElementSubCategory | 1 | 0 - 15 (decimal) |  | 0 - 15 | `CurrentElementSubCategory` |  | from the official app, untested |
| `01 1p 48` | PCApp | DeletePatternElement | 1 | 0 - 6 (decimal) |  |  | `DeletePatternElement` |  | from the official app, untested |
| `01 1p 50` | PCApp | MasterSlider1Assign | 1 | 0 - 24 (decimal) |  |  | `MasterSlider1Assign` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 09 on part 0 (MasterSlider1Assign) |
| `01 1p 51` | PCApp | MasterSlider2Assign | 1 | 0 - 24 (decimal) |  |  | `MasterSlider2Assign` |  | from the official app, untested |
| `01 1p 52` | PCApp | MasterSlider3Assign | 1 | 0 - 24 (decimal) |  |  | `MasterSlider3Assign` |  | from the official app, untested |
| `01 1p 53` | PCApp | SingleSlider1Assign | 1 | 0 - 24 (decimal) |  |  | `SingleSlider1Assign` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 09 on part 0 (SingleSlider1Assign) |
| `01 1p 54` | PCApp | SingleSlider2Assign | 1 | 0 - 24 (decimal) |  |  | `SingleSlider2Assign` |  | from the official app, untested |
| `01 1p 55` | PCApp | SingleSlider3Assign | 1 | 0 - 24 (decimal) |  |  | `SingleSlider3Assign` |  | from the official app, untested |
| `01 1p 56` | PCApp | SendSlider1Assign | 1 | 0 - 24 (decimal) |  |  | `SendSlider1Assign` |  | from the official app, untested |
| `01 1p 57` | PCApp | SendSlider2Assign | 1 | 0 - 24 (decimal) |  |  | `SendSlider2Assign` |  | from the official app, untested |
| `01 1p 58` | PCApp | SendSlider3Assign | 1 | 0 - 24 (decimal) |  |  | `SendSlider3Assign` |  | from the official app, untested |
| `01 1p 59` | PCApp | MasterSlider1ControlValue | 1 | 0 - 127 (decimal) |  |  | `MasterSlider1ControlValue` |  | from the official app, untested |
| `01 1p 5A` | PCApp | MasterSlider2ControlValue | 1 | 0 - 127 (decimal) |  |  | `MasterSlider2ControlValue` |  | from the official app, untested |
| `01 1p 5B` | PCApp | MasterSlider3ControlValue | 1 | 0 - 127 (decimal) |  |  | `MasterSlider3ControlValue` |  | from the official app, untested |
| `01 1p 5C` | PCApp | SingleSlider1ControlValue | 1 | 0 - 127 (decimal) |  |  | `SingleSlider1ControlValue` |  | `verified on hardware` ([05-live-state.md](05-live-state.md)) — readable on request, but not broadcast when the slider moves |
| `01 1p 5D` | PCApp | SingleSlider2ControlValue | 1 | 0 - 127 (decimal) |  |  | `SingleSlider2ControlValue` |  | from the official app, untested |
| `01 1p 5E` | PCApp | SingleSlider3ControlValue | 1 | 0 - 127 (decimal) |  |  | `SingleSlider3ControlValue` |  | from the official app, untested |
| `01 1p 5F` | PCApp | SendSlider1ControlValue | 1 | 0 - 127 (decimal) |  |  | `SendSlider1ControlValue` |  | from the official app, untested |
| `01 1p 60` | PCApp | SendSlider2ControlValue | 1 | 0 - 127 (decimal) |  |  | `SendSlider2ControlValue` |  | from the official app, untested |
| `01 1p 61` | PCApp | SendSlider3ControlValue | 1 | 0 - 127 (decimal) |  |  | `SendSlider3ControlValue` |  | from the official app, untested |
| `01 1p 71` | PCApp | *(name unresolved)* | 1 | 0 - 1 (decimal) |  |  | `<key=None>` |  | from the official app, untested |
| `01 31 00` | PCApp | DefragmentationWaveform | 1 | 1 - 1 (decimal) |  |  | `DefragmentationWaveform` |  | from the official app, untested |
| `01 31 01` | PCApp | DefragmentationSampleMemory | 1 | 1 - 1 (decimal) |  |  | `DefragmentationSampleMemory` |  | from the official app, untested |
| `01 31 02` | PCApp | DefragmentationResult | 1 | 0 - 127 (decimal) |  |  | `DefragmentationResult` |  | from the official app, untested |
| `01 34 00` | PCApp | FactoryReset | 1 | 0 - 1 (decimal) |  |  | `FactoryReset` |  | from the official app, untested |
| `01 34 01` | PCApp | FactoryResetResult | 1 | 0 - 127 (decimal) |  |  | `FactoryResetResult` |  | from the official app, untested |
| `18 00 00` | PCAppDrumKitStatus | CurrentDrumKitElement | 2 | 0 - 6143 (decimal) |  |  | `CurrentDrumKitElement` |  | from the official app, untested |
| `18 00 02` | PCAppDrumKitStatus | CurrentDrumKitElementName | 87 |  |  |  | `CurrentDrumKitElementName` |  | from the official app, untested |
| `18 00 03` | PCAppDrumKitStatus | CurrentDrumKitElementSubCategory | 1 | 0 - 15 (decimal) |  |  | `CurrentDrumKitElementSubCategory` |  | from the official app, untested |
| `18 00 04` | PCAppDrumKitStatus | DeletePatternDrumKitElement | 1 | 0 - 5 (decimal) |  |  | `DeletePatternDrumKitElement` |  | from the official app, untested |
| `18 00 05` | PCAppDrumKitStatus | DrumKitElementMute | 1 | 0 - 1 (decimal) |  |  | `DrumKitElementMute` |  | from the official app, untested |
