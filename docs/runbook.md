# Runbook

How to start, check and stop the whole chain from a cold state. Each step names what to observe.

## Prerequisites

TIA Portal V18 with the project, S7-PLCSIM V18 SP2, WinCC Runtime Professional V18, Python 3.13 with the packages of `docs/python_environment.txt`. One-time Python setup:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r tools\requirements.txt -r 05_iiot_data\python\requirements.txt

## Cold start

1. Close TIA Portal, the simulators, the runtime and every terminal. Restart the PC if the previous session ended abnormally.
2. Open the project in TIA Portal. Start the PLC simulation.
3. Perform a memory reset of the simulated CPU (MRES in the simulator panel, or the memory reset command of its menu, the label varies).
4. Download the whole PLC program with the initial values, then set the CPU to RUN.
5. Open a watch table and check the initial state below.
6. Start the HMI runtime simulation and check that the overview shows the state STOPPED.
7. Check the OPC UA endpoint: `netstat -ano | findstr LISTENING | findstr 4861` returns a line.
8. Optional: start the collector and the dashboard (see the commands in `docs/data_architecture.md`).

## Initial state

| Variable | Value |
| --- | --- |
| DB_StationState.StationState | 0 |
| DB_Sim.TankLevel_pct, SourceLevel_pct | 50.0, 80.0 |
| DB_Sim.Sim_Enable, Sim_Inputs | TRUE, TRUE |
| DB_Sim.V_EStopOK, V_P1FaultOK, V_P2FaultOK | TRUE |
| DB_Sim.V_SourceLow and the six Inject_ bits | FALSE |
| DB_Parameters.Time_Accel | 1.0 |
| DB_Parameters.Drain_Flow, Level_Low, Level_High | 3.0, 30.0, 80.0 |
| DB_Parameters.Restart_Delay | T#30s |
| DB_AutoCycle.Priority | 1 |
| DB_HMI.AlarmCount | 0 |
| DB_Pump1.StartCount, DB_Pump2.StartCount | 0 |
| DB_Pump1.Runtime_s, DB_Pump2.Runtime_s | 0 |

## Returning to the initial state without a cold start

1. Stop from the HMI, then reset. Wait for STOPPED.
2. Set every Inject_ bit to FALSE and the V_ bits to their healthy value.
3. Restore the parameters changed by the test.
4. Set Sim_Reset to TRUE (level 50, source 80).
5. If a result is surprising, restore the initial state and repeat once. A failure that disappears on repeat is a hidden state to understand, not to ignore.

## Shutdown

Stop the collector and the dashboard, stop the HMI runtime, set the CPU to STOP, close the simulator, close TIA Portal.

## Reproducibility checks

### Restore from the archive (T66)

1. Archive the project from TIA Portal (Project, Archive) into a temporary folder.
2. Retrieve it into a new folder (Project, Retrieve) and open it.
3. Rebuild all for the PLC and the HMI: zero errors.
4. Run the cold start above and one smoke test (T01).

### Clean clone (T67)

    cd C:\temp
    git clone https://github.com/HoraEmbedded/smart-pumping-station.git clean_check
    cd clean_check
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r tools\requirements.txt -r 05_iiot_data\python\requirements.txt
    python tools\verify_repo.py --final