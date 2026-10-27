# Appendix C — Preset sound list

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/sound_list.py`.
> Confidence: `from Yamaha Data List`.


All 2424 factory presets. Drum, Synth and DX share one numbering space (1-2032) under bank MSB 63; SAMPLER elements are numbered from 1 under bank MSB 62. **LSB** = `(number - 1) / 128`, **PC** = `(number - 1) % 128`.

The SEQTRAK transmits Bank Select MSB, Bank Select LSB and then a Program Change whenever the sound changes (`verified on hardware`), so a received triplet resolves to a row of this table directly. For **user** sounds, which are not listed here, and for the exact stored name, dump `31 0p 00` instead — see [06-sounds-presets.md](06-sounds-presets.md).

Machine-readable: [`../data/presets.csv`](../data/presets.csv).


## Drum sounds (855)


### Kick (112)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1 | Tight Punchy Kick 1 | 63 | 0 | 0 |
| 2 | Tight Punchy Kick 2 | 63 | 0 | 1 |
| 3 | Tight Punchy Kick 3 | 63 | 0 | 2 |
| 4 | Tight Punchy Kick 4 | 63 | 0 | 3 |
| 5 | Tight Punchy Kick 5 | 63 | 0 | 4 |
| 6 | Tight Punchy Kick 6 | 63 | 0 | 5 |
| 7 | Tight Punchy Kick 7 | 63 | 0 | 6 |
| 8 | Tight Punchy Kick 8 | 63 | 0 | 7 |
| 9 | Soft Kick 1 | 63 | 0 | 8 |
| 10 | Tight Soft Kick 1 | 63 | 0 | 9 |
| 11 | Tight Soft Kick 2 | 63 | 0 | 10 |
| 12 | Tight Soft Kick 3 | 63 | 0 | 11 |
| 13 | Tight Soft Kick 4 | 63 | 0 | 12 |
| 14 | Tight Soft Kick 5 | 63 | 0 | 13 |
| 15 | Tight Soft Kick 6 | 63 | 0 | 14 |
| 16 | Tight Soft Kick 7 | 63 | 0 | 15 |
| 17 | Punchy Fat Kick 1 | 63 | 0 | 16 |
| 18 | Punchy Fat Kick 2 | 63 | 0 | 17 |
| 19 | Punchy Fat Kick 3 | 63 | 0 | 18 |
| 20 | Punchy Fat Kick 4 | 63 | 0 | 19 |
| 21 | Punchy Fat Kick 5 | 63 | 0 | 20 |
| 22 | Bitcrushed Punchy Kick 1 | 63 | 0 | 21 |
| 23 | Punchy Fat Kick 6 | 63 | 0 | 22 |
| 24 | Punchy Fat Kick 7 | 63 | 0 | 23 |
| 25 | Distorted Kick 1 | 63 | 0 | 24 |
| 26 | Distorted Kick 2 | 63 | 0 | 25 |
| 27 | Distorted Kick 3 | 63 | 0 | 26 |
| 28 | Distorted Kick 4 | 63 | 0 | 27 |
| 29 | Distorted Kick 5 | 63 | 0 | 28 |
| 30 | Distorted Kick 6 | 63 | 0 | 29 |
| 31 | Distorted Kick 7 | 63 | 0 | 30 |
| 32 | Distorted Kick 8 | 63 | 0 | 31 |
| 33 | Saturated Tight Kick 1 | 63 | 0 | 32 |
| 34 | Saturated Fat Kick 1 | 63 | 0 | 33 |
| 35 | Saturated Tight Kick 2 | 63 | 0 | 34 |
| 36 | Saturated Fat Kick 2 | 63 | 0 | 35 |
| 37 | Saturated Fat Kick 3 | 63 | 0 | 36 |
| 38 | Saturated Fat Kick 4 | 63 | 0 | 37 |
| 39 | Saturated Fat Kick 5 | 63 | 0 | 38 |
| 40 | Saturated Fat Kick 6 | 63 | 0 | 39 |
| 41 | Saturated Fat Kick 7 | 63 | 0 | 40 |
| 42 | Punchy Saturated Kick 1 | 63 | 0 | 41 |
| 43 | Saturated Fat Kick 8 | 63 | 0 | 42 |
| 44 | Saturated Fat Kick 9 | 63 | 0 | 43 |
| 45 | Bitcrushed Kick 1 | 63 | 0 | 44 |
| 46 | Bitcrushed Kick 2 | 63 | 0 | 45 |
| 47 | Bitcrushed Kick 3 | 63 | 0 | 46 |
| 48 | Bitcrushed Kick 4 | 63 | 0 | 47 |
| 49 | Rumble Kick 1 | 63 | 0 | 48 |
| 50 | Rumble Kick 2 | 63 | 0 | 49 |
| 51 | Rumble Kick 3 | 63 | 0 | 50 |
| 52 | Rumble Kick 4 | 63 | 0 | 51 |
| 53 | Rumble Kick 5 | 63 | 0 | 52 |
| 54 | Punchy Kick + Reverb 1 | 63 | 0 | 53 |
| 55 | Punchy Kick + Reverb 2 | 63 | 0 | 54 |
| 56 | Punchy Kick + Reverb 3 | 63 | 0 | 55 |
| 57 | Muffled Kick 1 | 63 | 0 | 56 |
| 58 | Muffled Kick 2 | 63 | 0 | 57 |
| 59 | Muffled Kick 3 | 63 | 0 | 58 |
| 60 | Muffled Kick 4 | 63 | 0 | 59 |
| 61 | Muffled Kick 5 | 63 | 0 | 60 |
| 62 | Muffled Kick 6 | 63 | 0 | 61 |
| 63 | Lo-Fi Kick 1 | 63 | 0 | 62 |
| 64 | Lo-Fi Kick 2 | 63 | 0 | 63 |
| 65 | RX7 Kick 1 | 63 | 0 | 64 |
| 66 | RX5 Kick 1 | 63 | 0 | 65 |
| 67 | RX15 Kick 1 | 63 | 0 | 66 |
| 68 | RX7 Kick 2 | 63 | 0 | 67 |
| 69 | RX5 Kick 2 | 63 | 0 | 68 |
| 70 | RX7 Kick 3 | 63 | 0 | 69 |
| 71 | RX7 Kick 4 | 63 | 0 | 70 |
| 72 | RX7 Kick 5 | 63 | 0 | 71 |
| 73 | Acoustic Kick - Standard 1 | 63 | 0 | 72 |
| 74 | Acoustic Kick - Standard 2 | 63 | 0 | 73 |
| 75 | Acoustic Kick - Standard 3 | 63 | 0 | 74 |
| 76 | Acoustic Kick - Standard 4 | 63 | 0 | 75 |
| 77 | Acoustic Kick - Rock 1 | 63 | 0 | 76 |
| 78 | Acoustic Kick - Modern Rock 1 | 63 | 0 | 77 |
| 79 | Acoustic Kick - Jazz 1 | 63 | 0 | 78 |
| 80 | Acoustic Kick - Maple 1 | 63 | 0 | 79 |
| 81 | Modulated Kick 1 | 63 | 0 | 80 |
| 82 | Modulated Kick 2 | 63 | 0 | 81 |
| 83 | Punchy Kick + Electronic Ping 1 | 63 | 0 | 82 |
| 84 | Muffled Kick + Bell 1 | 63 | 0 | 83 |
| 85 | Punchy Kick + Perc 1 | 63 | 0 | 84 |
| 86 | Kick + Shaker 1 | 63 | 0 | 85 |
| 87 | Kick + Open Hat 1 | 63 | 0 | 86 |
| 88 | Kick + Open Hat 2 | 63 | 0 | 87 |
| 89 | Tonal Kick C | 63 | 0 | 88 |
| 90 | Tonal Kick C# | 63 | 0 | 89 |
| 91 | Tonal Kick D | 63 | 0 | 90 |
| 92 | Tonal Kick D# | 63 | 0 | 91 |
| 93 | Tonal Kick E | 63 | 0 | 92 |
| 94 | Tonal Kick F | 63 | 0 | 93 |
| 95 | Tonal Kick F# | 63 | 0 | 94 |
| 96 | Tonal Kick G | 63 | 0 | 95 |
| 97 | Tonal Kick G# | 63 | 0 | 96 |
| 98 | Tonal Kick A | 63 | 0 | 97 |
| 99 | Tonal Kick A# | 63 | 0 | 98 |
| 100 | Tonal Kick B | 63 | 0 | 99 |
| 101 | Distorted Tonal Kick C | 63 | 0 | 100 |
| 102 | Distorted Tonal Kick C# | 63 | 0 | 101 |
| 103 | Distorted Tonal Kick D | 63 | 0 | 102 |
| 104 | Distorted Tonal Kick D# | 63 | 0 | 103 |
| 105 | Distorted Tonal Kick E | 63 | 0 | 104 |
| 106 | Distorted Tonal Kick F | 63 | 0 | 105 |
| 107 | Distorted Tonal Kick F# | 63 | 0 | 106 |
| 108 | Distorted Tonal Kick G | 63 | 0 | 107 |
| 109 | Distorted Tonal Kick G# | 63 | 0 | 108 |
| 110 | Distorted Tonal Kick A | 63 | 0 | 109 |
| 111 | Distorted Tonal Kick A# | 63 | 0 | 110 |
| 112 | Distorted Tonal Kick B | 63 | 0 | 111 |

### Snare (102)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 113 | Tight Snare 1 | 63 | 0 | 112 |
| 114 | Tight Snare 2 | 63 | 0 | 113 |
| 115 | Tight Snare 3 | 63 | 0 | 114 |
| 116 | Short Pitched Snare 1 | 63 | 0 | 115 |
| 117 | Tight Snare 4 | 63 | 0 | 116 |
| 118 | Tight Snare + Reverb 1 | 63 | 0 | 117 |
| 119 | Tight Punchy Snare + Reverb 1 | 63 | 0 | 118 |
| 120 | Tight Snare 5 | 63 | 0 | 119 |
| 121 | Pitched Snare 1 | 63 | 0 | 120 |
| 122 | Tight Snare 6 | 63 | 0 | 121 |
| 123 | Tight Snare + Reverb 2 | 63 | 0 | 122 |
| 124 | Tight Snare + Reverb 3 | 63 | 0 | 123 |
| 125 | Tight Snare + Reverb 4 | 63 | 0 | 124 |
| 126 | Tight Snare + Reverb 5 | 63 | 0 | 125 |
| 127 | Tight Punchy Snare 1 | 63 | 0 | 126 |
| 128 | Punchy Fat Snare 1 | 63 | 0 | 127 |
| 129 | Distorted Pitched Snare 1 | 63 | 1 | 0 |
| 130 | Distorted Punchy Snare 1 | 63 | 1 | 1 |
| 131 | Punchy Fat Snare 2 | 63 | 1 | 2 |
| 132 | Distorted Fat Snare 1 | 63 | 1 | 3 |
| 133 | Distorted Fat Snare 2 | 63 | 1 | 4 |
| 134 | Punchy Fat Snare 3 | 63 | 1 | 5 |
| 135 | Punchy Fat Snare 4 | 63 | 1 | 6 |
| 136 | Punchy Fat Snare 5 | 63 | 1 | 7 |
| 137 | Distorted Low Snare 1 | 63 | 1 | 8 |
| 138 | Distorted Low Snare 2 | 63 | 1 | 9 |
| 139 | Punchy Long Snare 1 | 63 | 1 | 10 |
| 140 | Punchy Long Snare 2 | 63 | 1 | 11 |
| 141 | Click Wood Snare 1 | 63 | 1 | 12 |
| 142 | Double Click Snare 1 | 63 | 1 | 13 |
| 143 | Short Slow Snare 1 | 63 | 1 | 14 |
| 144 | Lo-Fi Snare 1 | 63 | 1 | 15 |
| 145 | Lo-Fi Snare 2 | 63 | 1 | 16 |
| 146 | Lo-Fi Snare 3 | 63 | 1 | 17 |
| 147 | Lo-Fi Snare 4 | 63 | 1 | 18 |
| 148 | Lo-Fi Snare 5 | 63 | 1 | 19 |
| 149 | Short Can Snare 1 | 63 | 1 | 20 |
| 150 | Muffled Snare 1 | 63 | 1 | 21 |
| 151 | Tight Snare + Reverb 6 | 63 | 1 | 22 |
| 152 | Tight Snare + Reverb 7 | 63 | 1 | 23 |
| 153 | Snare + Reverb 1 | 63 | 1 | 24 |
| 154 | Snare + Reverb 2 | 63 | 1 | 25 |
| 155 | Muffled Snare + Reverb 1 | 63 | 1 | 26 |
| 156 | Muffled Snare + Reverb 2 | 63 | 1 | 27 |
| 157 | Pitched Snare + Reverb 1 | 63 | 1 | 28 |
| 158 | Muffled Snare + Reverb 3 | 63 | 1 | 29 |
| 159 | Muffled Snare + Reverb 4 | 63 | 1 | 30 |
| 160 | Fat Snare + Reverb 1 | 63 | 1 | 31 |
| 161 | Punchy Snare + Reverb 1 | 63 | 1 | 32 |
| 162 | Distorted Snare + Reverb 1 | 63 | 1 | 33 |
| 163 | Gated Reverb Snare 1 | 63 | 1 | 34 |
| 164 | Gated Reverb Snare 2 | 63 | 1 | 35 |
| 165 | Spring Snare 1 | 63 | 1 | 36 |
| 166 | Trash Snare + Reverb 1 | 63 | 1 | 37 |
| 167 | Trash Snare + Reverb 2 | 63 | 1 | 38 |
| 168 | Trash Snare + Reverb 3 | 63 | 1 | 39 |
| 169 | Rx5 Snare 1 | 63 | 1 | 40 |
| 170 | Rx5 Snare 2 | 63 | 1 | 41 |
| 171 | RX7 Snare 1 | 63 | 1 | 42 |
| 172 | RX7 Snare 2 | 63 | 1 | 43 |
| 173 | RX7 Snare 3 | 63 | 1 | 44 |
| 174 | RX7 Snare 4 | 63 | 1 | 45 |
| 175 | RX7 Snare 5 | 63 | 1 | 46 |
| 176 | RX7 Snare 6 | 63 | 1 | 47 |
| 177 | Acoustic Snare - Standard 1 | 63 | 1 | 48 |
| 178 | Acoustic Snare - Standard 2 | 63 | 1 | 49 |
| 179 | Acoustic Snare - Soul 1 | 63 | 1 | 50 |
| 180 | Acoustic Snare - Standard 3 | 63 | 1 | 51 |
| 181 | Acoustic Snare - Standard 4 | 63 | 1 | 52 |
| 182 | Acoustic Snare - Punchy 1 | 63 | 1 | 53 |
| 183 | Acoustic Snare - Punchy 2 | 63 | 1 | 54 |
| 184 | Acoustic Snare - Metallic 1 | 63 | 1 | 55 |
| 185 | Acoustic Snare - Punchy 3 | 63 | 1 | 56 |
| 186 | Acoustic Snare - Tight 1 | 63 | 1 | 57 |
| 187 | Acoustic Snare - Tight 2 | 63 | 1 | 58 |
| 188 | Acoustic Snare + Reverb 1 | 63 | 1 | 59 |
| 189 | Acoustic Snare - Punchy 4 | 63 | 1 | 60 |
| 190 | Acoustic Snare - Punchy 5 | 63 | 1 | 61 |
| 191 | Acoustic Snare - Brush 1 | 63 | 1 | 62 |
| 192 | Acoustic Snare - Brush Tap 1 | 63 | 1 | 63 |
| 193 | Acoustic Snare - Flam 1 | 63 | 1 | 64 |
| 194 | Glitch Snare 1 | 63 | 1 | 65 |
| 195 | Glitch Snare 2 | 63 | 1 | 66 |
| 196 | Glitch Snare 3 | 63 | 1 | 67 |
| 197 | Hardcore Snare 1 | 63 | 1 | 68 |
| 198 | Hardcore Snare 2 | 63 | 1 | 69 |
| 199 | Hardcore Snare 3 | 63 | 1 | 70 |
| 200 | Hardcore Snare 4 | 63 | 1 | 71 |
| 201 | Hardcore Snare 5 | 63 | 1 | 72 |
| 202 | Snare + Wood Block 1 | 63 | 1 | 73 |
| 203 | Snare + Wood Block 2 | 63 | 1 | 74 |
| 204 | Wood Snare 1 | 63 | 1 | 75 |
| 205 | Factory Snare + Reverb 1 | 63 | 1 | 76 |
| 206 | Metallic Snare 1 | 63 | 1 | 77 |
| 207 | Metallic Snare 2 | 63 | 1 | 78 |
| 208 | Metallic Snare 3 | 63 | 1 | 79 |
| 209 | Metallic Snare 4 | 63 | 1 | 80 |
| 210 | Metallic Snare 5 | 63 | 1 | 81 |
| 211 | Glass Broken Snare 1 | 63 | 1 | 82 |
| 212 | Glass Broken Snare 2 | 63 | 1 | 83 |
| 213 | SFX Snare 1 | 63 | 1 | 84 |
| 214 | SFX Snare 2 | 63 | 1 | 85 |

### Rim (34)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 215 | Acoustic Rim - Jazz 1 | 63 | 1 | 86 |
| 216 | Acoustic Rim - Oak 1 | 63 | 1 | 87 |
| 217 | Acoustic Rim - Fat 1 | 63 | 1 | 88 |
| 218 | Acoustic Rim - Rock 1 | 63 | 1 | 89 |
| 219 | Acoustic Rim - Standard 1 | 63 | 1 | 90 |
| 220 | Acoustic Rim - High 1 | 63 | 1 | 91 |
| 221 | RX11 Rim 1 | 63 | 1 | 92 |
| 222 | RX5 Rim 1 | 63 | 1 | 93 |
| 223 | Acoustic Rim - Short 1 | 63 | 1 | 94 |
| 224 | Analog Rim 1 | 63 | 1 | 95 |
| 225 | Analog Rim 2 | 63 | 1 | 96 |
| 226 | Pitched Rim 1 | 63 | 1 | 97 |
| 227 | Lo-Fi Rim 1 | 63 | 1 | 98 |
| 228 | Lo-Fi Rim 2 | 63 | 1 | 99 |
| 229 | Lo-Fi Rim 3 | 63 | 1 | 100 |
| 230 | Stick Rim 1 | 63 | 1 | 101 |
| 231 | Acoustic Rim - Short 2 | 63 | 1 | 102 |
| 232 | High Pitched Rim 1 | 63 | 1 | 103 |
| 233 | Double Click Rim 1 | 63 | 1 | 104 |
| 234 | Acoustic Rim + Reverb 1 | 63 | 1 | 105 |
| 235 | Lo-Fi Rim + Reverb 1 | 63 | 1 | 106 |
| 236 | Acoustic Rim + Reverb 2 | 63 | 1 | 107 |
| 237 | Acoustic Rim + Reverb 3 | 63 | 1 | 108 |
| 238 | Noisy Rim 1 | 63 | 1 | 109 |
| 239 | Noisy Rim 2 | 63 | 1 | 110 |
| 240 | Noisy Rim 3 | 63 | 1 | 111 |
| 241 | Noisy Rim 4 | 63 | 1 | 112 |
| 242 | Noisy Rim 5 | 63 | 1 | 113 |
| 243 | Noisy Rim 6 | 63 | 1 | 114 |
| 244 | Noisy Rim 7 | 63 | 1 | 115 |
| 245 | Metallic Rim 1 | 63 | 1 | 116 |
| 246 | Double Click Rim 2 | 63 | 1 | 117 |
| 247 | Rim + Low 1 | 63 | 1 | 118 |
| 248 | Click Rim + Low 1 | 63 | 1 | 119 |

### Clap (48)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 249 | Hand Clap 1 | 63 | 1 | 120 |
| 250 | Hand Clap 2 | 63 | 1 | 121 |
| 251 | Hand Clap 3 | 63 | 1 | 122 |
| 252 | Hand Clap 4 | 63 | 1 | 123 |
| 253 | Group Clap 1 | 63 | 1 | 124 |
| 254 | Group Clap 2 | 63 | 1 | 125 |
| 255 | Group Clap 3 | 63 | 1 | 126 |
| 256 | Group Clap 4 | 63 | 1 | 127 |
| 257 | Hand Clap 5 | 63 | 2 | 0 |
| 258 | Bright Clap 1 | 63 | 2 | 1 |
| 259 | Bright Clap 2 | 63 | 2 | 2 |
| 260 | Lo-Fi Thin Clap 1 | 63 | 2 | 3 |
| 261 | Wide Thin Clap 1 | 63 | 2 | 4 |
| 262 | Bright Clap 3 | 63 | 2 | 5 |
| 263 | RX11 Clap 1 | 63 | 2 | 6 |
| 264 | Bitcrushed Clap 1 | 63 | 2 | 7 |
| 265 | Lo-Fi Clap 1 | 63 | 2 | 8 |
| 266 | Lo-Fi Clap + Reverb 1 | 63 | 2 | 9 |
| 267 | Slow Clap 1 | 63 | 2 | 10 |
| 268 | Short Clap 1 | 63 | 2 | 11 |
| 269 | Short Clap 2 | 63 | 2 | 12 |
| 270 | Short Double Clap 1 | 63 | 2 | 13 |
| 271 | Double Clap + Reverb 1 | 63 | 2 | 14 |
| 272 | Double Clap + Reverb 2 | 63 | 2 | 15 |
| 273 | Bright Clap 4 | 63 | 2 | 16 |
| 274 | Clicky Clap 1 | 63 | 2 | 17 |
| 275 | Long Clap + Reverb 1 | 63 | 2 | 18 |
| 276 | Long Clap + Reverb 2 | 63 | 2 | 19 |
| 277 | Hand Clap + Reverb 1 | 63 | 2 | 20 |
| 278 | Thin Clap + Reverb 1 | 63 | 2 | 21 |
| 279 | Thin Clap + Reverb 2 | 63 | 2 | 22 |
| 280 | Click Clap + Reverb 1 | 63 | 2 | 23 |
| 281 | Hand Clap + Reverb 2 | 63 | 2 | 24 |
| 282 | Hand Clap + Reverb 3 | 63 | 2 | 25 |
| 283 | Short Delay Clap 1 | 63 | 2 | 26 |
| 284 | Hand Clap + Reverb 4 | 63 | 2 | 27 |
| 285 | Hand Clap + Reverb 5 | 63 | 2 | 28 |
| 286 | Noise Clap 1 | 63 | 2 | 29 |
| 287 | Noise Clap 2 | 63 | 2 | 30 |
| 288 | Glitch Clap 1 | 63 | 2 | 31 |
| 289 | Glitch Clap 2 | 63 | 2 | 32 |
| 290 | Glitch Clap 3 | 63 | 2 | 33 |
| 291 | Glitch Clap 4 | 63 | 2 | 34 |
| 292 | Glitch Clap 5 | 63 | 2 | 35 |
| 293 | Modulated Hand Clap 1 | 63 | 2 | 36 |
| 294 | Woody Clap 1 | 63 | 2 | 37 |
| 295 | Arabic Hand Clap 1 | 63 | 2 | 38 |
| 296 | Woody Clap + Reverb 1 | 63 | 2 | 39 |

### Snap (15)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 297 | Finger Snap 1 | 63 | 2 | 40 |
| 298 | Finger Snap 2 | 63 | 2 | 41 |
| 299 | Finger Snap 3 | 63 | 2 | 42 |
| 300 | Finger Snap 4 | 63 | 2 | 43 |
| 301 | Finger Snap 5 | 63 | 2 | 44 |
| 302 | Finger Snap 6 | 63 | 2 | 45 |
| 303 | Wide Snap 1 | 63 | 2 | 46 |
| 304 | Wide Snap 2 | 63 | 2 | 47 |
| 305 | Fat Snap 1 | 63 | 2 | 48 |
| 306 | Fat Snap 2 | 63 | 2 | 49 |
| 307 | Woody Snap 1 | 63 | 2 | 50 |
| 308 | Snap + Reverb 1 | 63 | 2 | 51 |
| 309 | Snap + Reverb 2 | 63 | 2 | 52 |
| 310 | Click Snap 1 | 63 | 2 | 53 |
| 311 | Click Snap 2 | 63 | 2 | 54 |

### Closed HiHat (73)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 312 | Tight Closed Hat 1 | 63 | 2 | 55 |
| 313 | Tight Closed Hat 2 | 63 | 2 | 56 |
| 314 | Tight Closed Hat 3 | 63 | 2 | 57 |
| 315 | Tight Closed Hat 4 | 63 | 2 | 58 |
| 316 | Tight Closed Hat 5 | 63 | 2 | 59 |
| 317 | Tight Closed Hat 6 | 63 | 2 | 60 |
| 318 | Tight Closed Hat 7 | 63 | 2 | 61 |
| 319 | Tight Closed Hat 8 | 63 | 2 | 62 |
| 320 | Tight Closed Hat 9 | 63 | 2 | 63 |
| 321 | Tight Closed Hat 10 | 63 | 2 | 64 |
| 322 | Tight Closed Hat 11 | 63 | 2 | 65 |
| 323 | Tight Closed Hat 12 | 63 | 2 | 66 |
| 324 | Closed Hat 1 | 63 | 2 | 67 |
| 325 | Closed Hat 2 | 63 | 2 | 68 |
| 326 | Closed Hat 3 | 63 | 2 | 69 |
| 327 | Closed Hat 4 | 63 | 2 | 70 |
| 328 | Closed Hat 5 | 63 | 2 | 71 |
| 329 | Closed Hat 6 | 63 | 2 | 72 |
| 330 | Acoustic Closed Hat 1 | 63 | 2 | 73 |
| 331 | Closed Hat 7 | 63 | 2 | 74 |
| 332 | Closed Hat 8 | 63 | 2 | 75 |
| 333 | Closed Hat 9 | 63 | 2 | 76 |
| 334 | Acoustic Closed Hat 2 | 63 | 2 | 77 |
| 335 | Closed Hat 10 | 63 | 2 | 78 |
| 336 | Noise Closed Hat 1 | 63 | 2 | 79 |
| 337 | Noise Closed Hat 2 | 63 | 2 | 80 |
| 338 | Noise Closed Hat + Low 1 | 63 | 2 | 81 |
| 339 | Low Closed Hat 1 | 63 | 2 | 82 |
| 340 | Closed Hat + High Tone 1 | 63 | 2 | 83 |
| 341 | Acoustic Closed Hat 3 | 63 | 2 | 84 |
| 342 | Acoustic Closed Hat 4 | 63 | 2 | 85 |
| 343 | Acoustic Closed Hat 5 | 63 | 2 | 86 |
| 344 | Acoustic Closed Hat 6 | 63 | 2 | 87 |
| 345 | Acoustic Closed Hat 7 | 63 | 2 | 88 |
| 346 | Acoustic Closed Hat 8 | 63 | 2 | 89 |
| 347 | Acoustic Closed Hat 9 | 63 | 2 | 90 |
| 348 | Acoustic Closed Hat 10 | 63 | 2 | 91 |
| 349 | Acoustic Hat Pedal 1 | 63 | 2 | 92 |
| 350 | Acoustic Hat Pedal 2 | 63 | 2 | 93 |
| 351 | Acoustic Hat Pedal 3 | 63 | 2 | 94 |
| 352 | Acoustic Hat Pedal 4 | 63 | 2 | 95 |
| 353 | Acoustic Hat Pedal 5 | 63 | 2 | 96 |
| 354 | Acoustic Hat Pedal 6 | 63 | 2 | 97 |
| 355 | Click Closed Hat 1 | 63 | 2 | 98 |
| 356 | Lo-Fi Short Closed Hat 1 | 63 | 2 | 99 |
| 357 | Click Closed Hat 2 | 63 | 2 | 100 |
| 358 | Lo-Fi Short Closed Hat 2 | 63 | 2 | 101 |
| 359 | Lo-Fi Short Closed Hat 3 | 63 | 2 | 102 |
| 360 | Lo-Fi Short Closed Hat 4 | 63 | 2 | 103 |
| 361 | Lo-Fi Short Closed Hat 5 | 63 | 2 | 104 |
| 362 | Lo-Fi Short Closed Hat 6 | 63 | 2 | 105 |
| 363 | Lo-Fi Short Closed Hat 7 | 63 | 2 | 106 |
| 364 | Lo-Fi Short Closed Hat 8 | 63 | 2 | 107 |
| 365 | Lo-Fi Short Closed Hat 9 | 63 | 2 | 108 |
| 366 | Bitcrushed Hat 1 | 63 | 2 | 109 |
| 367 | Lo-Fi Closed Hat 1 | 63 | 2 | 110 |
| 368 | Lo-Fi Closed Hat 2 | 63 | 2 | 111 |
| 369 | Lo-Fi Closed Hat 3 | 63 | 2 | 112 |
| 370 | Lo-Fi Closed Hat 4 | 63 | 2 | 113 |
| 371 | Lo-Fi Closed Hat 5 | 63 | 2 | 114 |
| 372 | Lo-Fi Closed Hat 6 | 63 | 2 | 115 |
| 373 | Lo-Fi Closed Hat 7 | 63 | 2 | 116 |
| 374 | Lo-Fi Closed Hat 8 | 63 | 2 | 117 |
| 375 | Lo-Fi Closed Hat 9 | 63 | 2 | 118 |
| 376 | Closed Hat + Reverb 1 | 63 | 2 | 119 |
| 377 | Lo-Fi Closed Hat + Reverb 1 | 63 | 2 | 120 |
| 378 | Closed Hat + Reverb 2 | 63 | 2 | 121 |
| 379 | Closed Hat + Reverb 3 | 63 | 2 | 122 |
| 380 | Closed Hat + Reverb 4 | 63 | 2 | 123 |
| 381 | Closed Hat + Reverb 5 | 63 | 2 | 124 |
| 382 | Glitch Hat 1 | 63 | 2 | 125 |
| 383 | Glitch Hat 2 | 63 | 2 | 126 |
| 384 | Glitch Hat 3 | 63 | 2 | 127 |

### Open HiHat (72)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 385 | Bright Open Hat 1 | 63 | 3 | 0 |
| 386 | Bright Open Hat 2 | 63 | 3 | 1 |
| 387 | Bright Open Hat 3 | 63 | 3 | 2 |
| 388 | Bright Open Hat 4 | 63 | 3 | 3 |
| 389 | Bright Open Hat 5 | 63 | 3 | 4 |
| 390 | Noise Open Hat 1 | 63 | 3 | 5 |
| 391 | Noise Open Hat 2 | 63 | 3 | 6 |
| 392 | Noise Open Hat 3 | 63 | 3 | 7 |
| 393 | Noise Open Hat 4 | 63 | 3 | 8 |
| 394 | Noise Open Hat 5 | 63 | 3 | 9 |
| 395 | Noise Open Hat 6 | 63 | 3 | 10 |
| 396 | Noise Open Hat 7 | 63 | 3 | 11 |
| 397 | Noise Open Hat 8 | 63 | 3 | 12 |
| 398 | Noise Open Hat 9 | 63 | 3 | 13 |
| 399 | Noise Open Hat 10 | 63 | 3 | 14 |
| 400 | Noise Open Hat 11 | 63 | 3 | 15 |
| 401 | Noise Open Hat 12 | 63 | 3 | 16 |
| 402 | Noise Open Hat 13 | 63 | 3 | 17 |
| 403 | Noise Open Hat 14 | 63 | 3 | 18 |
| 404 | Noise Open Hat 15 | 63 | 3 | 19 |
| 405 | Bright Open Hat 6 | 63 | 3 | 20 |
| 406 | Acoustic Open Hat 1 | 63 | 3 | 21 |
| 407 | Acoustic Open Hat 2 | 63 | 3 | 22 |
| 408 | Acoustic Open Hat 3 | 63 | 3 | 23 |
| 409 | Acoustic Open Hat 4 | 63 | 3 | 24 |
| 410 | Acoustic Open Hat 5 | 63 | 3 | 25 |
| 411 | Acoustic Open Hat 6 | 63 | 3 | 26 |
| 412 | Acoustic Open Hat 7 | 63 | 3 | 27 |
| 413 | Crash Open Hat 1 | 63 | 3 | 28 |
| 414 | Crash Open Hat 2 | 63 | 3 | 29 |
| 415 | Crash Open Hat 3 | 63 | 3 | 30 |
| 416 | Bitcrushed Open Hat 1 | 63 | 3 | 31 |
| 417 | Bitcrushed Open Hat 2 | 63 | 3 | 32 |
| 418 | Bitcrushed Open Hat 3 | 63 | 3 | 33 |
| 419 | Bitcrushed Open Hat 4 | 63 | 3 | 34 |
| 420 | Distorted Open Hat 1 | 63 | 3 | 35 |
| 421 | Distorted Open Hat 2 | 63 | 3 | 36 |
| 422 | Distorted Open Hat 3 | 63 | 3 | 37 |
| 423 | Distorted Open Hat 4 | 63 | 3 | 38 |
| 424 | Distorted Open Hat 5 | 63 | 3 | 39 |
| 425 | Lo-Fi Open Hat 1 | 63 | 3 | 40 |
| 426 | Lo-Fi Open Hat 2 | 63 | 3 | 41 |
| 427 | Lo-Fi Open Hat 3 | 63 | 3 | 42 |
| 428 | Lo-Fi Open Hat 4 | 63 | 3 | 43 |
| 429 | Lo-Fi Open Hat 5 | 63 | 3 | 44 |
| 430 | Gated Open Hat 1 | 63 | 3 | 45 |
| 431 | Gated Open Hat 2 | 63 | 3 | 46 |
| 432 | Gated Open Hat 3 | 63 | 3 | 47 |
| 433 | Gated Open Hat 4 | 63 | 3 | 48 |
| 434 | Gated Open Hat 5 | 63 | 3 | 49 |
| 435 | Slow Attack Open Hat 1 | 63 | 3 | 50 |
| 436 | Slow Attack Open Hat 2 | 63 | 3 | 51 |
| 437 | Slow Attack Open Hat 3 | 63 | 3 | 52 |
| 438 | Slow Attack Open Hat 4 | 63 | 3 | 53 |
| 439 | Slow Attack Open Hat 5 | 63 | 3 | 54 |
| 440 | Slow Attack Open Hat 6 | 63 | 3 | 55 |
| 441 | Slow Attack Open Hat 7 | 63 | 3 | 56 |
| 442 | Open Hat with Bell 1 | 63 | 3 | 57 |
| 443 | Open Hat with Bell 2 | 63 | 3 | 58 |
| 444 | Open Hat with Bell 3 | 63 | 3 | 59 |
| 445 | Bell Open Hat 1 | 63 | 3 | 60 |
| 446 | Splash Open Hat 1 | 63 | 3 | 61 |
| 447 | Open Hat + Delay 1 | 63 | 3 | 62 |
| 448 | Open Hat + Reverb 1 | 63 | 3 | 63 |
| 449 | Open Hat + Reverb 2 | 63 | 3 | 64 |
| 450 | Panning Open Hat 1 | 63 | 3 | 65 |
| 451 | Panning Distorted Open Hat 1 | 63 | 3 | 66 |
| 452 | Modulated Open Hat 1 | 63 | 3 | 67 |
| 453 | Modulated Open Hat 2 | 63 | 3 | 68 |
| 454 | Modulated Open Hat 3 | 63 | 3 | 69 |
| 455 | Reversed Floor Hat 1 | 63 | 3 | 70 |
| 456 | Reversed Hat 1 | 63 | 3 | 71 |

### Shaker / Tambourine (41)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 457 | Shaker 1 | 63 | 3 | 72 |
| 458 | Shaker 2 | 63 | 3 | 73 |
| 459 | Shaker 3 | 63 | 3 | 74 |
| 460 | Shaker 4 | 63 | 3 | 75 |
| 461 | Shaker 5 | 63 | 3 | 76 |
| 462 | Shaker 6 | 63 | 3 | 77 |
| 463 | Shaker 7 | 63 | 3 | 78 |
| 464 | Shaker 8 | 63 | 3 | 79 |
| 465 | Shaker 9 | 63 | 3 | 80 |
| 466 | Shaker 10 | 63 | 3 | 81 |
| 467 | Shaker 11 | 63 | 3 | 82 |
| 468 | Short Shaker Accent 1 | 63 | 3 | 83 |
| 469 | Short Shaker Accent 2 | 63 | 3 | 84 |
| 470 | Short Shaker Accent 3 | 63 | 3 | 85 |
| 471 | Shaker + Reverb 1 | 63 | 3 | 86 |
| 472 | Shaker + Reverb 2 | 63 | 3 | 87 |
| 473 | Short Shaker Accent 4 | 63 | 3 | 88 |
| 474 | Shaker 12 | 63 | 3 | 89 |
| 475 | Shaker 13 | 63 | 3 | 90 |
| 476 | Shaker 14 | 63 | 3 | 91 |
| 477 | Shaker 15 | 63 | 3 | 92 |
| 478 | Arabic Maracas 1 | 63 | 3 | 93 |
| 479 | Caxixi 1 | 63 | 3 | 94 |
| 480 | Afoxe Open 1 | 63 | 3 | 95 |
| 481 | Muffled Shaker 1 | 63 | 3 | 96 |
| 482 | Tambourine 1 | 63 | 3 | 97 |
| 483 | Tambourine 2 | 63 | 3 | 98 |
| 484 | Tambourine 3 | 63 | 3 | 99 |
| 485 | Tambourine 4 | 63 | 3 | 100 |
| 486 | Tambourine 5 | 63 | 3 | 101 |
| 487 | Tambourine 6 | 63 | 3 | 102 |
| 488 | Tambourine 7 | 63 | 3 | 103 |
| 489 | Short Tambourine 1 | 63 | 3 | 104 |
| 490 | Tambourine 8 | 63 | 3 | 105 |
| 491 | RX5 Tambourine 1 | 63 | 3 | 106 |
| 492 | Long Tambourine 1 | 63 | 3 | 107 |
| 493 | Long Tambourine 2 | 63 | 3 | 108 |
| 494 | Long Tambourine 3 | 63 | 3 | 109 |
| 495 | Long Tambourine 4 | 63 | 3 | 110 |
| 496 | Long Tambourine 5 | 63 | 3 | 111 |
| 497 | Tambourine + Reverb 1 | 63 | 3 | 112 |

### Ride (30)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 498 | Sharp Ride 1 | 63 | 3 | 113 |
| 499 | Sharp Ride 2 | 63 | 3 | 114 |
| 500 | Noise Ride 1 | 63 | 3 | 115 |
| 501 | Sharp Ride 3 | 63 | 3 | 116 |
| 502 | Acoustic Ride 1 | 63 | 3 | 117 |
| 503 | Acoustic Ride - Brush 1 | 63 | 3 | 118 |
| 504 | Acoustic Ride 2 | 63 | 3 | 119 |
| 505 | Acoustic Ride 3 | 63 | 3 | 120 |
| 506 | RX7 Ride 1 | 63 | 3 | 121 |
| 507 | Ride Cup 1 | 63 | 3 | 122 |
| 508 | Ride Cup 2 | 63 | 3 | 123 |
| 509 | RX5 Ride Cup 1 | 63 | 3 | 124 |
| 510 | Color Ride 1 | 63 | 3 | 125 |
| 511 | Color Ride 2 | 63 | 3 | 126 |
| 512 | Color Ride 3 | 63 | 3 | 127 |
| 513 | Color Ride 4 | 63 | 4 | 0 |
| 514 | Color Ride 5 | 63 | 4 | 1 |
| 515 | Gate Ride 1 | 63 | 4 | 2 |
| 516 | Crash Ride 1 | 63 | 4 | 3 |
| 517 | Crash Ride 2 | 63 | 4 | 4 |
| 518 | Crash Ride 3 | 63 | 4 | 5 |
| 519 | Noise Ride 2 | 63 | 4 | 6 |
| 520 | Noise Long Ride 1 | 63 | 4 | 7 |
| 521 | High Noise Ride 1 | 63 | 4 | 8 |
| 522 | Synth Ride 1 | 63 | 4 | 9 |
| 523 | Synth Long Ride 1 | 63 | 4 | 10 |
| 524 | Dark Ride 1 | 63 | 4 | 11 |
| 525 | Slow Ride 1 | 63 | 4 | 12 |
| 526 | Noise Ride 3 | 63 | 4 | 13 |
| 527 | Bitcrushed Ride 1 | 63 | 4 | 14 |

### Crash (21)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 528 | RX5 Crash 1 | 63 | 4 | 15 |
| 529 | Acoustic Crash 1 | 63 | 4 | 16 |
| 530 | Acoustic Crash 2 | 63 | 4 | 17 |
| 531 | Acoustic Crash + Reverb 1 | 63 | 4 | 18 |
| 532 | Acoustic Crash 3 | 63 | 4 | 19 |
| 533 | Slow Acoustic Crash 1 | 63 | 4 | 20 |
| 534 | Acoustic Crash 4 | 63 | 4 | 21 |
| 535 | Acoustic Crash 5 | 63 | 4 | 22 |
| 536 | Splash Cymbal 1 | 63 | 4 | 23 |
| 537 | Splash Cymbal 2 | 63 | 4 | 24 |
| 538 | Splash Cymbal + Reverb 1 | 63 | 4 | 25 |
| 539 | Big Cymbal 1 | 63 | 4 | 26 |
| 540 | Big Cymbal 2 | 63 | 4 | 27 |
| 541 | Big Cymbal 3 | 63 | 4 | 28 |
| 542 | Cymbal Hammer 1 | 63 | 4 | 29 |
| 543 | China Cymbal 1 | 63 | 4 | 30 |
| 544 | 4th Delay Crash 1 | 63 | 4 | 31 |
| 545 | Long Crash + Reverb 1 | 63 | 4 | 32 |
| 546 | Noise Crash 1 | 63 | 4 | 33 |
| 547 | Noise Crash 2 | 63 | 4 | 34 |
| 548 | Noise Crash 3 | 63 | 4 | 35 |

### Tom (70)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 549 | Acoustic High Tom 1 | 63 | 4 | 36 |
| 550 | Acoustic High Tom 2 | 63 | 4 | 37 |
| 551 | Acoustic Mid Tom 1 | 63 | 4 | 38 |
| 552 | Acoustic Mid Tom 2 | 63 | 4 | 39 |
| 553 | Acoustic Mid Tom 3 | 63 | 4 | 40 |
| 554 | Acoustic Mid Tom 4 | 63 | 4 | 41 |
| 555 | Acoustic Low Tom 1 | 63 | 4 | 42 |
| 556 | Acoustic Low Tom 2 | 63 | 4 | 43 |
| 557 | Punchy High Tom 1 | 63 | 4 | 44 |
| 558 | Punchy High Tom 2 | 63 | 4 | 45 |
| 559 | Punchy High Tom 3 | 63 | 4 | 46 |
| 560 | Punchy Mid Tom 1 | 63 | 4 | 47 |
| 561 | Punchy Mid Tom 2 | 63 | 4 | 48 |
| 562 | Punchy Mid Tom 3 | 63 | 4 | 49 |
| 563 | Punchy Mid Tom 4 | 63 | 4 | 50 |
| 564 | Punchy Mid Tom 5 | 63 | 4 | 51 |
| 565 | Punchy Mid Tom 6 | 63 | 4 | 52 |
| 566 | Punchy Low Tom 1 | 63 | 4 | 53 |
| 567 | Punchy Low Tom 2 | 63 | 4 | 54 |
| 568 | Punchy Low Tom 3 | 63 | 4 | 55 |
| 569 | Electronic High Tom 1 | 63 | 4 | 56 |
| 570 | Electronic High Tom 2 | 63 | 4 | 57 |
| 571 | Electronic High Tom 3 | 63 | 4 | 58 |
| 572 | Electronic High Tom 4 | 63 | 4 | 59 |
| 573 | Electronic High Tom 5 | 63 | 4 | 60 |
| 574 | Electronic Mid Tom 1 | 63 | 4 | 61 |
| 575 | Electronic Mid Tom 2 | 63 | 4 | 62 |
| 576 | Electronic Low Tom 1 | 63 | 4 | 63 |
| 577 | Electronic Low Tom 2 | 63 | 4 | 64 |
| 578 | RX5 High Tom 1 | 63 | 4 | 65 |
| 579 | RX5 Mid Tom 1 | 63 | 4 | 66 |
| 580 | RX5 Mid Tom 2 | 63 | 4 | 67 |
| 581 | RX5 Low Tom 1 | 63 | 4 | 68 |
| 582 | Acoustic High Tom - Oak 1 | 63 | 4 | 69 |
| 583 | Acoustic Mid Tom - Oak 1 | 63 | 4 | 70 |
| 584 | Acoustic Low Tom - Oak 1 | 63 | 4 | 71 |
| 585 | Acoustic High Tom - Jazz 1 | 63 | 4 | 72 |
| 586 | Acoustic Mid Tom - Jazz 1 | 63 | 4 | 73 |
| 587 | Acoustic Low Tom - Jazz 1 | 63 | 4 | 74 |
| 588 | Acoustic High Tom - Rock 1 | 63 | 4 | 75 |
| 589 | Acoustic Mid Tom - Rock 1 | 63 | 4 | 76 |
| 590 | Acoustic Low Tom - Rock 1 | 63 | 4 | 77 |
| 591 | Acoustic High Tom - Maple 1 | 63 | 4 | 78 |
| 592 | Acoustic Mid Tom - Maple 1 | 63 | 4 | 79 |
| 593 | Acoustic Low Tom - Maple 1 | 63 | 4 | 80 |
| 594 | Electronic High Tom + Reverb 1 | 63 | 4 | 81 |
| 595 | Muffled Mid Tom + Reverb 1 | 63 | 4 | 82 |
| 596 | Acoustic Mid Tom + Reverb 1 | 63 | 4 | 83 |
| 597 | Modulated Tom 1 | 63 | 4 | 84 |
| 598 | Modulated Tom 2 | 63 | 4 | 85 |
| 599 | Modulated Tom 3 | 63 | 4 | 86 |
| 600 | RX5 High Tom 2 | 63 | 4 | 87 |
| 601 | RX5 Mid Tom 3 | 63 | 4 | 88 |
| 602 | RX5 Mid Tom 4 | 63 | 4 | 89 |
| 603 | RX5 Low Tom 2 | 63 | 4 | 90 |
| 604 | Distorted Tom 1 | 63 | 4 | 91 |
| 605 | Distorted Tom 2 | 63 | 4 | 92 |
| 606 | Distorted Tom 3 | 63 | 4 | 93 |
| 607 | Distorted Tom 4 | 63 | 4 | 94 |
| 608 | Distorted Tom 5 | 63 | 4 | 95 |
| 609 | Distorted Tom 6 | 63 | 4 | 96 |
| 610 | Distorted Tom 7 | 63 | 4 | 97 |
| 611 | Bitcrushed Tom 1 | 63 | 4 | 98 |
| 612 | Bitcrushed Tom 2 | 63 | 4 | 99 |
| 613 | Bass Tom 1 | 63 | 4 | 100 |
| 614 | Bass Tom 2 | 63 | 4 | 101 |
| 615 | Tonal Bass Tom 1 | 63 | 4 | 102 |
| 616 | Bass Tom 3 | 63 | 4 | 103 |
| 617 | Bass Tom 4 | 63 | 4 | 104 |
| 618 | Bass Tom 5 | 63 | 4 | 105 |

### Bell (32)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 619 | Analog Cowbell 1 | 63 | 4 | 106 |
| 620 | Analog Cowbell Accent 1 | 63 | 4 | 107 |
| 621 | Tonal Cowbell 1 | 63 | 4 | 108 |
| 622 | Tonal Cowbell 2 | 63 | 4 | 109 |
| 623 | Metallic Cowbell 1 | 63 | 4 | 110 |
| 624 | Metallic Cowbell 2 | 63 | 4 | 111 |
| 625 | Metallic Cowbell 3 | 63 | 4 | 112 |
| 626 | Cowbell High 1 | 63 | 4 | 113 |
| 627 | Cowbell 1 | 63 | 4 | 114 |
| 628 | Cowbell Mid 1 | 63 | 4 | 115 |
| 629 | Cowbell Mid 2 | 63 | 4 | 116 |
| 630 | Agogo High 1 | 63 | 4 | 117 |
| 631 | Agogo Low 1 | 63 | 4 | 118 |
| 632 | Small Bell 1 | 63 | 4 | 119 |
| 633 | Short Bell 1 | 63 | 4 | 120 |
| 634 | Short Bell 2 | 63 | 4 | 121 |
| 635 | Tingsha Bell 1 | 63 | 4 | 122 |
| 636 | Ringing Bell 1 | 63 | 4 | 123 |
| 637 | Muted Finger Cymbal 1 | 63 | 4 | 124 |
| 638 | Muted Finger Cymbal 2 | 63 | 4 | 125 |
| 639 | Sagat1 Open 1 | 63 | 4 | 126 |
| 640 | Sagat1 Close 1 | 63 | 4 | 127 |
| 641 | Sagat2 Open 1 | 63 | 5 | 0 |
| 642 | Sagat2 Close 1 | 63 | 5 | 1 |
| 643 | Sagat3 Open 1 | 63 | 5 | 2 |
| 644 | Sagat3 Close 1 | 63 | 5 | 3 |
| 645 | Atarigane 1 | 63 | 5 | 4 |
| 646 | High Bell 1 | 63 | 5 | 5 |
| 647 | Mind Bell 1 | 63 | 5 | 6 |
| 648 | Sci-Fi Bell 1 | 63 | 5 | 7 |
| 649 | Bell and Noise 1 | 63 | 5 | 8 |
| 650 | Modulated Bell 1 | 63 | 5 | 9 |

### Conga / Bongo (26)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 651 | RX5 Conga High Open 1 | 63 | 5 | 10 |
| 652 | RX5 Conga High Mute 1 | 63 | 5 | 11 |
| 653 | RX5 Conga Low Open 1 | 63 | 5 | 12 |
| 654 | Conga1 High Slap 1 | 63 | 5 | 13 |
| 655 | Conga1 High Slap Open 1 | 63 | 5 | 14 |
| 656 | Conga1 High Open 1 | 63 | 5 | 15 |
| 657 | Conga1 Low Open 1 | 63 | 5 | 16 |
| 658 | Conga2 High 1 | 63 | 5 | 17 |
| 659 | Conga2 Mid 1 | 63 | 5 | 18 |
| 660 | Conga2 Mid Mute 1 | 63 | 5 | 19 |
| 661 | Conga3 High Mute 1 | 63 | 5 | 20 |
| 662 | Conga3 Mid Slap Open 1 | 63 | 5 | 21 |
| 663 | Khalg Conga Low | 63 | 5 | 22 |
| 664 | Analog Conga High 1 | 63 | 5 | 23 |
| 665 | Analog Conga Mid 1 | 63 | 5 | 24 |
| 666 | Analog Conga Low 1 | 63 | 5 | 25 |
| 667 | RX5 Bongo High 1 | 63 | 5 | 26 |
| 668 | RX5 Bongo Low 1 | 63 | 5 | 27 |
| 669 | Bongo1 High Open 1 | 63 | 5 | 28 |
| 670 | Bongo1 Low Open 1 | 63 | 5 | 29 |
| 671 | Bongo2 High 1 | 63 | 5 | 30 |
| 672 | Bongo3 High 1 | 63 | 5 | 31 |
| 673 | Bongo3 High 2 | 63 | 5 | 32 |
| 674 | Bongo4 High 1 | 63 | 5 | 33 |
| 675 | Bongo4 Low 1 | 63 | 5 | 34 |
| 676 | Bongo4 Low 2 | 63 | 5 | 35 |

### World (111)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 677 | Djembe 1 | 63 | 5 | 36 |
| 678 | Djembe 2 | 63 | 5 | 37 |
| 679 | Djembe 3 | 63 | 5 | 38 |
| 680 | Djembe 4 | 63 | 5 | 39 |
| 681 | Talking Drum 1 | 63 | 5 | 40 |
| 682 | Talking Drum 2 | 63 | 5 | 41 |
| 683 | Talking Drum 3 | 63 | 5 | 42 |
| 684 | Talking Drum 4 | 63 | 5 | 43 |
| 685 | Tamborim Up 1 | 63 | 5 | 44 |
| 686 | Tamborim Down 1 | 63 | 5 | 45 |
| 687 | Tamborim Finger Back 1 | 63 | 5 | 46 |
| 688 | Tamborim Open 1 | 63 | 5 | 47 |
| 689 | Pandeiro Open 1 | 63 | 5 | 48 |
| 690 | Pandeiro Close 1 | 63 | 5 | 49 |
| 691 | Reco-reco 1 | 63 | 5 | 50 |
| 692 | Surdo Mute 1 | 63 | 5 | 51 |
| 693 | Surdo Stop 1 | 63 | 5 | 52 |
| 694 | Surdo Open 1 | 63 | 5 | 53 |
| 695 | Surdo Mute 2 | 63 | 5 | 54 |
| 696 | Surdo Stick 1 | 63 | 5 | 55 |
| 697 | Caixa Rim 1 | 63 | 5 | 56 |
| 698 | Vibraslap 1 | 63 | 5 | 57 |
| 699 | Darbuka Dum 1 | 63 | 5 | 58 |
| 700 | Darbuka Dom & Tak 1 | 63 | 5 | 59 |
| 701 | Darbuka Tak Finger 1 | 63 | 5 | 60 |
| 702 | Darbuka Tak Close 1 | 63 | 5 | 61 |
| 703 | Darbuka Slap 1 | 63 | 5 | 62 |
| 704 | Darbuka Sak 1 | 63 | 5 | 63 |
| 705 | Darbuka Rak 1 | 63 | 5 | 64 |
| 706 | Darbuka Flam 1 | 63 | 5 | 65 |
| 707 | Darbuka Noise 1 | 63 | 5 | 66 |
| 708 | Tunisian Bendir Dom 1 | 63 | 5 | 67 |
| 709 | Tunisian Bendir Tak 1 | 63 | 5 | 68 |
| 710 | Tunisian Bendir Tak 2 | 63 | 5 | 69 |
| 711 | Moroccan Bendir Dom 1 | 63 | 5 | 70 |
| 712 | Moroccan Bendir Dom 2 | 63 | 5 | 71 |
| 713 | Moroccan Bendir Dom 3 | 63 | 5 | 72 |
| 714 | Moroccan Bendir Edge 1 | 63 | 5 | 73 |
| 715 | Moroccan Tamtam 1 | 63 | 5 | 74 |
| 716 | Algerian Bendir Deza 1 | 63 | 5 | 75 |
| 717 | Algerian Bendir Kaf 1 | 63 | 5 | 76 |
| 718 | Algerian Galal Daza 1 | 63 | 5 | 77 |
| 719 | Riq Dum Open 1 | 63 | 5 | 78 |
| 720 | Riq Tek Open 1 | 63 | 5 | 79 |
| 721 | Riq Teke Open 1 | 63 | 5 | 80 |
| 722 | Riq Sak 1 | 63 | 5 | 81 |
| 723 | Riq Snouj Close 1 | 63 | 5 | 82 |
| 724 | Hollo Finger 1 | 63 | 5 | 83 |
| 725 | Bass Darbuka Dum 1 | 63 | 5 | 84 |
| 726 | Bass Darbuka Tek 1 | 63 | 5 | 85 |
| 727 | Bendir Tek 1 | 63 | 5 | 86 |
| 728 | Bendir Slap 1 | 63 | 5 | 87 |
| 729 | Bendir Large 1 | 63 | 5 | 88 |
| 730 | Merjaf Group Dom 1 | 63 | 5 | 89 |
| 731 | Merjaf Group Sak 1 | 63 | 5 | 90 |
| 732 | Zeer Dom 1 | 63 | 5 | 91 |
| 733 | Zeer Tak 1 | 63 | 5 | 92 |
| 734 | Merwas Group Dom 1 | 63 | 5 | 93 |
| 735 | Merwas Group Tak 1 | 63 | 5 | 94 |
| 736 | Medando Dom 1 | 63 | 5 | 95 |
| 737 | Medando Sak 1 | 63 | 5 | 96 |
| 738 | Sigal Marad Dom 1 | 63 | 5 | 97 |
| 739 | Sigal Marad Tak 1 | 63 | 5 | 98 |
| 740 | Doholla Dom 1 | 63 | 5 | 99 |
| 741 | Doholla Sak 1 | 63 | 5 | 100 |
| 742 | Katem Med Dom Open 1 | 63 | 5 | 101 |
| 743 | Katem Med Tak 1 | 63 | 5 | 102 |
| 744 | Katem Med Sak 1 | 63 | 5 | 103 |
| 745 | Taar Barashim Dom 1 | 63 | 5 | 104 |
| 746 | Taar Barashim Shake 1 | 63 | 5 | 105 |
| 747 | Req Sak 1 | 63 | 5 | 106 |
| 748 | Req Dom 1 | 63 | 5 | 107 |
| 749 | Req Open 1 | 63 | 5 | 108 |
| 750 | Req Sajat 1 | 63 | 5 | 109 |
| 751 | Udho Back 1 | 63 | 5 | 110 |
| 752 | Udho Chap Body 1 | 63 | 5 | 111 |
| 753 | Jahla Group Dom 1 | 63 | 5 | 112 |
| 754 | Iranian Bendir Tom 1 | 63 | 5 | 113 |
| 755 | Iranian Bendir Chap 1 | 63 | 5 | 114 |
| 756 | Iranian Bendir Back 1 | 63 | 5 | 115 |
| 757 | Tombak Tom 1 | 63 | 5 | 116 |
| 758 | Tombak Slap 1 | 63 | 5 | 117 |
| 759 | Tombak Chap 1 | 63 | 5 | 118 |
| 760 | Tombak Flam & Back 1 | 63 | 5 | 119 |
| 761 | Tempo Chap 1 | 63 | 5 | 120 |
| 762 | Tabla Dom 1 | 63 | 5 | 121 |
| 763 | Tabla Tak 1 | 63 | 5 | 122 |
| 764 | Tabla Sak 1 | 63 | 5 | 123 |
| 765 | Tabla 1 | 63 | 5 | 124 |
| 766 | Tabla 2 | 63 | 5 | 125 |
| 767 | Tabla 3 | 63 | 5 | 126 |
| 768 | Tabla 4 | 63 | 5 | 127 |
| 769 | Tabla 5 | 63 | 6 | 0 |
| 770 | Mridangam 1 | 63 | 6 | 1 |
| 771 | Mridangam 2 | 63 | 6 | 2 |
| 772 | Japanese Wa Taiko 1 | 63 | 6 | 3 |
| 773 | Japanese Oo Taiko 1 | 63 | 6 | 4 |
| 774 | Japanese Yagura Taiko 1 | 63 | 6 | 5 |
| 775 | Japanese Shime Taiko 1 | 63 | 6 | 6 |
| 776 | Japanese Tsuzumi 1 | 63 | 6 | 7 |
| 777 | Timbale 1 | 63 | 6 | 8 |
| 778 | Timbale 2 | 63 | 6 | 9 |
| 779 | Cajon 1 | 63 | 6 | 10 |
| 780 | Cajon 2 | 63 | 6 | 11 |
| 781 | Claves 1 | 63 | 6 | 12 |
| 782 | Wood Block 1 | 63 | 6 | 13 |
| 783 | Bones 1 | 63 | 6 | 14 |
| 784 | Bones 2 | 63 | 6 | 15 |
| 785 | Bones 3 | 63 | 6 | 16 |
| 786 | Bones Triplet 1 | 63 | 6 | 17 |
| 787 | Spoons 1 | 63 | 6 | 18 |

### SFX (68)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 788 | Laser - Falling 1 | 63 | 6 | 19 |
| 789 | Sci-Fi - Detected 1 | 63 | 6 | 20 |
| 790 | Sci-Fi - Drip 1 | 63 | 6 | 21 |
| 791 | Sci-Fi - Buzzed 1 | 63 | 6 | 22 |
| 792 | Laser - Falling 2 | 63 | 6 | 23 |
| 793 | Sci-Fi - Repeated 1 | 63 | 6 | 24 |
| 794 | Laser - Blast 1 | 63 | 6 | 25 |
| 795 | Laser - Scratch 1 | 63 | 6 | 26 |
| 796 | Fade In Noise 1 | 63 | 6 | 27 |
| 797 | Low Noise 1 | 63 | 6 | 28 |
| 798 | Gritty Noise 1 | 63 | 6 | 29 |
| 799 | Ambient Noise 1 | 63 | 6 | 30 |
| 800 | Ambient Percussion 1 | 63 | 6 | 31 |
| 801 | Ambient Percussion 2 | 63 | 6 | 32 |
| 802 | Ambient Percussion 3 | 63 | 6 | 33 |
| 803 | Ambient Percussion 4 | 63 | 6 | 34 |
| 804 | Ambient Percussion 5 | 63 | 6 | 35 |
| 805 | Ambient Percussion 6 | 63 | 6 | 36 |
| 806 | Percussion + Water 1 | 63 | 6 | 37 |
| 807 | Percussion + Water 2 | 63 | 6 | 38 |
| 808 | Percussion + Water 3 | 63 | 6 | 39 |
| 809 | Glass Crash 1 | 63 | 6 | 40 |
| 810 | Glass Broken 1 | 63 | 6 | 41 |
| 811 | Percussion + Glass Broken 1 | 63 | 6 | 42 |
| 812 | Glass Broken + Reverb 1 | 63 | 6 | 43 |
| 813 | Percussion + Glass Broken 2 | 63 | 6 | 44 |
| 814 | Foley Sound 1 | 63 | 6 | 45 |
| 815 | Foley Sound 2 | 63 | 6 | 46 |
| 816 | Foley Sound 3 | 63 | 6 | 47 |
| 817 | Foley Sound 4 | 63 | 6 | 48 |
| 818 | Foley Sound 5 | 63 | 6 | 49 |
| 819 | Foley Sound 6 | 63 | 6 | 50 |
| 820 | Foley Sound 7 | 63 | 6 | 51 |
| 821 | Foley Sound 8 | 63 | 6 | 52 |
| 822 | Camera Shutter 1 | 63 | 6 | 53 |
| 823 | Camera Shutter 2 | 63 | 6 | 54 |
| 824 | Camera Shutter 3 | 63 | 6 | 55 |
| 825 | Old Clock Tick 1 | 63 | 6 | 56 |
| 826 | Telephone 1 | 63 | 6 | 57 |
| 827 | Gunshot 1 | 63 | 6 | 58 |
| 828 | Bomb 1 | 63 | 6 | 59 |
| 829 | Scanning 1 | 63 | 6 | 60 |
| 830 | SFX High Bell 1 | 63 | 6 | 61 |
| 831 | SFX Pitched Tone 1 | 63 | 6 | 62 |
| 832 | Muffled Pitched Percussion 1 | 63 | 6 | 63 |
| 833 | Sine Percussion 1 | 63 | 6 | 64 |
| 834 | Water Tone 1 | 63 | 6 | 65 |
| 835 | Mid Resonated Tone 1 | 63 | 6 | 66 |
| 836 | Mid Resonated Tone 2 | 63 | 6 | 67 |
| 837 | Wood + Reverb 1 | 63 | 6 | 68 |
| 838 | Pitched SFX 1 | 63 | 6 | 69 |
| 839 | Trash Can 1 | 63 | 6 | 70 |
| 840 | Distorted Pitched Noise 1 | 63 | 6 | 71 |
| 841 | Dark Hit 1 | 63 | 6 | 72 |
| 842 | Percussion Hit 1 | 63 | 6 | 73 |
| 843 | Percussion Hit 2 | 63 | 6 | 74 |
| 844 | Percussion Hit 3 | 63 | 6 | 75 |
| 845 | Percussion Hit 4 | 63 | 6 | 76 |
| 846 | Gritty Hit 1 | 63 | 6 | 77 |
| 847 | Gritty Hit 2 | 63 | 6 | 78 |
| 848 | Panning Gritty Hit 1 | 63 | 6 | 79 |
| 849 | Punchy Gritty Hit 1 | 63 | 6 | 80 |
| 850 | Industrial Hit 1 | 63 | 6 | 81 |
| 851 | Industrial Hit 2 | 63 | 6 | 82 |
| 852 | Industrial Hit 3 | 63 | 6 | 83 |
| 853 | Industrial Hit 4 | 63 | 6 | 84 |
| 854 | Industrial Hit 5 | 63 | 6 | 85 |
| 855 | Industrial Hit 6 | 63 | 6 | 86 |

## Synth sounds (1077)


### Bass (95)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 856 | Rn Bass | 63 | 6 | 87 |
| 857 | Buzz Bass | 63 | 6 | 88 |
| 858 | Acid3 | 63 | 6 | 89 |
| 859 | Bass Morpher | 63 | 6 | 90 |
| 860 | 3 VCOs | 63 | 6 | 91 |
| 861 | Brain Bass | 63 | 6 | 92 |
| 862 | Lo Boy | 63 | 6 | 93 |
| 863 | Dark Bass | 63 | 6 | 94 |
| 864 | Fundamental | 63 | 6 | 95 |
| 865 | Fat Sine Resonance | 63 | 6 | 96 |
| 866 | Moon Bass | 63 | 6 | 97 |
| 867 | More Fatty | 63 | 6 | 98 |
| 868 | Chill Out Bass | 63 | 6 | 99 |
| 869 | Growler | 63 | 6 | 100 |
| 870 | Smacked | 63 | 6 | 101 |
| 871 | boooooooooom | 63 | 6 | 102 |
| 872 | Biting | 63 | 6 | 103 |
| 873 | Boogie A Legato | 63 | 6 | 104 |
| 874 | Uni Punch | 63 | 6 | 105 |
| 875 | Noise Bass | 63 | 6 | 106 |
| 876 | Single Oscillator | 63 | 6 | 107 |
| 877 | Unison | 63 | 6 | 108 |
| 878 | Long Spit | 63 | 6 | 109 |
| 879 | Big Bass | 63 | 6 | 110 |
| 880 | Bass & Comp! | 63 | 6 | 111 |
| 881 | Rave Blade | 63 | 6 | 112 |
| 882 | Plastic Bass | 63 | 6 | 113 |
| 883 | Funky Resonance | 63 | 6 | 114 |
| 884 | Phat Three | 63 | 6 | 115 |
| 885 | Needle Bass | 63 | 6 | 116 |
| 886 | Acidd | 63 | 6 | 117 |
| 887 | Boom Bass | 63 | 6 | 118 |
| 888 | West Coast | 63 | 6 | 119 |
| 889 | Wazzo | 63 | 6 | 120 |
| 890 | Fast PWM Bass | 63 | 6 | 121 |
| 891 | Bass Pedal | 63 | 6 | 122 |
| 892 | Oxide | 63 | 6 | 123 |
| 893 | Bowngo | 63 | 6 | 124 |
| 894 | Wide Synth Bass | 63 | 6 | 125 |
| 895 | Dry Synth Bass | 63 | 6 | 126 |
| 896 | Kick Bass Legato | 63 | 6 | 127 |
| 897 | Keep Dancin' | 63 | 7 | 0 |
| 898 | Velo Master | 63 | 7 | 1 |
| 899 | Wah Bass | 63 | 7 | 2 |
| 900 | Pulse Step | 63 | 7 | 3 |
| 901 | Phat Step | 63 | 7 | 4 |
| 902 | Octave Analog | 63 | 7 | 5 |
| 903 | Sync Bass | 63 | 7 | 6 |
| 904 | Sync Big | 63 | 7 | 7 |
| 905 | Puncher | 63 | 7 | 8 |
| 906 | Dark Comp | 63 | 7 | 9 |
| 907 | Simple Bass | 63 | 7 | 10 |
| 908 | Fat Sine | 63 | 7 | 11 |
| 909 | Kompressor | 63 | 7 | 12 |
| 910 | Dark Uni | 63 | 7 | 13 |
| 911 | Fight Bass | 63 | 7 | 14 |
| 912 | Byon Bass | 63 | 7 | 15 |
| 913 | One Voice | 63 | 7 | 16 |
| 914 | Pro-Attack | 63 | 7 | 17 |
| 915 | Bobby Bass | 63 | 7 | 18 |
| 916 | Trance Bass | 63 | 7 | 19 |
| 917 | Short SequenceBass | 63 | 7 | 20 |
| 918 | Lately | 63 | 7 | 21 |
| 919 | Faaat Pulse | 63 | 7 | 22 |
| 920 | Short PWM Bass | 63 | 7 | 23 |
| 921 | Hyper Velocity | 63 | 7 | 24 |
| 922 | Deep Point | 63 | 7 | 25 |
| 923 | Pulse Stop | 63 | 7 | 26 |
| 924 | Oh Bee Bass | 63 | 7 | 27 |
| 925 | Booming Bass | 63 | 7 | 28 |
| 926 | Army Bass | 63 | 7 | 29 |
| 927 | Punchy Drone | 63 | 7 | 30 |
| 928 | Dee Tune | 63 | 7 | 31 |
| 929 | Chorus Pulse | 63 | 7 | 32 |
| 930 | Sweeper | 63 | 7 | 33 |
| 931 | Synth Bass 1 | 63 | 7 | 34 |
| 932 | Synth Bass 2 | 63 | 7 | 35 |
| 933 | Universal | 63 | 7 | 36 |
| 934 | Analog Bullet Bass | 63 | 7 | 37 |
| 935 | Analog Perc Bass | 63 | 7 | 38 |
| 936 | Analog Step Bass | 63 | 7 | 39 |
| 937 | Upright | 63 | 7 | 40 |
| 938 | Prec Flat Wound | 63 | 7 | 41 |
| 939 | Round Wound | 63 | 7 | 42 |
| 940 | Mid Range Finger | 63 | 7 | 43 |
| 941 | Pick Open | 63 | 7 | 44 |
| 942 | Pick Mute | 63 | 7 | 45 |
| 943 | Slap Switch | 63 | 7 | 46 |
| 944 | Fretless Dry | 63 | 7 | 47 |
| 945 | Fretless Solo | 63 | 7 | 48 |
| 946 | Dist Tama Bass | 63 | 7 | 49 |
| 947 | 5th Fuzz Bass | 63 | 7 | 50 |
| 948 | Hybrid Bass 1 | 63 | 7 | 51 |
| 949 | Hybrid Bass 2 | 63 | 7 | 52 |
| 950 | House Organ Bass | 63 | 7 | 53 |

### Synth Lead (152)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 951 | Slow Saw Lead | 63 | 7 | 54 |
| 952 | Darker Things Drone | 63 | 7 | 55 |
| 953 | Analog Saw Dub | 63 | 7 | 56 |
| 954 | Percussive Dance 1 | 63 | 7 | 57 |
| 955 | Multi Saw DA | 63 | 7 | 58 |
| 956 | Dance Synth DA | 63 | 7 | 59 |
| 957 | Percussive Dance 2 | 63 | 7 | 60 |
| 958 | Percussive Dance 2 [Chord] | 63 | 7 | 61 |
| 959 | Power Hook | 63 | 7 | 62 |
| 960 | Dance Survivor | 63 | 7 | 63 |
| 961 | P5 Resonance Comp | 63 | 7 | 64 |
| 962 | P5 Analog Punch | 63 | 7 | 65 |
| 963 | P5 Analog Punch [Chord] | 63 | 7 | 66 |
| 964 | Saw Lead | 63 | 7 | 67 |
| 965 | Cool Trance | 63 | 7 | 68 |
| 966 | >Attack< | 63 | 7 | 69 |
| 967 | Club Finger | 63 | 7 | 70 |
| 968 | Wobbly | 63 | 7 | 71 |
| 969 | Wobbly [Chord] | 63 | 7 | 72 |
| 970 | Ana Dayz | 63 | 7 | 73 |
| 971 | Airy Nylon | 63 | 7 | 74 |
| 972 | Progressive Attack | 63 | 7 | 75 |
| 973 | Oracle | 63 | 7 | 76 |
| 974 | Big Comp | 63 | 7 | 77 |
| 975 | Big Comp [Chord] | 63 | 7 | 78 |
| 976 | Rezz Punch | 63 | 7 | 79 |
| 977 | Resonant Clavi | 63 | 7 | 80 |
| 978 | Straight | 63 | 7 | 81 |
| 979 | Straight [Chord] | 63 | 7 | 82 |
| 980 | Psych Noise | 63 | 7 | 83 |
| 981 | SquiffyMisbehaving | 63 | 7 | 84 |
| 982 | Lektro Codes | 63 | 7 | 85 |
| 983 | Lektro Codes [Chord] | 63 | 7 | 86 |
| 984 | Hard FM Keyboard | 63 | 7 | 87 |
| 985 | W Phaser | 63 | 7 | 88 |
| 986 | DPCM Attack | 63 | 7 | 89 |
| 987 | Talk | 63 | 7 | 90 |
| 988 | Digy SEQ | 63 | 7 | 91 |
| 989 | Nerve Nasty | 63 | 7 | 92 |
| 990 | Ring Zplus | 63 | 7 | 93 |
| 991 | Trance Attack | 63 | 7 | 94 |
| 992 | Trance Attack [Chord] | 63 | 7 | 95 |
| 993 | Tekno Attack | 63 | 7 | 96 |
| 994 | PWM Percussion | 63 | 7 | 97 |
| 995 | Stabby | 63 | 7 | 98 |
| 996 | Detroit Stab | 63 | 7 | 99 |
| 997 | Corrado | 63 | 7 | 100 |
| 998 | Synthetique | 63 | 7 | 101 |
| 999 | Noiz Rezz | 63 | 7 | 102 |
| 1000 | Tuxedo | 63 | 7 | 103 |
| 1001 | Queens | 63 | 7 | 104 |
| 1002 | Hip Voice | 63 | 7 | 105 |
| 1003 | GX1 | 63 | 7 | 106 |
| 1004 | GX1 [Chord] | 63 | 7 | 107 |
| 1005 | Night Watch | 63 | 7 | 108 |
| 1006 | Pluck Bells | 63 | 7 | 109 |
| 1007 | Power Dance Chords | 63 | 7 | 110 |
| 1008 | Hyper Trance | 63 | 7 | 111 |
| 1009 | Cosmic Psyche | 63 | 7 | 112 |
| 1010 | Brightness | 63 | 7 | 113 |
| 1011 | Brightness [Chord] | 63 | 7 | 114 |
| 1012 | Calliope Lead | 63 | 7 | 115 |
| 1013 | Voice Lead | 63 | 7 | 116 |
| 1014 | Chiff Lead | 63 | 7 | 117 |
| 1015 | Charan Lead | 63 | 7 | 118 |
| 1016 | Fifth Lead | 63 | 7 | 119 |
| 1017 | Bass & Lead | 63 | 7 | 120 |
| 1018 | PWM Stabs | 63 | 7 | 121 |
| 1019 | Queen of Pop | 63 | 7 | 122 |
| 1020 | EDM Talker | 63 | 7 | 123 |
| 1021 | Huge Lead | 63 | 7 | 124 |
| 1022 | Bleep Lead | 63 | 7 | 125 |
| 1023 | Detuned Vintage | 63 | 7 | 126 |
| 1024 | Space Lead | 63 | 7 | 127 |
| 1025 | Square Lead | 63 | 8 | 0 |
| 1026 | Dual Square Lead | 63 | 8 | 1 |
| 1027 | Dual Square Lead [Chord] | 63 | 8 | 2 |
| 1028 | Vintage Sync | 63 | 8 | 3 |
| 1029 | Dirty Hook | 63 | 8 | 4 |
| 1030 | Nu Mini | 63 | 8 | 5 |
| 1031 | ProgressiveRk Lead | 63 | 8 | 6 |
| 1032 | Lucky | 63 | 8 | 7 |
| 1033 | Opening | 63 | 8 | 8 |
| 1034 | Rap Lead 1 | 63 | 8 | 9 |
| 1035 | Mini Soft | 63 | 8 | 10 |
| 1036 | Feeling | 63 | 8 | 11 |
| 1037 | Early Lead | 63 | 8 | 12 |
| 1038 | Funky Pulse | 63 | 8 | 13 |
| 1039 | Mr. Finger | 63 | 8 | 14 |
| 1040 | Singleline | 63 | 8 | 15 |
| 1041 | Soft RnB | 63 | 8 | 16 |
| 1042 | Wind Synth | 63 | 8 | 17 |
| 1043 | Broken Sine | 63 | 8 | 18 |
| 1044 | Broken Sine [Chord] | 63 | 8 | 19 |
| 1045 | Duck Lead | 63 | 8 | 20 |
| 1046 | In da Night | 63 | 8 | 21 |
| 1047 | Mayday | 63 | 8 | 22 |
| 1048 | On D Line | 63 | 8 | 23 |
| 1049 | Early Soloist | 63 | 8 | 24 |
| 1050 | Heterodyne | 63 | 8 | 25 |
| 1051 | Classic 5th | 63 | 8 | 26 |
| 1052 | Vintage Saw | 63 | 8 | 27 |
| 1053 | Mini Three | 63 | 8 | 28 |
| 1054 | Phat Dino | 63 | 8 | 29 |
| 1055 | Dynamic Mini | 63 | 8 | 30 |
| 1056 | PWM Lead | 63 | 8 | 31 |
| 1057 | PWM Lead [Chord] | 63 | 8 | 32 |
| 1058 | Pulse Wound | 63 | 8 | 33 |
| 1059 | Think Sync | 63 | 8 | 34 |
| 1060 | Punch Lead | 63 | 8 | 35 |
| 1061 | Bright Saw | 63 | 8 | 36 |
| 1062 | Troy | 63 | 8 | 37 |
| 1063 | Wood Panel | 63 | 8 | 38 |
| 1064 | Push Ahead | 63 | 8 | 39 |
| 1065 | Eight | 63 | 8 | 40 |
| 1066 | Sync Power | 63 | 8 | 41 |
| 1067 | Glisten Lead | 63 | 8 | 42 |
| 1068 | Big Drone | 63 | 8 | 43 |
| 1069 | Screameemy | 63 | 8 | 44 |
| 1070 | Flange Filter | 63 | 8 | 45 |
| 1071 | Sutra | 63 | 8 | 46 |
| 1072 | Free LFO | 63 | 8 | 47 |
| 1073 | Rap Lead 2 | 63 | 8 | 48 |
| 1074 | Space Power Lead | 63 | 8 | 49 |
| 1075 | Nyquist | 63 | 8 | 50 |
| 1076 | Digimetal | 63 | 8 | 51 |
| 1077 | Saw Destroy | 63 | 8 | 52 |
| 1078 | Vinalog Saw | 63 | 8 | 53 |
| 1079 | Mady SQU | 63 | 8 | 54 |
| 1080 | Low Undulation | 63 | 8 | 55 |
| 1081 | Impact | 63 | 8 | 56 |
| 1082 | Talk Mod | 63 | 8 | 57 |
| 1083 | Digital Gangsta | 63 | 8 | 58 |
| 1084 | Plastic Squeeze | 63 | 8 | 59 |
| 1085 | Pinz Lead | 63 | 8 | 60 |
| 1086 | Dancy Saw Lead | 63 | 8 | 61 |
| 1087 | Buzz Around | 63 | 8 | 62 |
| 1088 | Xtreme Wheel | 63 | 8 | 63 |
| 1089 | Supertrance | 63 | 8 | 64 |
| 1090 | Supertrance [Chord] | 63 | 8 | 65 |
| 1091 | Poly Hook | 63 | 8 | 66 |
| 1092 | HPF Dance | 63 | 8 | 67 |
| 1093 | Tekk Glide | 63 | 8 | 68 |
| 1094 | Growl Tekk | 63 | 8 | 69 |
| 1095 | Plucked Chordz | 63 | 8 | 70 |
| 1096 | Chordz | 63 | 8 | 71 |
| 1097 | Cool Body | 63 | 8 | 72 |
| 1098 | Twist Sync | 63 | 8 | 73 |
| 1099 | TEKIE | 63 | 8 | 74 |
| 1100 | Sonix | 63 | 8 | 75 |
| 1101 | Big SkidHookLead 1 | 63 | 8 | 76 |
| 1102 | Big SkidHookLead 2 | 63 | 8 | 77 |

### Piano (32)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1103 | Full Concert Grand | 63 | 8 | 78 |
| 1104 | Concert GrandPiano | 63 | 8 | 79 |
| 1105 | Rock Grand Piano | 63 | 8 | 80 |
| 1106 | Rock Grand Piano [Chord] | 63 | 8 | 81 |
| 1107 | Rock Brite Piano | 63 | 8 | 82 |
| 1108 | Mellow Grand Piano | 63 | 8 | 83 |
| 1109 | Hall Mellow Grand | 63 | 8 | 84 |
| 1110 | Hall Mellow Grand [Chord] | 63 | 8 | 85 |
| 1111 | Glasgow | 63 | 8 | 86 |
| 1112 | Romantic Piano | 63 | 8 | 87 |
| 1113 | Aggressive Grand | 63 | 8 | 88 |
| 1114 | Tacky | 63 | 8 | 89 |
| 1115 | House Piano | 63 | 8 | 90 |
| 1116 | CP80 Layer | 63 | 8 | 91 |
| 1117 | CP80 | 63 | 8 | 92 |
| 1118 | CP80 [Chord] | 63 | 8 | 93 |
| 1119 | CP80 Amp | 63 | 8 | 94 |
| 1120 | CP80 Chorus | 63 | 8 | 95 |
| 1121 | CP 1979 | 63 | 8 | 96 |
| 1122 | CP70 Chorus | 63 | 8 | 97 |
| 1123 | Journey | 63 | 8 | 98 |
| 1124 | CP 2007 | 63 | 8 | 99 |
| 1125 | Old and Squashed | 63 | 8 | 100 |
| 1126 | Ballad Key | 63 | 8 | 101 |
| 1127 | 80s Layer | 63 | 8 | 102 |
| 1128 | Ballad Stack | 63 | 8 | 103 |
| 1129 | Piano Back | 63 | 8 | 104 |
| 1130 | Monaural Grand | 63 | 8 | 105 |
| 1131 | Old Blues | 63 | 8 | 106 |
| 1132 | Old Blues [Chord] | 63 | 8 | 107 |
| 1133 | 1968 | 63 | 8 | 108 |
| 1134 | Honkytonk | 63 | 8 | 109 |

### Keyboard (80)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1135 | E.Piano 1 | 63 | 8 | 110 |
| 1136 | Soft Case | 63 | 8 | 111 |
| 1137 | Soft Case [Chord] | 63 | 8 | 112 |
| 1138 | 74 Phase | 63 | 8 | 113 |
| 1139 | Vintage'74 | 63 | 8 | 114 |
| 1140 | R&B Soft | 63 | 8 | 115 |
| 1141 | Early 70's | 63 | 8 | 116 |
| 1142 | Crunchy Comp | 63 | 8 | 117 |
| 1143 | Vintage Case | 63 | 8 | 118 |
| 1144 | Hard Vintage | 63 | 8 | 119 |
| 1145 | Sweetness | 63 | 8 | 120 |
| 1146 | Phaser Vintage | 63 | 8 | 121 |
| 1147 | Vintage Phase | 63 | 8 | 122 |
| 1148 | Early Fusion | 63 | 8 | 123 |
| 1149 | Neo Soul | 63 | 8 | 124 |
| 1150 | 1983 | 63 | 8 | 125 |
| 1151 | 1983 [Chord] | 63 | 8 | 126 |
| 1152 | Contempo | 63 | 8 | 127 |
| 1153 | Clicky Dyno | 63 | 9 | 0 |
| 1154 | Dyno Straight | 63 | 9 | 1 |
| 1155 | Dyno Chorus | 63 | 9 | 2 |
| 1156 | 80s Boosted | 63 | 9 | 3 |
| 1157 | 80s Boosted [Chord] | 63 | 9 | 4 |
| 1158 | Chorus Hard | 63 | 9 | 5 |
| 1159 | Max Tine | 63 | 9 | 6 |
| 1160 | Bell Chorus | 63 | 9 | 7 |
| 1161 | Drive EP | 63 | 9 | 8 |
| 1162 | Vinyl EP | 63 | 9 | 9 |
| 1163 | Natural Wr | 63 | 9 | 10 |
| 1164 | Natural Wr [Chord] | 63 | 9 | 11 |
| 1165 | Wr EP Bright | 63 | 9 | 12 |
| 1166 | Wr Distortion | 63 | 9 | 13 |
| 1167 | Phaze Wr | 63 | 9 | 14 |
| 1168 | E.Piano 2 | 63 | 9 | 15 |
| 1169 | DX Legend | 63 | 9 | 16 |
| 1170 | Bell DX | 63 | 9 | 17 |
| 1171 | DX Woody | 63 | 9 | 18 |
| 1172 | DX Woody [Chord] | 63 | 9 | 19 |
| 1173 | Full Tine | 63 | 9 | 20 |
| 1174 | DX Mellow | 63 | 9 | 21 |
| 1175 | DX Crisp | 63 | 9 | 22 |
| 1176 | DX Celesta EP | 63 | 9 | 23 |
| 1177 | DX Pluck EP | 63 | 9 | 24 |
| 1178 | DX-7 II | 63 | 9 | 25 |
| 1179 | GS Tines | 63 | 9 | 26 |
| 1180 | Galaxy DX | 63 | 9 | 27 |
| 1181 | TX816 Bell Piano | 63 | 9 | 28 |
| 1182 | Marimba DX | 63 | 9 | 29 |
| 1183 | DX5-Zero | 63 | 9 | 30 |
| 1184 | Hybrid EP | 63 | 9 | 31 |
| 1185 | Mixed Up | 63 | 9 | 32 |
| 1186 | Dyno Wr | 63 | 9 | 33 |
| 1187 | Analog Piano | 63 | 9 | 34 |
| 1188 | AhrAmI | 63 | 9 | 35 |
| 1189 | Electro Piano | 63 | 9 | 36 |
| 1190 | Transistor Piano | 63 | 9 | 37 |
| 1191 | EP Pad | 63 | 9 | 38 |
| 1192 | DX Pad | 63 | 9 | 39 |
| 1193 | Grace EP | 63 | 9 | 40 |
| 1194 | Nu Touch Clavi | 63 | 9 | 41 |
| 1195 | Super Clavi 1 | 63 | 9 | 42 |
| 1196 | PhaserClavi Mt | 63 | 9 | 43 |
| 1197 | Vintage Clavi | 63 | 9 | 44 |
| 1198 | Super Clavi 2 | 63 | 9 | 45 |
| 1199 | Stereo Clavi | 63 | 9 | 46 |
| 1200 | Hollow Clavi | 63 | 9 | 47 |
| 1201 | Nu Phasing | 63 | 9 | 48 |
| 1202 | Touch Clavi | 63 | 9 | 49 |
| 1203 | Wah Clavi | 63 | 9 | 50 |
| 1204 | Pulse Clavi | 63 | 9 | 51 |
| 1205 | Brite Clavi | 63 | 9 | 52 |
| 1206 | Clavi Bril Treble | 63 | 9 | 53 |
| 1207 | Clavi Bril Treble [Chord] | 63 | 9 | 54 |
| 1208 | Clavi Amped | 63 | 9 | 55 |
| 1209 | Clavi Phaser | 63 | 9 | 56 |
| 1210 | Clavi Wah | 63 | 9 | 57 |
| 1211 | Harpsichord | 63 | 9 | 58 |
| 1212 | NaturalHarpsichord | 63 | 9 | 59 |
| 1213 | Octave Harpsichord | 63 | 9 | 60 |
| 1214 | E.Harpsichord | 63 | 9 | 61 |

### Organ (75)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1215 | 16 + 8 + 5&1/3 | 63 | 9 | 62 |
| 1216 | First 3 w/Perc | 63 | 9 | 63 |
| 1217 | Slow Jam | 63 | 9 | 64 |
| 1218 | Cool Cat | 63 | 9 | 65 |
| 1219 | Jazzy 1 | 63 | 9 | 66 |
| 1220 | Jazzy 1 [Chord] | 63 | 9 | 67 |
| 1221 | Jazzy 2 | 63 | 9 | 68 |
| 1222 | Jazzy Chorus | 63 | 9 | 69 |
| 1223 | Draw Organ | 63 | 9 | 70 |
| 1224 | Percussive Organ | 63 | 9 | 71 |
| 1225 | Rock Organ | 63 | 9 | 72 |
| 1226 | On Road | 63 | 9 | 73 |
| 1227 | Progressy | 63 | 9 | 74 |
| 1228 | Rocky | 63 | 9 | 75 |
| 1229 | Crunchy | 63 | 9 | 76 |
| 1230 | Glassy | 63 | 9 | 77 |
| 1231 | Clean | 63 | 9 | 78 |
| 1232 | Vib Chorus | 63 | 9 | 79 |
| 1233 | Soulemn | 63 | 9 | 80 |
| 1234 | Mellow | 63 | 9 | 81 |
| 1235 | Fully | 63 | 9 | 82 |
| 1236 | FullDraw/CVibrato | 63 | 9 | 83 |
| 1237 | Even Out | 63 | 9 | 84 |
| 1238 | A Few Wheels | 63 | 9 | 85 |
| 1239 | A Few Wheels [Chord] | 63 | 9 | 86 |
| 1240 | Left Manual | 63 | 9 | 87 |
| 1241 | Draw Control | 63 | 9 | 88 |
| 1242 | Clean Noise | 63 | 9 | 89 |
| 1243 | Walking Bass | 63 | 9 | 90 |
| 1244 | Greasy | 63 | 9 | 91 |
| 1245 | Swishie | 63 | 9 | 92 |
| 1246 | Solo Percussion | 63 | 9 | 93 |
| 1247 | Percussion Vibrato | 63 | 9 | 94 |
| 1248 | Tiny Combo Bars 1 | 63 | 9 | 95 |
| 1249 | Tiny Combo Bars 1 [Chord] | 63 | 9 | 96 |
| 1250 | Tiny Combo Bars 2 | 63 | 9 | 97 |
| 1251 | Panther | 63 | 9 | 98 |
| 1252 | 1967 Keyboard | 63 | 9 | 99 |
| 1253 | YD-45C | 63 | 9 | 100 |
| 1254 | Surf Rock | 63 | 9 | 101 |
| 1255 | Early Bird | 63 | 9 | 102 |
| 1256 | Vx Full Bars | 63 | 9 | 103 |
| 1257 | Vx Dark Bars | 63 | 9 | 104 |
| 1258 | Fr All Tabs | 63 | 9 | 105 |
| 1259 | Fr String Tabs | 63 | 9 | 106 |
| 1260 | Vx Full Bars Amped | 63 | 9 | 107 |
| 1261 | Vx Surf Organ | 63 | 9 | 108 |
| 1262 | Moet | 63 | 9 | 109 |
| 1263 | Bollinger | 63 | 9 | 110 |
| 1264 | Vinyl Organ | 63 | 9 | 111 |
| 1265 | Alternator | 63 | 9 | 112 |
| 1266 | Tradi | 63 | 9 | 113 |
| 1267 | Petit | 63 | 9 | 114 |
| 1268 | Petit [Chord] | 63 | 9 | 115 |
| 1269 | Fluty | 63 | 9 | 116 |
| 1270 | Fluty Pipe | 63 | 9 | 117 |
| 1271 | St. Peter | 63 | 9 | 118 |
| 1272 | St. Paul | 63 | 9 | 119 |
| 1273 | Impromptu | 63 | 9 | 120 |
| 1274 | Mixture | 63 | 9 | 121 |
| 1275 | Reed Split | 63 | 9 | 122 |
| 1276 | Medieval | 63 | 9 | 123 |
| 1277 | Medieval [Chord] | 63 | 9 | 124 |
| 1278 | Breath Pipe | 63 | 9 | 125 |
| 1279 | Reedy Pipe | 63 | 9 | 126 |
| 1280 | Sunday | 63 | 9 | 127 |
| 1281 | Church Organ | 63 | 10 | 0 |
| 1282 | Church Organ [Chord] | 63 | 10 | 1 |
| 1283 | Reed Organ | 63 | 10 | 2 |
| 1284 | Accordion | 63 | 10 | 3 |
| 1285 | Accordions | 63 | 10 | 4 |
| 1286 | Accordions [Chord] | 63 | 10 | 5 |
| 1287 | Tango Accordion 1 | 63 | 10 | 6 |
| 1288 | Tango Accordion 2 | 63 | 10 | 7 |
| 1289 | Master Accordion | 63 | 10 | 8 |

### Pad (149)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1290 | Round Saw Phase | 63 | 10 | 9 |
| 1291 | Ducker Cloud | 63 | 10 | 10 |
| 1292 | Multi Saw Pad | 63 | 10 | 11 |
| 1293 | Poly Synth Pad | 63 | 10 | 12 |
| 1294 | Poly Pad DA | 63 | 10 | 13 |
| 1295 | HyperTrance Stereo | 63 | 10 | 14 |
| 1296 | Ethereal | 63 | 10 | 15 |
| 1297 | Ethereal [Chord] | 63 | 10 | 16 |
| 1298 | Saw Pad | 63 | 10 | 17 |
| 1299 | Dark ModulationPad | 63 | 10 | 18 |
| 1300 | Dark Light | 63 | 10 | 19 |
| 1301 | Ambient Synth Pad | 63 | 10 | 20 |
| 1302 | 5th Lite | 63 | 10 | 21 |
| 1303 | Smooth BPF Sweep | 63 | 10 | 22 |
| 1304 | Trance | 63 | 10 | 23 |
| 1305 | Xtreme Sweep | 63 | 10 | 24 |
| 1306 | Warm Pad | 63 | 10 | 25 |
| 1307 | Nu Warm Pad | 63 | 10 | 26 |
| 1308 | Nu Warm Pad [Chord] | 63 | 10 | 27 |
| 1309 | 5th Atmosphere | 63 | 10 | 28 |
| 1310 | Dim | 63 | 10 | 29 |
| 1311 | Simple Air | 63 | 10 | 30 |
| 1312 | Nature Sine | 63 | 10 | 31 |
| 1313 | Nature Sine [Chord] | 63 | 10 | 32 |
| 1314 | Analog | 63 | 10 | 33 |
| 1315 | Perc Pad | 63 | 10 | 34 |
| 1316 | Dark Atmo Pad | 63 | 10 | 35 |
| 1317 | Dark Atmo Pad [Chord] | 63 | 10 | 36 |
| 1318 | Dark Organ Pad | 63 | 10 | 37 |
| 1319 | Soft Brassy | 63 | 10 | 38 |
| 1320 | Road to Nowhere | 63 | 10 | 39 |
| 1321 | Analog Sweep | 63 | 10 | 40 |
| 1322 | Sweep Pad | 63 | 10 | 41 |
| 1323 | Sweep Strings | 63 | 10 | 42 |
| 1324 | Brass Motion Pad | 63 | 10 | 43 |
| 1325 | Luminous | 63 | 10 | 44 |
| 1326 | Mother Ship | 63 | 10 | 45 |
| 1327 | Warm Backing Pad | 63 | 10 | 46 |
| 1328 | Feather | 63 | 10 | 47 |
| 1329 | Feather [Chord] | 63 | 10 | 48 |
| 1330 | Pan Sphere | 63 | 10 | 49 |
| 1331 | Square | 63 | 10 | 50 |
| 1332 | Shaper | 63 | 10 | 51 |
| 1333 | Early Digital | 63 | 10 | 52 |
| 1334 | Dramana | 63 | 10 | 53 |
| 1335 | Dream Shift | 63 | 10 | 54 |
| 1336 | Dream Shift [Chord] | 63 | 10 | 55 |
| 1337 | Sound Track | 63 | 10 | 56 |
| 1338 | Remote Space | 63 | 10 | 57 |
| 1339 | Fathoms | 63 | 10 | 58 |
| 1340 | Mother Earth | 63 | 10 | 59 |
| 1341 | Landing Pad | 63 | 10 | 60 |
| 1342 | The Breath | 63 | 10 | 61 |
| 1343 | Feather Pad | 63 | 10 | 62 |
| 1344 | Slow Attack Pad | 63 | 10 | 63 |
| 1345 | Hi Brite | 63 | 10 | 64 |
| 1346 | Pad & Syn | 63 | 10 | 65 |
| 1347 | Pad & Syn [Chord] | 63 | 10 | 66 |
| 1348 | Cosmic Swell Pad | 63 | 10 | 67 |
| 1349 | Sweet Flange | 63 | 10 | 68 |
| 1350 | Waterfall | 63 | 10 | 69 |
| 1351 | Phase Pad | 63 | 10 | 70 |
| 1352 | Pure Synth | 63 | 10 | 71 |
| 1353 | Pure Synth + Delay | 63 | 10 | 72 |
| 1354 | Pearls | 63 | 10 | 73 |
| 1355 | Flange Wall | 63 | 10 | 74 |
| 1356 | Tornado | 63 | 10 | 75 |
| 1357 | Ice Rink | 63 | 10 | 76 |
| 1358 | Bell Pad | 63 | 10 | 77 |
| 1359 | Bell Pad [Chord] | 63 | 10 | 78 |
| 1360 | New Age Pad | 63 | 10 | 79 |
| 1361 | Paradise | 63 | 10 | 80 |
| 1362 | Yellow River | 63 | 10 | 81 |
| 1363 | Love Me | 63 | 10 | 82 |
| 1364 | Frozen Pad | 63 | 10 | 83 |
| 1365 | Bowed Pad | 63 | 10 | 84 |
| 1366 | Metal Pad | 63 | 10 | 85 |
| 1367 | Pensive | 63 | 10 | 86 |
| 1368 | Sci-Fi | 63 | 10 | 87 |
| 1369 | Atmosphere | 63 | 10 | 88 |
| 1370 | Halo Pad | 63 | 10 | 89 |
| 1371 | Space Vocals | 63 | 10 | 90 |
| 1372 | Haah Pad | 63 | 10 | 91 |
| 1373 | Oooh Pad | 63 | 10 | 92 |
| 1374 | Oooh Pad [Chord] | 63 | 10 | 93 |
| 1375 | Back in Itopian | 63 | 10 | 94 |
| 1376 | Strings & Choir | 63 | 10 | 95 |
| 1377 | Angel Eyes | 63 | 10 | 96 |
| 1378 | Glass Choir | 63 | 10 | 97 |
| 1379 | Nativity | 63 | 10 | 98 |
| 1380 | Seraphim | 63 | 10 | 99 |
| 1381 | Aah Choir | 63 | 10 | 100 |
| 1382 | Ooh Choir | 63 | 10 | 101 |
| 1383 | Syn Voice | 63 | 10 | 102 |
| 1384 | Choir Pad | 63 | 10 | 103 |
| 1385 | Mellow Swell | 63 | 10 | 104 |
| 1386 | Frozen Glasspad | 63 | 10 | 105 |
| 1387 | Lunar Eclipse | 63 | 10 | 106 |
| 1388 | Prayer Call | 63 | 10 | 107 |
| 1389 | Granular Motion | 63 | 10 | 108 |
| 1390 | Mysterious Invention | 63 | 10 | 109 |
| 1391 | Gate of Eden | 63 | 10 | 110 |
| 1392 | Whispering Ghosts | 63 | 10 | 111 |
| 1393 | NighttrainToMunich | 63 | 10 | 112 |
| 1394 | Morning Dew | 63 | 10 | 113 |
| 1395 | Calling Mr. Reso | 63 | 10 | 114 |
| 1396 | 2 SwitchesToHeaven | 63 | 10 | 115 |
| 1397 | SEKAI-ISAN | 63 | 10 | 116 |
| 1398 | Setsunai | 63 | 10 | 117 |
| 1399 | Week End | 63 | 10 | 118 |
| 1400 | TiRiPAD | 63 | 10 | 119 |
| 1401 | Cluster | 63 | 10 | 120 |
| 1402 | Xtreme Rezz | 63 | 10 | 121 |
| 1403 | My Reality | 63 | 10 | 122 |
| 1404 | Magnetics | 63 | 10 | 123 |
| 1405 | Sand | 63 | 10 | 124 |
| 1406 | Felicity | 63 | 10 | 125 |
| 1407 | Vibrancy | 63 | 10 | 126 |
| 1408 | Radio Venus | 63 | 10 | 127 |
| 1409 | Elec Blue | 63 | 11 | 0 |
| 1410 | Chyo Ethno | 63 | 11 | 1 |
| 1411 | konjoh BEAM | 63 | 11 | 2 |
| 1412 | Blizzard | 63 | 11 | 3 |
| 1413 | SINGING BOWL | 63 | 11 | 4 |
| 1414 | Metalvox Pad | 63 | 11 | 5 |
| 1415 | Refraction | 63 | 11 | 6 |
| 1416 | Philanger | 63 | 11 | 7 |
| 1417 | Ellipsotron | 63 | 11 | 8 |
| 1418 | Envelope | 63 | 11 | 9 |
| 1419 | Whatsis | 63 | 11 | 10 |
| 1420 | Pearl Collection | 63 | 11 | 11 |
| 1421 | Four Dimensions | 63 | 11 | 12 |
| 1422 | Hallucination | 63 | 11 | 13 |
| 1423 | Electraid | 63 | 11 | 14 |
| 1424 | Clearing | 63 | 11 | 15 |
| 1425 | Long HiPa | 63 | 11 | 16 |
| 1426 | Quad Swell | 63 | 11 | 17 |
| 1427 | New Stab | 63 | 11 | 18 |
| 1428 | Vinyl Hit | 63 | 11 | 19 |
| 1429 | Hit Me | 63 | 11 | 20 |
| 1430 | Ambient Bite | 63 | 11 | 21 |
| 1431 | Bollog Puls | 63 | 11 | 22 |
| 1432 | Orchestra Hit | 63 | 11 | 23 |
| 1433 | Rain Pad | 63 | 11 | 24 |
| 1434 | Goblin | 63 | 11 | 25 |
| 1435 | Echoes | 63 | 11 | 26 |
| 1436 | Dripping Quarks | 63 | 11 | 27 |
| 1437 | Metallic Airstabs | 63 | 11 | 28 |
| 1438 | Descendant | 63 | 11 | 29 |

### Strings (78)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1439 | Violin | 63 | 11 | 30 |
| 1440 | Violin Solo | 63 | 11 | 31 |
| 1441 | Viola | 63 | 11 | 32 |
| 1442 | Viola Solo 1 | 63 | 11 | 33 |
| 1443 | Viola Solo 2 | 63 | 11 | 34 |
| 1444 | Cello Solo | 63 | 11 | 35 |
| 1445 | Cello Duo | 63 | 11 | 36 |
| 1446 | ContrabassSolo1 | 63 | 11 | 37 |
| 1447 | ContrabassSolo2 | 63 | 11 | 38 |
| 1448 | Quartet | 63 | 11 | 39 |
| 1449 | Small Section | 63 | 11 | 40 |
| 1450 | Small Ensemble | 63 | 11 | 41 |
| 1451 | Small Ensemble [Chord] | 63 | 11 | 42 |
| 1452 | Almighty | 63 | 11 | 43 |
| 1453 | Medium Section | 63 | 11 | 44 |
| 1454 | Medium Hall | 63 | 11 | 45 |
| 1455 | Quick Bows | 63 | 11 | 46 |
| 1456 | Large Section | 63 | 11 | 47 |
| 1457 | Strings Section 1 | 63 | 11 | 48 |
| 1458 | Strings Section 2 | 63 | 11 | 49 |
| 1459 | Octave Ensemble | 63 | 11 | 50 |
| 1460 | Full Chamber | 63 | 11 | 51 |
| 1461 | Stryngs | 63 | 11 | 52 |
| 1462 | Stryngs [Chord] | 63 | 11 | 53 |
| 1463 | Dynamic Bow | 63 | 11 | 54 |
| 1464 | Pizzicato | 63 | 11 | 55 |
| 1465 | SymphonicPizzicato | 63 | 11 | 56 |
| 1466 | Plucky Pizzicato | 63 | 11 | 57 |
| 1467 | Octave Pizzes | 63 | 11 | 58 |
| 1468 | Tremolo Strings 1 | 63 | 11 | 59 |
| 1469 | Tremolo Strings 2 | 63 | 11 | 60 |
| 1470 | Tremolo Strs Small | 63 | 11 | 61 |
| 1471 | Spicato Large | 63 | 11 | 62 |
| 1472 | Spicato Large [Chord] | 63 | 11 | 63 |
| 1473 | Disco | 63 | 11 | 64 |
| 1474 | Lush | 63 | 11 | 65 |
| 1475 | Back Ground | 63 | 11 | 66 |
| 1476 | Warm Back | 63 | 11 | 67 |
| 1477 | Stringy | 63 | 11 | 68 |
| 1478 | Big Strings | 63 | 11 | 69 |
| 1479 | F.Horn + Strings | 63 | 11 | 70 |
| 1480 | Wood Winds+Strings | 63 | 11 | 71 |
| 1481 | Synth Strings 1 | 63 | 11 | 72 |
| 1482 | Synth Strings 2 | 63 | 11 | 73 |
| 1483 | Gleaming Pad | 63 | 11 | 74 |
| 1484 | Fat PWM Synth Vel | 63 | 11 | 75 |
| 1485 | VintagePolyStrings | 63 | 11 | 76 |
| 1486 | PWM Strings | 63 | 11 | 77 |
| 1487 | PWM Strings [Chord] | 63 | 11 | 78 |
| 1488 | Mourn Strings | 63 | 11 | 79 |
| 1489 | VP Soft | 63 | 11 | 80 |
| 1490 | PWM Simple | 63 | 11 | 81 |
| 1491 | Glassy Rezonant | 63 | 11 | 82 |
| 1492 | Superstrings | 63 | 11 | 83 |
| 1493 | Light Pad | 63 | 11 | 84 |
| 1494 | Noble Pad | 63 | 11 | 85 |
| 1495 | Warm Big | 63 | 11 | 86 |
| 1496 | Sentimental | 63 | 11 | 87 |
| 1497 | Analog Strings | 63 | 11 | 88 |
| 1498 | Analog Ensemble | 63 | 11 | 89 |
| 1499 | Phase Strings | 63 | 11 | 90 |
| 1500 | Octave Strings | 63 | 11 | 91 |
| 1501 | 80s Clean Strings | 63 | 11 | 92 |
| 1502 | 3 Oscillators Vin | 63 | 11 | 93 |
| 1503 | Silver Strings | 63 | 11 | 94 |
| 1504 | Silver Strings [Chord] | 63 | 11 | 95 |
| 1505 | String Machine | 63 | 11 | 96 |
| 1506 | 3 Octave Strings | 63 | 11 | 97 |
| 1507 | TranceIntroduction | 63 | 11 | 98 |
| 1508 | Mystic Trance | 63 | 11 | 99 |
| 1509 | Electric Violin | 63 | 11 | 100 |
| 1510 | Tron Violin | 63 | 11 | 101 |
| 1511 | Tron Strings | 63 | 11 | 102 |
| 1512 | Tape Strings | 63 | 11 | 103 |
| 1513 | Orchestronic | 63 | 11 | 104 |
| 1514 | Vinyltron | 63 | 11 | 105 |
| 1515 | Beauty Harp | 63 | 11 | 106 |
| 1516 | Stereo Harp | 63 | 11 | 107 |

### Brass (73)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1517 | Trumpet | 63 | 11 | 108 |
| 1518 | Tp Romantic Legato | 63 | 11 | 109 |
| 1519 | Classical Trumpet | 63 | 11 | 110 |
| 1520 | Bright Trumpet | 63 | 11 | 111 |
| 1521 | Tp SoftJazz Legato | 63 | 11 | 112 |
| 1522 | SoftTrumpetLegato | 63 | 11 | 113 |
| 1523 | Trumpet Vibrato | 63 | 11 | 114 |
| 1524 | Trumpet Shake Vel | 63 | 11 | 115 |
| 1525 | Legend Mute | 63 | 11 | 116 |
| 1526 | Flugelhorn | 63 | 11 | 117 |
| 1527 | Jazzy Flugel | 63 | 11 | 118 |
| 1528 | Trumpet Section | 63 | 11 | 119 |
| 1529 | Trumpet Section [Chord] | 63 | 11 | 120 |
| 1530 | Trombone | 63 | 11 | 121 |
| 1531 | Blown Bone Legato | 63 | 11 | 122 |
| 1532 | Bright Trombone | 63 | 11 | 123 |
| 1533 | NewOrleansTrombone | 63 | 11 | 124 |
| 1534 | French Horn | 63 | 11 | 125 |
| 1535 | French Horn Solo | 63 | 11 | 126 |
| 1536 | Tuba | 63 | 11 | 127 |
| 1537 | BassTuba(Bb) | 63 | 12 | 0 |
| 1538 | Euphonium | 63 | 12 | 1 |
| 1539 | FrenchHornSection1 | 63 | 12 | 2 |
| 1540 | FrenchHornSection2 | 63 | 12 | 3 |
| 1541 | French Horns | 63 | 12 | 4 |
| 1542 | F.Horn + Trombone | 63 | 12 | 5 |
| 1543 | F.Hrn+Trombone+Trp | 63 | 12 | 6 |
| 1544 | Orchestra Brass | 63 | 12 | 7 |
| 1545 | Orchestra Brass [Chord] | 63 | 12 | 8 |
| 1546 | Movie Horns | 63 | 12 | 9 |
| 1547 | Symphonic | 63 | 12 | 10 |
| 1548 | Smooth Brass | 63 | 12 | 11 |
| 1549 | Soft Brass mp-mf | 63 | 12 | 12 |
| 1550 | Dynamic Brass | 63 | 12 | 13 |
| 1551 | Accent mf-fall | 63 | 12 | 14 |
| 1552 | Small BrassSection | 63 | 12 | 15 |
| 1553 | MediumBrassSection | 63 | 12 | 16 |
| 1554 | Lots O' Brass | 63 | 12 | 17 |
| 1555 | Bright Section | 63 | 12 | 18 |
| 1556 | Power Section | 63 | 12 | 19 |
| 1557 | Shiny Brass | 63 | 12 | 20 |
| 1558 | Big Brass | 63 | 12 | 21 |
| 1559 | Sforzando | 63 | 12 | 22 |
| 1560 | Soft Brass & Sax | 63 | 12 | 23 |
| 1561 | Big Band | 63 | 12 | 24 |
| 1562 | Sax Big Band | 63 | 12 | 25 |
| 1563 | Velo Falls | 63 | 12 | 26 |
| 1564 | Hybrid Section | 63 | 12 | 27 |
| 1565 | Hybrid Bright | 63 | 12 | 28 |
| 1566 | Hybrid Brass Swell | 63 | 12 | 29 |
| 1567 | The Synth Brass | 63 | 12 | 30 |
| 1568 | T Brass | 63 | 12 | 31 |
| 1569 | Lo-fi | 63 | 12 | 32 |
| 1570 | Quiet Brass | 63 | 12 | 33 |
| 1571 | Big Syn | 63 | 12 | 34 |
| 1572 | Thinth | 63 | 12 | 35 |
| 1573 | XP Brass Stereo | 63 | 12 | 36 |
| 1574 | Simple Saw Brass | 63 | 12 | 37 |
| 1575 | Brassy | 63 | 12 | 38 |
| 1576 | Kustom | 63 | 12 | 39 |
| 1577 | After 1984 | 63 | 12 | 40 |
| 1578 | After 1984 [Chord] | 63 | 12 | 41 |
| 1579 | Finale | 63 | 12 | 42 |
| 1580 | Huge CS80 | 63 | 12 | 43 |
| 1581 | CS-90 | 63 | 12 | 44 |
| 1582 | Oh Bee Soft | 63 | 12 | 45 |
| 1583 | Oh Bee Horns | 63 | 12 | 46 |
| 1584 | Slow PWM Brass | 63 | 12 | 47 |
| 1585 | Soft 5th Brass | 63 | 12 | 48 |
| 1586 | Synth Brass 1 | 63 | 12 | 49 |
| 1587 | Synth Brass 2 | 63 | 12 | 50 |
| 1588 | Oh Bee Syncomp | 63 | 12 | 51 |
| 1589 | Tacky Brass | 63 | 12 | 52 |

### Woodwind (53)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1590 | Soprano Sax | 63 | 12 | 53 |
| 1591 | Soprano Legato | 63 | 12 | 54 |
| 1592 | Soprano Soft | 63 | 12 | 55 |
| 1593 | Mellow Soprano | 63 | 12 | 56 |
| 1594 | Alto Sax | 63 | 12 | 57 |
| 1595 | Alto Vib Legato | 63 | 12 | 58 |
| 1596 | Alto Legato | 63 | 12 | 59 |
| 1597 | Alto | 63 | 12 | 60 |
| 1598 | Alto Accent Legato | 63 | 12 | 61 |
| 1599 | Tenor Sax | 63 | 12 | 62 |
| 1600 | Tenor Dynamic | 63 | 12 | 63 |
| 1601 | Tenor Soft Legato | 63 | 12 | 64 |
| 1602 | Velo Growl Legato | 63 | 12 | 65 |
| 1603 | Tenor Max | 63 | 12 | 66 |
| 1604 | SoftTenorSaxLegato | 63 | 12 | 67 |
| 1605 | Baritone Sax | 63 | 12 | 68 |
| 1606 | Baritone | 63 | 12 | 69 |
| 1607 | Hip Bari | 63 | 12 | 70 |
| 1608 | Tenor Section | 63 | 12 | 71 |
| 1609 | Sax Octave Section | 63 | 12 | 72 |
| 1610 | Mixed Sax Section | 63 | 12 | 73 |
| 1611 | Piccolo | 63 | 12 | 74 |
| 1612 | Piccolo Legato | 63 | 12 | 75 |
| 1613 | Flute | 63 | 12 | 76 |
| 1614 | Flute Legato | 63 | 12 | 77 |
| 1615 | Sweet Flute | 63 | 12 | 78 |
| 1616 | Wood Flute | 63 | 12 | 79 |
| 1617 | Tron Flute | 63 | 12 | 80 |
| 1618 | Flootz | 63 | 12 | 81 |
| 1619 | 2 Flutes | 63 | 12 | 82 |
| 1620 | Oboe | 63 | 12 | 83 |
| 1621 | Sweet Oboe Legato | 63 | 12 | 84 |
| 1622 | Oboe Soft Legato | 63 | 12 | 85 |
| 1623 | Clarinet | 63 | 12 | 86 |
| 1624 | Jazzy Cla Legato | 63 | 12 | 87 |
| 1625 | Bassoon 1 | 63 | 12 | 88 |
| 1626 | Bassoon 2 | 63 | 12 | 89 |
| 1627 | English Horn | 63 | 12 | 90 |
| 1628 | Flute & Clari | 63 | 12 | 91 |
| 1629 | 2 Oboes & Bassoon | 63 | 12 | 92 |
| 1630 | Woodwindind Quartet | 63 | 12 | 93 |
| 1631 | Harmonica | 63 | 12 | 94 |
| 1632 | Gentle Harp | 63 | 12 | 95 |
| 1633 | Woody Harp | 63 | 12 | 96 |
| 1634 | Bluz Distort | 63 | 12 | 97 |
| 1635 | Campfire | 63 | 12 | 98 |
| 1636 | Irish Pipe Legato | 63 | 12 | 99 |
| 1637 | Recorder | 63 | 12 | 100 |
| 1638 | Pan Flute | 63 | 12 | 101 |
| 1639 | Shakuhachi | 63 | 12 | 102 |
| 1640 | Whistle | 63 | 12 | 103 |
| 1641 | Ocarina | 63 | 12 | 104 |
| 1642 | Bagpipe | 63 | 12 | 105 |

### Guitar (96)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1643 | Classical | 63 | 12 | 106 |
| 1644 | High Tension | 63 | 12 | 107 |
| 1645 | Sao Paulo | 63 | 12 | 108 |
| 1646 | Barcelona | 63 | 12 | 109 |
| 1647 | Barcelona [Chord] | 63 | 12 | 110 |
| 1648 | Nylon Slide Vel | 63 | 12 | 111 |
| 1649 | NylonHarmonics Vel | 63 | 12 | 112 |
| 1650 | Classical12Strings | 63 | 12 | 113 |
| 1651 | Hip-HopNylonGuitar | 63 | 12 | 114 |
| 1652 | Old Strings | 63 | 12 | 115 |
| 1653 | Mute & Slide Vel | 63 | 12 | 116 |
| 1654 | SteelHarmonics Vel | 63 | 12 | 117 |
| 1655 | Hip-HopSteelGuitar | 63 | 12 | 118 |
| 1656 | Hi Strings | 63 | 12 | 119 |
| 1657 | Two Acoustics | 63 | 12 | 120 |
| 1658 | 2 Steel Strings | 63 | 12 | 121 |
| 1659 | Airy 12 | 63 | 12 | 122 |
| 1660 | Airy 12 [Chord] | 63 | 12 | 123 |
| 1661 | Wide 12 strings | 63 | 12 | 124 |
| 1662 | 12Strings Mono | 63 | 12 | 125 |
| 1663 | Clean El & Ac | 63 | 12 | 126 |
| 1664 | Jazzy Pick | 63 | 12 | 127 |
| 1665 | Melodic Jazz | 63 | 13 | 0 |
| 1666 | Touch Wah | 63 | 13 | 1 |
| 1667 | Baby | 63 | 13 | 2 |
| 1668 | Good Night | 63 | 13 | 3 |
| 1669 | Dynamic Clean | 63 | 13 | 4 |
| 1670 | Single Coil Chorus | 63 | 13 | 5 |
| 1671 | Single Coil Chorus [Chord] | 63 | 13 | 6 |
| 1672 | 1coil Clean | 63 | 13 | 7 |
| 1673 | 1coil Amped Vel | 63 | 13 | 8 |
| 1674 | Distant | 63 | 13 | 9 |
| 1675 | Some Hair | 63 | 13 | 10 |
| 1676 | Hit It Hard | 63 | 13 | 11 |
| 1677 | Paddy Clean | 63 | 13 | 12 |
| 1678 | Dual Coil '65 | 63 | 13 | 13 |
| 1679 | Dual Coil '65 [Chord] | 63 | 13 | 14 |
| 1680 | Dual Coil Amp | 63 | 13 | 15 |
| 1681 | Roto Guitar | 63 | 13 | 16 |
| 1682 | Dual Coil SlideVel | 63 | 13 | 17 |
| 1683 | Dual Coil Slap Vel | 63 | 13 | 18 |
| 1684 | Dual Coil 80sClean | 63 | 13 | 19 |
| 1685 | DualCoil80sCleanMt | 63 | 13 | 20 |
| 1686 | DualCoil80sCleanMt [Chord] | 63 | 13 | 21 |
| 1687 | Mute Guitar | 63 | 13 | 22 |
| 1688 | HIP Mute | 63 | 13 | 23 |
| 1689 | Dual Coil Rotary | 63 | 13 | 24 |
| 1690 | Electric 12Strings | 63 | 13 | 25 |
| 1691 | Rotator | 63 | 13 | 26 |
| 1692 | Middy Tremolo | 63 | 13 | 27 |
| 1693 | Retro Flanger | 63 | 13 | 28 |
| 1694 | Vintage Strum | 63 | 13 | 29 |
| 1695 | Vintage1coilChorus | 63 | 13 | 30 |
| 1696 | Spanky | 63 | 13 | 31 |
| 1697 | Rockabilly | 63 | 13 | 32 |
| 1698 | Surfin' 60s 1coil | 63 | 13 | 33 |
| 1699 | Pedal Steel | 63 | 13 | 34 |
| 1700 | 2 Electrics | 63 | 13 | 35 |
| 1701 | Light Blues | 63 | 13 | 36 |
| 1702 | DualCoil SemiClean | 63 | 13 | 37 |
| 1703 | Breakback Mountain | 63 | 13 | 38 |
| 1704 | Chorus Dist | 63 | 13 | 39 |
| 1705 | Tex Boogie | 63 | 13 | 40 |
| 1706 | Tex Boogie [Chord] | 63 | 13 | 41 |
| 1707 | 59 Combo | 63 | 13 | 42 |
| 1708 | Alternative Rocker | 63 | 13 | 43 |
| 1709 | Grunged Up | 63 | 13 | 44 |
| 1710 | Overdrive Mt&Harmo | 63 | 13 | 45 |
| 1711 | Crunched Up 376 | 63 | 13 | 46 |
| 1712 | Dynamic Amp | 63 | 13 | 47 |
| 1713 | Chuggin' Guitar | 63 | 13 | 48 |
| 1714 | Chugga | 63 | 13 | 49 |
| 1715 | Small Amp | 63 | 13 | 50 |
| 1716 | Small Amp [Chord] | 63 | 13 | 51 |
| 1717 | Metal Mute | 63 | 13 | 52 |
| 1718 | DistortionMt&Harmo | 63 | 13 | 53 |
| 1719 | Cool Drive | 63 | 13 | 54 |
| 1720 | Hard Drive | 63 | 13 | 55 |
| 1721 | Hard Ramp | 63 | 13 | 56 |
| 1722 | Heavy Drive | 63 | 13 | 57 |
| 1723 | No.1 Guitar | 63 | 13 | 58 |
| 1724 | No.1 Guitar [Chord] | 63 | 13 | 59 |
| 1725 | Snake Finger | 63 | 13 | 60 |
| 1726 | Dual Coil BlueLead | 63 | 13 | 61 |
| 1727 | Voodooman | 63 | 13 | 62 |
| 1728 | Killer Whammy | 63 | 13 | 63 |
| 1729 | Latin Lover | 63 | 13 | 64 |
| 1730 | Oct Fuzz Wah | 63 | 13 | 65 |
| 1731 | Dual Coil Lead Wah | 63 | 13 | 66 |
| 1732 | Crunchy Guitar | 63 | 13 | 67 |
| 1733 | Beater | 63 | 13 | 68 |
| 1734 | Mid Drive | 63 | 13 | 69 |
| 1735 | Hard Rocker | 63 | 13 | 70 |
| 1736 | Tough Tube | 63 | 13 | 71 |
| 1737 | Drive Wah | 63 | 13 | 72 |
| 1738 | Guitar Harmonics | 63 | 13 | 73 |

### World (35)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1739 | Sitar 1 | 63 | 13 | 74 |
| 1740 | Sitar 2 | 63 | 13 | 75 |
| 1741 | Sitar 3 | 63 | 13 | 76 |
| 1742 | Tambura | 63 | 13 | 77 |
| 1743 | Banjo 1 | 63 | 13 | 78 |
| 1744 | Banjo 2 | 63 | 13 | 79 |
| 1745 | Shamisen | 63 | 13 | 80 |
| 1746 | Koto | 63 | 13 | 81 |
| 1747 | Baglama | 63 | 13 | 82 |
| 1748 | Saz Feeze | 63 | 13 | 83 |
| 1749 | Kanun | 63 | 13 | 84 |
| 1750 | Kotoun | 63 | 13 | 85 |
| 1751 | Bouzuki | 63 | 13 | 86 |
| 1752 | Where Am I? | 63 | 13 | 87 |
| 1753 | Sakura | 63 | 13 | 88 |
| 1754 | Nomad | 63 | 13 | 89 |
| 1755 | Nomad [Chord] | 63 | 13 | 90 |
| 1756 | Pluk-o-dy | 63 | 13 | 91 |
| 1757 | Kalimba | 63 | 13 | 92 |
| 1758 | Mbira | 63 | 13 | 93 |
| 1759 | Glass Mbira | 63 | 13 | 94 |
| 1760 | Fiddle | 63 | 13 | 95 |
| 1761 | Kemence | 63 | 13 | 96 |
| 1762 | Kemen Wet | 63 | 13 | 97 |
| 1763 | Yayli | 63 | 13 | 98 |
| 1764 | Kawala | 63 | 13 | 99 |
| 1765 | Ney | 63 | 13 | 100 |
| 1766 | Zurna | 63 | 13 | 101 |
| 1767 | Pungi | 63 | 13 | 102 |
| 1768 | Snake Charmer | 63 | 13 | 103 |
| 1769 | Shehnai 1 | 63 | 13 | 104 |
| 1770 | Shehnai 2 | 63 | 13 | 105 |
| 1771 | Mythic Flute | 63 | 13 | 106 |
| 1772 | Didgeridoo | 63 | 13 | 107 |
| 1773 | Kodo | 63 | 13 | 108 |

### Mallet (20)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1774 | Xylophone | 63 | 13 | 109 |
| 1775 | Orch Xylophone | 63 | 13 | 110 |
| 1776 | Marimba | 63 | 13 | 111 |
| 1777 | Orch Marimba | 63 | 13 | 112 |
| 1778 | Soft Marimba | 63 | 13 | 113 |
| 1779 | Glocken | 63 | 13 | 114 |
| 1780 | Orch Glockenspiel | 63 | 13 | 115 |
| 1781 | Vibraphone | 63 | 13 | 116 |
| 1782 | Vibraphone Soft | 63 | 13 | 117 |
| 1783 | Vibes | 63 | 13 | 118 |
| 1784 | Vibes [Chord] | 63 | 13 | 119 |
| 1785 | Vibes Bow | 63 | 13 | 120 |
| 1786 | Celesta | 63 | 13 | 121 |
| 1787 | Ethnic Dream | 63 | 13 | 122 |
| 1788 | Orc Percussion | 63 | 13 | 123 |
| 1789 | Real Timpani | 63 | 13 | 124 |
| 1790 | Timpani + Cymbal | 63 | 13 | 125 |
| 1791 | Steel Drum | 63 | 13 | 126 |
| 1792 | Synth Steel Drum | 63 | 13 | 127 |
| 1793 | Dulcimer | 63 | 14 | 0 |

### Bell (34)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1794 | Metallic Bell | 63 | 14 | 1 |
| 1795 | Twinkle | 63 | 14 | 2 |
| 1796 | Stick Bell | 63 | 14 | 3 |
| 1797 | Ice Bells | 63 | 14 | 4 |
| 1798 | Ice Bells [Chord] | 63 | 14 | 5 |
| 1799 | Bell Ice | 63 | 14 | 6 |
| 1800 | Stack Bell | 63 | 14 | 7 |
| 1801 | J-Pop | 63 | 14 | 8 |
| 1802 | Crystal | 63 | 14 | 9 |
| 1803 | Chorus Bell | 63 | 14 | 10 |
| 1804 | Handbell | 63 | 14 | 11 |
| 1805 | Bell Chiff | 63 | 14 | 12 |
| 1806 | Bell Chiff [Chord] | 63 | 14 | 13 |
| 1807 | Sako Bell | 63 | 14 | 14 |
| 1808 | Nice Bell | 63 | 14 | 15 |
| 1809 | Noisy Bell | 63 | 14 | 16 |
| 1810 | Pop Bells & Pad | 63 | 14 | 17 |
| 1811 | Pop Bells & Pad [Chord] | 63 | 14 | 18 |
| 1812 | Digibox | 63 | 14 | 19 |
| 1813 | Nibelungen | 63 | 14 | 20 |
| 1814 | Wood Bell | 63 | 14 | 21 |
| 1815 | Marimbell | 63 | 14 | 22 |
| 1816 | Gamelan | 63 | 14 | 23 |
| 1817 | Mystic Bowl | 63 | 14 | 24 |
| 1818 | Island Bell | 63 | 14 | 25 |
| 1819 | Tibetan | 63 | 14 | 26 |
| 1820 | Tibetan [Chord] | 63 | 14 | 27 |
| 1821 | Rimba Bells | 63 | 14 | 28 |
| 1822 | Lost in Asia | 63 | 14 | 29 |
| 1823 | Music Box | 63 | 14 | 30 |
| 1824 | Tinkle Bell | 63 | 14 | 31 |
| 1825 | Tubular Bells 1 | 63 | 14 | 32 |
| 1826 | Tubular Bells 2 | 63 | 14 | 33 |
| 1827 | Timp/Bell/Glocken | 63 | 14 | 34 |

### Rhythmic (64)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1828 | Bass Morpher [Arp] | 63 | 14 | 35 |
| 1829 | Fat Sine Resonance [Arp] | 63 | 14 | 36 |
| 1830 | Boogie A Legato [Arp] | 63 | 14 | 37 |
| 1831 | Long Spit [Arp] | 63 | 14 | 38 |
| 1832 | Acidd [Arp] | 63 | 14 | 39 |
| 1833 | West Coast [Arp] | 63 | 14 | 40 |
| 1834 | Keep Dancin' [Arp] | 63 | 14 | 41 |
| 1835 | Phat Step [Arp] | 63 | 14 | 42 |
| 1836 | Short SequenceBass [Arp] | 63 | 14 | 43 |
| 1837 | Upright [Arp] | 63 | 14 | 44 |
| 1838 | Slap Switch [Arp] | 63 | 14 | 45 |
| 1839 | Multi Saw DA [Arp] | 63 | 14 | 46 |
| 1840 | Saw Lead [Arp] | 63 | 14 | 47 |
| 1841 | Airy Nylon [Arp] | 63 | 14 | 48 |
| 1842 | Rezz Punch [Arp] | 63 | 14 | 49 |
| 1843 | W Phaser [Arp] | 63 | 14 | 50 |
| 1844 | Noiz Rezz [Arp] | 63 | 14 | 51 |
| 1845 | Hip Voice [Arp] | 63 | 14 | 52 |
| 1846 | Hyper Trance [Arp] | 63 | 14 | 53 |
| 1847 | EDM Talker [Arp] | 63 | 14 | 54 |
| 1848 | Space Lead [Arp] | 63 | 14 | 55 |
| 1849 | Square Lead [Arp] | 63 | 14 | 56 |
| 1850 | ProgressiveRk Lead [Arp] | 63 | 14 | 57 |
| 1851 | Opening [Arp] | 63 | 14 | 58 |
| 1852 | Feeling [Arp] | 63 | 14 | 59 |
| 1853 | Mini Three [Arp] | 63 | 14 | 60 |
| 1854 | Nyquist [Arp] | 63 | 14 | 61 |
| 1855 | HPF Dance [Arp] | 63 | 14 | 62 |
| 1856 | Glasgow [Arp] | 63 | 14 | 63 |
| 1857 | House Piano [Arp] | 63 | 14 | 64 |
| 1858 | Vintage Case [Arp] | 63 | 14 | 65 |
| 1859 | Bell Chorus [Arp] | 63 | 14 | 66 |
| 1860 | PhaserClavi Mt [Arp] | 63 | 14 | 67 |
| 1861 | Marimba DX [Arp] | 63 | 14 | 68 |
| 1862 | Rocky [Arp] | 63 | 14 | 69 |
| 1863 | Crunchy [Arp] | 63 | 14 | 70 |
| 1864 | Walking Bass [Arp] | 63 | 14 | 71 |
| 1865 | Accordion [Arp] | 63 | 14 | 72 |
| 1866 | Perc Pad [Arp] | 63 | 14 | 73 |
| 1867 | Almighty [Arp] | 63 | 14 | 74 |
| 1868 | SymphonicPizzicato [Arp] | 63 | 14 | 75 |
| 1869 | Noble Pad [Arp] | 63 | 14 | 76 |
| 1870 | Trumpet [Arp] | 63 | 14 | 77 |
| 1871 | MediumBrassSection [Arp] | 63 | 14 | 78 |
| 1872 | Finale [Arp] | 63 | 14 | 79 |
| 1873 | Alto [Arp] | 63 | 14 | 80 |
| 1874 | Sao Paulo [Arp] | 63 | 14 | 81 |
| 1875 | Hip-HopNylonGuitar [Arp] | 63 | 14 | 82 |
| 1876 | Hip-HopSteelGuitar [Arp] | 63 | 14 | 83 |
| 1877 | Wide 12 strings [Arp] | 63 | 14 | 84 |
| 1878 | Baby [Arp] | 63 | 14 | 85 |
| 1879 | Dual Coil Amp [Arp] | 63 | 14 | 86 |
| 1880 | HIP Mute [Arp] | 63 | 14 | 87 |
| 1881 | Chorus Dist [Arp] | 63 | 14 | 88 |
| 1882 | Dynamic Amp [Arp] | 63 | 14 | 89 |
| 1883 | DistortionMt&Harmo [Arp] | 63 | 14 | 90 |
| 1884 | Heavy Drive [Arp] | 63 | 14 | 91 |
| 1885 | Banjo 2 [Arp] | 63 | 14 | 92 |
| 1886 | Sakura [Arp] | 63 | 14 | 93 |
| 1887 | Orch Xylophone [Arp] | 63 | 14 | 94 |
| 1888 | Celesta [Arp] | 63 | 14 | 95 |
| 1889 | J-Pop [Arp] | 63 | 14 | 96 |
| 1890 | Nibelungen [Arp] | 63 | 14 | 97 |
| 1891 | Lost in Asia [Arp] | 63 | 14 | 98 |

### SFX (41)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1892 | Blaster Beam | 63 | 14 | 99 |
| 1893 | InsideTheWormhole | 63 | 14 | 100 |
| 1894 | Men In Yellow | 63 | 14 | 101 |
| 1895 | Metamorphosis | 63 | 14 | 102 |
| 1896 | Perplex | 63 | 14 | 103 |
| 1897 | Outer Planet | 63 | 14 | 104 |
| 1898 | Industrial | 63 | 14 | 105 |
| 1899 | Space Walking | 63 | 14 | 106 |
| 1900 | Scraper | 63 | 14 | 107 |
| 1901 | SE 02 <Zero Two> | 63 | 14 | 108 |
| 1902 | Talking Machines | 63 | 14 | 109 |
| 1903 | Tobi Mage | 63 | 14 | 110 |
| 1904 | Bitzz | 63 | 14 | 111 |
| 1905 | Toda | 63 | 14 | 112 |
| 1906 | Auto Trapeze | 63 | 14 | 113 |
| 1907 | Harpist'sNightmare | 63 | 14 | 114 |
| 1908 | Find Newgt! | 63 | 14 | 115 |
| 1909 | Nile River | 63 | 14 | 116 |
| 1910 | New Age Atmo | 63 | 14 | 117 |
| 1911 | Wind Blows | 63 | 14 | 118 |
| 1912 | Fire! | 63 | 14 | 119 |
| 1913 | Scratching Machine | 63 | 14 | 120 |
| 1914 | Goa Psyche | 63 | 14 | 121 |
| 1915 | WaitForBadWeather | 63 | 14 | 122 |
| 1916 | Reverse The Audio | 63 | 14 | 123 |
| 1917 | Radio Static | 63 | 14 | 124 |
| 1918 | Surveillance | 63 | 14 | 125 |
| 1919 | Noise FX | 63 | 14 | 126 |
| 1920 | Sample&HoldVintage | 63 | 14 | 127 |
| 1921 | Lazerzz | 63 | 15 | 0 |
| 1922 | On The Fritz | 63 | 15 | 1 |
| 1923 | Argentina | 63 | 15 | 2 |
| 1924 | Reverse Cymbal | 63 | 15 | 3 |
| 1925 | Fret Noise | 63 | 15 | 4 |
| 1926 | Breath Noiz | 63 | 15 | 5 |
| 1927 | Seashore | 63 | 15 | 6 |
| 1928 | Tweet | 63 | 15 | 7 |
| 1929 | Telephone 2 | 63 | 15 | 8 |
| 1930 | Helicopter 1 | 63 | 15 | 9 |
| 1931 | Applause | 63 | 15 | 10 |
| 1932 | Gunshot 2 | 63 | 15 | 11 |

## DX sounds (100)


### Bass (13)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1933 | FM Lo-Fi Bass | 63 | 15 | 12 |
| 1934 | FM Up Bass | 63 | 15 | 13 |
| 1935 | FM Ducking Bass | 63 | 15 | 14 |
| 1936 | FM Amp Sub | 63 | 15 | 15 |
| 1937 | FM Decay Bass | 63 | 15 | 16 |
| 1938 | Wobble Bass | 63 | 15 | 17 |
| 1939 | FM Dark Bass | 63 | 15 | 18 |
| 1940 | Beep Bass | 63 | 15 | 19 |
| 1941 | Feel It | 63 | 15 | 20 |
| 1942 | Attack Bass | 63 | 15 | 21 |
| 1943 | FM Jet Bass | 63 | 15 | 22 |
| 1944 | FM Bold Bass | 63 | 15 | 23 |
| 1945 | FM Metal Dissonant | 63 | 15 | 24 |

### Synth Lead (14)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1946 | FM Metallic Lead | 63 | 15 | 25 |
| 1947 | FM Square and 5th Saw | 63 | 15 | 26 |
| 1948 | Dyna Lead | 63 | 15 | 27 |
| 1949 | Mo Dem Lead | 63 | 15 | 28 |
| 1950 | Bit Tune | 63 | 15 | 29 |
| 1951 | Bleep Clv | 63 | 15 | 30 |
| 1952 | Uni Lead | 63 | 15 | 31 |
| 1953 | FM Chorus 5th Lead | 63 | 15 | 32 |
| 1954 | FM Square Module | 63 | 15 | 33 |
| 1955 | FM Lil Dist Airy | 63 | 15 | 34 |
| 1956 | FM Ring Lead | 63 | 15 | 35 |
| 1957 | FM Pan Trem Lead | 63 | 15 | 36 |
| 1958 | FM Saw Bright | 63 | 15 | 37 |
| 1959 | FM Crush Computer | 63 | 15 | 38 |

### Piano (4)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1960 | FM Simple Piano | 63 | 15 | 39 |
| 1961 | FM B Piano | 63 | 15 | 40 |
| 1962 | FM B Piano [Chord] | 63 | 15 | 41 |
| 1963 | FM Clavi Piano | 63 | 15 | 42 |

### Keyboard (9)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1964 | Legend EP | 63 | 15 | 43 |
| 1965 | Legend EP [Chord] | 63 | 15 | 44 |
| 1966 | Wood EP | 63 | 15 | 45 |
| 1967 | Wood EP [Chord] | 63 | 15 | 46 |
| 1968 | Wood EP Tremolo | 63 | 15 | 47 |
| 1969 | Crystal EP | 63 | 15 | 48 |
| 1970 | FM Chorus Jazz EP | 63 | 15 | 49 |
| 1971 | FM Clear EP | 63 | 15 | 50 |
| 1972 | DigiChord | 63 | 15 | 51 |

### Organ (3)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1973 | Cheez Organ | 63 | 15 | 52 |
| 1974 | FM Rotate Organ | 63 | 15 | 53 |
| 1975 | FM Pipe A | 63 | 15 | 54 |

### Pad (16)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1976 | FM 5th Atmosphere | 63 | 15 | 55 |
| 1977 | FM Glass Dream | 63 | 15 | 56 |
| 1978 | FM Glass Dream [Chord] | 63 | 15 | 57 |
| 1979 | Motion Pad | 63 | 15 | 58 |
| 1980 | Begin Sweep | 63 | 15 | 59 |
| 1981 | Cloud Pad | 63 | 15 | 60 |
| 1982 | Sol Phase | 63 | 15 | 61 |
| 1983 | Flying Kode | 63 | 15 | 62 |
| 1984 | AlTi Pad | 63 | 15 | 63 |
| 1985 | Star Pad | 63 | 15 | 64 |
| 1986 | FM Warm Pad | 63 | 15 | 65 |
| 1987 | FM Warm Pad [Chord] | 63 | 15 | 66 |
| 1988 | FM Glass Harp | 63 | 15 | 67 |
| 1989 | FM Slow Phaser Pad | 63 | 15 | 68 |
| 1990 | FM Ambient Pad | 63 | 15 | 69 |
| 1991 | FM Strings Pad | 63 | 15 | 70 |

### Strings (2)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1992 | FM Strings | 63 | 15 | 71 |
| 1993 | FM Cold Strings | 63 | 15 | 72 |

### Brass (6)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1994 | FM Soft Brass | 63 | 15 | 73 |
| 1995 | FM Digital Brass | 63 | 15 | 74 |
| 1996 | FM Brass | 63 | 15 | 75 |
| 1997 | FM Hit Brass | 63 | 15 | 76 |
| 1998 | FM Hit Brass [Chord] | 63 | 15 | 77 |
| 1999 | FM Fun Brass | 63 | 15 | 78 |

### Woodwind (2)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2000 | FM Chorus Flute | 63 | 15 | 79 |
| 2001 | FM Sax | 63 | 15 | 80 |

### Guitar (5)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2002 | FM Chorus Guitar | 63 | 15 | 81 |
| 2003 | FM Chorus Guitar [Chord] | 63 | 15 | 82 |
| 2004 | FM Wah Guitar | 63 | 15 | 83 |
| 2005 | FM Dist Guitar | 63 | 15 | 84 |
| 2006 | Ambi Pluck | 63 | 15 | 85 |

### World (3)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2007 | FM Koto | 63 | 15 | 86 |
| 2008 | FM Shamisen | 63 | 15 | 87 |
| 2009 | FM Sitar | 63 | 15 | 88 |

### Mallet (3)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2010 | FM Echo Mallet | 63 | 15 | 89 |
| 2011 | Tin Perc | 63 | 15 | 90 |
| 2012 | FM Marimba | 63 | 15 | 91 |

### Bell (3)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2013 | FM Tubular Bells | 63 | 15 | 92 |
| 2014 | FM Tubular Bells [Chord] | 63 | 15 | 93 |
| 2015 | Future Bell | 63 | 15 | 94 |

### Rhythmic (14)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2016 | FM Decay Bass [Arp] | 63 | 15 | 95 |
| 2017 | FM Dark Bass [Arp] | 63 | 15 | 96 |
| 2018 | Mo Dem Lead [Arp] | 63 | 15 | 97 |
| 2019 | Bit Tune [Arp] | 63 | 15 | 98 |
| 2020 | Uni Lead [Arp] | 63 | 15 | 99 |
| 2021 | FM Simple Piano [Arp] | 63 | 15 | 100 |
| 2022 | Legend EP [Arp] | 63 | 15 | 101 |
| 2023 | Wood EP [Arp] | 63 | 15 | 102 |
| 2024 | Star Pad [Arp] | 63 | 15 | 103 |
| 2025 | FM Brass [Arp] | 63 | 15 | 104 |
| 2026 | Ambi Pluck [Arp] | 63 | 15 | 105 |
| 2027 | FM Echo Mallet [Arp] | 63 | 15 | 106 |
| 2028 | Tin Perc [Arp] | 63 | 15 | 107 |
| 2029 | FM Marimba [Arp] | 63 | 15 | 108 |

### SFX (3)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 2030 | D'n Beats | 63 | 15 | 109 |
| 2031 | Buzz Siren | 63 | 15 | 110 |
| 2032 | Chopper | 63 | 15 | 111 |

## SAMPLER sounds (392)


### Vocal Count (24)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 1 | Female Count 1 | 62 | 0 | 0 |
| 2 | Female Count 2 | 62 | 0 | 1 |
| 3 | Female Count 3 | 62 | 0 | 2 |
| 4 | Female Count 4 | 62 | 0 | 3 |
| 5 | Female Count 5 | 62 | 0 | 4 |
| 6 | Female Count 6 | 62 | 0 | 5 |
| 7 | Female Count 7 | 62 | 0 | 6 |
| 8 | Female Count 8 | 62 | 0 | 7 |
| 9 | Male Count 1 A | 62 | 0 | 8 |
| 10 | Male Count 2 A | 62 | 0 | 9 |
| 11 | Male Count 3 A | 62 | 0 | 10 |
| 12 | Male Count 4 A | 62 | 0 | 11 |
| 13 | Male Count 5 A | 62 | 0 | 12 |
| 14 | Male Count 6 A | 62 | 0 | 13 |
| 15 | Male Count 7 A | 62 | 0 | 14 |
| 16 | Male Count 8 A | 62 | 0 | 15 |
| 17 | Male Count 1 B | 62 | 0 | 16 |
| 18 | Male Count 2 B | 62 | 0 | 17 |
| 19 | Male Count 3 B | 62 | 0 | 18 |
| 20 | Male Count 4 B | 62 | 0 | 19 |
| 21 | Male Count 5 B | 62 | 0 | 20 |
| 22 | Male Count 6 B | 62 | 0 | 21 |
| 23 | Male Count 7 B | 62 | 0 | 22 |
| 24 | Male Count 8 B | 62 | 0 | 23 |

### Vocal Phrase / Chant (51)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 25 | Female Vocal - Ha | 62 | 0 | 24 |
| 26 | Female Vocal - Yo | 62 | 0 | 25 |
| 27 | Female Vocal - Hey | 62 | 0 | 26 |
| 28 | Female Vocal - Oh | 62 | 0 | 27 |
| 29 | Female Vocal - Money | 62 | 0 | 28 |
| 30 | Female Vocal - Go | 62 | 0 | 29 |
| 31 | Male Vocal - Yo | 62 | 0 | 30 |
| 32 | Male Vocal - Oh | 62 | 0 | 31 |
| 33 | Male Vocal - Uh 1 | 62 | 0 | 32 |
| 34 | Male Vocal - Go | 62 | 0 | 33 |
| 35 | Male Vocal- Whooh | 62 | 0 | 34 |
| 36 | Male Vocal - Hey | 62 | 0 | 35 |
| 37 | Male Vocal - OK | 62 | 0 | 36 |
| 38 | Male Vocal - Say What | 62 | 0 | 37 |
| 39 | Male Vocal - Big Up | 62 | 0 | 38 |
| 40 | Male Vocal - Let's Go | 62 | 0 | 39 |
| 41 | Male Vocal - Hey - Loud | 62 | 0 | 40 |
| 42 | Male Vocal - Ooh - Loud | 62 | 0 | 41 |
| 43 | Male Vocal - Wow - Loud | 62 | 0 | 42 |
| 44 | Male Vocal - Bon | 62 | 0 | 43 |
| 45 | Male Vocal - Get Funky | 62 | 0 | 44 |
| 46 | Male Vocal - Ow | 62 | 0 | 45 |
| 47 | Male Vocal - Uh 2 | 62 | 0 | 46 |
| 48 | Group Vocal - Ah uh | 62 | 0 | 47 |
| 49 | Group Vocal - Hey | 62 | 0 | 48 |
| 50 | Group Vocal - R U Ready? | 62 | 0 | 49 |
| 51 | Group Vocal - Check It Out | 62 | 0 | 50 |
| 52 | Group Vocal - Come On | 62 | 0 | 51 |
| 53 | Group Vocal - Here We Go | 62 | 0 | 52 |
| 54 | Group Vocal - Ho ho | 62 | 0 | 53 |
| 55 | Group Vocal- Ho ho uh uh | 62 | 0 | 54 |
| 56 | Group Vocal - Wussup | 62 | 0 | 55 |
| 57 | Group Vocal - You You You | 62 | 0 | 56 |
| 58 | Japanese Chant 1 | 62 | 0 | 57 |
| 59 | Japanese Chant 2 | 62 | 0 | 58 |
| 60 | Japanese Chant 3 | 62 | 0 | 59 |
| 61 | Japanese Chant 4 | 62 | 0 | 60 |
| 62 | Japanese Chant 5 | 62 | 0 | 61 |
| 63 | Japanese Chant 6 | 62 | 0 | 62 |
| 64 | Japanese Chant 7 | 62 | 0 | 63 |
| 65 | Japanese Chant 8 | 62 | 0 | 64 |
| 66 | Japanese Chant 9 | 62 | 0 | 65 |
| 67 | Japanese Chant 10 | 62 | 0 | 66 |
| 68 | Japanese Chant 11 | 62 | 0 | 67 |
| 69 | Japanese Chant 12 | 62 | 0 | 68 |
| 70 | Japanese Chant 13 | 62 | 0 | 69 |
| 71 | Japanese Chant 14 | 62 | 0 | 70 |
| 72 | Japanese Chant 15 | 62 | 0 | 71 |
| 73 | Japanese Chant 16 | 62 | 0 | 72 |
| 74 | Japanese Chant 17 | 62 | 0 | 73 |
| 75 | Japanese Chant 18 | 62 | 0 | 74 |

### Singing Vocal (23)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 76 | Singing - Female - Ah 1 | 62 | 0 | 75 |
| 77 | Singing - Female - Ah 2 | 62 | 0 | 76 |
| 78 | Singing - Female - Ai | 62 | 0 | 77 |
| 79 | Singing - Female - La ah ah | 62 | 0 | 78 |
| 80 | Singing - Female - Woo la | 62 | 0 | 79 |
| 81 | Singing - Female - Aw oh | 62 | 0 | 80 |
| 82 | Singing - Female - Ha ah 1 | 62 | 0 | 81 |
| 83 | Singing - Female - Haaaah | 62 | 0 | 82 |
| 84 | Singing - Male - Ah ah | 62 | 0 | 83 |
| 85 | Singing - Male - Oh oh woo | 62 | 0 | 84 |
| 86 | Singing - Male - La a a a | 62 | 0 | 85 |
| 87 | Singing - Male - Ah | 62 | 0 | 86 |
| 88 | Singing - Male - Hooo | 62 | 0 | 87 |
| 89 | Singing - Male - Hee | 62 | 0 | 88 |
| 90 | Singing - Male - Uu | 62 | 0 | 89 |
| 91 | Singing - Male - Everyday | 62 | 0 | 90 |
| 92 | Singing - Male - Every Night | 62 | 0 | 91 |
| 93 | Singing - Male - Yeeaaah | 62 | 0 | 92 |
| 94 | Singing - Male - Oh wo | 62 | 0 | 93 |
| 95 | Singing - Male - Oh wowo ah | 62 | 0 | 94 |
| 96 | Singing - Male - Yeah ah ah | 62 | 0 | 95 |
| 97 | Singing - Female - Ha ah 2 | 62 | 0 | 96 |
| 98 | Singing - Female - La la la la la | 62 | 0 | 97 |

### Robotic Vocal / Effect (21)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 99 | High pitched vocal - Ah | 62 | 0 | 98 |
| 100 | High pitched vocal - Top | 62 | 0 | 99 |
| 101 | Vocoder Beat The Band | 62 | 0 | 100 |
| 102 | Vocoder Love Is Blind | 62 | 0 | 101 |
| 103 | Vocoder Freezing Cold | 62 | 0 | 102 |
| 104 | Vocoder Destiny | 62 | 0 | 103 |
| 105 | Vocoder Forbidden Dreams | 62 | 0 | 104 |
| 106 | Vocoder Enjoying This | 62 | 0 | 105 |
| 107 | Vocoder Desperation | 62 | 0 | 106 |
| 108 | Vocoder Born Happy | 62 | 0 | 107 |
| 109 | Vocoder Day Life | 62 | 0 | 108 |
| 110 | Vocoder Reality | 62 | 0 | 109 |
| 111 | Vocoder Dreamin Of U | 62 | 0 | 110 |
| 112 | Vocoder Complicated | 62 | 0 | 111 |
| 113 | Vocoder Mystery | 62 | 0 | 112 |
| 114 | Vocoder Revolution | 62 | 0 | 113 |
| 115 | Vocoder Sweeping | 62 | 0 | 114 |
| 116 | Vocoder Yesterday | 62 | 0 | 115 |
| 117 | Vocoder Close Eyes | 62 | 0 | 116 |
| 118 | Vocoder Infinity | 62 | 0 | 117 |
| 119 | Vocoder Deepwater | 62 | 0 | 118 |

### Riser (17)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 120 | Riser - Noise 1 | 62 | 0 | 119 |
| 121 | Riser - Synth Lead & Noise 1 | 62 | 0 | 120 |
| 122 | Riser - Synth Lead 1 | 62 | 0 | 121 |
| 123 | Riser - Bubble 1 | 62 | 0 | 122 |
| 124 | Riser - Phase Synth Lead 1 | 62 | 0 | 123 |
| 125 | Riser - Phase Synth Lead 2 | 62 | 0 | 124 |
| 126 | Riser - Panned Synth Lead 1 | 62 | 0 | 125 |
| 127 | Riser - Panned Synth Lead 2 | 62 | 0 | 126 |
| 128 | Riser - Noise 2 | 62 | 0 | 127 |
| 129 | Riser - Bubble 2 | 62 | 1 | 0 |
| 130 | Riser - Noise 3 | 62 | 1 | 1 |
| 131 | Riser - Panned Noise 1 | 62 | 1 | 2 |
| 132 | Riser - Panned Noise 2 | 62 | 1 | 3 |
| 133 | Riser - Panned Noise 3 | 62 | 1 | 4 |
| 134 | Riser - Panned Noise 4 | 62 | 1 | 5 |
| 135 | Riser - Panned Noise 5 | 62 | 1 | 6 |
| 136 | Riser - Panned Noise 6 | 62 | 1 | 7 |

### Laser / Sci-Fi (60)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 137 | Laser - Blast 2 | 62 | 1 | 8 |
| 138 | Laser - Rapid Fire 1 | 62 | 1 | 9 |
| 139 | Laser - Blast 3 | 62 | 1 | 10 |
| 140 | Laser - Blast 4 | 62 | 1 | 11 |
| 141 | Laser - Blast 5 | 62 | 1 | 12 |
| 142 | Laser - Blast 6 | 62 | 1 | 13 |
| 143 | Laser - Blast 7 | 62 | 1 | 14 |
| 144 | Laser - Blast 8 | 62 | 1 | 15 |
| 145 | Noisy Laser - Blast 1 | 62 | 1 | 16 |
| 146 | Laser - Motion 1 | 62 | 1 | 17 |
| 147 | Laser - Rapid Fire 2 | 62 | 1 | 18 |
| 148 | Laser - Rapid Fire 3 | 62 | 1 | 19 |
| 149 | Laser - Flyby 1 | 62 | 1 | 20 |
| 150 | Laser - Echo 1 | 62 | 1 | 21 |
| 151 | Laser - Echo 2 | 62 | 1 | 22 |
| 152 | Laser - Echo 3 | 62 | 1 | 23 |
| 153 | Laser - Fizzer 1 | 62 | 1 | 24 |
| 154 | Laser - Vibration 1 | 62 | 1 | 25 |
| 155 | Laser - Echo 4 | 62 | 1 | 26 |
| 156 | Laser - Fleeting 1 | 62 | 1 | 27 |
| 157 | Laser - Signal 1 | 62 | 1 | 28 |
| 158 | Laser - Signal 2 | 62 | 1 | 29 |
| 159 | Laser - Signal 3 | 62 | 1 | 30 |
| 160 | Laser - Signal 4 | 62 | 1 | 31 |
| 161 | Laser - Signal 5 | 62 | 1 | 32 |
| 162 | Laser - Random Motion 1 | 62 | 1 | 33 |
| 163 | Laser - Signal 6 | 62 | 1 | 34 |
| 164 | Laser - Blast 9 | 62 | 1 | 35 |
| 165 | Sci-Fi - Data Transmission 1 | 62 | 1 | 36 |
| 166 | Sci-Fi - Data Transmission 2 | 62 | 1 | 37 |
| 167 | Sci-Fi - Data Transmission 3 | 62 | 1 | 38 |
| 168 | Laser - Falling 3 | 62 | 1 | 39 |
| 169 | Laser - After Shock 1 | 62 | 1 | 40 |
| 170 | Laser - Falling 4 | 62 | 1 | 41 |
| 171 | Laser - Falling 5 | 62 | 1 | 42 |
| 172 | Laser - Falling 6 | 62 | 1 | 43 |
| 173 | Laser - Falling 7 | 62 | 1 | 44 |
| 174 | Laser - Falling 8 | 62 | 1 | 45 |
| 175 | Laser - Falling 9 | 62 | 1 | 46 |
| 176 | Laser - Blast 10 | 62 | 1 | 47 |
| 177 | Laser - Blast 11 | 62 | 1 | 48 |
| 178 | Laser - Blast 12 | 62 | 1 | 49 |
| 179 | Laser - Echo 5 | 62 | 1 | 50 |
| 180 | Noisy Laser - Echo 1 | 62 | 1 | 51 |
| 181 | Noisy Laser - Echo 2 | 62 | 1 | 52 |
| 182 | Sci-Fi - Data Transmission 4 | 62 | 1 | 53 |
| 183 | Laser - Falling 10 | 62 | 1 | 54 |
| 184 | Laser - Falling 11 | 62 | 1 | 55 |
| 185 | Laser - Falling 12 | 62 | 1 | 56 |
| 186 | Laser - Signal 7 | 62 | 1 | 57 |
| 187 | Sci-Fi - Rapid Fire 1 | 62 | 1 | 58 |
| 188 | Sci-Fi - Detected 2 | 62 | 1 | 59 |
| 189 | Sci-Fi - Access Denied 1 | 62 | 1 | 60 |
| 190 | Sci-Fi - Error 1 | 62 | 1 | 61 |
| 191 | Sci-Fi - Calculation 1 | 62 | 1 | 62 |
| 192 | Sci-Fi - Connecting 1 | 62 | 1 | 63 |
| 193 | Sci-Fi - Deep Signal 1 | 62 | 1 | 64 |
| 194 | Sci-Fi - Deep Signal 2 | 62 | 1 | 65 |
| 195 | Sci-Fi - Deep Dive 1 | 62 | 1 | 66 |
| 196 | Sci-Fi - Deep Dive 2 | 62 | 1 | 67 |

### Impact (12)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 197 | Impact - Dark 1 | 62 | 1 | 68 |
| 198 | Impact - Tom & Cymbal 1 | 62 | 1 | 69 |
| 199 | Impact - Metal Hit 1 | 62 | 1 | 70 |
| 200 | Impact - Metal Hit 2 | 62 | 1 | 71 |
| 201 | Impact - Noise 1 | 62 | 1 | 72 |
| 202 | Impact - Noise 2 | 62 | 1 | 73 |
| 203 | Impact - Noise 3 | 62 | 1 | 74 |
| 204 | Impact - Noise 4 | 62 | 1 | 75 |
| 205 | Impact - Noise 5 | 62 | 1 | 76 |
| 206 | Impact - Noise 6 | 62 | 1 | 77 |
| 207 | Impact - Noise 7 | 62 | 1 | 78 |
| 208 | Impact - Noise 8 | 62 | 1 | 79 |

### Noise / Distorted Sound (34)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 209 | Noise - Fade In 1 | 62 | 1 | 80 |
| 210 | Noise - Fade In 2 | 62 | 1 | 81 |
| 211 | Noise - Fade In 3 | 62 | 1 | 82 |
| 212 | Noise - Explosion 1 | 62 | 1 | 83 |
| 213 | Noise - Explosion 2 | 62 | 1 | 84 |
| 214 | Noise - Explosion 3 | 62 | 1 | 85 |
| 215 | Noise - Explosion 4 | 62 | 1 | 86 |
| 216 | Distorted Hit 1 | 62 | 1 | 87 |
| 217 | Distorted Hit 2 | 62 | 1 | 88 |
| 218 | Distorted Hit 3 | 62 | 1 | 89 |
| 219 | Distorted Hit 4 | 62 | 1 | 90 |
| 220 | Distorted Hit 5 | 62 | 1 | 91 |
| 221 | Distorted Hit 6 | 62 | 1 | 92 |
| 222 | Distorted Hit 7 | 62 | 1 | 93 |
| 223 | Distorted Hit 8 | 62 | 1 | 94 |
| 224 | Distorted Hit 9 | 62 | 1 | 95 |
| 225 | Noise - Blast 1 | 62 | 1 | 96 |
| 226 | Noise - Blast 2 | 62 | 1 | 97 |
| 227 | Noise - Blast 3 | 62 | 1 | 98 |
| 228 | Noise - Blast 4 | 62 | 1 | 99 |
| 229 | Noise - Alert 1 | 62 | 1 | 100 |
| 230 | Noise - Signal 1 | 62 | 1 | 101 |
| 231 | Noise - Signal 2 | 62 | 1 | 102 |
| 232 | Noise - Signal 3 | 62 | 1 | 103 |
| 233 | Noise - Signal 4 | 62 | 1 | 104 |
| 234 | Noise - Passing 1 | 62 | 1 | 105 |
| 235 | Noise - Passing 2 | 62 | 1 | 106 |
| 236 | Noise - Passing 3 | 62 | 1 | 107 |
| 237 | Noise - Passing 4 | 62 | 1 | 108 |
| 238 | Noise - Passing 5 | 62 | 1 | 109 |
| 239 | Noise - Passing 6 | 62 | 1 | 110 |
| 240 | Noise - Take Off 1 | 62 | 1 | 111 |
| 241 | Noise - Take Off 2 | 62 | 1 | 112 |
| 242 | Granular Noise 1 | 62 | 1 | 113 |

### Ambient / Soundscape (12)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 243 | Ambient - Noise 1 | 62 | 1 | 114 |
| 244 | Ambient - Noise 2 | 62 | 1 | 115 |
| 245 | Ambient - Unstable 1 | 62 | 1 | 116 |
| 246 | Ambient - Synth bass 1 | 62 | 1 | 117 |
| 247 | Ambient - Unstable 2 | 62 | 1 | 118 |
| 248 | Ambient - Noise 3 | 62 | 1 | 119 |
| 249 | Ambient - Noise 4 | 62 | 1 | 120 |
| 250 | Ambient - Strings & Noise 1 | 62 | 1 | 121 |
| 251 | Ambient - Strings & Noise 2 | 62 | 1 | 122 |
| 252 | Ambient - Strings 1 | 62 | 1 | 123 |
| 253 | Ambient - Pad & Noise 1 | 62 | 1 | 124 |
| 254 | Ambient - Pad & Noise 2 | 62 | 1 | 125 |

### SFX (14)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 255 | Samba Whistle 1 | 62 | 1 | 126 |
| 256 | Gunshot 3 | 62 | 1 | 127 |
| 257 | Helicopter 2 | 62 | 2 | 0 |
| 258 | Police 1 | 62 | 2 | 1 |
| 259 | Can 1 | 62 | 2 | 2 |
| 260 | Cashier 1 | 62 | 2 | 3 |
| 261 | Gear 1 | 62 | 2 | 4 |
| 262 | Train Whistle 1 | 62 | 2 | 5 |
| 263 | Train Crossing 1 | 62 | 2 | 6 |
| 264 | Zipper 1 | 62 | 2 | 7 |
| 265 | Tongue Clicking 1 | 62 | 2 | 8 |
| 266 | Heart Beat 1 | 62 | 2 | 9 |
| 267 | Water Drop 1 | 62 | 2 | 10 |
| 268 | Metal Hit 1 | 62 | 2 | 11 |

### Scratch (24)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 269 | Scratch 1 | 62 | 2 | 12 |
| 270 | Scratch 2 | 62 | 2 | 13 |
| 271 | Scratch 3 | 62 | 2 | 14 |
| 272 | Scratch 4 | 62 | 2 | 15 |
| 273 | Scratch 5 | 62 | 2 | 16 |
| 274 | Scratch 6 | 62 | 2 | 17 |
| 275 | Scratch 7 | 62 | 2 | 18 |
| 276 | Scratch 8 | 62 | 2 | 19 |
| 277 | Scratch 9 | 62 | 2 | 20 |
| 278 | Scratch 10 | 62 | 2 | 21 |
| 279 | Scratch 11 | 62 | 2 | 22 |
| 280 | Scratch 12 | 62 | 2 | 23 |
| 281 | Scratch 13 | 62 | 2 | 24 |
| 282 | Scratch 14 | 62 | 2 | 25 |
| 283 | Scratch 15 | 62 | 2 | 26 |
| 284 | Scratch 16 | 62 | 2 | 27 |
| 285 | Scratch 17 | 62 | 2 | 28 |
| 286 | Scratch 18 | 62 | 2 | 29 |
| 287 | Scratch 19 | 62 | 2 | 30 |
| 288 | Scratch 20 | 62 | 2 | 31 |
| 289 | Scratch 21 | 62 | 2 | 32 |
| 290 | Scratch 22 | 62 | 2 | 33 |
| 291 | Scratch 23 | 62 | 2 | 34 |
| 292 | Scratch 24 | 62 | 2 | 35 |

### Nature / Animals (8)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 293 | Bird 1 | 62 | 2 | 36 |
| 294 | Bird 2 | 62 | 2 | 37 |
| 295 | Sheep 1 | 62 | 2 | 38 |
| 296 | Lion 1 | 62 | 2 | 39 |
| 297 | Thunder 1 | 62 | 2 | 40 |
| 298 | Thunder 2 | 62 | 2 | 41 |
| 299 | Rain 1 | 62 | 2 | 42 |
| 300 | Rain 2 | 62 | 2 | 43 |

### Hit / Stab / Musical Instrument Sound (19)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 301 | Brass Hit 1 | 62 | 2 | 44 |
| 302 | Brass Hit 2 | 62 | 2 | 45 |
| 303 | Brass Hit 3 | 62 | 2 | 46 |
| 304 | Synth Brass Hit 1 | 62 | 2 | 47 |
| 305 | Synth Brass Hit 2 | 62 | 2 | 48 |
| 306 | Synth Brass Hit 3 | 62 | 2 | 49 |
| 307 | Trumpet HIT 1 | 62 | 2 | 50 |
| 308 | String Hit 1 | 62 | 2 | 51 |
| 309 | Synth Chord Hit 1 | 62 | 2 | 52 |
| 310 | Piano Chord Hit 1 | 62 | 2 | 53 |
| 311 | Piano Chord Hit 2 | 62 | 2 | 54 |
| 312 | Piano Chord Hit 3 | 62 | 2 | 55 |
| 313 | Piano Chord Hit 4 | 62 | 2 | 56 |
| 314 | Guitar Clean - Delay 1 | 62 | 2 | 57 |
| 315 | Guitar Clean - Delay 2 | 62 | 2 | 58 |
| 316 | Guitar Clean - Delay 3 | 62 | 2 | 59 |
| 317 | Guitar Mute 1 | 62 | 2 | 60 |
| 318 | Guitar Mute 2 | 62 | 2 | 61 |
| 319 | Donk Bass 1 | 62 | 2 | 62 |

### Percussion (71)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 320 | Bongo3 High 3 | 62 | 2 | 63 |
| 321 | Bongo3 Low 1 | 62 | 2 | 64 |
| 322 | Bongo4 High 2 | 62 | 2 | 65 |
| 323 | Bongo4 Mid 1 | 62 | 2 | 66 |
| 324 | Bongo4 Low 3 | 62 | 2 | 67 |
| 325 | Analog Conga 1 | 62 | 2 | 68 |
| 326 | Analog Conga 2 | 62 | 2 | 69 |
| 327 | Conga3 High Slap Open 1 | 62 | 2 | 70 |
| 328 | Conga3 High Open 1 | 62 | 2 | 71 |
| 329 | Conga3 High Slap Mute 1 | 62 | 2 | 72 |
| 330 | Conga3 Low Open 1 | 62 | 2 | 73 |
| 331 | Conga3 Low Mute 1 | 62 | 2 | 74 |
| 332 | Repique 1 | 62 | 2 | 75 |
| 333 | Repique Rim 1 | 62 | 2 | 76 |
| 334 | Timbale 3 | 62 | 2 | 77 |
| 335 | Tan-tan Body 1 | 62 | 2 | 78 |
| 336 | Tan-tan Close 1 | 62 | 2 | 79 |
| 337 | Tan-tan Open 1 | 62 | 2 | 80 |
| 338 | Tan-tan Slap 1 | 62 | 2 | 81 |
| 339 | Surdo Mute 3 | 62 | 2 | 82 |
| 340 | Surdo Open 2 | 62 | 2 | 83 |
| 341 | Surdo Stop 2 | 62 | 2 | 84 |
| 342 | High Tom - Standard 1 | 62 | 2 | 85 |
| 343 | Mid Tom - Standard 1 | 62 | 2 | 86 |
| 344 | Low Tom - Standard 1 | 62 | 2 | 87 |
| 345 | Low Tom - Standard 2 | 62 | 2 | 88 |
| 346 | Floor Tom - Standard 1 | 62 | 2 | 89 |
| 347 | Cajon Ghost 1 | 62 | 2 | 90 |
| 348 | Cajon Low 1 | 62 | 2 | 91 |
| 349 | Analog Cowbell 2 | 62 | 2 | 92 |
| 350 | RX11 Cowbell 1 | 62 | 2 | 93 |
| 351 | Acoustic Cowbell 1 | 62 | 2 | 94 |
| 352 | Acoustic Cowbell 2 | 62 | 2 | 95 |
| 353 | Electric Wood Block 1 | 62 | 2 | 96 |
| 354 | Electric Wood Block 2 | 62 | 2 | 97 |
| 355 | Analog Claves 1 | 62 | 2 | 98 |
| 356 | Castanet 1 | 62 | 2 | 99 |
| 357 | Agogo High 2 | 62 | 2 | 100 |
| 358 | Agogo Low 2 | 62 | 2 | 101 |
| 359 | Analog Hand Clap 1 | 62 | 2 | 102 |
| 360 | Open Rim Shot 1 | 62 | 2 | 103 |
| 361 | Punchy Analog Snare 1 | 62 | 2 | 104 |
| 362 | Analog Snare 1 | 62 | 2 | 105 |
| 363 | Distorted Analog Snare 1 | 62 | 2 | 106 |
| 364 | Standard Hand Clap 1 | 62 | 2 | 107 |
| 365 | Electronic Snare 1 | 62 | 2 | 108 |
| 366 | Shaker 16 | 62 | 2 | 109 |
| 367 | Shaker 17 | 62 | 2 | 110 |
| 368 | Shaker 18 | 62 | 2 | 111 |
| 369 | Cabasa 1 | 62 | 2 | 112 |
| 370 | Cabasa 2 | 62 | 2 | 113 |
| 371 | Cabasa 3 | 62 | 2 | 114 |
| 372 | Maracas 1 | 62 | 2 | 115 |
| 373 | Shaker 19 | 62 | 2 | 116 |
| 374 | Tambourine 10 | 62 | 2 | 117 |
| 375 | Guiro 1 | 62 | 2 | 118 |
| 376 | Vibraslap 2 | 62 | 2 | 119 |
| 377 | Reco-reco 2 | 62 | 2 | 120 |
| 378 | Analog Closed Hat 1 | 62 | 2 | 121 |
| 379 | Analog Closed Hat 2 | 62 | 2 | 122 |
| 380 | Electronic Closed Hat 1 | 62 | 2 | 123 |
| 381 | Analog Open Hat 1 | 62 | 2 | 124 |
| 382 | Analog Open Hat 2 | 62 | 2 | 125 |
| 383 | Electronic Open Hat 1 | 62 | 2 | 126 |
| 384 | Ride 1 | 62 | 2 | 127 |
| 385 | Ride 2 | 62 | 3 | 0 |
| 386 | Ride 3 | 62 | 3 | 1 |
| 387 | Ride Brush 1 | 62 | 3 | 2 |
| 388 | Analog Crash 1 | 62 | 3 | 3 |
| 389 | Analog Crash 2 | 62 | 3 | 4 |
| 390 | Analog Glass 1 | 62 | 3 | 5 |

### Recorded Sound (2)

| No. | Name | Bank MSB | Bank LSB | Program |
|---|---|---|---|---|
| 391 | Recorded Sample 1 | 62 | 3 | 6 |
| 392 | Recorded Sample 2 | 62 | 3 | 7 |
