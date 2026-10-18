# Anomaly Rules

Rules ANO_01 to ANO_06 are implemented in `05_iiot_data/python/anomaly_rules.py` and scored by `anomaly_eval.py`. Each flag carries an explanation with the measured values and the threshold crossed. Results are generated in `05_iiot_data/anomaly_results.md`.

## Principles

- The rules read measured signals only. The injection columns of the datasets are used by the evaluation module only, and a unit test checks that the rules never name them.
- Delays are counted on the sample counter (real seconds). Windows and rates use the simulated clock.
- A flag marks a period of abnormal behavior. It does not prove a single cause.
- Thresholds shared with the PLC keep the same value, so the offline analysis and the PLC protection agree.

## Rules

| ID | Condition | Persistence | Reading |
| --- | --- | --- | --- |
| ANO_01 | A pump confirms running and the flow is below Flow_Min | 5 s on the sample counter | Closed valve, clogged filter, dry run, leak or flow sensor fault. The current orients the diagnosis |
| ANO_02 | The same single pump runs for the whole window and the tank level rises by less than the minimum rate | Window of 5 simulated minutes | Leak, excessive consumption, flow sensor error or pump wear |
| ANO_03 | Motor current above Current_High while the flow is below Flow_Min | 5 s on the sample counter | Blockage or friction |
| ANO_04 | More starts than FreqStarts_Max in the trailing window | Window of 60 simulated minutes | Narrow level band, noisy level signal or leak |
| ANO_05 | A value outside its physical range, or an inconsistent state: flow with no pump confirming, current with the feedback off, feedback without a run command | Range: none. States: 2 s on the sample counter | Wire break, sensor failure, contactor or scaling fault |
| ANO_06 | A pump draws more current than the mean of the other pump, at comparable flow | Pump settled for 2 s, reference of at least 5 samples | One pump degrades, or the two pumps differ |

## Thresholds

| Parameter | Value | Origin |
| --- | --- | --- |
| Flow minimum | 2.0 m3/h | Same as the PLC low flow alarm |
| Symptom delay | 5 s | Half of the 10 s PLC validation delay, at least five samples at 1 Hz |
| Current high | 12 A | Same as the PLC warning, 120 percent of the 10 A nominal current |
| State delay | 2 s | The model runs in a 100 ms interrupt while the export runs in the main cycle, so one sample can show a mixed state |
| Rise window and minimum rate | 5 simulated minutes, 0.5 %/min | One pump alone raises the level by 1.5 %/min in the reference scenario, the threshold is a third of it. The window gives 7.5 percent of expected rise against a level resolution far below |
| Start limit and window | 3 starts, 60 simulated minutes | A healthy cycle gives at most 0.6 starts per hour, so four starts in one hour is abnormal |
| Deviation | 15 percent | Engineering assumption: wider than the pump to pump dispersion expected between two identical pumps, to be set on field data |
| Comparable flow | within 10 percent of the median pumping flow | Same operating point for both pumps |

## Known false positives and blind spots

| Observation | Where | Explanation | Consequence |
| --- | --- | --- | --- |
| ANO_02 also fires on low flow faults | D02, D04 | With no flow the level cannot rise, it is a secondary symptom of the same cause | Two rules for one fault, counted as expected |
| ANO_02 cannot judge short runs | D06 | A run shorter than the 5 minute window never reaches the evaluation | Narrow level bands are covered by ANO_04 instead |
| ANO_02 cannot separate a leak from other causes | D05 | A level that does not rise says nothing on its origin | A mass balance residual (level change against integrated flow) would separate a leak from a flow sensor fault |
| ANO_06 cannot judge the first run of a dataset | D03 | The rule compares with the other pump and has no reference yet | Recall below 100 percent, depends on which pump runs first |
| ANO_06 does not say which pump deviates | D03 | It compares two pumps with each other | The flag names the pump drawing more current, a maintenance check decides |
| ANO_06 misses two pumps that degrade equally | none | The comparison stays within 15 percent | A drift of the pair needs a long term trend on the nominal current |
| ANO_01 sees the symptom while a pump runs only | D02, D04 | The PLC stops the pump after 10 s, the rule alerts after 5 s | A short observation window of about 5 samples |
| ANO_05 state checks need 2 seconds | all | One sample can show a mixed state because the model and the export run in different cycles | Short real glitches stay unflagged |
| Thresholds come from a noiseless simulation | all | No sensor noise, no pump wear, no real consumption profile | Margins have to be measured again on field data before any use |