# Requirements

Statements use "shall". Method: T = Test, I = Inspection, A = Analysis, D = Demonstration. Priority: M = Must, S = Should. Thresholds are defined in docs/parameters.md.

## Control

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-001 | In Auto mode, the station shall request pumping when the tank level falls to or below the low threshold | M | T | V1 |
| REQ-002 | The station shall stop the running pump when the tank level reaches the high threshold | M | T | V1 |
| REQ-003 | A normal stop request shall stop all pumps in a controlled way and bring the station to STOPPED | M | T | V1 |
| REQ-004 | The station shall provide the modes Stop, Initialization, Auto, Manual, Maintenance and Fault following the state machine in mode_state_description.md | M | I, T | V1 |
| REQ-005 | Only one pump shall run at a time | M | T | V2 |
| REQ-006 | The priority pump shall alternate after each completed normal cycle | M | T | V2 |
| REQ-007 | If the priority pump is unavailable, the other pump shall be used | M | T | V2 |
| REQ-008 | A pump in fault shall not be started | M | T | V2 |
| REQ-009 | A minimum restart delay shall separate a stop and the next start of the same pump | M | T | V2 |

## Interlocks and faults

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-010 | Source level below the minimum, or DI_Source_Low active, shall stop the pumps and inhibit starts (ALM_002) | M | T | V1 |
| REQ-011 | The simulated emergency stop shall stop all pump commands and latch the station in FAULT (ALM_001) | M | T | V1 |
| REQ-012 | A tank level above the critical threshold shall stop all pumps and raise ALM_003 | M | T | V1 |
| REQ-013 | Manual and Maintenance commands shall not bypass critical interlocks | M | T | V1 |
| REQ-014 | A reset shall not clear a fault whose cause persists. After correction, a reset shall return the station to an authorized state | M | T | V1 |
| REQ-015 | When pumping is requested and both pumps are unavailable, the station shall raise ALM_009 and go to FAULT | M | T | V2 |

## Diagnostics and counters

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-016 | A running pump with flow below the minimum after the validation delay shall raise ALM_004 or ALM_005 and become unavailable | M | T | V2 |
| REQ-017 | An analog value out of range or below 4 mA shall be flagged inconsistent and raise ALM_008 | M | T | V2 |
| REQ-018 | A start rate above the threshold shall raise ALM_010 | S | T | V2 |
| REQ-019 | Run hours and start count shall be kept per pump, a start being counted on the rising edge of the validated run command | M | T | V2 |
| REQ-020 | Each alarm shall have probable causes, a system reaction, an HMI text and a reset condition | M | I | V2 |

## HMI

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-021 | The HMI shall provide five screens: overview, commands, alarms, maintenance, trends | M | D | V3 |
| REQ-022 | The HMI shall distinguish a run command from a run feedback and shall never use color as the only indicator | M | I, D | V3 |
| REQ-023 | The HMI shall allow alarm acknowledgment and shall refuse unauthorized actions with a message | M | T | V3 |

## Data and analytics

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-024 | The system shall export the defined variables with a timestamp to CSV at a 1 s period | M | T | V4 |
| REQ-025 | Dashboard values shall match the PLC values | M | T | V4 |
| REQ-026 | KPIs shall be computed: run hours, starts, time in fault, availability, mean flow, specific energy, frequent start rate | M | A, T | V4 |
| REQ-027 | Rules ANO_01 to ANO_06 shall flag abnormal periods on fault datasets, with documented false positives | M | A, T | V5 |

## Quality

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-028 | Thresholds and delays shall be stored in DB_Parameters and be editable without changing the logic | M | I, T | V1 |
| REQ-029 | PLC code shall use functional tag names and commented networks | M | I | V1 |
| REQ-030 | The full system launch shall be reproducible from a documented procedure | M | D | V6 |
| REQ-031 | No credential shall be stored in the repository and the PLC shall not be exposed to the Internet | M | I | V4 |
| REQ-032 | Every requirement shall be linked to at least one test or inspection | M | I | V0 |

## Derived requirements (from state machine design)

| ID | Requirement | Prio | Method | Release |
| --- | --- | --- | --- | --- |
| REQ-033 | At power-up and after a start request, the station shall go through INITIALIZING, check input coherence and absence of critical alarms, and only then reach READY | M | T | V1 |
| REQ-034 | Any change of operating mode shall pass through READY so that the pumps are stopped before the new mode starts | M | T | V1 |
| REQ-035 | After a fault reset the station shall return to STOPPED and shall not restart without a new start request | M | T | V1 |
| REQ-036 | In Maintenance mode a pump test shall be limited to Maint_Test_Max_s | S | T | V1 |
| REQ-037 | A run command without run feedback within Run_Feedback_Timeout_s shall make the pump unavailable and raise ALM_006 or ALM_007 | M | T | V2 |