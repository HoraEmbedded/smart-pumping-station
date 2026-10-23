# Final Test Report V6

## Scope

Final test campaign on the frozen build of the Smart Pumping Station, before the v1.0.0 release. Requirements REQ-001 to REQ-056, tests T01 to T69. The campaign covers the PLC logic, the HMI, the data path, the reliability indicators, the anomaly rules, the emergency stop request added at the end of the project, and five end-to-end acceptance scenarios.

## Environment

| Item | Value |
| --- | --- |
| TIA Portal | V18 |
| S7-PLCSIM | V18 SP2 |
| WinCC Runtime Professional | V18 with its OPC UA server |
| Python | 3.13 (packages in `docs/python_environment.txt`) |
| OPC UA client | asyncua, read-only collector |
| Datasets | D01 to D06, collected through the OPC UA collector |

## Results

| Group | Tests | Passed | Failed | Pending |
| --- | --- | --- | --- | --- |
| PLC logic | 31 | 31 | 0 | 0 |
| HMI | 14 | 14 | 0 | 0 |
| Data | 7 | 7 | 0 | 0 |
| Analytics | 6 | 6 | 0 | 0 |
| Process and reproducibility | 6 | 6 | 0 | 0 |
| Acceptance | 5 | 5 | 0 | 0 |
| **All** | **69** | **69** | **0** | **0** |

**Requirements verified: 56 of 56.**

### Acceptance scenarios

| Test | Use case | Result |
| --- | --- | --- |
| T61 | Normal start in Auto | Pass |
| T62 | Fill and stop at the high level | Pass |
| T63 | Pump failure, backup takes over | Pass |
| T64 | Source shortage, starts inhibited | Pass |
| T65 | Low flow, backup takes over | Pass |

### Emergency stop request (added before v1.0.0)

| Test | Subject | Result |
| --- | --- | --- |
| T68 | HMI emergency stop on a single press, no confirmation, latched | Pass |
| T69 | Release with confirmation, cancel keeps the stop engaged | Pass |

### Reproducibility

| Test | Subject | Result |
| --- | --- | --- |
| T28 | Cold start procedure twice, 15 initial values identical | Pass |
| T66 | Restore the project from its release archive in a new folder, rebuild all, zero errors | Pass |
| T67 | Clean clone of the repository, automated verification in final mode, all checks pass | Pass |

## Defects found

| ID | Description | Severity | Resolution |
| --- | --- | --- | --- |
| BUG-001 | Clock tag undefined: clock memory byte enabled in the CPU | Minor | Fixed |
| BUG-002 | Instance data blocks out of date after a block interface change | Minor | Update order documented, fixed |
| BUG-003 | Communication driver error of the HMI connection | Minor | HMI connection recreated, fixed |
| BUG-004 | External S7 reader cannot reach the simulated S7-1200 | Major | Route changed to OPC UA, fixed |
| BUG-005 | OPC UA port closed | Major | Runtime package, certificate authority and IIS set up, fixed |

No new defect was found during the final campaign on the frozen build.

## Regression after the emergency stop change

The HMI emergency stop request was added at the end of the project, after the campaign had started. The change is purely additive: `EStop_Request` is a new `Bool` field (`FALSE` by default), and the line added in `FC_Interlocks` only acts when this bit is `TRUE`. When it is `FALSE`, the behaviour is identical to v0.14.0.

Per DEC-073, a shared block (`DB_HMI`, `FC_Interlocks`) triggers the full level 1 regression. The 24 level 1 tests were replayed: T04 to T09, T15, T22, T35, T37, T23, T43, T46, T47, T48, T10, T28, T61 to T65, T68, T69. All passed. T66 and T67 were done at the end of the campaign, after the last commit and before the tag v1.0.0.

## Release readiness

| Exit criterion | Status |
| --- | --- |
| Every test passed on the frozen build | Met (69 of 69) |
| Every Must requirement verified | Met (56 of 56) |
| No open critical or major defect | Met (none) |
| Minor defects listed in the defect log | Met |
| Cold start, archive restore, clean clone | Met (T28, T66, T67) |

## Open points

- Validation is entirely in simulation: no physical controller or sensor.
- The indicators and the datasets come from a simulation, they illustrate the calculation and are not field statistics.
- Thresholds come from a noiseless simulation: their margins must be measured again on field data.
- The HMI emergency stop request is a supplementary action, the reference emergency stop remains the hardware contact.