# Roadmap

Planned over 14 weeks, one iteration at a time, one commit per step. Source: unified project roadmap.

## Iteration plan

| Iteration | Week | Scope | Tag | Status |
| --- | --- | --- | --- | --- |
| I1 | 1 | Repository foundation and scope | v0.1.0 | Done |
| I2 | 1 to 2 | Process study, P&ID, I/O list, alarm matrix | v0.2.0 | Done |
| I3 | 2 | Requirements, traceability, test plan | v0.3.0 | Done |
| I4 | 3 | Grafcet and state machine | v0.4.0 | Done |
| I5 | 4 | TIA project and V1 level control | v0.5.0 | Done |
| I6 | 5 | Modes, interlocks, critical faults | v0.6.0 | Done|
| I7 | 6 | Two pumps, alternation, backup | v0.7.0 | In progress |
| I8 | 7 | Low flow, current, frequent starts | v0.8.0 | Planned |
| I9 | 8 | HMI overview, commands, alarms | v0.9.0 | Planned |
| I10 | 9 | HMI finalization and operator guide | v0.10.0 | Planned |
| I11 | 10 | Historization and IIoT architecture | v0.11.0 | Planned |
| I12 | 11 | Dashboard and KPI | v0.12.0 | Planned |
| I13 | 12 | Python analytics and anomalies | v0.13.0 | Planned |
| I14 | 13 | Test campaign and regression | v0.14.0 | Planned |
| I15 | 14 | Packaging, report, video | v1.0.0 | Planned |

| Week | Objective | Expected evidence |
| --- | --- | --- |
| 1 | Scope, process architecture, simplified P&ID | Scope, P&ID |
| 2 | Requirements, I/O list, alarm matrix, traceability, test plan before coding | Requirements, I/O, alarms, test plan v0 |
| 3 | Grafcet and state machine | Grafcet PDF, mode and state description |
| 4 | TIA V18 project and V1 single pump control | Tag table, logic screenshots, V1 test report |
| 5 | Manual, Maintenance, simulated E-stop, interlocks | Interlock tests |
| 6 | Two pumps, alternation, backup | Short demo video, V2 test matrix |
| 7 | Low flow, current, frequent starts | Fault tests, causes list |
| 8 | HMI: overview, commands, alarms, maintenance, trends | Screenshots |
| 9 | HMI finalization and operator guide | Guide, demo video |
| 10 | Historization and IIoT architecture | Timestamped CSV |
| 11 | Dashboard and KPI | KPI marked as simulated |
| 12 | Python analysis and explainable anomalies (ANO_01 to ANO_06) | Notebook, charts, limits |
| 13 | Test campaign and regression | Complete test report |
| 14 | Portfolio packaging, report, video | Publishable project |

## File name mapping (roadmap vs repository)

| Roadmap name | Repository file |
| --- | --- |
| project_scope.md, cahier_des_charges.md | 01_requirements/scope.md, requirements.md |
| pid_simplifie.pdf | 02_design/diagrams/pid_simplified.pdf |
| grafcet_station.pdf | 02_design/diagrams/grafcet_station.* |
| mode_state_description.md | 02_design/mode_state_description.md |
| requirements_traceability_matrix.csv | 01_requirements/requirements_traceability_matrix.csv |
| test_plan_v0.md | 06_tests/test_plan.md |