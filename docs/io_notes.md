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