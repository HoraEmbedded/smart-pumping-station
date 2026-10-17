# KPI Definitions

All indicators are computed from the export datasets by `05_iiot_data/python/kpi.py`. Each interval between two consecutive samples is weighted by its duration on the simulated clock and takes the values of the sample at its start. Intervals with a stopped clock have no weight. The figures come from the process simulation.

| Indicator | Formula | Columns | Unit |
| --- | --- | --- | --- |
| Run hours | Sum of the interval durations with the run feedback on, divided by 3600 | P1_RunFeedback, P2_RunFeedback, SimTime_s | h |
| Duty | Run time divided by total time, times 100 | same | % |
| Starts | Last start count minus first start count | P1_StartCount, P2_StartCount | count |
| Start rate | (Starts P1 + starts P2) divided by the total hours | same | 1/h |
| Station availability | (1 minus time in FAULT divided by the time the station is started) times 100 | StationState | % |
| Time in fault | Time in FAULT divided by the time the station is started, times 100 | StationState | % |
| Pump availability | (1 minus time unavailable divided by total time) times 100 | AlarmWord1 bits 3 and 5 (pump 1), 4 and 6 (pump 2) | % |
| MTBF | Pump run time divided by the number of failures | same | h |
| MTTR | Mean duration of the completed repairs | same | h |
| Mean flow while pumping | Sum of flow times dt over the intervals where a pump runs, divided by the sum of dt | Flow_m3h | m3/h |
| Volume | Sum of flow times dt, divided by 3600 | Flow_m3h | m3 |
| Energy | Sum of power times dt, divided by 3600 | Power_kW | kWh |
| Specific energy | Energy divided by volume, shown above 0.01 m3 only | Power_kW, Flow_m3h | kWh/m3 |

## Events

A pump failure is a rising edge of its unavailability, a repair is the falling edge. An event still open at the end of the data counts in the downtime but not in the MTTR. The MTBF is not defined without a failure. A started station is any station whose state is not STOPPED.

## Reference values of the tank model

| Quantity | Value |
| --- | --- |
| Duty | 25 percent |
| Steady start rate | 0.45 per hour |
| Power at 10 A, 400 V, power factor 0.85 | 5.889 kW |
| Specific energy at 12 m3/h | 0.491 kWh/m3 |

## Reading the indicators

- The gap between station availability and pump availability measures the value of the backup pump.
- Specific energy rises when energy is consumed without volume, for example on a blocked line. It stays normal during a leak, because the pump itself behaves normally: the level based rule is needed for that.
- Duty alone does not reveal frequent cycling, the start rate does.
- An MTBF built from one or two events is an illustration, not a statistic.

## Worked example

Eleven samples 60 s apart (ten intervals, 600 s in total). Pump 1 runs in intervals 1 to 5 at 12 m3/h and 6 kW, one start is counted, pump 1 is unavailable in intervals 6 and 7, the station is in FAULT in intervals 8 and 9.

| Indicator | Hand calculation | Result |
| --- | --- | --- |
| Run hours pump 1 | 300 s / 3600 | 0.0833 h |
| Duty pump 1 | 300 / 600 | 50 % |
| Start rate | 1 / (600 / 3600) | 6.0 per hour |
| Station availability | 1 - 120 / 600 | 80 % |
| Pump 1 availability | 1 - 120 / 600 | 80 % |
| MTTR pump 1 | one repair of 120 s | 0.0333 h |
| MTBF pump 1 | 300 s / 1 failure | 0.0833 h |
| Mean flow while pumping | 12 x 300 / 300 | 12 m3/h |
| Volume | 12 x 300 / 3600 | 1.0 m3 |
| Energy | 6 x 300 / 3600 | 0.5 kWh |
| Specific energy | 0.5 / 1.0 | 0.5 kWh/m3 |