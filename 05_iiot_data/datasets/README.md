# Datasets

Collected with the PLC process model at acceleration 60 (one real second is one simulated minute). Columns are described in ../data_dictionary.md. Columns starting with GT_ give the injected fault and must not be read by detection rules.

| File | Scenario | Injection | Rows | Targets |
| --- | --- | --- | --- | --- |
| D01_normal | Five normal cycles with alternation | None | 699 | Reference, false positive check |
| D02_low_flow_p1 | Blocked flow on pump 1 until a reset | P1 low flow, 0 to 300 s | 588 | Low flow while pumping |
| D03_pump_deviation_p1 | Pump 1 draws more current than pump 2 | P1 high current, whole run | 704 | Pump 1 versus pump 2 deviation |
| D04_blocked_line_p1 | High current and low flow together | P1 low flow and high current, 0 to 240 s | 407 | High current with low flow |
| D05_leak | Drain larger than the pump flow | Drain 13 m3/h, 0 to 150 s | 296 | Level not rising |
| D06_frequent_starts | Narrow level band and short restart delay | Level 48 to 52, restart delay 1 s | 233 | Too frequent starts |

A sensor value out of range is not covered by a dataset: the process model supplies valid signals, so that rule is checked on constructed values in the analytics phase.