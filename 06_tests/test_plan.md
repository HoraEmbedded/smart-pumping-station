# Test Plan v0

## Environment

TIA Portal V18, S7-PLCSIM V18 SP2, WinCC Runtime Professional Simulation V18, Python 3.13. Process model inside the PLC (FC_SimulationModel). Faults are injected through simulation control tags and the PLCSIM table. Time acceleration allowed, delays expressed in simulated seconds.

## Rules

- Every test has an ID, a linked requirement, a release, an expected result and an evidence file.
- Evidence is stored in `06_tests/evidence/` as `Txx_short_name.png` or `.mp4`.
- A test passes only if the expected result is observed, otherwise it is logged as failed with the defect.
- A release is tagged only when all its tests pass.

## Exit criteria for V1

T01, T02, T06, T08, T09, T11, T12, T13, T15, T27, T31 passed.

## Tests

| ID | Test | Req | Rel. | Setup and action | Expected result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | Auto start at low level | 001 | V1 | Auto, source OK, tank level set to 20 percent | Available pump starts, run feedback confirmed | Capture |
| T02 | Stop at high level | 002 | V1 | Pump running, level set to 80 percent | Active pump stops | Capture |
| T03 | Alternation | 006 | V2 | Two normal cycles | Priority P1 then P2 | Video |
| T04 | Backup | 007, 008 | V2 | P1 unavailable, level low | P2 starts, ALM_006 active | Capture |
| T05 | No pump available | 015 | V2 | P1 and P2 unavailable, level low | ALM_009 active, state FAULT | Capture |
| T06 | Source low | 010 | V1 | Source below 15 percent, start requested, then during run | No start, pump stops, ALM_002 | Capture |
| T07 | Low flow P1 | 016 | V2 | P1 running, flow forced to 0 | After 10 s ALM_004, P1 unavailable | Capture |
| T08 | Simulated E-stop | 011 | V1 | Pump running, DI_EStop_Sim set FALSE | Pumps stopped, FAULT, ALM_001 latched | Capture |
| T09 | Reset before correction | 014 | V1 | Fault active, cause present, reset | Fault maintained | Capture |
| T10 | PLC and dashboard consistency | 024, 025 | V4 | Change a variable in PLCSIM | Dashboard and CSV show the same value | Capture |
| T11 | Normal stop | 003, 004 | V1 | Pump running, stop request | Pump stops, state STOPPED | Capture |
| T12 | Reset without fault | 014 | V1 | No fault, reset | No change in behavior | Capture |
| T13 | Manual refused with source low | 013 | V1 | Manual mode, source low, run command | Command refused | Capture |
| T14 | Maintenance mode | 004, 013 | V1 | Maintenance mode, level low | No automatic cycle, interlocks still active | Capture |
| T15 | Critical high level | 012 | V1 | Level forced above 95 percent | Pumps stopped, ALM_003 | Capture |
| T16 | One pump at a time | 005 | V2 | Demand with both pumps available | Never two run commands together | Capture |
| T17 | Restart delay | 009 | V2 | Stop then immediate demand | Restart blocked for 30 s | Capture |
| T18 | Faulted pump cannot start | 008 | V2 | Fault on P1, then on P2, demand | Faulted pump never receives run command | Capture |
| T19 | Counters | 019 | V2 | 3 starts, known runtime | Start count 3, hours match runtime | Capture |
| T20 | Sensor below 4 mA | 017 | V2 | Raw value below the low limit | Value flagged inconsistent, ALM_008 | Capture |
| T21 | Frequent starts | 018 | V2 | Force 4 starts in 60 min simulated | ALM_010 | Capture |
| T22 | Low flow P2 | 016 | V2 | P2 running, flow forced to 0 | After 10 s ALM_005, P2 unavailable | Capture |
| T23 | HMI command versus feedback | 022, 023 | V3 | Command without feedback, acknowledge alarms | Distinct displays, acknowledgment works, refusal message shown | Capture |
| T24 | Alarm matrix completeness | 020 | V2 | Review alarm_matrix.csv | Every alarm has cause, reaction, text, reset | Review note |
| T25 | KPI calculation | 026 | V4 | Dataset with known values | KPIs equal hand calculation | Notebook |
| T26 | Anomaly rules | 027 | V5 | Normal and fault datasets | Fault periods flagged, false positives listed | Notebook |
| T27 | Parameter editing | 028 | V1 | Change low threshold in DB_Parameters | New threshold applied, no logic edit | Capture |
| T28 | Cold start reproducibility | 030 | V6 | Follow launch procedure from scratch | Same initial state each time | Video |
| T29 | Secret scan | 031 | V4 | Search repository for credentials | None found | Command output |
| T30 | HMI screens | 021 | V3 | Open the five screens | All present and navigable | Capture |
| T31 | Code conventions | 029 | V1 | Review blocks and tags | Functional names, commented networks | Review note |
| T32 | Traceability review | 032 | V0 | Run the check on the matrix | Every requirement has a test and every test a requirement | Command output |
| T33 | Initialization sequence | 033 | V1 | Power cycle, start request | State goes 0, 10, then 20 only after Init_Delay_s | Capture |
| T34 | Mode change stops pumps | 034 | V1 | Pump running in Auto, switch selector to Manual | Pump stops, state passes through READY, then Manual | Capture |
| T35 | No restart after reset | 035 | V1 | Cause cleared, reset | State STOPPED, no pump command until a new start request | Capture |
| T36 | Maintenance test limit | 036 | V1 | Maintenance mode, pump test command | Pump stops after Maint_Test_Max_s | Capture |
| T37 | Run feedback timeout | 037 | V2 | Command a pump with feedback forced FALSE | After 5 s ALM_006, pump unavailable | Capture |