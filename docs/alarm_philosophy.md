# Alarm Philosophy

Inspired by ISA 18.2 principles.

## Rules

- Every alarm requires an operator action. Information without action is a message, not an alarm.
- Every alarm has an ID, a priority, probable causes, a system reaction and a reset condition.
- Critical faults latch: no automatic restart after a critical fault.
- Simulated safety logic is labeled Sim.
- Alarm text is short, readable and states the consequence.
- Color is never the only indicator: text and symbol are always displayed.
- An alarm indicates abnormal behavior, it does not prove a single cause.

## Alarm flood prevention

A single cause must not raise a cascade of alarms. Dependent alarms are suppressed when a higher priority alarm already explains them (for example, low flow is suppressed when the source is low).