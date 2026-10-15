# Data Dictionary

Export block `DB_IIoTExport` (DB100, standard access, 70 bytes, big-endian), refreshed every scan. The collector adds the timestamp. CSV columns follow the table order below, except that Timestamp comes first.

| Column | Type | Offset | Source | Unit or meaning |
| --- | --- | --- | --- | --- |
| Timestamp | text | n/a | Collector, PC clock, UTC | ISO 8601 |
| TankLevel_pct | Real | 0 | DB_Process | % |
| SourceLevel_pct | Real | 4 | DB_Process | % |
| Flow_m3h | Real | 8 | DB_Process | m3/h |
| Pressure_bar | Real | 12 | DB_Process | bar |
| P1_Current_A | Real | 16 | DB_Process | A |
| P2_Current_A | Real | 20 | DB_Process | A |
| P1_RunHours | Real | 24 | DB_HMI, PLC real time | h |
| P2_RunHours | Real | 28 | DB_HMI, PLC real time | h |
| Power_kW | Real | 32 | Computed from the currents | kW, simulated |
| GT_Drain_m3h | Real | 36 | Drain parameter | m3/h, ground truth |
| P1_StartCount | UDInt | 40 | DB_Pump1 | starts |
| P2_StartCount | UDInt | 44 | DB_Pump2 | starts |
| SampleCounter | UDInt | 48 | PLC | +1 per real second |
| SimTime_s | LReal | 52 | Process model | simulated seconds |
| StationState | Int | 60 | DB_StationState | 0, 10, 20, 30, 40, 50, 90 |
| ActiveAlarmCount | Int | 62 | DB_HMI | count |
| AlarmWord1 | Word | 64 | DB_HMI | fault bits |
| AlarmWord2 | Word | 66 | DB_HMI | warning bits |
| P1_RunCmd | Bool | 68.0 | DB_Pump1 | run command |
| P2_RunCmd | Bool | 68.1 | DB_Pump2 | run command |
| P1_RunFeedback | Bool | 68.2 | DB_Process | run feedback |
| P2_RunFeedback | Bool | 68.3 | DB_Process | run feedback |
| P1_Fault | Bool | 68.4 | DB_Alarms | latched pump fault |
| P2_Fault | Bool | 68.5 | DB_Alarms | latched pump fault |
| SourceOK | Bool | 68.6 | DB_StationState | source available |
| Demand | Bool | 68.7 | DB_StationState | pumping demand |
| GT_Inject_P1_LowFlow | Bool | 69.0 | DB_Sim | ground truth |
| GT_Inject_P2_LowFlow | Bool | 69.1 | DB_Sim | ground truth |
| GT_Inject_P1_NoFeedback | Bool | 69.2 | DB_Sim | ground truth |
| GT_Inject_P2_NoFeedback | Bool | 69.3 | DB_Sim | ground truth |
| GT_Inject_P1_HighCurrent | Bool | 69.4 | DB_Sim | ground truth |
| GT_Inject_P2_HighCurrent | Bool | 69.5 | DB_Sim | ground truth |

Bits 69.6 and 69.7 are spare.

## Alarm bits

AlarmWord1: bit 0 emergency stop, 1 source low, 2 tank level critical, 3 low flow P1, 4 low flow P2, 5 fault P1, 6 fault P2, 7 tank sensor, 8 no pump available.
AlarmWord2: bit 0 frequent starts, 1 high current P1, 2 high current P2, 3 maintenance due P1, 4 maintenance due P2, 5 level not rising, 6 non critical sensor.

## Rules

- Columns starting with GT_ describe the injected fault and the true drain flow. They exist to evaluate the anomaly rules. They are not available in a real plant and no rule reads them.
- Rates and cycle statistics use SimTime_s. Protection delays are measured with SampleCounter.
- P1_RunHours and P2_RunHours count PLC real time. Simulated run hours are computed from SimTime_s.