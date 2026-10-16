# Operator Guide

Pumping station operator manual, two pages. Screens are reached from the navigation bar at the bottom.

## 1. Reading the screen

The header shows the station state, the alarm level (NORMAL, WARNING, CRITICAL) and the number of active alarms. Below it, a message bar explains why an action was refused or delayed. Every state is also written as text: color is a second channel.

| State | Meaning |
| --- | --- |
| STOPPED | Pumps off, known state |
| INITIALIZING | Start-up checks, about 2 seconds |
| READY | Waiting for a mode |
| AUTO RUNNING | The station keeps the tank between 30 and 80 percent |
| MANUAL RUNNING | You command each pump |
| MAINTENANCE | Controlled pump tests, limited to 60 seconds |
| FAULT | Pumps off, a critical fault needs a reset |

## 2. Starting the station

1. Commands screen, press **Start**. The state goes to INITIALIZING, then READY.
2. Choose a mode: **Auto**, **Manual** or **Maintenance**. A mode change always passes through READY, so the pumps stop first.
3. **Stop** brings the station back to STOPPED.

## 3. Pumps

Each pump shows its status: STOPPED, RUNNING, STARTING or UNAVAILABLE. The two circles show the **command** (what the station asks) and the **feedback** (what the pump confirms). A command without feedback shows STARTING, then UNAVAILABLE after 5 seconds.

In Manual and Maintenance, use the pump buttons. The message bar tells you why a pump does not start: unavailable, source low, other pump running, restart delay (30 seconds) or test time reached.

## 4. Alarms

Open the **Alarms** screen. Each alarm shows its class, time and text. Press **Info text** to read the probable causes and the action to take.

| Class | Meaning | Acknowledgment |
| --- | --- | --- |
| [ X ] CRITICAL | Immediate stop, FAULT | Required |
| [ ! ] HIGH | Quick action needed | Required |
| [ ! ] MEDIUM | Action needed, not urgent | Required |
| [ i ] WARNING | Information, clears by itself | Not required |

**Acknowledge** means you have seen the alarm. It changes nothing in the process. **Reset** clears a latched fault, and only works when its cause is gone, otherwise the message bar says RESET REFUSED. After a reset the station returns to STOPPED and waits for a new Start.

**Silence horn** stops the siren for the current alarms. A new critical alarm sounds it again.

## 5. Maintenance screen

Run hours, start counts, current and service status per pump, and the validity of every signal. A signal shown INVALID points to a wiring or sensor problem. When a pump shows DUE, schedule its maintenance and reset its hours from the Commands screen in Maintenance mode.

## 6. Typical situations

| Situation | What you see | What to do |
| --- | --- | --- |
| Emergency stop | EMERGENCY STOP ACTIVE, state FAULT | Check the area, release the E-stop, Reset, Start |
| Low flow on a pump | LOW FLOW ON PUMP 1, other pump takes over | Check valves and filter, inspect the pump, Reset |
| Source level low | SOURCE LEVEL LOW, pumps cannot start | Check the supply, the alarm clears when the level recovers |
| No pump available | NO PUMP AVAILABLE, state FAULT | Repair a pump, Reset, Start |
| Tank level not rising | WARNING, pump keeps running | Check consumption and the line |
| Frequent starts | WARNING | Review the level thresholds, check for leaks |

## 7. Trends

The Trends screen shows tank level, flow, pressure and the active pump over the last 10 minutes.