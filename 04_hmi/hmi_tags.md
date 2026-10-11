# HMI Tag Reference

All HMI tags are linked to DB_HMI through HMI_Connection_1, with a 500 ms acquisition cycle. Names follow the pattern `DB_HMI_<member>`.

## Read only (filled by the PLC)

| Member | Type | Use |
| --- | --- | --- |
| StationState | Int | State text and color (list StationStates) |
| AlarmLevel, AlarmCount | Int | Header indicator (list AlarmLevels), alarm counter |
| PriorityPump | Int | Priority pump (list PumpPriority) |
| TankLevel_pct, SourceLevel_pct | Real | Level bars and values |
| SourceOK | Bool | Source status (list SourceStatus) |
| Flow_m3h, Pressure_bar | Real | Discharge measurements |
| P1_Current_A, P2_Current_A | Real | Motor currents |
| P1_Status, P2_Status | Int | Pump status text and color (list PumpStatus) |
| P1_RunCmd, P2_RunCmd, P1_Feedback, P2_Feedback | Bool | Command and feedback indicators |
| P1_Runtime_h, P2_Runtime_h, P1_StartCount, P2_StartCount | Real, UDInt | Maintenance screen |
| Level_Low, Level_High, Level_CritHigh | Real | Limit lines on the level bar |

## Written by the operator

| Member | Type | Action |
| --- | --- | --- |
| Cmd_Start, Cmd_Stop, Cmd_Reset | Bool | Set while the button is pressed, cleared on release |
| ModeSelect | Int | 1 Auto, 2 Manual, 3 Maintenance, 0 none |
| P1_PumpCmd, P2_PumpCmd | Bool | Toggled by the manual pump buttons |
| MaintReset_P1, MaintReset_P2 | Bool | Set while the button is pressed, effective in Maintenance only |