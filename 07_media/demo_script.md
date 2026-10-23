# Demonstration Script

Target length: 4 min 40 s. Screen recording, text captions, no voice-over.

## Preparation before recording

| Window | Content |
| --- | --- |
| A | Browser tab 1: dashboard on http://127.0.0.1:8050 (LIVE pill, green) |
| B | TIA Portal: Watch Table with the 15 exported variables |
| C | WinCC Runtime: Overview screen |
| D | Browser tab 2: P&ID diagram (02_design/diagrams/pid_simplified.png) |
| E | Browser tab 3: D05_leak_anomalies.png figure |

Close Slack, mail, and every other window that shows notifications.

## Sequence

| Time | Segment | Shown | Caption text |
| --- | --- | --- | --- |
| 0:00 | Industrial problem | P&ID | A utility station keeps a tank between two levels with two pumps. It must avoid dry running, excessive starts, overflow and unsafe restarts. |
| 0:15 | Architecture | OT/IT diagram | 24 signals, a S7-1200 program in 14 blocks, a WinCC HMI, a read-only OPC UA data path. |
| 0:35 | Watch table | TIA Portal, variables | The same values, exported every second: level, flow, currents, pumps, alarms. |
| 0:55 | Auto cycle low level | IHM Overview | Auto mode. Pump 1 starts at 30 percent, feedback confirmed, flow 12 m3/h. |
| 1:20 | Auto cycle high level | IHM Overview | At 80 percent the pump stops. Priority passes to pump 2. No alarm. |
| 1:40 | Alternation | Watch Table, Priority field | After a normal cycle the priority switches. Pump wear stays balanced. |
| 2:00 | Fault injection | Watch Table, Inject_P1_LowFlow TRUE | The PLC detects the fault. Pump 1 unavailable, ALM 004. Pump 2 takes over. |
| 2:30 | Alarms screen | IHM Alarms | Acknowledging the alarm means "seen". It never clears a latched fault. |
| 2:50 | Reset refused | IHM Overview | Reset is refused while the cause persists. A real reset needs the cause cleared. |
| 3:10 | Dashboard | Browser, dashboard | Reliability indicators, live. Availability, duty, specific energy, anomaly rules. |
| 3:35 | Anomaly rules | D05_leak_anomalies.png figure | Six explainable rules. Each flag gives the values and the threshold crossed. |
| 4:10 | Limits and skills | Closing caption | Validated in simulation. No physical controller, no field data. Skills: PLC in SCL and Ladder, HMI and alarms, data, testing, traceability. |

## Caption style

- Font: Segoe UI Bold, size 22, white text on semi-transparent black band
- Position: bottom of the frame, 40 px margin
- Timing: 1 caption per segment, displayed for the whole segment

## Recording tips

- Record segment by segment, not in one take
- Between segments, take a breath and reset the scene
- Keep the mouse still during a recording (no shaking)
- No mouse cursor visible on captions if possible
- Resolution: 1920x1080 if the screen allows, otherwise 1366x768