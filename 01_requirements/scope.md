# Scope

## Context

The station transfers water from a low source to a storage tank. It keeps the tank level between a low and a high threshold while avoiding dry running, excessive starts, overflow and continued operation after a critical fault. Two pumps are modeled: duty and standby, with alternation to balance runtime.

## In scope

- Level control with two thresholds
- Operating modes: Stop, Initialization, Auto, Manual, Maintenance, Fault
- Two-pump alternation and standby takeover
- Simulated interlocks and emergency stop (Sim)
- Alarm management with acknowledgment and reset
- Low-flow detection after a stabilization delay
- Runtime and start counters, reliability KPIs
- HMI, data historization, rule-based anomaly analysis
- Requirements traceability and test evidence

## Out of scope

- Real hydraulic sizing and head-flow (H-Q) curves
- Real variable frequency drive tuning
- Certified safety function (IEC 61508, ISO 13849)
- Industrial cybersecurity compliance (IEC 62443)
- Connection of the PLC to the Internet
- Connection to a real production SCADA
