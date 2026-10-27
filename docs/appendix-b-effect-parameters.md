# Appendix B — Effect parameter list

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/effect_params.py`.
> Confidence: `from Yamaha Data List`.


Each effect type exposes up to 16 parameters. Parameter *k* is written at offset `al = 0x01 | (k << 1)` inside its effect block — two bytes, MSB first — so parameter 1 is at `03`, parameter 2 at `05`, and so on. That formula came out of the official app and has been confirmed twice against live traffic (`verified on hardware`, see [10-verified-behaviour.md](10-verified-behaviour.md)).

**Value range** is what goes on the wire; **display range** is what the hardware and app show. **Data assign table** names the conversion table between them, in [`../data/effect-data-assign-tables.csv`](../data/effect-data-assign-tables.csv). **Default slider** is which of the three hardware sliders picks that parameter up by default.

1445 rows. Machine-readable: [`../data/effect-parameters.csv`](../data/effect-parameters.csv).


## SPX HALL, SPX ROOM, SPX STAGE — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 30.0s | (0 - 69) | 4 | 2 |
| 2 | `05` | Diffusion | 0 - 10 | (0 - 10) |  |  |
| 3 | `07` | Initial Delay | 0.1ms - 99.3ms | (0 - 63) | 5 |  |
| 4 | `09` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 5 | `0B` | LPF Cutoff Frequency | 1.0kHz -20.0kHz | (34 - 60) | 3 | 3 |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Reverb Delay | 0.1ms - 99.3ms | (0 - 63) | 5 |  |
| 12 | `19` | Density | 0 - 4 | (0 - 4) |  |  |
| 13 | `1B` | ER/Rev Balance | E63>R - E=R - E<R63 | (1 - 127) |  |  |
| 14 | `1D` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 15 | `1F` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 16 | `21` | --- |  |  |  |  |

## EARLY REFLECTION — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Type | S-hall, L-hall, Random, Reverse, Plate, Spring | (0 - 5) |  |  |
| 2 | `05` | Room Size | 0.1 - 20.0 | (0 - 127) | 6 | 2 |
| 3 | `07` | Diffusion | 0 - 10 | (0 - 10) |  |  |
| 4 | `09` | Initial Delay | 0.1ms - 200ms | (0 - 127) | 5 |  |
| 5 | `0B` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 6 | `0D` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 7 | `0F` | LPF Cutoff Frequency | 1.0kHz-20.0kHz | (34 - 60) | 3 | 3 |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Liveness | 0 - 10 | (0 - 10) |  |  |
| 12 | `19` | Density | 0 - 3 | (0 - 3) |  |  |
| 13 | `1B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## GATED REVERB, REVERSE REVERB — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Type | TypeA, TypeB | (0 - 1) |  |  |
| 2 | `05` | Room Size | 0.1 - 20.0 | (0 - 127) | 6 | 2 |
| 3 | `07` | Diffusion | 0 - 10 | (0 - 10) |  |  |
| 4 | `09` | Initial Delay | 0.1ms - 200ms | (0 - 127) | 5 |  |
| 5 | `0B` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 6 | `0D` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 7 | `0F` | LPF Cutoff Frequency | 1.0kHz -20.0kHz | (34 - 60) | 3 | 3 |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Liveness | 0 - 10 | (0 - 10) |  |  |
| 12 | `19` | Density | 0 - 3 | (0 - 3) |  |  |
| 13 | `1B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## CROSS DELAY — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L>R | 0.1ms-1638.3ms | (1 - 16383) |  | 2 |
| 2 | `05` | Delay Time R>L | 0.1ms-1638.3ms | (1 – 16383) |  | 2 |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 4 | `09` | Input Select | L, R, L&R, L-MODE2, R-MODE2 | (0 - 4) |  |  |
| 5 | `0B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | EQ Low Frequency | 32Hz - 2.0kHz | (4 - 40) | 3 |  |
| 14 | `1D` | EQ Low Gain | -12dB - +12dB | (52 - 76) |  |  |
| 15 | `1F` | EQ High Frequency | 500Hz - 16.0kHz | (28 - 58) | 3 |  |
| 16 | `21` | EQ High Gain | -12dB - +12dB | (52 - 76) |  |  |

## TEMPO CROSS DELAY — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L>R | 32nd/3 - 4thx6 | (0 - 19) | 13 | 2 |
| 2 | `05` | Delay Time R>L | 32nd/3 - 4thx6 | (0 - 19) | 13 | 2 |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 4 | `09` | Input Select | L, R, L&R, L-MODE2, R-MODE2 | (0 - 4) |  |  |
| 5 | `0B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 6 | `0D` | Lag | -63ms - +63ms | (1 - 127) |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## TEMPO DELAY MONO — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 32nd/3 - 4thx6 | (0 - 19) | 13 | 2 |
| 2 | `05` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 3 | `07` | Feedback High Damp | 0.1 – 1.0 | (1 - 10) |  |  |
| 4 | `09` | L/R Diffusion | -63ms - +63ms | (1 - 127) |  |  |
| 5 | `0B` | Lag | -63ms - +63ms | (1 - 127) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## TEMPO DELAY STEREO — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 32nd/3 - 4thx6 | (0 - 19) | 13 | 2 |
| 2 | `05` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 3 | `07` | Feedback High Damp | 0.1 – 1.0 | (1 - 10) |  |  |
| 4 | `09` | L/R Diffusion | -63ms - +63ms | (1 - 127) |  |  |
| 5 | `0B` | Lag | -63ms - +63ms | (1 - 127) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## CONTROL DELAY — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 0.1ms-1486.0ms | (1 - 14860) |  | 2 |
| 2 | `05` | Delay Transition Rate | 1 - 48 | (1 - 48) |  |  |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 4 | `09` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## DELAY LR — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L | 0.1ms-1638.3ms | (1 - 16383) | Table No. | Assign No. 2 |
| 2 | `05` | Delay Time R | 0.1ms-1638.3ms | (1 - 16383) |  | 2 |
| 3 | `07` | Feedback Time L | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 4 | `09` | Feedback Time R | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 5 | `0B` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 6 | `0D` | Feedback High Damp | 0.1 – 1.0 | (1 - 10) |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## DELAY LCR — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L | 0.1ms-1638.3ms | (1 - 16383) |  | 2 |
| 2 | `05` | Delay Time R | 0.1ms-1638.3ms | (1 - 16383) |  | 2 |
| 3 | `07` | Delay Time C | 0.1ms-1638.3ms | (1 - 16383) |  | 2 |
| 4 | `09` | Feedback Time | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 5 | `0B` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 6 | `0D` | Delay Level C | 0 – 127 | (0 - 127) |  |  |
| 7 | `0F` | Feedback High Damp | 0.1 – 1.0 | (1 - 10) |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## ANALOG DELAY RETRO — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 25ms - 800ms | (0 - 127) | 41 | 2 |
| 2 | `05` | Feedback Level | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | Delay Input Level | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Type | Mellow, Dub, Narrow, Soft, Dark | (0 - 4) | 43 |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## ANALOG DELAY MODERN — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 50ms - 1.0s | (0 - 127) | 42 | 2 |
| 2 | `05` | Feedback Level | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | Delay Input Level | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Type | Urban, Dub, Narrow, Soft, Dark | (0 - 4) | 44 |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## CONTROL FILTER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Filter Type | LPF(12dB), LPF(18dB), LPF(24dB), HPF, BPF | (0 - 4) |  |  |
| 2 | `05` | Cutoff Frequency Control | 0 - 127 | (0 - 127) |  | 1 |
| 3 | `07` | Resonance | 0 - 127 | (0 - 127) |  | 2 |
| 4 | `09` | Filter Output Level | -12dB-+12dB | (52 - 76) |  | 3 |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM MINI FILTER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Cutoff Frequency | 0.00 - 100.00 | (0 - 10000) |  | 1 |
| 2 | `05` | Resonance | 0.0 - 1.0 | (0 - 500) |  | 2 |
| 3 | `07` | --- |  |  |  |  |
| 4 | `09` | Type | LPH, HPF | (0 - 1) |  |  |
| 5 | `0B` | Texture | Retro, Standard, Modern | (0 - 2) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | Input Level | -36 - +24dB | (0 - 120) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Output Level | -40 - +20dB | (0 - 120) |  | 3 |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## LP-HP FILTER — Single / Master Effect Block

> (*) Internally limited depending on Resonance.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LPF/HPF Cutoff Frequency (*) | -256--1 (LPF24A), 0 (Thru), +1-+256 (HPF24A) | (0-256-512) |  | 1 |
| 2 | `05` | Resonance | -6-0-41.625[dB] (0.375[dB]step) | (0-16-127) |  | 2 |
| 3 | `07` | --- |  |  |  |  |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM COMPRESSOR 376 — Single / Master Effect Block

> (*) for Ducker.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Input Level | -∞ - 0.00dB | (0 - 200) | 25 | 2 |
| 2 | `05` | Output Level | -∞ - 0.00dB | (0 - 200) | 25 | 3 |
| 3 | `07` | Ratio | 2, 4, 8, 12, 20 | (0 - 4) |  | 1 |
| 4 | `09` | Attack | 0.022ms-50.40ms | (0 - 200) | 26 | 2 (*) |
| 5 | `0B` | Release | 10.88ms-544.22ms | (0 - 200) | 27 | 3 (*) |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 | 1 (*) |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## CLASSIC COMPRESSOR — Single / Master Effect Block

> (*) for Ducker.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Attack | 1ms - 40ms | (0 - 19) | 8 | 2 (*) |
| 2 | `05` | Release | 10ms - 680ms | (0 - 15) | 9 | 3 (*) |
| 3 | `07` | Threshold | -48dB - -6dB | (79 - 121) |  | 2 |
| 4 | `09` | Ratio | 1.0-20.0 | (0 - 7) | 10 | 1 |
| 5 | `0B` | Output Level | 0 - 127 | (0 - 127) |  | 3 |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 | 1 (*) |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## MULTI BAND COMP — Single / Master Effect Block

> (*) for Ducker.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Low Attack | 1ms - 200ms | (0 - 29) | 8 |  |
| 2 | `05` | Low Threshold | -54dB - -6dB | (73 - 121) |  |  |
| 3 | `07` | Low Ratio | 1.0 - 20.0 | (0 - 7) | 10 | 1 |
| 4 | `09` | Low Gain | -∞ - +18dB | (0 - 55) | 14 |  |
| 5 | `0B` | Mid Attack | 1ms - 200ms | (0 - 29) | 8 | 2 (*) |
| 6 | `0D` | Mid Threshold | -54dB - -6dB | (73 - 121) |  |  |
| 7 | `0F` | Mid Ratio | 1.0 - 20.0 | (0 - 7) | 10 | 2 |
| 8 | `11` | Mid Gain | -∞ - +18dB | (0 - 55) | 14 |  |
| 9 | `13` | High Attack | 1ms - 200ms | (0 - 29) | 8 |  |
| 10 | `15` | High Threshold | -54dB - -6dB | (73 - 121) |  |  |
| 11 | `17` | High Ratio | 1.0 - 20.0 | (0 - 7) | 10 | 3 |
| 12 | `19` | High Gain | -∞ - +18dB | (0 - 55) | 14 |  |
| 13 | `1B` | Divide Freq Low | 16Hz - 20kHz | (0 - 124) | 28 |  |
| 14 | `1D` | Divide Freq High | 16Hz - 20kHz | (0 - 124) | 28 |  |
| 15 | `1F` | Common Release | 10ms - 3000ms | (0 - 23) | 9 | 3 (*) |
| 16 | `21` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 | 1 (*) |

## UNIVERSAL COMPRESSOR DOWN — Single / Master Effect Block

> (*) for Ducker.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Threshold | -60dB - 0dB | (0 - 120) |  | 2 |
| 2 | `05` | Knee | 0 - 8 | (0 - 8) |  |  |
| 3 | `07` | Attack | 0.01ms - 80ms | (0 - 127) | 50 | 2 (*) |
| 4 | `09` | Release | 6.25ms-999.0ms | (0 - 127) | 51 | 3 (*) |
| 5 | `0B` | Ratio | 1.00 - ∞ | (0 - 127) | 52 | 1 |
| 6 | `0D` | Side Chain EQ Switch | Off, On | (0 - 1) |  |  |
| 7 | `0F` | Side Chain EQ Q | 0.1 - 10.0 | (0 - 126) | 53 |  |
| 8 | `11` | Side Chain EQ Frequency | 11.89Hz-17.78kHz | (0 - 127) | 54 |  |
| 9 | `13` | Side Chain EQ Gain | -30 - +30dB | (0 - 120) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | Output Level | -20 - +40dB | (0 - 120) |  |  |
| 12 | `19` | Make Up Gain | -20 - +40dB | (0 - 120) |  | 3 |
| 13 | `1B` | Post-comp HPF | Off, 1.035Hz-80.35Hz | (0 - 127) | 55 |  |
| 14 | `1D` | Clipper | Off, 1 - 100 | (0 - 100) |  |  |
| 15 | `1F` | Clipper Source | Dry+Wet, Wet | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |
| 17 |  | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 | 1 (*) |

## UNIVERSAL COMPRESSOR UP — Single / Master Effect Block

> (*) for Ducker.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Threshold | -60dB - 0dB | (0 - 120) |  | 2 |
| 2 | `05` | Knee | 0 - 8 | (0 - 8) |  |  |
| 3 | `07` | Attack | 0.01ms - 80ms | (0 - 127) | 50 | 2 (*) |
| 4 | `09` | Release | 6.25ms-999.0ms | (0 - 127) | 51 | 3 (*) |
| 5 | `0B` | Ratio | 1 - ∞ | (0 - 127) | 52 | 1 |
| 6 | `0D` | Side Chain EQ Switch | Off, On | (0 - 1) |  |  |
| 7 | `0F` | Side Chain EQ Q | 0.1 - 10.0 | (0 - 126) | 53 |  |
| 8 | `11` | Side Chain EQ Frequency | 11.89Hz-17.78kHz | (0 - 127) | 54 |  |
| 9 | `13` | Side Chain EQ Gain | -30 - +30 dB | (0 - 120) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | Output Level | -20 - +40dB | (0 - 120) |  |  |
| 12 | `19` | Make Up Gain | -20 - +20dB | (0 - 80) |  | 3 |
| 13 | `1B` | Post-comp HPF | Off, 1.035Hz-80.35Hz | (0 - 127) | 55 |  |
| 14 | `1D` | Clipper | Off, 1 - 100 | (0 - 100) |  |  |
| 15 | `1F` | Clipper Source | Dry+Wet, Wet | (0 - 1) |  |  |
| 16 | `21` | Gain Limit | 0 - +12dB | (0 - 120) |  |  |
| 17 |  | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 | 1 (*) |

## PARALLEL COMPRESSOR — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Type | Natural,Rich, Punchy, Electronic,Loud | (0 - 4) |  |  |
| 2 | `05` | Compression | 0 - 100 | (0 - 100) |  | 1 |
| 3 | `07` | Texture | 0 - 100 | (0 - 100) |  | 2 |
| 4 | `09` | Output Level | -18dB - +18dB | (0 - 120) |  | 3 |
| 5 | `0B` | Input Level | -18dB - +18dB | (0 - 120) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## AMP SIMULATOR 1 — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Overdrive | 0 - 100% | (0 - 100) |  | 2 |
| 2 | `05` | Device | Transistor, Vintage Tube, Distortion1, Distortion2, Fuzz | (0 - 4) |  |  |
| 3 | `07` | Speaker Type | Flat, Stack, Combo, Twin, Radio, Megaphone | (0 - 5) |  |  |
| 4 | `09` | Presence | -10 - +10 | (0 - 20) |  | 3 |
| 5 | `0B` | Output Level | 0 - 100% | (0 - 100) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## AMP SIMULATOR 2 — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Overdrive | 0 - 127 | (0 - 127) |  | 2 |
| 2 | `05` | AMP Type | Off, Stack, Combo, Tube, Crunch, Hi Gain, British | (0 - 6) |  |  |
| 3 | `07` | LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 | 3 |
| 4 | `09` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## COMP DISTORTION — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Overdrive | 0 - 127 | (0 - 127) |  | 2 |
| 2 | `05` | EQ Low Frequency | 32Hz - 2.0kHz | (4 - 40) | 3 |  |
| 3 | `07` | EQ Low Gain | -12dB - +12dB | (52 - 76) |  |  |
| 4 | `09` | LPF Cutoff Frequency | 1.0kHz-20.0kHz | (34 - 60) | 3 | 3 |
| 5 | `0B` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 8 | `11` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 9 | `13` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Edge | 0 - 127 | (0 - 127) |  |  |
| 12 | `19` | Attack | 1ms - 40ms | (0 - 19) | 8 |  |
| 13 | `1B` | Release | 10ms - 680ms | (0 - 15) | 9 |  |
| 14 | `1D` | Threshold | -48dB - -6dB | (79 - 121) |  |  |
| 15 | `1F` | Ratio | 1.0 - 20.0 | (0 - 7) | 10 |  |
| 16 | `21` | --- |  |  |  |  |

## COMP DISTORTION DELAY — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Overdrive | 0 - 100% | (0 - 100) |  | 2 |
| 2 | `05` | Device | Transistor, Vintage Tube, Distortion1, Distortion2, Fuzz | (0 - 4) |  |  |
| 3 | `07` | Speaker Type | Flat, Stack, Combo, Twin, Radio, Megaphone | (0 - 5) |  |  |
| 4 | `09` | Presence | -10 - 10 | (0 - 20) |  | 3 |
| 5 | `0B` | Output Level | 0 - 100% | (0 - 100) |  |  |
| 6 | `0D` | Delay Time L | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 7 | `0F` | Delay Time R | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 8 | `11` | Feedback Time | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 9 | `13` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Delay Mix | 0 - 127 | (0 - 127) |  |  |
| 12 | `19` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 13 | `1B` | Compress | -48dB - -6dB | (79 - 121) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## US COMBO — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Gain Boost | Low, High | (0 - 1) |  |  |
| 2 | `05` | Volume | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 3 | `07` | Low Cut | 0.0 - 10.0 | (0 - 100) |  |  |
| 4 | `09` | Mid Cut | 0.0 - 10.0 | (0 - 100) |  |  |
| 5 | `0B` | Mid Width | 0.0 - 10.0 | (0 - 100) |  |  |
| 6 | `0D` | Mid Sweep | 0.0 - 10.0 | (0 - 100) |  |  |
| 7 | `0F` | High Cut | 0.0 - 10.0 | (0 - 100) |  |  |
| 8 | `11` | Balance | 0.0 - 10.0 | (0 - 100) |  | 2 |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, BS 4x12, AC 2x12, AC 1x12, AC 4x10, BC 2x12, AM 4x12, YC 4x12, JC 2x12, OC 2x12, OC 1x8 | (0 - 10) | 30 |  |
| 12 | `19` | Speaker Air | 0 - 2 | (0 - 2) |  |  |
| 13 | `1B` | Mic Position | Center, Edge | (0 - 1) |  |  |
| 14 | `1D` | Presence | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## JAZZ COMBO — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Panning | 0.0 - 10.0 | (0 - 100) |  |  |
| 2 | `05` | Volume | 0.0 - 10.0 | (0 - 100) |  |  |
| 3 | `07` | Distortion | Off, 0.1 - 10.0 | (0 - 100) |  | 1 |
| 4 | `09` | Bass | 0.0 - 10.0 | (0 - 100) |  |  |
| 5 | `0B` | Middle | 0.0 - 10.0 | (0 - 100) |  |  |
| 6 | `0D` | Treble | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 7 | `0F` | High Treble | 0.0 - 10.0 | (0 - 100) |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, BS 4x12, AC 2x12, AC 1x12, AC 4x10, BC 2x12, AM 4x12, YC 4x12, JC 2x12, OC 2x12, OC 1x8 | (0 - 10) | 30 |  |
| 12 | `19` | Speaker Air | 0 - 2 | (0 - 2) |  |  |
| 13 | `1B` | Mic Position | Center, Edge | (0 - 1) |  |  |
| 14 | `1D` | Chorus | Off, Chorus, Vib | (0 - 2) |  |  |
| 15 | `1F` | Vib Speed | 0.0 - 10.0 | (0 - 100) |  |  |
| 16 | `21` | Depth | 0.0 - 10.0 | (0 - 100) |  | 2 |

## US HIGH GAIN — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Type | Raw1, Vintage1, Modern1, Raw2, Vintage2, Modern2 | (0 - 5) | 32 |  |
| 2 | `05` | Gain | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 3 | `07` | --- |  |  |  |  |
| 4 | `09` | Bass | 0.0 - 10.0 | (0 - 100) |  |  |
| 5 | `0B` | Middle | 0.0 - 10.0 | (0 - 100) |  | 2 |
| 6 | `0D` | Treble | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 7 | `0F` | Presence | 0.0 - 10.0 | (0 - 100) |  |  |
| 8 | `11` | Master Volume | 0.0 - 10.0 | (0 - 100) |  |  |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, BS 4x12, AC 2x12, AC 1x12, AC 4x10, BC 2x12, AM 4x12, YC 4x12, JC 2x12, OC 2x12, OC 1x8 | (0 - 10) | 30 |  |
| 12 | `19` | Speaker Air | 0 - 2 | (0 - 2) |  |  |
| 13 | `1B` | Mic Position | Center, Edge | (0 - 1) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## BRITISH LEAD — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Type | Crunch, Hi-Gain, Lead | (0 - 2) | Table No. | Assign No. |
| 2 | `05` | Preamp | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 3 | `07` | Tone Shift | Normal, Loose, Tight | (0 - 2) |  |  |
| 4 | `09` | Bass | 0.0 - 10.0 | (0 - 100) |  |  |
| 5 | `0B` | Middle | 0.0 - 10.0 | (0 - 100) |  | 2 |
| 6 | `0D` | Treble | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 7 | `0F` | Presence | 0.0 - 10.0 | (0 - 100) |  |  |
| 8 | `11` | Master Volume | 0.0 - 10.0 | (0 - 100) |  |  |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, BS 4x12, AC 2x12, AC 1x12, AC 4x10, BC 2x12, AM 4x12, YC 4x12, JC 2x12, OC 2x12, OC 1x8 | (0 - 10) | 30 |  |
| 12 | `19` | Speaker Air | 0 - 2 | (0 - 2) |  |  |
| 13 | `1B` | Mic Position | Center, Edge | (0 - 1) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## MULTI FX — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Comp. Sustain | Off, 0.1 - 10.0 | (0 - 100) |  | 2 |
| 2 | `05` | Wah SW | Off, Wah Pedal, Auto+ Full, Auto+ Mid, Auto+ Light, Auto- Full, Auto- Mid, Auto- Light | (0 - 7) | 33 |  |
| 3 | `07` | Wah Pedal | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Dist SW | Off, Overdrive, Distortion1, Distortion2, Clean, Crunch, Hi-Gain, Modern | (0 - 7) | 34 |  |
| 5 | `0B` | Dist Drive | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 6 | `0D` | Dist EQ | High Boost, Mid Boost, Mid Cut 1, Mid Cut 2, Mid Cut 3, Low Cut 1, Low Cut 2, High Cut, High/Low | (0 - 8) | 35 |  |
| 7 | `0F` | Dist Tone | 0.0 - 10.0 | (0 - 100) |  |  |
| 8 | `11` | Dist Presence | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, Stack, Twin, Tweed, Oldies, Modern, Mean, Soft, Small, Dip1, Dip2, Metal, Light | (0 - 12) | 31 |  |
| 12 | `19` | LFO Speed | 0.100Hz-9.925Hz | (0 - 127) | 36 |  |
| 13 | `1B` | Phaser SW | Off, Standard, Wide, Vibe, Tremolo | (0 - 4) | 37 |  |
| 14 | `1D` | Delay SW | Off, Delay M, Echo1 M, Echo2 M, Chorus M, Dly Chorus M, Flanger1 M, Flanger2 M, Flanger3 M, Delay St, Echo1 St, Echo2 St, Chorus St, Dl Chorus St, Flanger1 St, Flanger2 St, Flanger3 St | (0 - 16) | 38 |  |
| 15 | `1F` | Delay Ctrl | 0 - 127 | (0 - 127) |  |  |
| 16 | `21` | Delay Time | 0 - 127 | (0 - 127) |  |  |

## SMALL STEREO — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Comp. SW | Off, On | (0 - 1) |  |  |
| 2 | `05` | Comp. Sustain | 0.0 - 10.0 | (0 - 100) |  |  |
| 3 | `07` | Comp. Level | 0.0 - 10.0 | (0 - 100) |  |  |
| 4 | `09` | Dist Type | Overdrive, Distortion1, Distortion2, Clean, Crunch, Hi-Gain, Modern | (1 - 7) | 34 |  |
| 5 | `0B` | Dist Drive | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 6 | `0D` | Dist EQ | High Boost, Mid Boost, Mid Cut 1, Mid Cut 2, Mid Cut 3, Low Cut 1, Low Cut 2, High Cut, High/Low | (0 - 8) | 35 |  |
| 7 | `0F` | Dist Tone | 0.0 - 10.0 | (0 - 100) |  | 2 |
| 8 | `11` | Dist Presence | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, Stack, Twin, Tweed, Oldies, Modern, Mean, Soft, Small, Dip1, Dip2, Metal, Light | (0 - 12) | 31 |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## BRITISH COMBO — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Mode | Bright, Top Boost | (0 - 1) |  |  |
| 2 | `05` | Normal | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 3 | `07` | Brilliant | 0.0 - 10.0 | (0 - 100) |  | 2 |
| 4 | `09` | Bass | 0.0 - 10.0 | (0 - 100) |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | Treble | 0.0 - 10.0 | (0 - 100) |  |  |
| 7 | `0F` | Cut | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, BS 4x12, AC 2x12, AC 1x12, AC 4x10, BC 2x12, AM 4x12, YC 4x12, JC 2x12, OC 2x12, OC 1x8 | (0 - 10) | 30 |  |
| 12 | `19` | Speaker Air | 0 - 2 | (0 - 2) |  |  |
| 13 | `1B` | Mic Position | Center, Edge | (0 - 1) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## BRITISH LEGEND — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sensitivity | High, Low | (0 - 1) |  |  |
| 2 | `05` | Preamp | 0.0 - 10.0 | (0 - 100) |  | 1 |
| 3 | `07` | --- |  |  |  |  |
| 4 | `09` | Bass | 0.0 - 10.0 | (0 - 100) |  |  |
| 5 | `0B` | Middle | 0.0 - 10.0 | (0 - 100) |  | 2 |
| 6 | `0D` | Treble | 0.0 - 10.0 | (0 - 100) |  | 3 |
| 7 | `0F` | Presence | 0.0 - 10.0 | (0 - 100) |  |  |
| 8 | `11` | Master Volume | 0.0 - 10.0 | (0 - 100) |  |  |
| 9 | `13` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Speaker Type | Off, BS 4x12, AC 2x12, AC 1x12, AC 4x10, BC 2x12, AM 4x12, YC 4x12, JC 2x12, OC 2x12, OC 1x8 | (0 - 10) | 30 |  |
| 12 | `19` | Speaker Air | 0 - 2 | (0 - 2) |  |  |
| 13 | `1B` | Mic Position | Center, Edge | (0 - 1) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## LO-FI — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sampling Frequency Control | 44.1KHz-344.5Hz | (0 - 127) | 12 | 1 |
| 2 | `05` | Word Length | 1 - 127 | (1 - 127) |  | 2 |
| 3 | `07` | Output Level | -6dB - +36dB | (0 - 42) |  |  |
| 4 | `09` | Pre-LPF Cutoff Frequency | 63Hz - 20.0kHz | (10 - 60) | 3 |  |
| 5 | `0B` | Filter Type | Thru, PowerBass, Radio, Telephone, Clean, Low | (0 - 5) |  |  |
| 6 | `0D` | Pre-LPF Resonance | 1.0 - 12.0 | (10 - 120) |  |  |
| 7 | `0F` | Bit Assign | 0 - 6 | (0 - 6) |  |  |
| 8 | `11` | Emphasis | Off, On | (0 - 1) |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 3 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | Input Mode | Mono, Stereo | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |

## NOISY — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Mod Depth | 0 - 10 | (0 - 10) |  |  |
| 2 | `05` | Mod Speed | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Mod Feedback | 0 - 63 | (64 - 127) |  |  |
| 4 | `09` | Mod Mix Balance | 1 - 127 | (1 - 127) |  |  |
| 5 | `0B` | Drive | 0 - 127 | (0 - 127) |  | 2 |
| 6 | `0D` | AM Speed | 0.00Hz - 39.7Hz | (0 - 127) | 1 |  |
| 7 | `0F` | AM Depth | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 | 3 |
| 9 | `13` | LPF Resonance | 1.0 - 12.0 | (10 - 120) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Width | 1.0 - 12.0 | (10 - 120) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## DIGITAL TURNTABLE — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Click Density | 0 - 5 | (0 - 5) | Table No. | Assign No. |
| 2 | `05` | Click Level | 0 - 127 | (0 - 127) |  | 2 |
| 3 | `07` | Noise Tone | 0 - 6 | (0 - 6) |  |  |
| 4 | `09` | Noise Mod Speed | 0.00Hz - 39.7Hz | (0 - 127) | 1 |  |
| 5 | `0B` | Noise Mod Depth | 0 - 127 | (0 - 127) |  |  |
| 6 | `0D` | Dry Send to Noise | 0 - 127 | (0 - 127) |  | 3 |
| 7 | `0F` | Noise LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 |  |
| 8 | `11` | Noise LPF Q | 1.0 - 12.0 | (10 - 120) |  |  |
| 9 | `13` | Noise Level | 0 - 127 | (0 - 127) |  | 1 |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Dry Level | 0 - 127 | (0 - 127) |  |  |
| 12 | `19` | Dry LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## BIT CRUSHER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sample Rate | 0 - 100.00 | (0 -16383) |  | 1 |
| 2 | `05` | Bit | 1 - 16 | (1 - 16) |  | 2 |
| 3 | `07` | Crush Type | Soft, Hard | (0 - 1) |  |  |
| 4 | `09` | Input Level | -19.5dB - +12dB | (1 - 127) | 47 |  |
| 5 | `0B` | M/S | Off, On | (0 - 1) |  |  |
| 6 | `0D` | Side Sample Rate | 0 - 100.00 | (0 - 16383) |  |  |
| 7 | `0F` | Side Bit | 1 - 16 | (1 - 16) |  |  |
| 8 | `11` | Sample Rate Link | -1.0 - +1.0 | (0 - 100) |  |  |
| 9 | `13` | Bit Link | -1.0 - +1.0 | (0 - 100) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 3 |
| 11 | `17` | Output Level | -19.5dB - +12dB | (1 - 127) | 47 |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## WAVE FOLDER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Fold | 0.000 - 1.000 | (0 - 1000) |  | 2 |
| 2 | `05` | Fold Type | Soft, Hard | (0 - 1) |  |  |
| 3 | `07` | LFO Depth | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | LFO Speed | 0.01Hz - 1400Hz | (0 - 1023) | 62 |  |
| 5 | `0B` | LFO Shape | -50 - +50 | (0 - 100) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | Input Level | -40 - +20dB | (0 - 120) |  | 3 |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Output Level | -40 - +20dB | (0 - 120) |  |  |
| 12 | `19` | SEQ Depth | 0 - 127 | (0 - 127) |  |  |
| 13 | `1B` | SEQ Clock | 0.5x - 10.0x | (0 - 15) | 63 |  |
| 14 | `1D` | SEQ Pattern | A- J | (0 - 9) | 64 |  |
| 15 | `1F` | SEQ Variation | 0 - 100 | (0 - 100) |  |  |
| 16 | `21` | SEQ Phase Reset | OFF, Key On, Seq Start, Seq Start + Bar | (0 - 3) |  |  |

## G CHORUS — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 | 2 |
| 2 | `05` | --- |  |  |  |  |
| 3 | `07` | PM Depth | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 5 | `0B` | Delay Offset | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | Input Mode | Mono, Stereo | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |

## 2 MODULATOR — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 | 2 |
| 2 | `05` | AM Depth | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | PM Depth | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 5 | `0B` | Delay Offset | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | Input Mode | Mono, Stereo | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |

## SPX CHORUS — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 | 2 |
| 2 | `05` | LFO Depth | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 4 | `09` | Delay Offset | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D= W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | Input Mode | Mono, Stereo | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |

## SYMPHONIC — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 | 2 |
| 2 | `05` | LFO Depth | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | Delay Offset | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## ENSEMBLE DETUNE — Single / Master Effect Block

> 11 - 14 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Detune | -50cent-+50cent | (14 - 114) |  | 2 |
| 2 | `05` | Initial Delay Lch | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 3 | `07` | Initial Delay Rch | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 4 | `09` | Spread | 0 - 63 | (0 - 63) |  | 3 |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D= W - D<W63 | (1 - 127) |  | 1 |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM FLANGER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Speed | 0.040Hz-10.00Hz | (0 - 235) | 20 | 2 |
| 2 | `05` | Manual | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Depth | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Feedback | 0 - 127 | (0 - 127) |  |  |
| 5 | `0B` | Type | 1 - 3 | (0 - 2) |  |  |
| 6 | `0D` | Spread | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Mix | 0 - 127 | (0 - 127) |  | 1 |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## CLASSIC FLANGER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 | 2 |
| 2 | `05` | LFO Depth | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | LFO Wave | Triangle, Sine, Random | (0 - 2) |  |  |
| 4 | `09` | Delay Offset | 0.09 - 36.21ms | (0 - 139) | 18 |  |
| 5 | `0B` | Feedback Level | 0 - 100% | (100 - 200) |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | Modulation Phase | -180 - +180 | (0 - 16) | 19 |  |
| 15 | `1F` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 16 | `21` | Analog Feel | 0 - 10 | (0 - 10) |  |  |

## TEMPO FLANGER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 16th - 4thx16 | (5 - 29) | 13 | 2 |
| 2 | `05` | LFO Depth | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 4 | `09` | Delay Offset | 0.0ms - 50.0ms | (0 - 127) | 2 |  |
| 5 | `0B` | LFO Phase Reset | Off(free run), KeyOnReset, SEQ Start Reset | (0 - 2) |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | LFO Phase Difference | -180deg - +180deg | (4 - 124) |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## DYNAMIC FLANGER — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sensitivity | 0 - 127 | (0 - 127) |  | 2 |
| 2 | `05` | Delay Offset | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 4 | `09` | Attack Time | 0.3ms - 227ms | (0 - 127) | 15 |  |
| 5 | `0B` | Release Time | 2.6ms - 2171ms | (0 - 127) | 16 |  |
| 6 | `0D` | Release Curve | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Direction | Up, Down | (0 - 1) |  |  |
| 8 | `11` | Dyna Threshold Level | 0 - 127 | (0 - 127) |  |  |
| 9 | `13` | Dyna Level Offset | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 |  |

## CONTROL FLANGER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Flanger Control | 0 - 127 | (0 - 127) |  | 1 |
| 2 | `05` | Bottom | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Top | 0 - 127 | (0 - 127) |  | 2 |
| 4 | `09` | Feedback | 0 - 127 | (0 - 127) |  | 3 |
| 5 | `0B` | Type | 1 - 3 | (0 - 2) |  |  |
| 6 | `0D` | Spread | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Mix | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM PHASER MONO — Single / Master Effect Block

> The Color parameter is not available in the following conditions: When Mode is set to 1 and Stage is set to 4, 6, 8, 12 or 16; or when Mode is set to 2 and Stage is set to 4 or 10.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Speed | 0.100Hz-10.00Hz | (0 - 252) | 21 | 2 |
| 2 | `05` | Manual | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Depth | 0 - 127 | (0 - 127) |  | 1 |
| 4 | `09` | Feedback | 0 - 127 | (0 - 127) |  | 3 |
| 5 | `0B` | Stage | 4, 6, 8, 10, 12, 16 | (0 - 5) |  |  |
| 6 | `0D` | Mode | 1, 2, 3 | (0 - 2) |  |  |
| 7 | `0F` | Color | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM PHASER STEREO — Single / Master Effect Block

> The Color parameter is not available in the following conditions: When Mode is set to 1 and Stage is set to 4, 6, or 8; or when Mode is set to 2 and Stage is set to 4 or 10.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Speed | 0.100Hz-10.00Hz | (0 - 252) | 21 | 2 |
| 2 | `05` | Manual | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Depth | 0 - 127 | (0 - 127) |  | 1 |
| 4 | `09` | Feedback | 0 - 127 | (0 - 127) |  | 3 |
| 5 | `0B` | Stage | 4, 6, 8, 10 | (0 - 3) |  |  |
| 6 | `0D` | Mode | 1, 2 | (0 - 1) |  |  |
| 7 | `0F` | Color | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | Spread | 0 - 127 | (0 - 127) |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## TEMPO PHASER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 16th - 4thx16 | (5 - 29) | 13 | 2 |
| 2 | `05` | LFO Depth | 0 - 127 | (0 - 127) |  | 1 |
| 3 | `07` | Phase Shift Offset | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 5 | `0B` | LFO Phase Reset | Off(free run), KeyOnReset, SEQ Start Reset | (0 - 2) |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | Stage | 4 - 22 | (4 - 22) |  |  |
| 12 | `19` | Diffusion | Mono, Stereo | (0 - 1) |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## DYNAMIC PHASER — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sensitivity | 0 - 127 | (0 - 127) |  | 2 |
| 2 | `05` | Dyna Level Offset | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 3 |
| 4 | `09` | Attack Time | 0.3ms - 227ms | (0 - 127) | 15 |  |
| 5 | `0B` | Release Time | 2.6ms - 2171ms | (0 - 127) | 16 |  |
| 6 | `0D` | Release Curve | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Direction | Up, Down | (0 - 1) |  |  |
| 8 | `11` | Dyna Threshold Level | 0 - 127 | (0 - 127) |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Stage | 4, 5, 6 | (4 - 6) |  |  |
| 12 | `19` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 |  |

## CONTROL PHASER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Phase Control | 0 - 127 | (0 - 127) |  | 1 |
| 2 | `05` | Bottom | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Top | 0 - 127 | (0 - 127) |  | 2 |
| 4 | `09` | Feedback | 0 - 127 | (0 - 127) |  | 3 |
| 5 | `0B` | Stage | 4, 6, 8, 10 | (0 - 3) |  |  |
| 6 | `0D` | Mode | 1, 2 | (0 - 1) |  |  |
| 7 | `0F` | Color | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | Spread | 0 - 127 | (0 - 127) |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## AUTO PAN — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 | 2 |
| 2 | `05` | L/R Depth | 0 - 127 | (0 - 127) |  | 1 |
| 3 | `07` | F/R Depth | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Pan Direction | L<>R, L>>R, L<<R, L Turn, R Turn, L/R | (0 - 5) |  |  |
| 5 | `0B` | LFO Wave | 0 - 28 | (0 - 28) |  | 3 |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | Input Mode | Mono, Stereo | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |

## TREMOLO — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | Table No. 1 | Assign No. 2 |
| 2 | `05` | AM Depth | 0 - 127 | (0 - 127) |  | 1 |
| 3 | `07` | PM Depth | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 12 | `19` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 13 | `1B` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |
| 14 | `1D` | LFO Phase Difference | -180deg-+180deg | (4 - 124) |  |  |
| 15 | `1F` | Input Mode | Mono, Stereo | (0 - 1) |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM AUTO WAH — Single / Master Effect Block

> When the value of Bottom is greater than Top, the sound will not be modulated and only the Bottom value is available.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Speed | 0.100Hz-20.00Hz | (0 - 254) | 22 | 1 |
| 2 | `05` | Bottom | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Top | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Resonance Offset | -12.0 - +12.0 | (40 - 88) |  | 2 |
| 5 | `0B` | LFO Wave | Sin, Trp | (0 - 1) |  |  |
| 6 | `0D` | Type | High, Mid, Low, Bass | (0 - 3) |  |  |
| 7 | `0F` | Overdrive | 0.0dB - +40.0dB | (0 - 80) |  |  |
| 8 | `11` | Output | -20.0dB-+10.0dB | (24 - 84) |  | 3 |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM TOUCH WAH — Single / Master Effect Block

> When the value of Bottom is greater than Top, the sound will not be modulated and only the Bottom value is available.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sensitivity | 0 - 127 | (0 - 127) |  | 1 |
| 2 | `05` | Bottom | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Top | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Resonance Offset | -12.0 - +12.0 | (40 - 88) |  | 2 |
| 5 | `0B` | Direction | Up, Down | (0 - 1) |  |  |
| 6 | `0D` | Type | High, Mid, Low, Bass | (0 - 3) |  |  |
| 7 | `0F` | Overdrive | 0.0dB - +40.0dB | (0 - 80) |  |  |
| 8 | `11` | Output | -20.0dB-+10.0dB | (24 - 84) |  | 3 |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Attack Offset | -5 - +5 | (59 - 69) |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM PEDAL WAH — Single / Master Effect Block

> When the value of Bottom is greater than Top, the sound will not be modulated and only the Bottom value is available.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Pedal Control | 0 - 127 | (0 - 127) |  | 1 |
| 2 | `05` | Bottom | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | Top | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Resonance Offset | -12.0 - +12.0 | (40 - 88) |  | 2 |
| 5 | `0B` | Direction | Up, Down | (0 - 1) |  |  |
| 6 | `0D` | Type | High, Mid, Low, Bass | (0 - 3) |  |  |
| 7 | `0F` | Overdrive | 0.0dB - +40.0dB | (0 - 80) |  |  |
| 8 | `11` | Output | -20.0dB-+10.0dB | (24 - 84) |  | 3 |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## RING MODULATOR — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | OSC Frequency Coarse | 0.5Hz - 5kHz | (0 - 127) | 17 | 2 |
| 2 | `05` | OSC Frequency Fine | 0 - 127 | (0 - 127) |  |  |
| 3 | `07` | LFO Wave | Tri, Sine | (0 - 1) |  |  |
| 4 | `09` | LFO Depth | 0 - 127 | (0 - 127) |  | 3 |
| 5 | `0B` | LFO Speed | 0.0Hz - 39.70Hz | (0 - 127) | 1 |  |
| 6 | `0D` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 7 | `0F` | LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | Modulator Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 |  |

## DYNAMIC RING MODULATOR — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Sensitivity | 0 - 127 | (0 - 127) |  | 2 |
| 2 | `05` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 3 | `07` | LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 |  |
| 4 | `09` | Attack Time | 0.3ms - 227ms | (0 - 127) | 15 |  |
| 5 | `0B` | Release Time | 2.6ms - 2171ms | (0 - 127) | 16 |  |
| 6 | `0D` | Release Curve | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Direction | Up, Down | (0 - 1) |  |  |
| 8 | `11` | Dyna Threshold Level | 0 - 127 | (0 - 127) |  | 3 |
| 9 | `13` | Dyna Level Offset | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 |  |

## SPIRALIZER P / SPIRALIZER F — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Spiral Speed | -39.7Hz-0.00Hz- +39.7Hz | (1 - 255) | 60 | 2 |
| 2 | `05` | Filter Offset | C-2 - G8 | (0 - 127) |  |  |
| 3 | `07` | Feedback | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Spiral Step Mode | Continuous, Semitone, Scale | (0 - 2) |  |  |
| 5 | `0B` | Spiral Step Semitones | 1 semitones - 12 semitones | (0 - 11) |  |  |
| 6 | `0D` | Spiral Step Scale Type | Maj, Min(Natural), Min(Harmonic) | (0 - 2) |  |  |
| 7 | `0F` | Spiral Sync | Step, Octave | (0 - 1) |  |  |
| 8 | `11` | Offset Transition Rate | 1 - 62 | (1 - 62) |  |  |
| 9 | `13` | Spiral Step Transition Rate | 1/48 - 1/2 | (0 - 14) | 61 |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D= W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | Spiral Switch | Off, On | (0 - 1) |  |  |

## TEMPO SPIRALIZER P / TEMPO SPIRALIZER F — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Spiral Speed | 32nd/3 - 4thx6 | (0 - 19) | 13 | 2 |
| 2 | `05` | Filter Offset | C-2 - G8 | (0 - 127) |  |  |
| 3 | `07` | Feedback | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Spiral Step Mode | Continuous, Semitone, Scale | (0 - 2) |  |  |
| 5 | `0B` | Spiral Step Semitones | 1 semitones - 12 semitones | (0 - 11) |  |  |
| 6 | `0D` | Spiral Step Scale Type | Maj, Min(Natural), Min(Harmonic) | (0 - 2) |  |  |
| 7 | `0F` | Spiral Sync | Step, Octave | (0 - 1) |  |  |
| 8 | `11` | Offset Transition Rate | 1 - 62 | (1 - 62) |  |  |
| 9 | `13` | Spiral Step Transition Rate | 1/48 - 1/2 | (0 - 14) | 61 |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D= W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | Direction | Up, Down | (0 - 1) |  |  |
| 16 | `21` | Spiral Switch | Off, On | (0 - 1) |  |  |

## TECH MODULATION — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Mod Speed | 0 - 127 | (0 - 127) |  | 2 |
| 2 | `05` | Mod Depth | 0 - 127 | (0 - 127) |  | 3 |
| 3 | `07` | Mod Gain | -12 - +12dB | (52 - 76) |  |  |
| 4 | `09` | Mod Mix Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 5 | `0B` | Pre Mod HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 6 | `0D` | Mod LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 |  |
| 7 | `0F` | Mod LPF Resonance | 1.0 - 12.0 | (10 - 120) |  |  |
| 8 | `11` | Delay Time | 0.1 - 740.0ms | (1 - 7400) |  |  |
| 9 | `13` | Delay Time Offset R | 0 - 884 | (0 - 884) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 12 | `19` | FB Level Offset R | -63 - +63 | (1 - 127) |  |  |
| 13 | `1B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 14 | `1D` | FB Hi Damp Offset R | -0.9 - +0.9 | (1 - 19) |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## ROTARY SPEAKER 1 — Single / Master Effect Block

> 11 - 14 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Rotor Speed Slow | 0.0Hz - 2.65Hz | (0 - 63) | 1 |  |
| 2 | `05` | Horn Speed Slow | 0.0Hz - 2.65Hz | (0 - 63) | 1 |  |
| 3 | `07` | Rotor Speed Fast | 2.69Hz-39.70Hz | (64 - 127) | 1 |  |
| 4 | `09` | Horn Speed Fast | 2.69Hz-39.70Hz | (64 - 127) | 1 |  |
| 5 | `0B` | Slow-Fast Time of Rotor | 0 - 127 | (0 - 127) |  |  |
| 6 | `0D` | Slow-Fast Time of Horn | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Drive Rotor | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | Drive Horn | 0 - 127 | (0 - 127) |  |  |
| 9 | `13` | Rotor/ Horn Balance | R63>H - R=H - R<H63 | (1 - 127) |  | 2 |
| 10 | `15` | --- |  |  |  |  |
| 15 | `1F` | Mic L-R Angle | 0deg - 180deg | (0 - 60) |  | 3 |
| 16 | `21` | Speed Control | Slow, Fast | (0 - 1) |  | 1 |

## ROTARY SPEAKER 2 — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Speed Control | Slow, Fast | (0 - 1) |  | 1 |
| 2 | `05` | Drive | 0.0 - 10.0 | (0 - 100) |  |  |
| 3 | `07` | Tone | 0.0 - 10.0 | (0 - 100) |  |  |
| 4 | `09` | Rotor/ Horn Balance | R63>H - R=H - R<H63 | (1 - 127) |  | 2 |
| 5 | `0B` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 6 | `0D` | Mic L-R Angle | 0deg, 90deg, 120deg, 180deg | (0 - 3) |  |  |
| 7 | `0F` | Input Level | -6dB-0dB-+6dB | (52 - 76) |  |  |
| 8 | `11` | Modulation Depth | 0 - 63 | (0 - 63) |  | 3 |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Slow-Fast Time of Horn | x0.21 - x1.00 - x2.00 | (14 - 127) | 49 |  |
| 12 | `19` | Fast-Slow Time of Horn | x0.21 - x1.00 - x2.00 | (14 - 127) | 49 |  |
| 13 | `1B` | Rotor Speed Slow | 0.0rpm - 88.3rpm | (0 - 127) | 56 |  |
| 14 | `1D` | Horn Speed Slow | 0.0rpm - 89.6rpm | (0 - 127) | 57 |  |
| 15 | `1F` | Rotor Speed Fast | 189.3rpm-736.8rpm | (1 - 127) | 58 |  |
| 16 | `21` | Horn Speed Fast | 209.4rpm-817.6rpm | (1 - 127) | 59 |  |
| 17 |  | Slow-Fast Time of Rotor | x0.21 - x1.00 - x2.00 | (14 - 127) | 49 |  |
| 18 |  | Fast-Slow Time of Rotor | x0.21 - x1.00 - x2.00 | (14 - 127) | 49 |  |

## DYNAMIC FILTER — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Filter Type | LPF(12dB), LPF(18dB), LPF(24dB), HPF, BPF, BEF | (0 - 5) |  |  |
| 2 | `05` | Sensitivity | 0 - 127 | (0 - 127) |  | 2 |
| 3 | `07` | Dyna Level Offset | 0 - 127 | (0 - 127) |  |  |
| 4 | `09` | Resonance | -16 - +111 | (0 - 127) |  | 3 |
| 5 | `0B` | Attack Time | 0.3ms - 227ms | (0 - 127) | 15 |  |
| 6 | `0D` | Release Time | 2.6ms - 2171ms | (0 - 127) | 16 |  |
| 7 | `0F` | Release Curve | 0 - 127 | (0 - 127) |  |  |
| 8 | `11` | Direction | Up, Down | (0 - 1) |  |  |
| 9 | `13` | Dyna Threshold Level | 0 - 127 | (0 - 127) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | Side Chain Input Level | -∞dB-0dB-+24dB | (0 - 127) | 45 |  |

## AUTO SYNTH  Data Default — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Mod Speed | 0 - 127 | (0 - 127) |  |  |
| 2 | `05` | Mod Wave Type | TypeA, TypeB, TypeC, TypeD | (0 - 3) |  |  |
| 3 | `07` | Mod Depth | 0 - 127 | (0 - 127) |  | 1 |
| 4 | `09` | Mod Depth Offset R | -63 - +63 | (1 - 127) |  |  |
| 5 | `0B` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 6 | `0D` | LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 |  |
| 7 | `0F` | Delay Time | 0.1ms - 370.0ms | (1 - 3700) |  |  |
| 8 | `11` | Delay Time Offset R | 0 - 884 | (0 - 884) |  |  |
| 9 | `13` | Delay Level | 0 - 127 | (0 - 127) |  | 3 |
| 10 | `15` | Dry Mix Level | 0 - 127 | (0 - 127) |  |  |
| 11 | `17` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 12 | `19` | FB Level Offset R | -63 - +63 | (1 - 127) |  |  |
| 13 | `1B` | AM Speed | 0.00Hz - 39.7Hz | (0 - 127) | 1 |  |
| 14 | `1D` | AM Wave | Tri, Sine, Saw Up, Saw Down | (0 - 3) |  |  |
| 15 | `1F` | AM Depth | 0 - 127 | (0 - 127) |  | 2 |
| 16 | `21` | AM Inverse R | Normal, Inverse | (0 - 1) |  |  |

## ISOLATOR — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | On/Off Switch | Off, On | (0 - 1) |  |  |
| 2 | `05` | Low Level | -64 - +63 | (0 - 127) |  | 1 |
| 3 | `07` | Mid Level | -64 - +63 | (0 - 127) |  | 2 |
| 4 | `09` | High Level | -64 - +63 | (0 - 127) |  | 3 |
| 5 | `0B` | Low Mute | Off, On | (0 - 1) |  |  |
| 6 | `0D` | Mid Mute | Off, On | (0 - 1) |  |  |
| 7 | `0F` | High Mute | Off, On | (0 - 1) |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## SLICE — Single / Master Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Divide Type | 16th - 4th | (5 - 11) | 13 | 3 |
| 2 | `05` | Gate Time | 0 - 100% | (0 - 100) |  | 2 |
| 3 | `07` | Pan AEG Type | A- E | (0 - 4) |  |  |
| 4 | `09` | Pan AEG Min Level | 0 - 127 | (0 - 127) |  |  |
| 5 | `0B` | Pan Depth | -63 - +63 | (1 - 127) |  |  |
| 6 | `0D` | Divide Min Level | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Pan Type | A- J | (0 - 9) |  |  |
| 8 | `11` | Drive | 0 - 127 | (0 - 127) |  |  |
| 9 | `13` | AEG Phase | 0-15(×16th note) | (0 - 15) |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D= W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Phase Reset | Off(free run), KeyOnReset, SEQ Start Reset | (0 - 2) |  |  |
| 12 | `19` | --- |  |  |  |  |

## VINYL BREAK — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Break | Off, On | (0 - 1) |  | 1 |
| 2 | `05` | Speed | Fast, Middle, Slow, Vinyl Stop, Power Off | (0 - 4) |  | 2 |
| 3 | `07` | Speed Adjust | +30% - -30% | (0 - 120) |  | 3 |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | Output Level | -19.5dB - +12dB | (1 - 127) | 47 |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## BEAT REPEAT — Single / Master Effect Block

> This effect does not work properly below BPM42.

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Repeat | Off, On | (0 - 1) | Table No. | Assign No. 1 |
| 2 | `05` | Length | 1/256 - 1/1 | (0 - 8) | 48 | 1 |
| 3 | `07` | Freeze | Off, On | (0 - 1) |  |  |
| 4 | `09` | Gate Time | 1 - 100% | (1 - 100) |  | 2 |
| 5 | `0B` | Attack Time | 0 - 100% | (0 - 100) |  |  |
| 6 | `0D` | Release Time | 0 - 100% | (0 - 100) |  |  |
| 7 | `0F` | Play Speed | 0.0 - +1.0 | (65 - 127) |  | 3 |
| 8 | `11` | Pitch Sweep | -63 - +63 | (1 - 127) |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | Filter Type | THRU, LPF, HPF | (0 - 2) |  |  |
| 12 | `19` | Cutoff | 14.1Hz-21.1kHz | (0 - 127) | 46 |  |
| 13 | `1B` | Resonance | 0.0 - 12.7 | (0 - 127) |  |  |
| 14 | `1D` | Output Level | -19.5dB - +12dB | (1 - 127) | 47 |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM EQ 501 — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | EQ1(LSH) Frequency | 31.5Hz - 2.0kHz | (12 - 84) | 28 |  |
| 2 | `05` | EQ1(LSH) Gain | -12.0dB-+12.0dB | (60 - 300) |  | 1 |
| 3 | `07` | EQ2 Q | 0.50 - 16.00 | (0 - 60) | 29 |  |
| 4 | `09` | EQ2 Frequency | 50.0Hz-20.0kHz | (20 - 124) | 28 |  |
| 5 | `0B` | EQ2 Gain | -18.0dB-+18.0dB | (0 - 360) |  |  |
| 6 | `0D` | EQ3 Q | 0.50 - 16.00 | (0 - 60) | 29 |  |
| 7 | `0F` | EQ3 Frequency | 50.0Hz-20.0kHz | (20 - 124) | 28 |  |
| 8 | `11` | EQ3 Gain | -18.0dB-+18.0dB | (0 - 360) |  | 2 |
| 9 | `13` | EQ4 Q | 0.50 - 16.00 | (0 - 60) | 29 |  |
| 10 | `15` | EQ4 Frequency | 50.0Hz-20.0kHz | (20 - 124) | 28 |  |
| 11 | `17` | EQ4 Gain | -18.0dB-+18.0dB | (0 - 360) |  |  |
| 12 | `19` | EQ5(HSH) Frequency | 500Hz - 20.0kHz | (60 - 124) | 28 |  |
| 13 | `1B` | EQ5(HSH) Gain | -12.0dB-+12.0dB | (60 - 300) |  | 3 |
| 14 | `1D` | Output Level | -12.0dB-+12.0dB | (60 - 300) |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## PRESENCE — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Presence | 0 - 100 | (0 - 100) |  | 1 |
| 2 | `05` | Texture | 0 - 100 | (0 - 100) |  | 2 |
| 3 | `07` | Output Level | -6dB - +6dB | (0 - 120) |  | 3 |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## HARMONIC ENHANCER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | HPF Cutoff Frequency | 500Hz - 16.0kHz | (28 - 58) | 3 | 3 |
| 2 | `05` | Drive | 0 - 127 | (0 - 127) |  | 2 |
| 3 | `07` | Mix Level | 0 - 127 | (0 - 127) |  | 1 |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## STEREOPHONIC OPTIMIZER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Low Subband Gain Lch | -14.00dB-6.00dB | (5801-7801) |  |  |
| 2 | `05` | Low Subband Gain | -14.00dB-6.00dB | (5801-7801) |  |  |
| 3 | `07` | Rch Mid1 Subband Gain Lch Mid1 Subband Gain | -14.00dB-6.00dB | (5801-7801) |  |  |
| 4 | `09` |  | -14.00dB-6.00dB | (5801-7801) |  |  |
| 5 | `0B` | Rch Mid2 Subband Gain Lch Mid2 Subband Gain | -14.00dB-6.00dB | (5801-7801) |  |  |
| 6 | `0D` |  | -14.00dB-6.00dB | (5801-7801) |  |  |
| 7 | `0F` | Rch Mid3 Subband Gain Lch Mid3 Subband Gain | -14.00dB-6.00dB | (5801-7801) |  |  |
| 8 | `11` |  | -14.00dB-6.00dB | (5801-7801) |  |  |
| 9 | `13` | Rch High Subband Gain Lch | -14.00dB-6.00dB | (5801-7801) |  |  |
| 10 | `15` | High Subband Gain Rch | -14.00dB-6.00dB | (5801-7801) |  |  |
| 11 | `17` | Width Low | 0.00 - 1.00 | (0 - 100) |  | 1 |
| 12 | `19` | Width Mid1 | 0.00 - 1.00 | (0 - 100) |  |  |
| 13 | `1B` | Width Mid2 | 0.00 - 1.00 | (0 - 100) |  | 2 |
| 14 | `1D` | Width Mid3 | 0.00 - 1.00 | (0 - 100) |  |  |
| 15 | `1F` | Width High | 0.00 - 1.00 | (0 - 100) |  | 3 |
| 16 | `21` | On/Off Switch | Off - On | (0 - 1) |  |  |

## TALKING MODULATOR — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Vowel | a, i, u, e, o | (0 - 4) |  | 1 |
| 2 | `05` | Move Speed | 1 - 62 | (1 - 62) |  | 2 |
| 3 | `07` | Drive | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Output Level | 0 - 127 | (0 - 127) |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## VCM MINI BOOSTER — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | EQ Frequency | 0.00 - 100.00 | (0 - 10000) |  | 2 |
| 2 | `05` | Resonance | 0.0 - 1.0 | (0 - 500) |  | 3 |
| 3 | `07` | Gain | 0.0 - 20.0dB | (0 - 100) |  | 1 |
| 4 | `09` | Type | Low Shelf, High Shelf | (0 - 1) |  |  |
| 5 | `0B` | Texture | Retro, Standard, Modern | (0 - 2) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | Input Level | -36 - +24dB | (0 - 120) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Output Level | -40 - +20dB | (0 - 120) |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## DAMPER RESONANCE — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | --- |  |  |  |  |
| 2 | `05` | --- |  |  |  |  |
| 3 | `07` | --- |  |  |  |  |
| 4 | `09` | --- |  |  |  |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | Damper Control | 0 - 127 | (0 - 127) |  | 2, 3 |

## PITCH CHANGE — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Pitch 1 | -24 - +24 | (40 - 88) |  | 2 |
| 2 | `05` | Fine 1 | -50 - +50 | (14 - 114) |  |  |
| 3 | `07` | Initial Delay 1 | 0.1ms - 400.0ms | (0 - 127) | 7 |  |
| 4 | `09` | Feedback Level 1 | 0 - 63 | (64 - 127) |  |  |
| 5 | `0B` | Pitch 2 | -24 - +24 | (40 - 88) |  | 3 |
| 6 | `0D` | Fine 2 | -50 - +50 | (14 - 114) |  |  |
| 7 | `0F` | Initial Delay 2 | 0.1ms - 400.0ms | (0 - 127) | 7 |  |
| 8 | `11` | Feedback Level 2 | 0 - 63 | (64 - 127) |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  | 1 |
| 11 | `17` | Pan 1 | L63 - C - R63 | (1 - 127) |  |  |
| 12 | `19` | Output Level1 | 0 - 127 | (0 - 127) |  |  |
| 13 | `1B` | Pan 2 | L63 - C - R63 | (1 - 127) |  |  |
| 14 | `1D` | Output Level2 | 0 - 127 | (0 - 127) |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## NOISE GATE+COMP+EQ — Single / Master Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Comp Attack | 1ms - 40ms | (0 - 19) | 8 |  |
| 2 | `05` | Comp Release | 10ms - 680ms | (0 - 15) | 9 |  |
| 3 | `07` | Comp Threshold | -48dB - -6dB | (79 - 121) |  | 3 |
| 4 | `09` | Comp Ratio | 1.0 - 20.0 | (0 - 7) | 10 | 2 |
| 5 | `0B` | Comp Output Level | 0 - 127 | (0 - 127) |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Noise Gate Attack | 1ms - 40ms | (0 - 19) |  |  |
| 12 | `19` | Noise Gate Release | 10ms - 680ms | (0 - 15) |  |  |
| 13 | `1B` | Noise Gate Threshold | -73dB - -30dB | (54 - 97) |  | 1 |
| 14 | `1D` | EQ Mid Frequency | 100Hz - 10.0kHz | (14 - 54) | 3 |  |
| 15 | `1F` | EQ Mid Gain | -12dB - +12dB | (52 - 76) |  |  |
| 16 | `21` | EQ Mid Width | 0.1 - 12.0 | (1 - 120) |  |  |

## 2 Band EQ — Single EQ Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | EQ1 Type | Thru, LPF (-6dB/oct), HPF (-6dB/oct), Low Shelving, Hi Shelving, Peak/Dip | 0 - 5 |  |  |
| 2 | `05` | EQ1 Freq | 63Hz - 18.0Hz | 48 - 244 | 39 |  |
| 3 | `07` | EQ1 Gain | -12dB-0dB-+12dB | 40 - 64 -88 |  |  |
| 4 | `09` | EQ1 Q | 0.1 - 12.0 | 1 - 120 |  |  |
| 5 | `0B` | EQ2 Type | Thru, LPF (-6dB/oct), HPF (-6dB/oct), Low Shelving, Hi Shelving, Peak/Dip | 0 - 5 |  |  |
| 6 | `0D` | EQ2 Freq | 63Hz - 18.0Hz | 48 - 244 | 39 |  |
| 7 | `0F` | EQ2 Gain | -12dB-0dB-+12dB | 40 - 64 -88 |  |  |
| 8 | `11` | EQ2 Q | 0.1 - -12.0 | 1 - 120 |  |  |
| 9 | `13` | Output Gain | -12dB-0dB-+12dB | 40 - 64 -88 |  |  |

## Master EQ — Single EQ Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | EQ1 Gain | -12dB - +12dB | 52 - 76 |  |  |
| 2 | `05` | EQ1 Frequency | 32Hz - 2.0kHz | 4 - 40 | 3 |  |
| 3 | `07` | EQ1 Q | 0.1 - 12.0 | 1 - 120 |  |  |
| 4 | `09` | EQ1 Shape | Shelving, Peaking | 0 - 1 |  |  |
| 5 | `0B` | EQ2 Gain | -12dB - +12dB | 52 - 76 |  |  |
| 6 | `0D` | EQ2 Frequency | 100Hz - 10kHz | 14 - 54 | 3 |  |
| 7 | `0F` | EQ2 Q | 0.1 - 12.0 | 1 - 120 |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | EQ3 Gain | -12dB - +12dB | 52 - 76 |  |  |
| 10 | `15` | EQ3 Frequency | 100Hz - 10kHz | 14 - 54 | 3 |  |
| 11 | `17` | EQ3 Q | 0.1 - 12.0 | 1 - 120 |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | EQ4 Gain | -12dB - +12dB | 52 - 76 |  |  |
| 14 | `1D` | EQ4 Frequency | 100Hz - 10kHz | 14 - 54 | 3 |  |
| 15 | `1F` | EQ4 Q | 0.1 - 12.0 | 1 - 120 |  |  |
| 16 | `21` | --- |  |  |  |  |
| 17 |  | EQ5 Gain | -12dB - +12dB | 52 - 76 |  |  |
| 18 |  | EQ5 Frequency | 500Hz - 16kHz | 28 - 58 | 3 |  |
| 19 |  | EQ5 Q | 0.1 - 12.0 | 1 - 120 |  |  |
| 20 |  | EQ5 Shape | Shelving, Peaking | 0 - 1 |  |  |

## SPX HALL, SPX ROOM, SPX STAGE — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 30.0s | (0 - 69) | 4 | 1 |
| 2 | `05` | Diffusion | 0 - 10 | (0 - 10) |  | 2 |
| 3 | `07` | Initial Delay | 0.1ms - 99.3ms | (0 - 63) | 5 |  |
| 4 | `09` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 5 | `0B` | LPF Cutoff Frequency | 1.0kHz -20.0kHz | (34 - 60) | 3 | 3 |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | Reverb Delay | 0.1ms - 99.3ms | (0 - 63) | 5 |  |
| 12 | `19` | Density | 0 - 4 | (0 - 4) |  |  |
| 13 | `1B` | ER/Rev Balance | E63>R - E= R - E<R63 | (1 - 127) |  |  |
| 14 | `1D` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 15 | `1F` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 16 | `21` | --- |  |  |  |  |

## HD HALL, HD ROOM — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 30.0s | (0 - 69) | 4 | 1 |
| 2 | `05` | Room Size | 0 - 4 | (0 - 4) |  | 2 |
| 3 | `07` | Initial Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 4 | `09` | High Damp Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 | 3 |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | High Ratio | 0.0 - 1.0 | (0 - 10) |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | EQ Low Frequency | 22Hz - 1.0kHz | (1 - 34) | 3 |  |
| 14 | `1D` | EQ Low Gain | -12dB-0dB-+12dB | (52 - 76) |  |  |
| 15 | `1F` | EQ High Frequency | 500Hz - 18.0kHz | (28 - 59) | 3 |  |
| 16 | `21` | EQ High Gain | -12dB-0dB-+12dB | (52 - 76) |  |  |

## HD PLATE — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 30.0s | (0 - 69) | 4 | 1 |
| 2 | `05` | Plate Type | 1 - 3 | (0 - 2) |  | 2 |
| 3 | `07` | Initial Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 4 | `09` | High Damp Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 | 3 |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | High Ratio | 0.0 - 1.0 | (0 - 10) |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | EQ Low Frequency | 22Hz - 1.0kHz | (1 - 34) | 3 |  |
| 14 | `1D` | EQ Low Gain | -12dB-0dB-+12dB | (52 - 76) |  |  |
| 15 | `1F` | EQ High Frequency | 500Hz - 18.0kHz | (28 - 59) | 3 |  |
| 16 | `21` | EQ High Gain | -12dB-0dB-+12dB | (52 - 76) |  |  |

## REV-X HALL, REV-X ROOM — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 18.0s | (0 - 69) | 23/24 | 1 |
| 2 | `05` | Diffusion | 0 - 10 | (0 - 10) |  |  |
| 3 | `07` | Initial Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 4 | `09` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 5 | `0B` | LPF Cutoff Frequency | 1.0kHz - 20.0kHz | (34 - 60) | 3 | 3 |
| 6 | `0D` | Room Size | 0 – 31 | (0 - 31) |  | 2 |
| 7 | `0F` | High Ratio | 0.1 - 1.0 | (1 - 10) |  |  |
| 8 | `11` | Low Ratio | 0.1 - 1.4 | (1 - 14) |  |  |
| 9 | `13` | Decay | 0 - 63 | (0 - 63) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## R3 HALL, R3 ROOM, R3 PLATE — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 30.0s | (0 - 69) | 4 | 1 |
| 2 | `05` | Diffusion | 0 – 10 | (0 - 10) |  | 2 |
| 3 | `07` | Initial Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 4 | `09` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 5 | `0B` | LPF Cutoff Frequency | 1.0kHz -20.0kHz | (34 - 60) | 3 | 3 |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Reverb Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 12 | `19` | Density | 0 - 4 | (0 - 4) |  |  |
| 13 | `1B` | ER/Rev Balance | E63>R - E=R - E<R63 | (1 - 127) |  |  |
| 14 | `1D` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 15 | `1F` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 16 | `21` | --- |  |  |  |  |

## SPACE SIMULATOR — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Reverb Time | 0.3s - 30.0s | (0 - 69) | 4 | 1 |
| 2 | `05` | Diffusion | 0 – 10 | (0 - 10) |  | 2 |
| 3 | `07` | Initial Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 4 | `09` | HPF Cutoff Frequency | 20Hz - 8.0kHz | (0 - 52) | 3 |  |
| 5 | `0B` | LPF Cutoff Frequency | 1.0kHz -20.0kHz | (34 - 60) | 3 | 3 |
| 6 | `0D` | Width | 0.5m - 30.2m | (0 - 104) | 11 |  |
| 7 | `0F` | Height | 0.5m - 30.2m | (0 - 104) | 11 |  |
| 8 | `11` | Depth | 0.5m - 30.2m | (0 - 104) | 11 |  |
| 9 | `13` | Wall Vary | 0 - 30 | (0 - 30) |  |  |
| 10 | `15` | --- |  |  |  |  |
| 11 | `17` | Reverb Delay | 0.1ms - 200.0ms | (0 - 127) | 5 |  |
| 12 | `19` | Density | 0 - 4 | (0 - 4) |  |  |
| 13 | `1B` | ER/Rev Balance | E63>R - E= R - E<R63 | (1 - 127) |  |  |
| 14 | `1D` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  |  |
| 15 | `1F` | Feedback Level | 0 - 63 | (64 - 127) |  |  |
| 16 | `21` | Space Type | 1 - 2 | (0-1) |  |  |

## CROSS DELAY — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L>R | 0.1ms-1638.3ms | (1 - 16383) |  | 1 |
| 2 | `05` | Delay Time R>L | 0.1ms-1638.3ms | (1 - 16383) |  | 1 |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 4 | `09` | Input Select | L, R, L&R, L-MODE2, R-MODE2 | (0 - 4) |  |  |
| 5 | `0B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | EQ Low Frequency | 32Hz - 2.0kHz | (4 - 40) | 3 |  |
| 14 | `1D` | EQ Low Gain | -12dB - +12dB | (52 - 76) |  |  |
| 15 | `1F` | EQ High Frequency | 500Hz - 16.0kHz | (28 - 58) | 3 |  |
| 16 | `21` | EQ High Gain | -12dB - +12dB | (52 - 76) |  |  |

## TEMPO CROSS DELAY — Send Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L>R | 32nd/3 - 4thx6 | (0 - 19) | 13 | 1 |
| 2 | `05` | Delay Time R>L | 32nd/3 - 4thx6 | (0 - 19) | 13 | 1 |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 4 | `09` | Input Select | L, R, L&R, L-MODE2, R-MODE2 | (0 - 4) |  |  |
| 5 | `0B` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 6 | `0D` | Lag | -63ms - +63ms | (1 - 127) |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## TEMPO DELAY MONO — Send Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 32nd/3 - 4thx6 | (0 - 19) | 13 | 1 |
| 2 | `05` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 3 | `07` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 4 | `09` | L/R Diffusion | -63ms - +63ms | (1 - 127) |  |  |
| 5 | `0B` | Lag | -63ms - +63ms | (1 - 127) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## TEMPO DELAY STEREO — Send Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 32nd/3 - 4thx6 | (0 - 19) | 13 | 1 |
| 2 | `05` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 3 | `07` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 4 | `09` | L/R Diffusion | -63ms - +63ms | (1 - 127) |  |  |
| 5 | `0B` | Lag | -63ms - +63ms | (1 - 127) |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## CONTROL DELAY — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 0.1ms-1486.0ms | (1 - 14860) |  | 1 |
| 2 | `05` | Delay Transition Rate | 1 - 48 | (1 - 48) |  |  |
| 3 | `07` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 4 | `09` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 5 | `0B` | --- |  |  |  |  |
| 6 - 9 |  | Same as the parameters | shaded in gray | in CROSS DELAY |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## DELAY LR — Send Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L | 0.1ms-1638.3ms | (1 - 16383) | Table No. | Assign No. 1 |
| 2 | `05` | Delay Time R | 0.1ms-1638.3ms | (1 - 16383) |  | 1 |
| 3 | `07` | Feedback Time L | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 4 | `09` | Feedback Time R | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 5 | `0B` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 6 | `0D` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## DELAY LCR — Send Effect Block

> 13 - 16 Same as the parameters shaded in gray in CROSS DELAY

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time L | 0.1ms-1638.3ms | (1 - 16383) |  | 1 |
| 2 | `05` | Delay Time R | 0.1ms-1638.3ms | (1 - 16383) |  | 1 |
| 3 | `07` | Delay Time C | 0.1ms-1638.3ms | (1 - 16383) |  | 1 |
| 4 | `09` | Feedback Time | 0.1ms-1638.3ms | (1 - 16383) |  |  |
| 5 | `0B` | Feedback Level | 0 - 63 | (64 - 127) |  | 2 |
| 6 | `0D` | Delay Level C | 0 - 127 | (0 - 127) |  |  |
| 7 | `0F` | Feedback High Damp | 0.1 - 1.0 | (1 - 10) |  | 3 |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |

## ANALOG DELAY RETRO — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 25ms - 800ms | (0 - 127) | 41 | 1 |
| 2 | `05` | Feedback Level | 0 - 127 | (0 - 127) |  | 2 |
| 3 | `07` | Delay Input Level | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Type | Mellow, Dub, Narrow, Soft, Dark | (0 - 4) | 43 |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |

## ANALOG DELAY MODERN — Send Effect Block

| No. | Offset | Parameter | Display range | Value range | Data assign table | Default slider |
|---|---|---|---|---|---|---|
| 1 | `03` | Delay Time | 50ms - 1.0s | (0 - 127) | 42 | 1 |
| 2 | `05` | Feedback Level | 0 - 127 | (0 - 127) |  | 2 |
| 3 | `07` | Delay Input Level | 0 - 127 | (0 - 127) |  | 3 |
| 4 | `09` | Type | Urban, Dub, Narrow, Soft, Dark | (0 - 4) | 44 |  |
| 5 | `0B` | --- |  |  |  |  |
| 6 | `0D` | --- |  |  |  |  |
| 7 | `0F` | --- |  |  |  |  |
| 8 | `11` | --- |  |  |  |  |
| 9 | `13` | --- |  |  |  |  |
| 10 | `15` | Dry/Wet Balance | D63>W - D=W - D<W63 | (1 - 127) |  |  |
| 11 | `17` | --- |  |  |  |  |
| 12 | `19` | --- |  |  |  |  |
| 13 | `1B` | --- |  |  |  |  |
| 14 | `1D` | --- |  |  |  |  |
| 15 | `1F` | --- |  |  |  |  |
| 16 | `21` | --- |  |  |  |  |
