# Test Report V2

## Scope

Two-pump control: alternation, backup, interlocks, diagnostics, counters and monitoring. Requirements REQ-005 to REQ-009, REQ-015 to REQ-020, REQ-037 to REQ-040.

## Environment

TIA Portal V18, S7-PLCSIM V18 SP2, process model in the PLC, faults injected through DB_Sim. Protection delays tested in real time.

## Results

| Group | Tests | Result |
| --- | --- | --- |
| Pumps and cycle | T03, T04, T05, T16, T17, T18 | Pass |
| Diagnostics | T07, T22, T37 | Pass |
| Counters and monitoring | T19, T20, T21, T38, T39, T40 | Pass |
| Reviews | T24, T32 | Pass |
| Regression of V1 tests | 21 tests | Pass |

Details and evidence: test_results.md and the evidence folder.

## Open points

- Alarm acknowledgment and the alarm list arrive with the HMI.
- Frequent starts window and maintenance counters are re-checked on the dataset in the analytics phase.



## Defects found

| ID | Description | Resolution |
| --- | --- | --- |
| **DF-001** | Interface mismatch on `FB_ModeManager` (31 compilation errors in OB1). | Updated the `FB_ModeManager` call parameters inside `Main (OB1)` and executed a right-click > "Update block call" on `DB_ModeManager` to synchronize the instance DB. |
| **DF-002** | Wrong operand mapping in `FC_AlarmLatch` Network 4 (`ResetPulse` used instead of `LevelCritCause`). | Replaced the contact variable with `LevelCritCause` in the Ladder block, allowing the critical high-level alarm to correctly set the latch bit. |
| **DF-003** | Missing summary interlock connection for the dual-pump failure flag in Ladder. | Added a fourth parallel branch containing the Normally Open contact `"DB_Alarms".NoPumpLatched` into Network 8 (`Critical summary`) of `FC_AlarmLatch`. |
| **DF-004** | Overriding simulation behavior during the stagnation test (T40). | Frozen the process model calculations by turning `"DB_Sim".Sim_Run` to `FALSE` in order to safely evaluate the level-rise monitoring window without numerical drift. |
