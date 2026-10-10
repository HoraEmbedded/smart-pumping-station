# Workstation and Toolchain

Baseline of the development environment. Update this file whenever a tool version changes.

## Hardware

| Item | Value |
| --- | --- |
| Manufacturer / model | HP Envy x360 2-in-1 Laptop 15-fe1xxx |
| CPU | Intel Core Ultra 7 155U |
| RAM | 32 GB |
| Storage | 954 GB |
| GPU | None |
| OS | Windows 11, 64-bit |

## Software

| Software | Version | Role | Status |
| --- | --- | --- | --- |
| TIA Portal | V18 | PLC programming | Installed |
| S7-PLCSIM | V18 SP2 | PLC runtime simulation | Installed |
| Automation License Manager | V6.2 + SP5 | TIA license management | Installed |
| Git for Windows | 2.53.0 | Version control | Installed |
| VS Code | 1.139.1 | Documentation and scripts | Installed |
| Python | 3.13.x (TO FILL) | KPI and anomaly analysis | Installed |
| WinCC (within TIA) | V18 | HMI/SCADA |V18 |
| Node-RED | n/a | Data flow | Planned (Iteration 10) |
| Grafana or equivalent | n/a | Dashboard | Planned (Iteration 11) |

## Notes

- All work is done on Windows.
- TIA Portal project files are not versioned in Git (see docs/decision_log.md, DEC-003).