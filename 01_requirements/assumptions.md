# Simulation Assumptions

| ID | Assumption | Impact |
| --- | --- | --- |
| ASM-01 | Tank capacity is normalized from 0 to 100 percent | Levels are not physical volumes |
| ASM-02 | Tank level rises when a pump runs and the source is available | Simplified fill model |
| ASM-03 | Tank level drops through a configurable simulated drain | Consumption is not measured data |
| ASM-04 | Flow is simulated and follows the pump command, except during injected faults | Flow is not calibrated |
| ASM-05 | Motor current is simulated and rises under an injected overload | Not a real motor signature |
| ASM-06 | Analog tags are realistic in range but not calibrated for a physical plant | No metrological validity |
| ASM-07 | Emergency stop is a logic simulation only | Not a safety chain |
| ASM-08 | All KPIs are simulated and do not represent real plant availability | Never present them as field data |
| ASM-09 | Initial thresholds: low 30 %, high 80 %, critical 95 %, source minimum 15 %, minimum flow 2 m3/h, flow validation 10 s, restart delay 30 s | To be refined in Mission 2 |
| ASM-10 | V_tank = 10 m3 | Reference volume for the level model |
| ASM-11 | Q_pump nominal = 12 m3/h | Simulated, not a real pump curve |
| ASM-12 | Q_out = 3 m3/h constant. Time acceleration applies to the physical model only, protection delays run in PLC seconds and are tested at acceleration 1 | Constant drain is a simplification |