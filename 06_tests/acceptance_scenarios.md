# Acceptance Scenarios

End to end runs of the five use cases on the whole chain: PLC simulation, HMI runtime, OPC UA collector. Start from the cold start of docs/runbook.md, set the acceleration to 60, save the collector files in 06_tests/evidence/final. Between scenarios return to the initial state (runbook).

| Test | Use case | Actions | Expected | Expected alarms | Evidence |
| --- | --- | --- | --- | --- | --- |
| T61 | UC-01 | Collector for 120 s, HMI: Start, then Auto. The level falls from 50 to 30 percent in about 40 s | Pump 1 starts at 30 percent, feedback confirmed, the level rises | none | Overview screenshot with pump 1 running, CSV T61_uc01_uc02.csv |
| T62 | UC-02 | Same run, wait for 80 percent | The pump stops, the priority shows pump 2, no alarm | none | Overview screenshot of the stopped pump with PRIORITY P2 |
| T63 | UC-03 | Collector for 90 s, Auto, level forced to 20, with pump 1 running set V_P1FaultOK to FALSE | Pump 1 stops and is locked out, pump 2 takes over | ALM_006 | Alarms screenshot, CSV T63_uc03.csv, AlarmWord1 equals 32 |
| T64 | UC-04 | Collector for 90 s, Auto, level forced to 20, with a pump running set V_SourceLow to TRUE, then back to FALSE and the source level at 25 | The pump stops, no start while the source is low, restart after recovery and the restart delay | ALM_002 | Alarms screenshot, CSV T64_uc04.csv, AlarmWord1 equals 2 |
| T65 | UC-05 | Collector for 90 s, Auto, level forced to 20, with pump 1 running set Inject_P1_LowFlow to TRUE | After about 10 s pump 1 is unavailable and pump 2 takes over | ALM_004 | Alarms screenshot, CSV T65_uc05.csv, AlarmWord1 equals 8 |

Collector command (change the file name and the duration):

    python 05_iiot_data\python\opcua_collector.py --out 06_tests\evidence\final\T63_uc03.csv --duration 90

Check each file with `python 05_iiot_data\python\validate_dataset.py 06_tests\evidence\final\T6*.csv`.

Optional link with the anomaly rules, for T65:

    python -c "import sys; sys.path.insert(0, '05_iiot_data/python'); from kpi import load_rows; from anomaly_rules import run_all, periods; r = load_rows('06_tests/evidence/final/T65_uc05.csv'); f = run_all(r); print([(round(g['t_start_min']), g['message']) for g in periods(r, f['ANO_01'])])"