# Fault Causes and Diagnostics

An alarm reports abnormal behavior, not a proven cause. This table lists the usual causes and the first checks, ordered from the cheapest check to the most expensive.

| Symptom | Possible causes | First checks |
| --- | --- | --- |
| Low flow on a pump | Closed discharge valve, clogged filter, dry run, leak, flow sensor fault, worn pump | Valve positions, filter, source level, flow sensor signal, motor current |
| Low flow with high current | Blockage, mechanical friction | Discharge valve, impeller, bearing |
| Low flow with low current | Dry run, broken coupling, air in the suction line | Source level, suction line, coupling |
| No run feedback after a command | Contactor not pulling in, auxiliary contact fault, control wiring | Contactor coil, auxiliary contact, protection state |
| High motor current | Overload, mechanical friction, voltage problem | Pump load, bearing, supply |
| Frequent starts | Tight thresholds, consumption leak, noisy level sensor | Level thresholds, level signal stability, line leak |
| Level not rising while a pump runs | Leak or excessive consumption, flow sensor error, pump wear | Consumption, flow versus level trend, pump condition |
| Inconsistent sensor | Wire break, sensor failure, scaling error | Wiring, signal in mA, scaling range |

## Reading combinations

| Flow | Current | Most likely direction |
| --- | --- | --- |
| Low | High | Blockage or friction |
| Low | Low | Dry run or lost drive |
| Normal | High | Overload or electrical issue |
| Normal | Normal, level not rising | Consumption or leak |

## Alarm dependencies

- Flow alarms are not raised while the flow signal is invalid, the sensor warning explains it.
- A pump cannot raise a low flow alarm when the source is low, because it is not allowed to run.