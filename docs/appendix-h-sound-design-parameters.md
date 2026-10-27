# Appendix H — Sound design parameter list

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/misc_tables.py`.
> Confidence: `from Yamaha Data List`.


What each hardware knob page edits, per engine, and which of those parameters can be parameter-locked or motion-recorded. This is the bridge between a physical control and the SysEx address that backs it: look the detailed parameter name up in the parameter documents (`03a`-`03g`).

| Engine | Page | Adjustment item | Index display | Scope | Detailed parameter name | Parameter lock / motion recording | Note |
|---|---|---|---|---|---|---|---|
| Drum (Type1: Drum) | 1 | Sound Select | SOUND | - | Bank Select, Program Change |  |  |
| Drum (Type1: Drum) | 1 | Pitch | PITCH | Sound | Note Shift | yes |  |
| Drum (Type1: Drum) | 1 | Pan | PAN | Track | Track Pan | yes |  |
| Drum (Type1: Drum) | 1 | Volume (Velocity*) | VOLUME | Track (Note*) | Track Volume (Note Velocity*) | yes |  |
| Drum (Type1: Drum) | 2 | AEG Attack | ATTACK | Sound | AEG Attack Time | yes |  |
| Drum (Type1: Drum) | 2 | AEG Decay | DECAY | Sound | AEG Decay Time | yes |  |
| Drum (Type1: Drum) | 2 | LP-HP Filter Cutoff | FILTER | Sound | LPF/HPF Cutoff Frequency | yes |  |
| Drum (Type1: Drum) | 2 | LP-HP Filter Resonance | RESONANCE | Sound | LPF/HPF Resonance | yes |  |
| Drum (Type1: Drum) | 3 | Reverb Send | REVERB | Sound | Reverb Send | yes |  |
| Drum (Type1: Drum) | 3 | Delay Send | DELAY | Sound | Variation Send | yes |  |
| Drum (Type1: Drum) | 3 | EQ High Gain | OTHER | Sound | 2bandEQ High Gain | yes |  |
| Drum (Type1: Drum) | 3 | EQ Low Gain | OTHER | Sound | 2bandEQ Low Gain | yes |  |
| Drum (Type2: DrumKit) | 1 | Sound Select | SOUND | - | Element Change |  |  |
| Drum (Type2: DrumKit) | 1 | Pitch | PITCH | Element | Coarse Tune | yes |  |
| Drum (Type2: DrumKit) | 1 | Pan | PAN | Element | Pan | yes |  |
| Drum (Type2: DrumKit) | 1 | Volume | VOLUME | Element | Level (Note Velocity*) | yes | *Parameter Lock |
| Drum (Type2: DrumKit) | 2 | AEG Attack | ATTACK | Element | AEG Attack Time | yes |  |
| Drum (Type2: DrumKit) | 2 | AEG Decay | DECAY | Element | Decay 1/2 Time(*1), Release Time(*2) | yes | *1 Trigger(default), *2 Gate |
| Drum (Type2: DrumKit) | 2 | LP-HP Filter Cutoff | FILTER | Sound | LPF/HPF Cutoff Frequency | yes |  |
| Drum (Type2: DrumKit) | 2 | LP-HP Filter Resonance | RESONANCE | Sound | LPF/HPF Resonance | yes |  |
| Drum (Type2: DrumKit) | 3 | Reverb Send | REVERB | Sound | Reverb Send | yes |  |
| Drum (Type2: DrumKit) | 3 | Delay Send | DELAY | Sound | Variation Send | yes |  |
| Drum (Type2: DrumKit) | 3 | EQ High Gain | OTHER | Sample | EQ2 Gain | yes |  |
| Drum (Type2: DrumKit) | 3 | EQ Low Gain | OTHER | Sample | EQ1 Gain | yes |  |
| Drum (Type3: Synth) | 1 | Sound Select | SOUND | - | Bank Select, Program Change |  |  |
| Drum (Type3: Synth) | 1 | Mono/Poly/Chord | MONO/POLY or CHORD | Sound | Mono/Poly Mode, Chordset Select |  |  |
| Drum (Type3: Synth) | 1 | Pan | PAN | Track | Track Pan | yes |  |
| Drum (Type3: Synth) | 1 | Volume | VOLUME | Track | Track Volume (Note Velocity*1, Sound Volume*2) | yes | *1 Parameter Lock *2 Motion Recording |
| Drum (Type3: Synth) | 2 | AEG Attack | ATTACK | Sound | AEG Attack Time | yes |  |
| Drum (Type3: Synth) | 2 | AEG Decay/Release | DECAY | Sound | AEG Decay/Release Offset | yes |  |
| Drum (Type3: Synth) | 2 | LP-HP Filter Cutoff | FILTER | Sound | LPF/HPF Cutoff Frequency | yes |  |
| Drum (Type3: Synth) | 2 | LP-HP Filter Resonance | RESONANCE | Sound | LPF/HPF Resonance | yes |  |
| Drum (Type3: Synth) | 3 | Reverb Send | REVERB | Sound | Reverb Send | yes |  |
| Drum (Type3: Synth) | 3 | Delay Send | DELAY | Sound | Variation Send | yes |  |
| Drum (Type3: Synth) | 3 | EQ High Gain | OTHER | Sound | 2bandEQ High Gain | yes |  |
| Drum (Type3: Synth) | 3 | EQ Low Gain | OTHER | Sound | 2bandEQ Low Gain | yes |  |
| Drum (Type3: Synth) | 4 | Portamento Time | OTHER | Sound | Portamento Time/Switch | yes |  |
| Drum (Type3: Synth) | 4 | Arpeggiator Type | OTHER | Sound | Arpeggiator Preset/Switch |  |  |
| Drum (Type3: Synth) | 4 | Arpeggiator Gate Time | OTHER | Sound | Arpeggiator Gate Time Rate | yes |  |
| Drum (Type3: Synth) | 4 | Arpeggiator Speed | OTHER | Sound | Arpeggiator Unit |  |  |
| Synth | 1 | Sound Select | SOUND | - | Bank Select, Program Change |  |  |
| Synth | 1 | Mono/Poly/Chord | MONO/POLY or CHORD | Sound | Mono/Poly Mode, Chordset Select |  |  |
| Synth | 1 | Pan | PAN | Track | Track Pan | yes |  |
| Synth | 1 | Volume | VOLUME | Track | Track Volume (Note Velocity*1, Sound Volume*2) | yes | *1 Parameter Lock *2 Motion Recording |
| Synth | 2 | AEG Attack | ATTACK | Sound | AEG Attack Time | yes |  |
| Synth | 2 | AEG Decay/Release | DECAY | Sound | AEG Decay/Release Offset | yes |  |
| Synth | 2 | LP-HP Filter Cutoff | FILTER | Sound | LPF/HPF Cutoff Frequency | yes |  |
| Synth | 2 | LP-HP Filter Resonance | RESONANCE | Sound | LPF/HPF Resonance | yes |  |
| Synth | 3 | Reverb Send | REVERB | Sound | Reverb Send | yes |  |
| Synth | 3 | Delay Send | DELAY | Sound | Variation Send | yes |  |
| Synth | 3 | EQ High Gain | OTHER | Sound | 2bandEQ High Gain | yes |  |
| Synth | 3 | EQ Low Gain | OTHER | Sound | 2bandEQ Low Gain | yes |  |
| Synth | 4 | Portamento Time | OTHER | Sound | Portamento Time/Switch | yes |  |
| Synth | 4 | Arpeggiator Type | OTHER | Sound | Arpeggiator Preset/Switch |  |  |
| Synth | 4 | Arpeggiator Gate Time | OTHER | Sound | Arpeggiator Gate Time Rate | yes |  |
| Synth | 4 | Arpeggiator Speed | OTHER | Sound | Arpeggiator Unit |  |  |
| DX | 1 | Sound Select | SOUND | - | Bank Select, Program Change |  |  |
| DX | 1 | Mono/Poly/Chord | MONO/POLY or CHORD | Sound | Mono/Poly Mode, Chordset Select |  |  |
| DX | 1 | Pan | PAN | Track | Track Pan | yes |  |
| DX | 1 | Volume | VOLUME | Track | Track Volume (Note Velocity*1, Sound Volume*2) | yes | *1 Parameter Lock *2 Motion Recording |
| DX | 2 | AEG Attack | ATTACK | Sound | AEG Attack Time | yes |  |
| DX | 2 | AEG Decay/Release | DECAY | Sound | AEG Decay/Release Offset | yes |  |
| DX | 2 | LP-HP Filter Cutoff | FILTER | Sound | LPF/HPF Cutoff Frequency | yes |  |
| DX | 2 | LP-HP Filter Resonance | RESONANCE | Sound | LPF/HPF Resonance | yes |  |
| DX | 3 | Reverb Send | REVERB | Sound | Reverb Send | yes |  |
| DX | 3 | Delay Send | DELAY | Sound | Variation Send | yes |  |
| DX | 3 | EQ High Gain | OTHER | Sound | 2bandEQ High Gain | yes |  |
| DX | 3 | EQ Low Gain | OTHER | Sound | 2bandEQ Low Gain | yes |  |
| DX | 4 | Portamento Time | OTHER | Sound | Portamento Time | yes | Mono olnly |
| DX | 4 | Arpeggiator Type | OTHER | Sound | Arpeggiator Preset/Switch |  |  |
| DX | 4 | Arpeggiator Gate Time | OTHER | Sound | Arpeggiator Gate Time Rate | yes |  |
| DX | 4 | Arpeggiator Speed | OTHER | Sound | Arpeggiator Unit |  |  |
| DX | 5 | FM Algorithm | OTHER | FM Operator | FM Algorithm | yes |  |
| DX | 5 | Modulator Amount | OTHER | Sound | Mod Amount Offset | yes |  |
| DX | 5 | Modulator Frequency | OTHER | Sound | Freq Ratio Offset | yes |  |
| DX | 5 | Modulator Feedback | OTHER | Sound | Feedback Offset | yes |  |
| SAMPLER | 1 | Sound Select | SOUND | - | Element Change |  |  |
| SAMPLER | 1 | Pitch | PITCH | Element | Coarse Tune | yes |  |
| SAMPLER | 1 | Pan | PAN | Element | Pan | yes |  |
| SAMPLER | 1 | Volume | VOLUME | Element | Level (Note Velocity*) | yes | * Parameter Lock |
| SAMPLER | 2 | AEG Attack | ATTACK | Element | AEG Attack Time | yes |  |
| SAMPLER | 2 | AEG Decay | DECAY | Element | Release Time *1, Decay 1/2 Time *2 | yes | *1 Gate, *2 Trigger |
| SAMPLER | 2 | LP-HP Filter Cutoff | FILTER | Sound | LPF/HPF Cutoff Frequency | yes |  |
| SAMPLER | 2 | LP-HP Filter Resonance | RESONANCE | Sound | LPF/HPF Resonance | yes |  |
| SAMPLER | 3 | Reverb Send | REVERB | Sound | Reverb Send | yes |  |
| SAMPLER | 3 | Delay Send | DELAY | Sound | Variation Send | yes |  |
| SAMPLER | 3 | EQ High Gain | OTHER | Sample | EQ2 Gain | yes |  |
| SAMPLER | 3 | EQ Low Gain | OTHER | Sample | EQ1 Gain | yes |  |
| SAMPLER | 4 | Start Point | OTHER | Sample | Start Point |  |  |
| SAMPLER | 4 | End Point | OTHER | Sample | End Point |  |  |
| SAMPLER | 4 | Loop On/Off | OTHER | Sample | Loop On/Off |  |  |
| SAMPLER | 4 | Loop Length | OTHER | Sample | Loop Length |  |  |
| SAMPLER | 5 | PEG Attack Level | OTHER | Sample | PEG Attack Level | yes |  |
| SAMPLER | 5 | PEG Attack Time | OTHER | Sample | PEG Attack Time | yes |  |
| SAMPLER | 5 | PEG Decay Level | OTHER | Sample | PEG Decay1/Decay2/Release Level | yes |  |
| SAMPLER | 5 | PEG Decay Time | OTHER | Sample | PEG Decay1 Time | yes |  |
