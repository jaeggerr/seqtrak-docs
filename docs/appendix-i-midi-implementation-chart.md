# Appendix I — MIDI implementation chart

> **Source**: Yamaha *SEQTRAK Data List* (OS V2.00), transcribed from `reference/SEQTRAK_data_list_En_D0.pdf` by `tools/pdf-extract/misc_tables.py`.
> Confidence: `from Yamaha Data List`.


Yamaha's standard chart, dated 26 September 2023, version 1.0. `O` means supported, `X` not supported.

| Function | | Transmitted | Recognized | Remarks |
|---|---|---|---|---|
| Basic | Default | 1 - 11 | 1 - 11 |  |
| Channel | Changed | X | X |  |
|  | Default | X | 3 |  |
| Mode | Messages | X | 3,4(m=1) *1 |  |
|  | Altered | ************** | X |  |
| Note |  | 0 - 127 | 0 - 127 |  |
| Number : True | voice | ************** | 0 - 127 |  |
| Velocity | Note ON | O 9nH,v=1-127 | O 9nH,v=1-127 |  |
|  | Note OFF | X 8nH,v=0 | X 9nH,v=0 or 8nH |  |
| After | Key's | X | X |  |
| Touch | Ch's | X | X |  |
| Pitch Bend |  | O | O |  |
|  | 0,32 | O | O | Bank Select |
|  | 5 | O | O | Portamento Time |
|  | 7,10 | O | O | Channel Volume,Pan |
|  | 6,38 | X | O | Data Entry |
|  | 11 | X | O | Expression |
|  | 20,21,25-29 | O | O | Model-Specific *2 |
|  | 23,24 | X | O | Model-Specific *2 |
| Control | 64 | X | O | Sustain Switch |
| Change | 65 | O | O | Portamento Switch |
|  | 66 | X | O | Sostenuto |
|  | 71,73-75 | O | O | Sound Control |
|  | 91,94 | O | O | Reverb/Delay Send |
|  | 96,97 | X | O | RPN Inc,Dec |
|  | 100,101 | X | O | RPN LSB,MSB |
|  | 102-119 | O | O | Model-Specific *2 |
|  | 126,127 | X | O | Mono On,Poly On |
| Prog |  | O 0 - 127 *3 | O 0 - 127 *3 |  |
| Change : | True # | ************** | O 0 - 127 *3 |  |
| System | Exclusive | O *3 | O |  |
| : | Song Pos. | X | X |  |
| Common : | Song Sel. | X | X |  |
| : | Tune | X | X |  |
| System : | Clock | O *4 | O *5 |  |
| Real Time : | Commands | O *3 | O |  |
| : All | Sound Off | X | O (120) |  |
| Aux : Reset | All Cntrls | X | O (121) |  |
| : Local | ON/OFF | X | X |  |
| Mes- : All | Notes OFF | X | O (123-125) |  |
| sages: Active | Sense | O | O |  |
| : Reset |  | X | X |  |
| *1 Notes: | m is always | treated as "1" | regardless of its | value. |
| *2 | Please | refer to the manual. |  |  |
| *3 | If switch | is on. |  |  |
| *4 | If clock | out is on and SEQTRAK | uses the internal | clock. |
| *5 | If MIDI | sync is "MIDI(Auto)". |  |  |
