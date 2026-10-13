### 2026-10-10 - CPU frozen at state 0 and TIA compilation errors (Mission 6)

- Context: Integration of critical alarms into Main (OB1) and FB_ModeManager.
- Symptom: PLC stuck at state 0 (Start ignored). Attempted fixes generated over 30 syntax errors (e.g., "Tag FUNCTION_BLOCK not defined").
- Attempts:
  1. Verified that all block calls were present in OB1.
  2. Pasted raw SCL file code (including headers) directly into the TIA block editor.
- Root cause: The FB_ModeManager interface was modified without updating its associated instance DB. Syntax errors were caused by mixing raw text file headers inside the graphical block environment.
- Solution: Cleaned the code sheets, right-clicked on DB_ModeManager > "Update block call", and performed a full software rebuild.
- Lesson learned: Always update the instance DB immediately after modifying a Function Block (FB) interface. Never paste structural file declarations (FUNCTION_BLOCK/END_VAR) into standard TIA Portal block editors.

### 2026-10-11 - WinCC RT Professional invalid HMI connection and missing subnet interface

- Context: Adding the PC-based HMI device (WinCC RT Professional V18) and establishing the symbolic PROFINET link to the PLC.
- Symptom: Hardware compilation failed with 3 errors stating "Partly specified connection - Local interface missing; Partner subnet not connected". The HMI connection remained invalid, and tracing a link only created a logical relation line instead of a green PROFINET cable.
- Attempts:
  1. Tried to force-connect the link directly in the Network view using the "HMI Connection" routing option. This resulted in an invalid link because the PC station had no physical port to bind to.
- Root cause: By default, a new SIMATIC PC Station inside TIA Portal is created with a blank hardware rack. It does not possess a built-in Ethernet network card, preventing the software compiler from assigning an IP address or tying it to the PROFINET subnet.
- Solution: Opened the HMI_Station Device View, selected "IE General" from the Hardware Catalog (Communications modules > PROFINET/Ethernet), and dragged it into an empty slot of the PC rack. Then traced the green network cable from the new Ethernet port to the PLC CPU, and performed a full Software Rebuild All.
- Lesson learned: Unlike specialized touch panels (Comfort Panels) which have fixed built-in ports, PC-based runtimes (WinCC Professional) require explicit hardware configuration. An industrial network card module (like IE General) must always be inserted into the virtual PC chassis before any network or connection routing can take place.
