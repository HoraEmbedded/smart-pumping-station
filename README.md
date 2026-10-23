# Smart Pumping Station

**Industrial Utility Pumping Station: PLC Control, HMI, Reliability Monitoring and Explainable Anomaly Detection**

[Version française](README.fr.md) | [Technical report](08_report/report_final.pdf) | [Demonstration video](https://youtu.be/cKYuNFylUhU)

![Overview screen](04_hmi/screens/overview.png)

## Project purpose

A two-pump utility station that keeps a storage tank between two water levels, built as a complete engineering case: requirements, design, PLC program, HMI, data, indicators, anomaly rules and a verified test campaign.

| Key figures | |
| --- | --- |
| Requirements | 56, each with a test |
| Tests | 69, all passed on the frozen build |
| PLC | S7-1200, 14 code blocks, SCL and Ladder |
| Alarms | 13, in four classes |
| Datasets | 6, one normal and five with injected faults |
| Anomaly rules | 6, each flag explained |
| Decisions logged | 61 |

## Industrial context

Utility stations move water to a storage tank that feeds a plant. They must avoid dry running, excessive pump starts, overflow and an unsafe restart after a critical fault.

## Functional requirements

56 testable requirements written with "shall", a verification method each, and a traceability matrix checked by script in both directions. See [requirements](01_requirements/requirements.md) and the [traceability matrix](01_requirements/requirements_traceability_matrix.csv).

## Assumptions and limitations

Assumptions of the model: tank 10 m3, pump 12 m3/h, constant drain 3 m3/h, process simulated inside the PLC, simulated 4-20 mA signals. See [assumptions](01_requirements/assumptions.md).

Limitations, stated once:
- Validated in simulation (S7-PLCSIM, WinCC Runtime), no physical controller or sensor.
- Indicators and datasets come from the simulation: they illustrate the calculation and are not field statistics.
- Emergency stop and latched faults are simulated logic, not a certified safety chain. The HMI emergency stop request is a supplementary action, the reference emergency stop remains the hardware contact.
- No IEC 62443 compliance claimed, the OPC UA endpoint is anonymous on the lab PC only.
- Thresholds come from a noiseless simulation, their margins must be measured again on field data.
- The anomaly rules have documented blind spots, see [anomaly rules](docs/anomaly_rules.md).

## System architecture

![OT and IT architecture](02_design/diagrams/architecture_ot_it.png)

## P&ID and I/O map

![P&ID](02_design/diagrams/pid_simplified.png)

24 signals (12 digital inputs, 6 analog inputs, 6 digital outputs): [I/O list](02_design/io_list.csv).

## PLC architecture

Siemens S7-1200, TIA Portal V18. OB1 orchestrates only, the tank model runs in a 100 ms cyclic interrupt, thresholds live in one parameter block, no raw address in the code.

| Block | Role |
| --- | --- |
| FB_ModeManager | State machine |
| FB_AutoCycle | Level demand, alternation, backup |
| FB_PumpControl | Run command, restart delay, flow and feedback checks, counters |
| FB_StationMonitor | Frequent starts, maintenance, level rise, sensor warnings |
| FC_AlarmLatch, FC_Indicators | Latched alarms, lamps and siren (Ladder) |

Details in [TIA Portal notes](03_plc/notes_tia_portal.md). Sources are versioned in `03_plc/src`, the project archive is attached to each release.

## Operating modes

Seven states (stopped, initializing, ready, auto, manual, maintenance, fault), every mode change passes through ready. Latched critical faults, reset only when the cause is gone, no automatic restart. See the [state machine](02_design/mode_state_description.md).

![Grafcet](02_design/diagrams/grafcet_station.png)

## Alarm strategy

Inspired by ISA-18.2: every alarm requires an action, acknowledgment never clears a fault, the siren re-arms on a new critical alarm. See the [alarm matrix](02_design/alarm_matrix.csv) and the [alarm philosophy](docs/alarm_philosophy.md).

## HMI

WinCC Runtime Professional V18, five screens, a native alarm system with info texts, status always written as text. An emergency stop request is available on every screen: it acts on a single press without confirmation, like the emergency stop contact, and its release asks for a confirmation. See the [operator guide](04_hmi/operator_guide.md).

![Alarm screen](04_hmi/screens/alarms.png)

## Data and KPI architecture

The WinCC Runtime OPC UA server is read by a read-only Python client. Indicators are time-weighted, availability is shown at station and pump level. A local read-only dashboard shows them live.

![Dashboard](captures/iteration-12/dashboard_live.png)

See the [data architecture](docs/data_architecture.md), the [KPI definitions](docs/kpi_definitions.md) and the [datasets](05_iiot_data/datasets/README.md).

## Anomaly detection rules

Six rules on measured signals, each flag gives the values and the threshold crossed. Evaluated against injected faults, with measured threshold margins. See [anomaly rules](docs/anomaly_rules.md) and the [results](05_iiot_data/anomaly_results.md).

![Leak dataset](05_iiot_data/figures/D05_leak_anomalies.png)

## Test plan and results

69 tests replayed on a frozen build, five end-to-end acceptance scenarios plus the two HMI emergency stop tests, defects logged with cause and fix. See the [test plan](06_tests/test_plan.md), the [final report](06_tests/test_report_final.md) and the [defect log](06_tests/defect_log.md).

## Demonstration

Four minutes of the station in operation: [video on YouTube](https://youtu.be/cKYuNFylUhU). Script in [07_media](07_media/demo_script.md). To run it yourself, follow the [runbook](docs/runbook.md).

## Future improvements

- Secure the OPC UA endpoint (signed and encrypted messages, certificate management)
- Security assessment by zones and conduits (IEC 62443)
- Port to an S7-1500 for PLCSIM Advanced and a native OPC UA server
- Leak detection by mass-balance residual
- Statistical or learned detector evaluated against the rules on field data
- Physical HMI panel with user profiles, hardware-in-the-loop bench

## Repository structure

| Folder | Content |
| --- | --- |
| `01_requirements/` | Scope, assumptions, requirements, use cases, traceability |
| `02_design/` | P&ID, I/O list, alarm matrix, state machine, diagrams |
| `03_plc/` | SCL sources, exports, TIA Portal notes |
| `04_hmi/` | Screens, operator guide, design standard |
| `05_iiot_data/` | Datasets, Python code, dashboard, figures, results |
| `06_tests/` | Test plan, results, campaign, defect log, evidence |
| `07_media/` | Demonstration script and video notes |
| `08_report/` | Technical report (LaTeX source and PDF) |
| `docs/` | Process, parameters, runbook, decision log, glossary |
| `tools/` | Figure generation, campaign, verification, impact analysis |

## License

MIT, see [LICENSE](LICENSE).