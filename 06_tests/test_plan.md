# Test Plan v0

## Environment

TIA Portal V18, S7-PLCSIM V18 SP2, WinCC Runtime Professional Simulation V18, Python 3.13. Process model inside the PLC (FC_SimulationModel). Faults are injected through simulation control tags and the PLCSIM table. Time acceleration allowed, delays expressed in simulated seconds.

## Simulated field signals

While DB_Sim.Sim_Inputs is TRUE (default), procedures that name a physical input are carried out on the simulation bit: DI_EStop_Sim is DB_Sim.V_EStopOK, DI_P1_Fault is DB_Sim.V_P1FaultOK, DI_P2_Fault is DB_Sim.V_P2FaultOK, DI_Source_Low is DB_Sim.V_SourceLow. All start healthy, so no input needs to be set before a run.

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
| T10 | PLC, collector and dashboard consistency | 024, 025 | V4 | Force known values in the PLC simulation, then a pump fault | Watch table, last CSV row and dashboard show the same values within 2 s, the alarm appears and clears | Capture |
| V4 | Change a variable in PLCSIM | Dashboard and CSV show the same value | Capture |
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
| T25 | Indicator calculation | 026 | V4 | Dataset with known values, unit tests | Indicators equal the hand calculation of the worked example | Command output |
| T26 | Anomaly rules on the datasets | 027 | V5 | Run the rules on the six datasets, compare with the expectation table and the written predictions | Every fault dataset triggers its expected rules, every deviation is explained in the analysis | Command output |
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
| T38 | High current warning | 038 | V2 | P1 running, high current injected | After the delay a warning is raised, the pump keeps running | Capture |
| T39 | Maintenance due | 039 | V2 | Short interval, P1 runs, then maintenance reset | Warning raised, cleared by reset in Maintenance only | Capture |
| T40 | Level not rising | 040 | V2 | Excess drain, pump running 60 s | Warning raised, cleared when the level rises again | Capture |
| T41 | Operator command cleared on mode change | 041 | V3 | Manual, pump 1 commanded and running, switch to Auto, then back to Manual | Command bit cleared, pump does not restart until commanded again | Capture |
| T42 | HMI displays the PLC values | 042 | V3 | Auto cycle running, compare overview and watch table | State, levels, flow, pressure, currents and pump status match | Capture |
| T43 | HMI commands and mode selection | 043 | V3 | Start, Auto, Manual, Stop from the HMI, then conflicting selector, E-stop and reset | States follow the state machine, conflict gives READY, reset refused until the cause is cleared | Capture |
| T44 | Command distinct from feedback | 022 | V3 | Manual, feedback injected off, pump 1 commanded from the HMI | STARTING with command lit and feedback unlit, then UNAVAILABLE after the timeout | Capture |
| T45 | Navigation | 021 | V3 | Press each navigation button | Correct screen opens, header and bar stay | Capture |
| T46 | HMI alarm display | 025 | V3 | Trigger each alarm from the PLC watch table | The alarm appears on the HMI banner with its text and severity color | Capture |
| T47 | HMI navigation | 021 | V3 | Press each navigation button | Correct screen opens, header and bar stay | Capture |
| T48 | HMI trend display | 026 | V3 | Open the trends screen while the pump is running | The curves show the running state and the level rises | Capture |
| T49 | HMI setpoint change | 030 | V3 | Change Level_Low from 30 to 40 | The next pump start happens at 40 percent | Capture |
| T50 | HMI reset behavior | 035 | V3 | Trigger a fault, then press Reset | The alarm clears and the pump can start again | Capture |
| T51 | Export block content and offsets | 049 | V4 | Compare the block to its sources, sample counter, simulated clock, power, ground truth bits | Values equal, counter plus 10 in 10 s, simulated time near plus 600 at acceleration 60, offsets as in the data dictionary | Capture |
| T52 | Collector CSV | 049 | V4 | Frozen values, 15 s run | One row per sample, consecutive counter, no missed sample, values as in the watch table | Capture |
| T53 | Dataset validation | 050 | V4 | Run the validator on the six datasets | All pass, no missed samples | Capture |
| T54 | Frequent starts on simulated time | 018 | V4 | Acceleration 60 normal cycles, then narrow level band | No warning in normal operation, warning with the narrow band | Capture |
| T55 | Stale data indicator | 051 | V4 | Stop the collector, then restart it | STALE shown within 7 s, LIVE again after the restart | Capture |
| T56 | Indicators of the six datasets | 026 | V4 | Summary command on all datasets, compared to the written predictions | Each result explained against the prediction | Command output |
| T57 | Dashboard exposure | 052 | V4 | Listening address check, POST request | Local address only, POST refused | Command output |
| T58 | Rule unit tests | 027, 054 | V5 | Run the unit tests on constructed values | All pass, the rule source names no ground truth column | Command output |
| T59 | Normal dataset stays quiet | 027 | V5 | Count the flags on the normal dataset, read the threshold margins | No flag, margins documented | Command output |
| T60 | Explanations | 053 | V5 | Count flagged periods without an explanation, read three of them | None without explanation, each gives the values and the threshold | Command output |
| T61 | Acceptance UC-01 normal start in Auto | 001, 004 | V6 | Cold start, Auto from the HMI, collector recording | Priority pump starts after the restart delay, feedback confirmed, level rises, no alarm | Capture and CSV |
| T62 | Acceptance UC-02 fill and stop at high level | 002, 006 | V6 | Continue UC-01 up to the high level | Pump stops at 80 percent, the priority passes to the other pump, no alarm | Capture and CSV |
| T63 | Acceptance UC-03 pump failure during operation | 007, 008, 015 | V6 | Auto with pump 1 running, its protection contact opened | Pump 1 stops and is locked out, pump 2 takes over, ALM_006 | Capture and CSV |
| T64 | Acceptance UC-04 source water shortage | 010 | V6 | Pump running, source low signal set | Pump stops, starts inhibited until the source recovers, ALM_002 | Capture and CSV |
| T65 | Acceptance UC-05 low flow detection | 016 | V6 | Pump 1 running, low flow injected | After 10 s pump 1 is unavailable, pump 2 is used, ALM_004 | Capture and CSV |
| T66 | Restore from the release archive | 055 | V6 | Retrieve the project archive into a new folder, rebuild all | Zero compilation errors, one smoke test passes | Capture |
| T67 | Clean clone verification | 055 | V6 | Fresh clone, new virtual environment, verification script in final mode | All checks pass | Command output |
| T68 | HMI emergency stop on a single press | 056 | V6 | Auto, pump running, press EMERGENCY STOP once | Pump stops at once, state FAULT, ALM_001, siren, no confirmation window, reset refused while engaged | Capture |
| T69 | HMI emergency stop release with confirmation | 056 | V6 | From T68, press Release then Cancel, then Release and confirm, then reset and start | Cancel keeps the stop engaged, confirmation clears it, reset gives STOPPED, no pump starts until a new start request | Capture |


## Exit criteria for V2

T03 to T05, T07, T16 to T22, T24, T32, T37 to T40 passed, regression of the V1 tests passed.

## Exit criteria for V4

T10, T25, T29, T51 to T57 passed. No change to the PLC in this iteration, the regression run of the previous iteration remains valid.

## Exit criteria for V5
T26, T58, T59, T60 passed. No change to the PLC in this iteration, the regression of the previous iteration remains valid.

## Exit criteria for V6 and release 1.0

All tests of the final campaign passed on the frozen build, every Must requirement verified, no open defect of severity critical or major, known minor defects listed in the defect log.