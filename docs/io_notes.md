# I/O Notes

## Fail-safe logic

- DI_EStop_Sim is wired as a normally closed (NC) contact. A broken wire gives FALSE, which the PLC reads as an emergency stop. A visible fault is preferred to a hidden one. This is simulated logic only, not a certified safety chain.
- DI_P1_Fault and DI_P2_Fault follow the same NC principle: FALSE means fault.

## Analog scaling

    Value_eng = Min + (Raw / 27648) x (Max - Min)

Below 4 mA (wire break) the value is flagged inconsistent and raises ALM_008.

## Addresses

Addresses are indicative and may be adjusted in TIA Portal. Names are the reference.

## Operator commands

There is no physical pump pushbutton in the I/O list. In Manual and Maintenance the run request comes from DB_HMI (P1_PumpCmd), written from the watch table now and from the HMI later.
Start, stop, reset and mode selection can come from the local inputs or from the HMI (DB_HMI command bits). They are combined with a logical OR. The HMI mode selection behaves like a selector switch: it keeps its position. Two different mode positions at the same time (local and HMI) count as no selection, and the station stays in READY. Operator pump commands are cleared when the station leaves Manual and Maintenance.

## Alarm and message interface

Active alarms are published as bits of two Word tags in DB_HMI. AlarmWord1 carries the faults (bit 0 emergency stop to bit 8 no pump available), AlarmWord2 carries the warnings (bit 0 frequent starts to bit 6 non critical sensor). The mapping is listed in 04_hmi/hmi_alarms.csv. Cmd_Silence silences the siren without clearing any alarm. OperatorMessage carries the reason of a refused or delayed operator action.