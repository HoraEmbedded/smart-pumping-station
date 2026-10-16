# OPC UA Setup Notes

Sequence that gave a Python client access to the export tags on the lab PC (2026-10-16).

## Sequence that worked

| Step | Observation |
| --- | --- |
| Simulation component only | Port 4861 stayed closed, connection refused |
| WinCC Runtime Professional V18 package installed | Port still closed, the certificate manager reported no certificate authority |
| Certificate authority created, server certificate generated | The installer component check then failed on the IIS components |
| IIS features enabled (ASP.NET, IIS 6 Metabase Compatibility, Windows and Anonymous Authentication) | Rebuild all of the HMI, runtime started, port 4861 listening |

Which of these steps was individually required was not isolated.

## Access

| Item | Value |
| --- | --- |
| Endpoint | opc.tcp://localhost:4861 |
| Security used for the local test | Anonymous policy (None) |
| Tag nodes | ns=1;s=t|<HMI tag name> |
| Tag list node | ns=1;s=f|@LOCALMACHINE::List of all tags |
| Native PLC endpoint (port 4840) | Answers BadServiceUnsupported, the simulated S7-1200 does not serve OPC UA |

## Housekeeping

Certificates and keys stay out of the repository.