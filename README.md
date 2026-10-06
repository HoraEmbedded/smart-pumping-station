# Smart Pumping Station

**Industrial Utility Pumping Station: PLC Control, HMI/SCADA, Reliability Monitoring and Explainable Anomaly Detection**

[Version française](README.fr.md)

> **Safety disclaimer.** This is an educational simulation. It is not a certified hydraulic, electrical or functional safety design, and must not be used to operate a real installation.

## Problem

A factory utility station must keep a storage tank between two water levels while avoiding dry running, excessive starts, overflow and unsafe restarts after a critical fault.

## Solution overview

A simulated two-pump station controlled by a Siemens S7-1200 (TIA Portal V18), with:

- Modular PLC architecture (modes, interlocks, pump alternation, alarm manager)
- Operator HMI (overview, alarms, maintenance, trends)
- Reliability KPIs (availability, MTBF, MTTR, specific energy)
- Rule-based, explainable anomaly detection
- Requirements traceability and documented test evidence

## Project status

| Version | Goal | Status |
| --- | --- | --- |
| V0 | Design: requirements, P&ID, I/O list, Grafcet, test plan | In progress |
| V1 | Single pump control | Planned |
| V2 | Two pumps, alternation, faults | Planned |
| V3 | HMI/SCADA | Planned |
| V4 | Data connection and dashboard | Planned |
| V5 | Anomaly detection | Planned |
| V6 | Final report and portfolio | Planned |

## Repository structure

| Folder | Content |
| --- | --- |
| `01_requirements/` | Scope, assumptions, requirements, traceability matrix |
| `02_design/` | P&ID, I/O list, alarm matrix, Grafcet |
| `03_plc/` | PLC exports and notes |
| `04_hmi/` | HMI screens and operator guide |
| `05_iiot_data/` | Data flow, datasets, Python analysis |
| `06_tests/` | Test plan, results, evidence |
| `07_media/` | Demo material |
| `08_report/` | Final report |
| `docs/` | Cross-cutting documentation and decision log |
| `captures/` | Screenshots, organized by mission |

## Tooling

TIA Portal V18, S7-PLCSIM V18 SP2, Python 3.13, Git, VS Code. See [docs/workstation.md](docs/workstation.md).

## Limitations

Simulated signals only. No real hydraulic sizing, no certified safety function, no IEC 62443 claim. Details in [01_requirements/assumptions.md](01_requirements/assumptions.md).

## License

MIT, see [LICENSE](LICENSE).