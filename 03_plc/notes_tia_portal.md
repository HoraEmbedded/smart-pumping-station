# TIA Portal Notes

## Project

| Item | Value |
| --- | --- |
| Project | SPS_SmartPumping_V1 (TIA Portal V18) |
| Device | PLC_Station, CPU 1214C DC/DC/DC, firmware V4.x (highest available) |
| Signal modules | 2 x SM 1231 AI 4 x 13 bit (slot 2 at %IW64, slot 3 at %IW72) |
| Analog channels | Current 4 to 20 mA, scaled 0 to 27648 |
| Onboard analog inputs | Moved to %IW80 and %IW82, unused |
| Clock memory | Byte MB0, Clock_1Hz = %M0.5 |
| Simulation | S7-PLCSIM V18 SP2 |

## Language and sources

All logic is written in SCL (IEC 61131-3). Sources live in `03_plc/src/` and are imported with Generate blocks from source. After any edit made inside TIA, regenerate the source from the blocks and overwrite the file in the repository. The binary project is not versioned, it is archived in GitHub Releases.

## Naming

| Prefix | Meaning |
| --- | --- |
| OB | Organization block |
| FB / FC | Function block / function |
| DB | Data block |
| DI_ AI_ DO_ | Digital input, analog input, digital output tags |