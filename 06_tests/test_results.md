# Test Results

| ID | Date | Result | Evidence | Notes |
| --- | --- | --- | --- | --- |
| T33 | 2026-10-10 | Pass | evidence/T33_init_sequence.png | State 0, 10, 20 after 2 s |
| T34 | 2026-10-10 | Pass | evidence/T34_mode_change.png | Pump stops through READY |
| T01 | 2026-10-10 | Pass | evidence/T01_auto_start_low_level.png | Automated cycle starts at low level |
| T02 | 2026-10-10 | Pass | evidence/T02_stop_high_level.png | Automated cycle stops at high level |
| T11 | 2026-10-10 | Pass | evidence/T11_normal_stop.png | Instant pump cutoff, returns to state 0 |
| T12 | 2026-10-10 | Pass | evidence/T12_reset_no_fault.png | Reset has no effect when no fault exists |
| T27 | 2026-10-10 | Pass | evidence/T27_parameter_edit.png | Immediate threshold update without reload |
| T31 | 2026-10-10 | Pass | Command output | No raw address in sources |
| T06 | 2026-10-10 | Pass | evidence/T06_source_low.png | Interlock active on low source, hysteresis verified at 21% |
| T13 | 2026-10-10 | Pass | evidence/T13_manual_refused.png | HMI command ignored if source low, runs when water returns |
| T14 | 2026-10-10 | Pass | evidence/T14_maintenance.png | Auto mode isolated, manual control authorized |
| T36 | 2026-10-10 | Pass | evidence/T36_test_limit.png | Maintenance pump runtime cutoff triggered after 10 s |
| T08 | 2026-10-10 | Pass | evidence/T08_estop.png | Emergency stop forces state 90, red lamp and siren active |
| T09 | 2026-10-10 | Pass | evidence/T09_reset_before_fix.png | Reset command rejected while E-stop button is pressed |
| T35 | 2026-10-10 | Pass | evidence/T35_no_restart.png | Safe state 0 recovery on reset, no automatic pump restart |
| T15 | 2026-10-10 | Pass | evidence/T15_level_critical.png | Tank overflow (96%) locks state 90, reset allowed below 95% |
| T31b| 2026-10-10 | Pass | evidence/T31_bonus_sensor_fault.png | **Bonus:** Sensor open loop (-600 on %IW64) triggers state 90 |
