# Appendix J — Value conversion tables

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/effect_assign_tables.py` and `tools/pdf-extract/misc_tables.py`.
> Confidence: `from Yamaha Data List`.


Two families of lookup tables turn a transmitted byte into the value the hardware shows. They are long and purely numeric, so the rows live in CSV rather than in Markdown; this page is the index.

## Effect data assign tables

Referenced by number from the **Data assign table** column of [appendix-b-effect-parameters.md](appendix-b-effect-parameters.md). Rows: [`../data/effect-data-assign-tables.csv`](../data/effect-data-assign-tables.csv) (7330 rows across 63 tables).

```bash
# every entry of table 41 (short delay times)
awk -F, '$1==41' data/effect-data-assign-tables.csv
```

| Table | Quantity | Entries | Data range |
|---|---|---|---|
| 1 | LFO Frequency | 128 | 0 - 127 |
| 2 | Modulation Delay Offset | 128 | 0 - 127 |
| 3 | EQ Frequency | 61 | 0 - 60 |
| 4 | Reverb Time | 70 | 0 - 69 |
| 5 | Delay Time (0.1 – 200.0 [ms]) | 128 | 0 - 127 |
| 6 | Room Size | 128 | 0 - 127 |
| 7 | Delay Time (0.1 – 400.0 [ms]) | 128 | 0 - 127 |
| 8 | Compressor Attack Time | 30 | 0 - 29 |
| 9 | Compressor Release Time | 24 | 0 - 23 |
| 10 | Compressor Ratio | 8 | 0 - 7 |
| 11 | Reverb Width; Depth; Height | 105 | 0 - 104 |
| 12 | LO-FI Sampling Frequency Control | 128 | 0 - 127 |
| 13 | Tempo | 30 | 0 - 29 |
| 14 | Multi Compressor Gain (dB) | 56 | 0 - 55 |
| 15 | Dyna Attack Time (ms) | 128 | 0 - 127 |
| 16 | Dyna Release Time (ms) | 128 | 0 - 127 |
| 17 | Ring Mod OSC Freq Coarse (Hz) | 128 | 0 - 127 |
| 18 | Classic Flanger Delay Offset | 140 | 0 - 139 |
| 19 | Modulation Phase | 17 | 0 - 16 |
| 20 | VCM Flanger Speed | 236 | 0 - 235 |
| 21 | VCM Phaser Speed | 253 | 0 - 252 |
| 22 | VCM Wah Speed | 255 | 0 - 254 |
| 23 | Rev Hall Time | 70 | 0 - 69 |
| 24 | Rev Room Time | 70 | 0 - 69 |
| 25 | VCM Comp Level | 201 | 0 - 200 |
| 26 | VCM Comp Attack Time | 201 | 0 - 200 |
| 27 | VCM Comp Release Time | 201 | 0 - 200 |
| 28 | VCM EQ Frequency | 137 | 0 - 136 |
| 29 | VCM EQ Q | 61 | 0 - 60 |
| 30 | Speaker Type | 11 | 0 - 10 |
| 31 | Speaker Type2 | 13 | 0 - 12 |
| 32 | Distortion Type | 6 | 0 - 5 |
| 33 | Wah Switch | 8 | 0 - 7 |
| 34 | Distortion Switch | 8 | 0 - 7 |
| 35 | Distortion EQ | 9 | 0 - 8 |
| 36 | LFO Speed | 128 | 0 - 127 |
| 37 | Phaser Switch | 5 | 0 - 4 |
| 38 | Delay Switch | 17 | 0 - 16 |
| 39 | EQ Frequency | 256 | 0 - 255 |
| 41 | Delay Time (short) | 128 | 0 - 127 |
| 42 | Delay Time (long) | 128 | 0 - 127 |
| 43 | Analog Delay Retro | 5 | 0 - 4 |
| 44 | Analog Delay Modern | 5 | 0 - 4 |
| 45 | Side Chain Input Level | 128 | 0 - 127 |
| 46 | Beat Repeat Cutoff | 128 | 0 - 127 |
| 47 | Beat Repeat Gain | 127 | 1 - 127 |
| 48 | Beat Repeat Length | 128 | 0 - 127 |
| 49 | Rotary Windup/down Accel | 114 | 14 - 127 |
| 50 | Downward Comp Attack | 128 | 0 - 127 |
| 51 | Downward Comp Release | 128 | 0 - 127 |
| 52 | Downward Comp Ratio | 128 | 0 - 127 |
| 53 | Downward Comp EQ Q | 127 | 0 - 126 |
| 54 | Downward Comp EQ Freq | 128 | 0 - 127 |
| 55 | Downward Comp Post HPF | 128 | 0 - 127 |
| 56 | Rotary Speaker 2 Speed Slow Woofer | 128 | 0 - 127 |
| 57 | Rotary Speaker 2 Speed Slow Horn | 128 | 0 - 127 |
| 58 | Rotary Speaker 2 Speed Fast Woofer | 128 | 0 - 127 |
| 59 | Rotary Speaker 2 Speed Fast Horn | 128 | 0 - 127 |
| 60 | Reversible LFO Frequency | 256 | 0 - 255 |
| 61 | LFO Step Transitional Rate | 15 | 0 - 14 |
| 62 | Wave Folder LFO Speed | 1024 | 0 - 1023 |
| 63 | Wave Folder Seq Speed | 16 | 0 - 15 |
| 64 | Wave Folder Seq Pattern | 10 | 0 - 9 |

Table numbers are Yamaha's own and are not contiguous — there is no table 40.

## EQ frequency tables

Used by the 3-band and 2-band EQ frequency parameters, which are two-byte values. Each row gives the decimal data value, the two transmitted bytes in hex, and the resulting frequency in Hz. Rows: [`../data/eq-frequency-tables.csv`](../data/eq-frequency-tables.csv) (512 rows).

| Table | Entries | Data range |
|---|---|---|
| 2bandEQ Frequency | 256 | 0 - 255 |
| 3bandEQ Frequency | 256 | 0 - 255 |
