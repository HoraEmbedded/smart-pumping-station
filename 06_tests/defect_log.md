# Defect Log

Severity: Critical (interlock, wrong data or loss of the main function), Major (a function is lost or misleading), Minor (cosmetic or documentation). Status: Open, Fixed (fix committed and retest passed), Accepted (documented limit).

## Defects found by execution

| ID | Found in | Description | Severity | Cause | Fix | Retest | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BUG-001 | Compilation, iteration 5 | Clock tag undefined in two blocks | Minor | Clock memory byte not enabled in the CPU properties | Enabled in the CPU, Clock_1Hz at %M0.5 | Rebuild without error | Fixed |
| BUG-002 | Compilation, iteration 8 | Instance data blocks out of date after a function block interface change | Minor | Instance blocks not recompiled before the blocks that read them | Update order written in notes_tia_portal.md | Rebuild without error | Fixed |
| BUG-003 | HMI compilation, iteration 9 | Error on the communication driver of the HMI connection | Minor | Wrong PLC connection name after renaming the CPU | Updated the connection in the HMI project, recompiled | HMI compiles, runtime connects | Fixed |
| BUG-004 | Feasibility test, iteration 11 | External S7 reader cannot reach the simulated S7-1200 | Major | The advanced simulator does not support this CPU | Route changed to the OPC UA server of the HMI runtime | T52, T53 | Fixed |
| BUG-005 | Feasibility test, iteration 11 | OPC UA port stayed closed | Major | Not isolated: runtime package, certificate authority and IIS features set up in sequence | Sequence documented in docs/opcua_setup.md | Port listening, tags readable | Fixed |

## Findings from design review

| ID | Found in | Description | Resolution | Test |
| --- | --- | --- | --- | --- |
| DR-001 | State machine design, iteration 4 | Five requirements were missing | Derived requirements added | T33 to T37 |
| DR-002 | Pump logic review, iteration 7 | The no-pump alarm cause depended on latches and needed two resets | Cause based on the contact states | T05 |
| DR-003 | HMI interface design, iteration 9 | A pump command typed in Manual survived a mode change | Commands cleared outside Manual and Maintenance | T41 |
| DR-004 | Data design, iteration 11 | The frequent start window counted real time while the process ran accelerated | Window moved to simulated time | T54 |

## Defects found in the final campaign

| ID | Test | Description | Severity | Cause | Fix | Retest | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| No defect was found in the final campaign. | | | | | | | |