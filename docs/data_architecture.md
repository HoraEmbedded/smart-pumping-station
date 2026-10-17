# Data Architecture

![OT and IT architecture](../02_design/diagrams/architecture_ot_it.png)

## Data flow

| Stage | Component | Role |
| --- | --- | --- |
| Source | PLC, DB_IIoTExport | Flat data block refreshed every scan, one sample per second |
| Transport | HMI connection, then OPC UA (read only) | The WinCC Runtime reads the block, its OPC UA server publishes the tags |
| Collection | opcua_collector.py | Reads the 32 export tags twice per second, adds the PC timestamp, keeps only new samples, counts missed ones |
| Storage | CSV files in 05_iiot_data/datasets | One file per run, one row per sample |
| Use | Dashboard, KPI, anomaly rules | Read the CSV files |

The column list is in 05_iiot_data/data_dictionary.md. Setup notes are in docs/opcua_setup.md.

## Time bases

| Column | Clock | Use |
| --- | --- | --- |
| Timestamp | PC clock, UTC, applied at reading | Alignment with external events |
| SampleCounter | PLC, +1 per real second | Gap detection, delays that run in real time |
| SimTime_s | Process model, step times acceleration | Rates per simulated hour, cycle durations |

Protection delays (flow validation, restart delay, feedback timeout) run in PLC real seconds. The process dynamics and the frequent-start window run on simulated time. At acceleration 1 both clocks are equal.

## Sampling

One sample per second. The shortest protection delay is 5 s, so every delay spans at least five samples. The collector polls every 0.5 s so that no sample is lost between two counter increments.

## Security measures

| Measure | How |
| --- | --- |
| Lab PC only | The OPC UA endpoint is used locally, remote access is blocked at the firewall |
| Read only collector | The code only calls read functions, it has no write call |
| Anonymous policy | Accepted for the local test. The server also offers signed and encrypted policies, listed in the perspectives |
| No external S7 access | PUT/GET is disabled on the CPU, data leaves the PLC only through the HMI connection |
| No secrets in the repository | Nothing in the code needs a credential, certificates and keys are excluded by .gitignore, a repository scan is part of the tests |
| Simulated field signals | Replaced by the physical inputs by switching Sim_Inputs off |

## Alternatives considered

| Route | Pattern | Status |
| --- | --- | --- |
| External S7 collector (Python) | Direct PLC read | Rejected: PLCSIM Advanced does not support the S7-1200, and the standard simulator is not reachable from outside |
| NetToPLCSim network bridge | Third-party proxy for the simulator | Rejected: reported to work only with the S7-300 and S7-400 family on PLCSIM V5.x |
| HMI runtime script writing a CSV | Local logging | Alternative: write test passed, not maintained |
| SQL access to the WinCC archive | Historian queried by a database client | Not tested, access conditions unverified |
| MQTT or web API from the PLC | Edge publishing | Not testable: needs a network-exposed controller |
| WinCC OPC UA server and an OPC UA client | SCADA as gateway | Retained: feasibility test passed |

## Dashboard

`05_iiot_data/python/dashboard.py` serves one page on 127.0.0.1 (port 8050) and a JSON view of a CSV file. It reads the file written by the collector, so live display and replay of a recorded dataset use the same code. A pill shows LIVE, STALE (no new sample for more than 5 s) or REPLAY. The server answers GET requests only. The level guides at 30, 80 and 95 percent are the default thresholds, they do not follow a changed parameter.

Live run: `opcua_collector.py --out ...\datasets\live.csv --duration 3600` in one terminal, `dashboard.py --csv ...\datasets\live.csv` in another.