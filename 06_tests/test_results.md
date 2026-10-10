# Test Results - Mission 7 Update

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
| T16 | 2026-10-10 | Pass | evidence/T16_one_pump.png | Mutual exclusion validated, pump 1 takes priority |
| T17 | 2026-10-10 | Pass | evidence/T17_restart_delay.png | Anti-short cycle delay blocks restart for 30 s |
| T18 | 2026-10-10 | Pass | evidence/T18_faulted_pump.png | Pump hardware faults are securely latched until reset |
| T04 | 2026-10-10 | Pass | evidence/T04_backup.png | Automated switchover to backup pump 2 on P1 fault |
| **T05** | 2026-10-10 | Pass | evidence/T05_no_pump.png | Dual fault locks state 90, single reset recovery works |
| T03 | 2026-10-10 | Pass | evidence/T03_alternation.mp4 | Alternation swaps priority between pumps after normal cycle |
| T04b| 2026-10-10 | Pass | evidence/T04b_mid_cycle_takeover.png | **Bonus:** Mid-cycle takeover verified, priority preserved |
