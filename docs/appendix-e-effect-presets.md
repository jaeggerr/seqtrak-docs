# Appendix E — Effect preset list

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/effect_presets.py`.
> Confidence: `from Yamaha Data List`.


The eight-per-category presets the hardware's effect selection steps through. A preset sets the effect type plus a template number (offset `02` of the effect block) and decides which parameters the three sliders control.

Machine-readable: [`../data/effect-presets.csv`](../data/effect-presets.csv).


## Single effect — FILTER

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | LPF - NO RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 2 | LPF - LOW RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 3 | LPF - MID RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 4 | LPF - HIGH RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 5 | HPF - NO RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 6 | HPF - LOW RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 7 | HPF - MID RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 8 | HPF - HIGH RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |

## Single effect — REVERB

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | SMALL ROOM 1 | SPX ROOM | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 2 | SMALL ROOM 2 | SPX ROOM | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 3 | MID ROOM | SPX ROOM | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 4 | SMALL HALL | SPX HALL | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 5 | MID HALL | SPX HALL | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 6 | STAGE | SPX STAGE | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 7 | GATED REVERB | GATED REVERB | Dry/Wet | Room Size | LPF Cutoff Frequency |
| 8 | REVERSE REVERB | REVERSE REVERB | Dry/Wet | Room Size | LPF Cutoff Frequency |

## Single effect — DELAY

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | TEMPO DELAY 4th | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 2 | PING PONG DELAY 4th | TEMPO CROSS DELAY | Dry/Wet | Delay Time L>R & Delay Time R>L | Feedback |
| 3 | TEMPO DELAY 8th DOT | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 4 | TEMPO DELAY 8th | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 5 | PING PONG DELAY 8th | TEMPO CROSS DELAY | Dry/Wet | Delay Time L>R & Delay Time R>L | Feedback |
| 6 | TEMPO DELAY 16th | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 7 | ANALOG DELAY MODERN | ANALOG DELAY MODERN | Dry/Wet | Delay Time | Feedback |
| 8 | ANALOG DELAY RETRO | ANALOG DELAY RETRO | Dry/Wet | Delay Time | Feedback |

## Single effect — COMPRESSOR

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | COMP - SETTING 1 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 2 | COMP - SETTING 2 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 3 | COMP - SETTING 3 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 4 | COMP - SETTING 4 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 5 | COMP - SETTING 5 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 6 | COMP - SETTING 6 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 7 | COMP - SETTING 7 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 8 | COMP - SETTING 8 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |

## Single effect — DISTORTION

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | WAVE FOLDER – SATURATION | WAVE FOLDER | Dry/Wet | Fold | Input Level |
| 2 | AMP SIMULATOR 2 – SETTING 1 | AMP SIMULATOR 2 | Dry/Wet | Overdrive | LPF Cutoff Frequency |
| 3 | AMP SIMULATOR 2 – SETTING 2 | AMP SIMULATOR 2 | Dry/Wet | Overdrive | LPF Cutoff Frequency |
| 4 | JAZZ COMBO | JAZZ COMBO | Distortion | Depth | Treble |
| 5 | AMP SIMULATOR 1 | AMP SIMULATOR 1 | Dry/Wet | Overdrive | Presence |
| 6 | SMALL STEREO | SMALL STEREO | Dist Drive | Dist Tone | Dist Presence |
| 7 | BIT CRUSHER | BIT CRUSHER | Sample Rate | Bit | Dry/Wet |
| 8 | DIGITAL TURNTABLE | DIGITAL TURNTABLE | Noise Level | Click Level | Dry Send to Noise |

## Single effect — MODULATION

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | SPX CHORUS | SPX CHORUS | Dry/Wet | LFO Speed | LFO Depth |
| 2 | TEMPO FLANGER | TEMPO FLANGER | Dry/Wet | LFO Speed | LFO Depth |
| 3 | TEMPO PHASER | TEMPO PHASER | LFO Depth | LFO Speed | Feedback Level |
| 4 | ENSEMBLE DETUNE | ENSEMBLE DETUNE | Dry/Wet | Detune | Spread |
| 5 | AUTO PAN | AUTO PAN | L/R Depth | LFO Speed | LFO Wave |
| 6 | TREMOLO | TREMOLO | AM Depth | LFO Speed | PM Depth |
| 7 | VCM AUTO WAH | VCM AUTO WAH | Speed | Resonance Offset | Output |
| 8 | RING MODULATOR | RING MODULATOR | Dry/Wet | Osc Freq | LFO Depth |

## Single effect — DUCKER

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | DUCKER - SETTING 1 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 2 | DUCKER - SETTING 2 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 3 | DUCKER - SETTING 3 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 4 | DUCKER - SETTING 4 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 5 | DUCKER - SETTING 5 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 6 | DUCKER - SETTING 6 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 7 | DUCKER - SETTING 7 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 8 | DUCKER - SETTING 8 | UNI COMP DOWN | Side Chain Level | Attack | Release |

## Single effect — OTHER

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | BEAT REPEAT | BEAT REPEAT | Repeat & Length | Gate Time | Freeze |
| 2 | TALKING MODULATOR | TALKING MODULATOR | Vowel | Move Speed | Drive |
| 3 | ROTARY SPEAKER 1-SLOW | ROTARY SPEAKER 1 | Speed Control | Rotor/Horn Balance | Mic L-R Angle |
| 4 | ROTARY SPEAKER 2 - FAST | ROTARY SPEAKER 2 | Speed Control | Rotor/Horn Balance | Modulation Depth |
| 5 | HARMONIC ENHANCER | HARMONIC ENHANCER | Mix Level | Drive | HPF Cutoff Frequency |
| 6 | AUTO SYNTH | AUTO SYNTH | Mod Depth | AM Depth | Delay Level |
| 7 | SLICE | SLICE | Dry/Wet | Gate Time | Divide Type |
| 8 | VINYL BREAK | VINYL BREAK | Break | Speed | Speed Adjust |

## Send effect — REVERB

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | HD ROOM | HD ROOM | Reverb Time | Room Size | Hi Damp Freq |
| 2 | R3 ROOM | R3 ROOM | Reverb Time | Diffusion | LPF Cutoff Frequency |
| 3 | R3 HALL | R3 HALL | Reverb Time | Diffusion | LPF Cutoff Frequency |
| 4 | HD HALL | HD HALL | Reverb Time | Room Size | Hi Damp Freq |
| 5 | R3 PLATE | R3 PLATE | Reverb Time | Diffusion | LPF Cutoff Frequency |
| 6 | HD PLATE | HD PLATE | Reverb Time | Plate Type | Hi Damp Freq |
| 7 | SPX STAGE | SPX STAGE | Reverb Time | Diffusion | LPF Cutoff Frequency |
| 8 | REV-X HALL | REV-X HALL | Reverb Time | Room Size | LPF Cutoff Frequency |

## Send effect — DELAY

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | TEMPO DELAY 4th | TEMPO DELAY STEREO | Delay Time | Feedback | Feedback High Damp |
| 2 | PING PONG DELAY 4th | TEMPO CROSS DELAY | Delay Time L>R & Delay Time R>L | Feedback | Feedback High Damp |
| 3 | TEMPO DELAY 8th DOT | TEMPO DELAY STEREO | Delay Time | Feedback | Feedback High Damp |
| 4 | TEMPO DELAY 8th | TEMPO DELAY STEREO | Delay Time | Feedback | Feedback High Damp |
| 5 | PING PONG DELAY 8th | TEMPO CROSS DELAY | Delay Time L>R & Delay Time R>L | Feedback | Feedback High Damp |
| 6 | TEMPO DELAY 16th | TEMPO DELAY STEREO | Delay Time | Feedback | Feedback High Damp |
| 7 | ANALOG DELAY MODERN | ANALOG DELAY MODERN | Delay Time | Feedback | Delay Input Level |
| 8 | ANALOG DELAY RETRO | ANALOG DELAY RETRO | Delay Time | Feedback | Delay Input Level |

## Master effect — FILTER

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | LPF - NO RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 2 | LPF - LOW RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 3 | LPF - MID RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 4 | LPF - HIGH RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 5 | HPF - NO RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 6 | HPF - LOW RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 7 | HPF - MID RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |
| 8 | HPF - HIGH RESONANCE | CONTROL FILTER | Cutoff | Resonance | Output Level |

## Master effect — REVERB

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | SMALL ROOM 1 | SPX ROOM | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 2 | SMALL ROOM 2 | SPX ROOM | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 3 | MID ROOM | SPX ROOM | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 4 | SMALL HALL | SPX HALL | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 5 | MID HALL | SPX HALL | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 6 | STAGE | SPX STAGE | Dry/Wet | Reverb Time | LPF Cutoff Frequency |
| 7 | GATED REVERB | GATED REVERB | Dry/Wet | Room Size | LPF Cutoff Frequency |
| 8 | REVERSE REVERB | REVERSE REVERB | Dry/Wet | Room Size | LPF Cutoff Frequency |

## Master effect — DELAY

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | TEMPO DELAY 4th | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 2 | PING PONG DELAY 4th | TEMPO CROSS DELAY | Dry/Wet | Delay Time L>R & Delay Time R>L | Feedback |
| 3 | TEMPO DELAY 8th DOT | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 4 | TEMPO DELAY 8th | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 5 | PING PONG DELAY 8th | TEMPO CROSS DELAY | Dry/Wet | Delay Time L>R & Delay Time R>L | Feedback |
| 6 | TEMPO DELAY 16th | TEMPO DELAY STEREO | Dry/Wet | Delay Time | Feedback |
| 7 | ANALOG DELAY MODERN | ANALOG DELAY MODERN | Dry/Wet | Delay Time | Feedback |
| 8 | ANALOG DELAY RETRO | ANALOG DELAY RETRO | Dry/Wet | Delay Time | Feedback |

## Master effect — COMPRESSOR

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | COMP - SETTING 1 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 2 | COMP - SETTING 2 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 3 | COMP - SETTING 3 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 4 | COMP - SETTING 4 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 5 | COMP - SETTING 5 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 6 | COMP - SETTING 6 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 7 | COMP - SETTING 7 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |
| 8 | COMP - SETTING 8 | UNI COMP DOWN | Ratio | Threshold | Make Up Gain |

## Master effect — DISTORTION

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | WAVE FOLDER - SATURATION | WAVE FOLDER | Dry/Wet | Fold | Input Level |
| 2 | COMP DISTORTION | COMP DISTORTION | Dry/Wet | Overdrive | LPF Cutoff Frequency |
| 3 | WAVE FOLDER | WAVE FOLDER | Dry/Wet | Fold | Input Level |
| 4 | AMP SIMULATOR 2 - SETTING 1 | AMP SIMULATOR 2 | Dry/Wet | Overdrive | LPF Cutoff Frequency |
| 5 | AMP SIMULATOR 1 | AMP SIMULATOR 1 | Dry/Wet | Overdrive | Presence |
| 6 | AMP SIMULATOR 2 - SETTING 2 | AMP SIMULATOR 2 | Dry/Wet | Overdrive | LPF Cutoff Frequency |
| 7 | BIT CRUSHER | BIT CRUSHER | Sample Rate | Bit | Dry/Wet |
| 8 | DIGITAL TURNTABLE | DIGITAL TURNTABLE | Noise Level | Click Level | Dry Send to Noise |

## Master effect — MODULATION

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | SPX CHORUS | SPX CHORUS | Dry/Wet | LFO Speed | LFO Depth |
| 2 | TEMPO FLANGER | TEMPO FLANGER | Dry/Wet | LFO Speed | LFO Depth |
| 3 | TEMPO PHASER | TEMPO PHASER | LFO Depth | LFO Speed | Feedback Level |
| 4 | ENSEMBLE DETUNE | ENSEMBLE DETUNE | Dry/Wet | Detune | Spread |
| 5 | AUTO PAN | AUTO PAN | L/R Depth | LFO Speed | LFO Wave |
| 6 | TREMOLO | TREMOLO | AM Depth | LFO Speed | PM Depth |
| 7 | VCM AUTO WAH | VCM AUTO WAH | Speed | Resonance Offset | Output |
| 8 | RING MODULATOR | RING MODULATOR | Dry/Wet | Osc Freq | LFO Depth |

## Master effect — DUCKER

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | DUCKER - SETTING 1 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 2 | DUCKER - SETTING 2 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 3 | DUCKER - SETTING 3 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 4 | DUCKER - SETTING 4 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 5 | DUCKER - SETTING 5 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 6 | DUCKER - SETTING 6 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 7 | DUCKER - SETTING 7 | UNI COMP DOWN | Side Chain Level | Attack | Release |
| 8 | DUCKER - SETTING 8 | UNI COMP DOWN | Side Chain Level | Attack | Release |

## Master effect — OTHER

| Preset | Name | Effect type | Slider 1 | Slider 2 | Slider 3 |
|---|---|---|---|---|---|
| 1 | BEAT REPEAT | BEAT REPEAT | Repeat & Length | Gate Time | Play Speed |
| 2 | TALKING MODULATOR | TALKING MODULATOR | Vowel | Move Speed | Drive |
| 3 | ROTARY SPEAKER 1-SLOW | ROTARY SPEAKER 1 | Speed Control | Rotor/Horn Balance | Mic L-R Angle |
| 4 | ROTARY SPEAKER 2 - FAST | ROTARY SPEAKER 2 | Speed Control | Rotor/Horn Balance | Modulation Depth |
| 5 | HARMONIC ENHANCER | HARMONIC ENHANCER | Mix Level | Drive | HPF Cutoff Frequency |
| 6 | AUTO SYNTH | AUTO SYNTH | Mod Depth | AM Depth | Delay Level |
| 7 | SLICE | SLICE | Dry/Wet | Gate Time | Divide Type |
| 8 | VINYL BREAK | VINYL BREAK | Break | Speed | Speed Adjust |
