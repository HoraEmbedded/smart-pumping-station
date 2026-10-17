# Test Report V4

## Scope

Data export, collection, datasets, indicators and dashboard. Requirements REQ-024 to REQ-026, REQ-031, REQ-049 to REQ-052.

## Environment

TIA Portal V18, S7-PLCSIM V18 SP2, WinCC Runtime Professional V18 with its OPC UA server, Python 3.13, asyncua. Process model and fault injection in the PLC.

## Results

| Group | Tests | Result |
| --- | --- | --- |
| Export and collection | T51, T52, T53, T54, T29 | Pass |
| Indicators | T25, T56 | Pass |
| Dashboard | T10, T55, T57 | Pass |

Details and evidence: test_results.md and the evidence folder.

## Defects found

| ID | Description | Resolution |
| --- | --- | --- |
| 1 | The planned external S7 reader could not reach the simulated S7-1200, the advanced simulator does not support this CPU | Feasibility tests, route changed to the WinCC Runtime OPC UA server, decisions logged |
| 2 | OPC UA port stayed closed after enabling the server | Runtime package, certificate authority and IIS features set up, sequence documented |
| 3 | The frequent start window counted real time while the process ran accelerated, a false warning would have appeared | Window moved to the simulated clock, test T54 |

## Open points

- Alarm history is limited to the runtime buffer, the timestamped alarm log needs a database.
- The OPC UA endpoint accepts anonymous access on the lab PC only, a secured endpoint is a perspective.
- Reliability indicators on simulated runs with one or two failures illustrate the calculation, they are not statistics.