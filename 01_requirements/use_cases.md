# Use Cases

## UC-01 Normal start in Auto
- Given: state READY, Auto mode, source level above 15 percent, no active alarm
- When: tank level falls to 30 percent
- Then: the priority pump starts after the restart delay, run feedback is confirmed, tank level rises
- Expected alarms: none

## UC-02 Fill and stop at high level
- Given: one pump running in Auto
- When: tank level reaches 80 percent
- Then: the pump stops normally and the priority switches to the other pump after a normal cycle
- Expected alarms: none

## UC-03 Pump failure during operation
- Given: P1 running in Auto
- When: P1 fault input becomes FALSE
- Then: P1 stops and is locked out, P2 takes over if available, otherwise the station goes to FAULT
- Expected alarms: ALM_006, and ALM_009 if P2 is also unavailable

## UC-04 Source water shortage
- Given: a pump is running or a start is requested
- When: source level falls below 15 percent or DI_Source_Low is TRUE
- Then: the pump stops and any start is inhibited until the source recovers
- Expected alarms: ALM_002

## UC-05 Low flow detection
- Given: P1 running, flow validation delay of 10 simulated seconds elapsed
- When: flow stays below 2 m3/h
- Then: P1 becomes unavailable and P2 is used if allowed
- Expected alarms: ALM_004