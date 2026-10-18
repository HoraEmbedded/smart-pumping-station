# Test Report V5

## Scope

Explainable anomaly rules ANO_01 to ANO_06, their evaluation against the injected faults and the normal dataset. Requirements REQ-027, REQ-053, REQ-054.

## Environment

Python 3.13, datasets D01 to D06 collected through the OPC UA collector. No change to the PLC.

## Results

| Group | Tests | Result |
| --- | --- | --- |
| Rule behavior | T58 | Pass |
| Evaluation | T26, T59 | Pass |
| Explanations | T60 | Pass |

Summary: All rules fired as expected on the 6 datasets. D01_normal stayed quiet (0 flags). ANO_01 detection delay is approximately 5 samples. 

## Defects found

| ID | Description | Resolution |
| --- | --- | --- |
| 1 | ANO_06 misses the first run of a pump because it needs a reference from the other pump | Documented as a known blind spot in docs/anomaly_rules.md |

## Open points

- The thresholds come from a noiseless simulation, the margins must be measured again on field data.
- Blind spots are listed in docs/anomaly_rules.md.