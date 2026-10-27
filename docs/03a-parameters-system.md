# System and Wi-Fi (`00 xx xx`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

60 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `00 00 00` | System / General | Speaker Master Volume | 1 | 00 - 7F | 64 | 0 - 127 | `SpeakerMasterVolume` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 3D = 61 (Speaker Master Volume) — also `from Yamaha Data List` |
| `00 00 01` | System / General | Headphone Master Volume | 1 | 00 - 7F | 20 | 0 - 127 | `HeadphoneMasterVolume` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 29 = 41 (Headphone Master Volume) — also `from Yamaha Data List` |
| `00 00 02` | System / General | Master Tune | 4 | 00 - 00 00 - 07 00 - 0F 00 - 0F | 00 04 00 00 | -102.4 - +102.3 1st bit3-0 → bit15-12, 2nd bit3-0 → bit11-8 3rd bit3-0 → bit7-4, 4th bit3-0 → bit3-0 | `` | MIDI Master Tuning | from Yamaha Data List |
| `00 00 06` | System / General | Local Switch | 1 | 00 - 01 | 01 | Off, On | `LocalSwitch` |  | from Yamaha Data List |
| `00 00 07` | System / General | Receive/Transmit Bank Select | 1 | 00 - 01 | 01 | Off, On | `ReceiveTransmitBankSelect` |  | from Yamaha Data List |
| `00 00 08` | System / General | Receive/Transmit Program Change | 1 | 00 - 01 | 01 | Off, On | `ReceiveTransmitProgramChange` |  | from Yamaha Data List |
| `00 00 09` | System / General | Legacy MIDI In/Out | 1 | 00 - 01 | 01 | Off, On | `MidiInOut` |  | from Yamaha Data List |
| `00 00 0A` | System / General | Legacy MIDI Transmit Channel Message | 1 | 00 - 01 | 01 | Off, On | `LegacyMidiTransmitChannelMessage` |  | from Yamaha Data List |
| `00 00 0B` | System / General | Legacy MIDI Transmit Control Change Transmit Bank Select Transmit Program Change | 1 | 00 - 70 | 00 | bit 6:CC Off, On bit 5:BS Off, On bit 4:PC Off, On bit 3-0:reserved | `LegacyMidiTransmitCcBsPc` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 70 — all three TX bits set on the TRS interface — also `from Yamaha Data List` |
| `00 00 0C` | System / General | Legacy MIDI Transmit System Exclusive Message | 1 | 00 - 01 | 00 | Off, On | `LegacyMidiTransmitSystemExclusiveMessage` |  | from Yamaha Data List |
| `00 00 0D` | System / General | USB MIDI In/Out | 1 | 00 - 01 | 01 | Off, On | `` |  | from Yamaha Data List |
| `00 00 0E` | System / General | USB MIDI Transmit Channel Message | 1 | 00 - 01 | 01 | Off, On | `UsbMidiTransmitChannelMessage` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the USB interface settings sweep — also `from Yamaha Data List` |
| `00 00 0F` | System / General | USB MIDI Transmit Control Change Transmit Bank Select Transmit Program Change | 1 | 00 - 70 | 00 | bit 6:CC Off, On bit 5:BS Off, On bit 4:PC Off, On bit 3-0:reserved | `UsbMidiTransmitCcBsPc` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 70 — all three TX bits set on the USB interface — also `from Yamaha Data List` |
| `00 00 10` | System / General | USB MIDI Transmit System Exclusive Message | 1 | 00 - 01 | 00 | Off, On | `UsbMidiTransmitSystemExclusiveMessage` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 01 = On, against a documented default of Off — also `from Yamaha Data List` |
| `00 00 11` | System / General | Bluetooth MIDI In/Out | 1 | 00 - 01 | 00 | Off, On | `BluetoothMidiInOut` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 on a unit that had just carried a full Bluetooth MIDI session; the value does not report whether BLE MIDI works — also `from Yamaha Data List` |
| `00 00 12` | System / General | Bluetooth MIDI Transmit Channel Message | 1 | 00 - 01 | 01 | Off, On | `BluetoothMidiTransmitChannelMessage` |  | from Yamaha Data List |
| `00 00 13` | System / General | Bluetooth MIDI Transmit Control Change Transmit Bank Select Transmit Program Change | 1 | 00 - 70 | 00 | bit 6:CC Off, On bit 5:BS Off, On bit 4: PC Off, On bit 3-0:reserved | `BluetoothMidiTransmitCcBsPc` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 70 — all three TX bits set on the Bluetooth interface — also `from Yamaha Data List` |
| `00 00 14` | System / General | Bluetooth MIDI Transmit System Exclusive Message | 1 | 00 - 01 | 00 | Off, On | `BluetoothMidiTransmitSystemExclusiveMessage` |  | from Yamaha Data List |
| `00 00 15` | System / General | USB Audio Output Gain | 1 | 00 - 03 | 00 | 00:-6dB, 01:+0dB, 02:+6dB, 03:+12dB | `UsbAudioOutputGain` |  | from Yamaha Data List |
| `00 00 16` | System / General | Wireless LAN | 1 | 00 - 01 | 00 | Off, On | `WirelessLAN` |  | `verified on hardware` ([07-transports.md](07-transports.md)) — read 0 on a unit with Wi-Fi off — also `from Yamaha Data List` |
| `00 00 17` | System / General | USB Role | 1 | 00 - 01 | 00 | To Host, To Device | `` |  | from Yamaha Data List |
| `00 00 18` | System / General | Analog Audio Output Gain | 1 | 00 - 03 | 01 | 00:-6dB, 01:+0dB, 02:+6dB, 03:+12dB | `AnalogAudioOutputGain` |  | from Yamaha Data List |
| `00 00 19` | System / General | Sampling Source | 1 | 00 - 02 | 01 | Resampling, Mic/Line In, USB Audio In | `SamplingSource` |  | from Yamaha Data List |
| `00 00 1A` | System / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `00 00 1B` | System / General | Sampling Count In | 1 | 00 - 01 | 01 | Off, On | `SamplingCountIn` |  | from Yamaha Data List |
| `00 00 1C` | System / General | Auto Normalize | 1 | 00 - 01 | 01 | Off, On | `AutoNormalize` |  | from Yamaha Data List |
| `00 00 1D` | System / General | Project Resume Switch | 1 | 00 - 01 | 01 | Off, On | `ResumeSwitch` |  | from Yamaha Data List |
| `00 00 1E` | System / General | Project Resume Auto Trigger | 1 | 00 - 01 | 00 | Off, On | `ResumeAutoTrigger` |  | from Yamaha Data List |
| `00 00 1F` | System / General | Record Quantize Value | 1 | 00 - 05 | 03 | Off, 60, 80, 120, 160, 240 | `RecordQuantizeValue` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 (Off) against a documented default of 03 — also `from Yamaha Data List` |
| `00 00 20` | System / General | Pad Velocity | 1 | 01 - 7F | 64 | 1 - 127 | `PadVelocity` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 64 (pad velocity 100) — also `from Yamaha Data List` |
| `00 00 21` | System / General | Sound Design Mode | 1 | 00 - 01 | 00 | Normal, Advanced | `SoundDesignMode` |  | from Yamaha Data List |
| `00 00 22` | System / General | Legacy MIDI Thru | 1 | 00 - 03 | 00 | Off, Channel, Realtime, Both | `LegacyMidiThru` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 03 (Both) against a documented default of 00 — also `from Yamaha Data List` |
| `00 00 23` | System / General | USB To Host MIDI Thru | 1 | 00 - 03 | 03 | Off, Channel, Realtime, Both | `UsbMidiThru` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the MIDI-thru settings sweep — also `from Yamaha Data List` |
| `00 00 24` | System / General | Bluetooth MIDI Thru | 1 | 00 - 03 | 03 | Off, Channel, Realtime, Both | `BluetoothMidiThru` |  | from Yamaha Data List |
| `00 00 25` | System / General | Click Switch | 1 | 00 - 01 | 00 | Off, On | `ClickSwitch` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read 00 (metronome off) — also `from Yamaha Data List` |
| `00 00 26` | System / General | Click Type | 1 | 00 - 09 | 00 | 1 - 10 | `ClickType` |  | from Yamaha Data List |
| `00 00 27` | System / General | Click Volume | 1 | 00 - 7F | 40 | 0 -127 | `ClickVolume` |  | from Yamaha Data List |
| `00 00 28` | System / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `00 00 29` | System / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `00 00 2A` | System / General | Midi Sync | 1 | 00 - 01 | 01 | Internal, MIDI(Auto) | `MidiSync` |  | from Yamaha Data List |
| `00 00 2B` | System / General | Transmit Sequencer Control | 1 | 00 - 01 | 01 | Off, On | `ReceiveSequencerControl` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the sequencer-control settings sweep — also `from Yamaha Data List` |
| `00 00 2C` | System / General | reserved | 1 |  | 00 |  | `` |  | from Yamaha Data List |
| `00 00 2D` | System / General | Midi Clock Out | 1 | 00 - 01 | 01 | Off, On | `MidiClockOut` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read Off in 2026-08 and On in 2026-10 after the user enabled it — also `from Yamaha Data List` |
| `00 00 2E` | System / General | Sink Current Setting | 1 | 00 - 02 | 00 | Auto, Fixed 0A, Forbidden 500mA | `` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the sink-current settings sweep — also `from Yamaha Data List` |
| `00 00 2F` | System / General | Pattern Select Sensitivity | 1 | 01 - 03 | 01 | 1, 2, 3 | `PatternSelectSensitivity` |  | from Yamaha Data List |
| `00 60 00` | System | WiFiMode | 1 | 0 - 1 (decimal) |  |  | `WiFiMode` |  | `verified on hardware` ([07-transports.md](07-transports.md)) — read 0 on a unit with Wi-Fi off |
| `00 60 01` | System | WiFiReady | 1 | 0 - 1 (decimal) |  |  | `WiFiReady` |  | `verified on hardware` ([07-transports.md](07-transports.md)) — read 0 on a unit with Wi-Fi off |
| `00 60 02` | System | WiFiAudio | 1 | 0 - 1 (decimal) |  |  | `WiFiAudio` |  | from the official app, untested |
| `00 60 06` | System | CountryCode | 2 |  |  |  | `CountryCode` |  | from the official app, untested |
| `00 60 08` | System | PortNumber | 8 |  |  |  | `PortNumber` |  | from the official app, untested |
| `00 61 00` | System | SecurityProtocolSTA | 1 | 0 - 7 (decimal) |  |  | `SecurityProtocolSTA` |  | from the official app, untested |
| `00 61 01` | System | DHCPClientSwitch | 1 | 0 - 1 (decimal) |  |  | `DHCPClientSwitch` |  | from the official app, untested |
| `00 61 02` | System | Connection | 1 | 0 - 1 (decimal) |  |  | `Connection` |  | from the official app, untested |
| `00 61 10` | System | SSID_STA | 32 |  |  |  | `SSID_STA` |  | from the official app, untested |
| `00 61 30` | System | SecurityKeySTA | 64 |  |  |  | `SecurityKeySTA` |  | from the official app, untested |
| `00 61 70` | System | IPAddressSTA | 16 |  |  |  | `IPAddressSTA` |  | from the official app, untested |
| `00 62 00` | System | SecurityProtocolAP | 1 | 0 - 7 (decimal) |  |  | `SecurityProtocolAP` |  | from the official app, untested |
| `00 62 10` | System | SSID_AP | 32 |  |  |  | `SSID_AP` |  | from the official app, untested |
| `00 62 30` | System | SecurityKeyAP | 64 |  |  |  | `SecurityKeyAP` |  | from the official app, untested |
| `00 62 70` | System | IPAddressAP | 16 |  |  |  | `IPAddressAP` |  | from the official app, untested |
