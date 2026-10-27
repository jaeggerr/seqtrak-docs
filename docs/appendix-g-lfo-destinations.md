# Appendix G — LFO destination numbers

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/misc_tables.py`.
> Confidence: `from Yamaha Data List`.


The value written to `LFO Box1/2/3 Destination` (`31 4p 0B`, `0E`, `11`). Destinations 0-23 and 32-55 reach the two insertion effects' parameters; 64-68 reach element-level controls. The last two columns say which engines accept the destination.

| No. | No. (HEX) | No. (BIN) | Parameter | Drum/Synth/SAMPLER part | DX part |
|---|---|---|---|---|---|
| 0 | `0000` | `00000000` | Insertion Effect A Parameter 1 | yes | yes |
| 1 | `0001` | `00000001` | Insertion Effect A Parameter 2 | yes | yes |
| 2 | `0002` | `00000010` | Insertion Effect A Parameter 3 | yes | yes |
| 3 | `0003` | `00000011` | Insertion Effect A Parameter 4 | yes | yes |
| 4 | `0004` | `00000100` | Insertion Effect A Parameter 5 | yes | yes |
| 5 | `0005` | `00000101` | Insertion Effect A Parameter 6 | yes | yes |
| 6 | `0006` | `00000110` | Insertion Effect A Parameter 7 | yes | yes |
| 7 | `0007` | `00000111` | Insertion Effect A Parameter 8 | yes | yes |
| 8 | `0008` | `00001000` | Insertion Effect A Parameter 9 | yes | yes |
| 9 | `0009` | `00001001` | Insertion Effect A Parameter 10 | yes | yes |
| 10 | `000A` | `00001010` | Insertion Effect A Parameter 11 | yes | yes |
| 11 | `000B` | `00001011` | Insertion Effect A Parameter 12 | yes | yes |
| 12 | `000C` | `00001100` | Insertion Effect A Parameter 13 | yes | yes |
| 13 | `000D` | `00001101` | Insertion Effect A Parameter 14 | yes | yes |
| 14 | `000E` | `00001110` | Insertion Effect A Parameter 15 | yes | yes |
| 15 | `000F` | `00001111` | Insertion Effect A Parameter 16 | yes | yes |
| 16 | `0010` | `00010000` | Insertion Effect A Parameter 17 | yes | yes |
| 17 | `0011` | `00010001` | Insertion Effect A Parameter 18 | yes | yes |
| 18 | `0012` | `00010010` | Insertion Effect A Parameter 19 | yes | yes |
| 19 | `0013` | `00010011` | Insertion Effect A Parameter 20 | yes | yes |
| 20 | `0014` | `00010100` | Insertion Effect A Parameter 21 | yes | yes |
| 21 | `0015` | `00010101` | Insertion Effect A Parameter 22 | yes | yes |
| 22 | `0016` | `00010110` | Insertion Effect A Parameter 23 | yes | yes |
| 23 | `0017` | `00010111` | Insertion Effect A Parameter 24 | yes | yes |
| 24 | `0018` | `00011000` | reserved |  |  |
| 25 | `0019` | `00011001` | reserved |  |  |
| 26 | `001A` | `00011010` | reserved |  |  |
| 27 | `001B` | `00011011` | reserved |  |  |
| 28 | `001C` | `00011100` | reserved |  |  |
| 29 | `001D` | `00011101` | reserved |  |  |
| 30 | `001E` | `00011110` | reserved |  |  |
| 31 | `001F` | `00011111` | reserved |  |  |
| 32 | `0020` | `00100000` | Insertion Effect B Parameter 1 | yes | yes |
| 33 | `0021` | `00100001` | Insertion Effect B Parameter 2 | yes | yes |
| 34 | `0022` | `00100010` | Insertion Effect B Parameter 3 | yes | yes |
| 35 | `0023` | `00100011` | Insertion Effect B Parameter 4 | yes | yes |
| 36 | `0024` | `00100100` | Insertion Effect B Parameter 5 | yes | yes |
| 37 | `0025` | `00100101` | Insertion Effect B Parameter 6 | yes | yes |
| 38 | `0026` | `00100110` | Insertion Effect B Parameter 7 | yes | yes |
| 39 | `0027` | `00100111` | Insertion Effect B Parameter 8 | yes | yes |
| 40 | `0028` | `00101000` | Insertion Effect B Parameter 9 | yes | yes |
| 41 | `0029` | `00101001` | Insertion Effect B Parameter 10 | yes | yes |
| 42 | `002A` | `00101010` | Insertion Effect B Parameter 11 | yes | yes |
| 43 | `002B` | `00101011` | Insertion Effect B Parameter 12 | yes | yes |
| 44 | `002C` | `00101100` | Insertion Effect B Parameter 13 | yes | yes |
| 45 | `002D` | `00101101` | Insertion Effect B Parameter 14 | yes | yes |
| 46 | `002E` | `00101110` | Insertion Effect B Parameter 15 | yes | yes |
| 47 | `002F` | `00101111` | Insertion Effect B Parameter 16 | yes | yes |
| 48 | `0030` | `00110000` | Insertion Effect B Parameter 17 | yes | yes |
| 49 | `0031` | `00110001` | Insertion Effect B Parameter 18 | yes | yes |
| 50 | `0032` | `00110010` | Insertion Effect B Parameter 19 | yes | yes |
| 51 | `0033` | `00110011` | Insertion Effect B Parameter 20 | yes | yes |
| 52 | `0034` | `00110100` | Insertion Effect B Parameter 21 | yes | yes |
| 53 | `0035` | `00110101` | Insertion Effect B Parameter 22 | yes | yes |
| 54 | `0036` | `00110110` | Insertion Effect B Parameter 23 | yes | yes |
| 55 | `0037` | `00110111` | Insertion Effect B Parameter 24 | yes | yes |
| 56 | `0038` | `00111000` | reserved |  |  |
| 57 | `0039` | `00111001` | reserved |  |  |
| 58 | `003A` | `00111010` | reserved |  |  |
| 59 | `003B` | `00111011` | reserved |  |  |
| 60 | `003C` | `00111100` | reserved |  |  |
| 61 | `003D` | `00111101` | reserved |  |  |
| 62 | `003E` | `00111110` | reserved |  |  |
| 63 | `003F` | `00111111` | reserved |  |  |
| 64 | `0040` | `01000000` | Element Level | yes |  |
| 65 | `0041` | `01000001` | Element Pitch | yes |  |
| 66 | `0042` | `01000010` | Element Filter Cutoff | yes |  |
| 67 | `0043` | `01000011` | Element Filter Resonance/Width | yes |  |
| 68 | `0044` | `01000100` | Element Pan | yes |  |
