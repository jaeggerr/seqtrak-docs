# Sequencer and song (`11`, `12`, `70`, `71`)

One row per address. `p` is a part number, `e` an element number, `o` an FM operator number, `n` a master-effect number and `nn`/`mm` a bulk selector; see [02-sysex-format.md](02-sysex-format.md) for how those nibbles are filled in.

The **Source** column is the confidence marker. `from Yamaha Data List` means the row is in Yamaha's published table. `from the official app, untested` means it was recovered from the official app and has no Yamaha documentation. `verified on hardware` means the behaviour was established on a real unit, and the cell says what was established and where it is written up — that comes from [`../data/hardware-verified.csv`](../data/hardware-verified.csv), the one input to this table that is not an extraction. A marker there is an assertion about **that** address, never about its block or its neighbours.

Machine-readable: [`../data/parameters.csv`](../data/parameters.csv).

69 addresses.

| Address | Block | Parameter | Size | Value range (hex) | Default (hex) | Display / meaning | App name | Notes | Source |
|---|---|---|---|---|---|---|---|---|---|
| `11 00 nn` | Bulk Control / Header | Bulk Header | 1 | - | - | Project Edit Buffer (nn = 0) | `` |  | from Yamaha Data List |
| `11 01 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Project User 1 (nn = 0-7) | `` |  | from Yamaha Data List |
| `11 02 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound Edit Buffer Part nn (nn = 0-10) | `` |  | from Yamaha Data List |
| `11 03 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 1 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 04 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 2 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 05 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 3 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 06 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 4 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 07 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 5 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 08 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 6 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 09 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 7 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 0A nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 8 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 0B nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 9 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 0C nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 10 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 0D nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 11 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 0E nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 12 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 0F nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 13 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 10 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 14 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 11 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 15 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 12 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sound User 16 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 13 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element Edit Buffer Element nn (nn = 0-6) | `` |  | from Yamaha Data List |
| `11 14 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 1 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 15 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 2 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 16 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 3 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 17 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 4 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 18 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 5 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 19 nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 6 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 1A nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 7 (nn = 0-127) | `` |  | from Yamaha Data List |
| `11 1B nn` | Parameter Change Table / Bulk Control | Bulk Header | 1 | - | - | Sampler Element User 8 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 00 nn` | Bulk Control / Footer | Bulk Footer | 1 | - | - | Project Edit Buffer (nn = 0) | `` |  | from Yamaha Data List |
| `12 01 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Project User 1 (nn = 0-7) | `` |  | from Yamaha Data List |
| `12 02 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound Edit Buffer Part nn (nn = 0-10) | `` |  | from Yamaha Data List |
| `12 03 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 1 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 04 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 2 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 05 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 3 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 06 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 4 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 07 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 5 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 08 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 6 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 09 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 7 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 0A nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 8 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 0B nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 9 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 0C nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 10 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 0D nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 11 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 0E nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 12 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 0F nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 13 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 10 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 14 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 11 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 15 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 12 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sound User 16 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 13 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element Edit Buffer Element nn (nn = 0-6) | `` |  | from Yamaha Data List |
| `12 14 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 1 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 15 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 2 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 16 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 3 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 17 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 4 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 18 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 5 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 19 nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 6 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 1A nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 7 (nn = 0-127) | `` |  | from Yamaha Data List |
| `12 1B nn` | Parameter Change Table / Bulk Control | Bulk Footer | 1 | - | - | Sampler Element User 8 (nn = 0-127) | `` |  | from Yamaha Data List |
| `70 00 00` | StepRec | *(name unresolved)* | 1 | 0 - 4 (decimal) |  |  | `<key=0>` |  | from the official app, untested |
| `71 00 00` | Song | AddScene | 1 | 0 - 15 (decimal) |  |  | `AddScene` |  | `verified on hardware` ([14-song-mode.md](14-song-mode.md)) — created scene 3 on a project that had three; the number travels in the data |
| `71 10 00` | Song | ChangeLength | 3 | 0 - 245903 (decimal) |  |  | `ChangeLength` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — ChangeLength accepted as <scene> <msb> <lsb> on a scene created for the test; byte 1 of the Scene Info reply tracked both values written (64 then 100) and no other byte moved |
| `71 10 03` | Song | ChangeSoloTrack | 2 | 0 - 1931 (decimal) |  |  | `ChangeSoloTrack` |  | from the official app, untested |
| `71 10 04` | Song | CurrentScene | 1 | 0 - 15 (decimal) |  |  | `CurrentScene` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the Song-mode sweep (CurrentScene) |
| `71 10 05` | Song | ReserveChangeCurrentScene | 1 | 0 - 15 (decimal) |  |  | `ReserveChangeCurrentScene` |  | from the official app, untested |
| `71 10 06` | Song | ChangePlayMode | 1 | 0 - 2 (decimal) |  |  | `ChangePlayMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the Song-mode sweep |
| `71 10 07` | Song | ChangeSceneLoop | 1 | 0 - 1 (decimal) |  |  | `ChangeSceneLoop` |  | from the official app, untested |
| `71 1p 01` | Song | ChangePattern | 2 | 0 - 1925 (decimal) |  |  | `ChangePattern` |  | `verified on hardware` ([14-song-mode.md](14-song-mode.md)) — behaves as described with the scene byte in the data |
| `71 1p 02` | Song | ChangeMute | 2 | 0 - 1921 (decimal) |  |  | `ChangeMute` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — ChangeMute accepted as <scene> <mute>: writing 00 00 on part 7 cleared byte 14+part of the SceneInfo reply for scene 0 from 1 to 0, and the ten other mute bytes did not move |
| `71 1p 09` | Song | ChangeSamplerElementMute | 2 | 0 - 1921 (decimal) |  |  | `ChangeSamplerElementMute` |  | from the official app, untested |
| `71 20 00` | Song | RemoveScene | 1 | 0 - 15 (decimal) |  |  | `RemoveScene` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — removed scene 3 again, restoring the initial state; broadened 2026-10-23 to ten consecutive removals, all 16 indices re-read afterwards and only scene 0 answering |
| `71 50 00` | Song | ChangeSceneMode | 1 | 0 - 1 (decimal) |  |  | `ChangeSceneMode` |  | `verified on hardware` ([10-verified-behaviour.md](10-verified-behaviour.md)) — read as part of the Song-mode sweep |
