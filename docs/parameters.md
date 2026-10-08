# Parameter Table

Single source of truth for thresholds and delays. Mirrored in `DB_Parameters` (PLC). Any change here is followed by a regression run of the affected tests.

| ID | DB tag | Default | Unit | Origin |
| --- | --- | --- | --- | --- |
| P01 | Level_Low | 30 | % | Start threshold, hysteresis |
| P02 | Level_High | 80 | % | Stop threshold, hysteresis |
| P03 | Level_CritHigh | 95 | % | Critical high, ALM_003 |
| P04 | Source_Min | 15 | % | Source low, ALM_002 |
| P05 | Flow_Min | 2 | m3/h | Low flow, ALM_004 and ALM_005 |
| P06 | Flow_Validation_s | 10 | s | Delay before flow evaluation |
| P07 | Restart_Delay_s | 30 | s | Anti-restart delay |
| P08 | FreqStarts_Max | 3 | starts | Threshold per window, ALM_010 |
| P09 | FreqStarts_Window_min | 60 | min | Window for P08 |
| P10 | Current_Nominal_A | 10 | A | Simulated nominal current |
| P11 | Current_High_A | 12 | A | WRN_002 threshold (120 percent) |
| P12 | Current_High_Delay_s | 5 | s | Ignore start-up inrush |
| P13 | Maintenance_Interval_h | 500 | h | WRN_003 |
| P14 | Raw_Low_Limit | -500 | count | About 3.7 mA, wire break, ALM_008 |
| P15 | Raw_High_Limit | 28500 | count | Over-range, ALM_008 |
| P16 | LevelRise_Window_s | 60 | s | Window for rule ANO_02 |
| P17 | LevelRise_Min_pct | 0.5 | % | Minimum rise expected in P16 |
| P18 | Tank_Volume_m3 | 10 | m3 | Level model |
| P19 | Pump_Flow_m3h | 12 | m3/h | Level model |
| P20 | Drain_Flow_m3h | 3 | m3/h | Level model |
| P21 | Sim_Step_s | 0.1 | s | Euler step |
| P22 | Time_Accel | 60 | x | Simulation acceleration |
| P23 | Run_Feedback_Timeout_s | 5 | s | Run feedback expected after a run command, IL-04 |
| P24 | Init_Delay_s | 2 | s | Duration of INITIALIZING |
| P25 | Maint_Test_Max_s | 60 | s | Maximum pump test in Maintenance |
| P26 | Source_Hyst_pct | 5 | % | Hysteresis for source recovery, IL-02 |

## Formulas

    mA = 4 + Raw / 1728
    Value_eng = Min + (Raw / 27648) x (Max - Min)

