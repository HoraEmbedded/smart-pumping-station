### 2026-10-10 - CPU frozen at state 0 and TIA compilation errors (Iteration 6)

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

### 2026-10-15 - WinCC Professional Trend View Reset & Reversed Axis (iteration 10)

- Context: WinCC RT Professional Trend View setup for a smart pumping system.
- Symptom: Graph reset to zero on page change, and time axis read backwards (decreasing).
- Attempts:
  1. Used online real-time mode: Data reset every time the page was left.
  2. Changed "Trend" setting to "From the right": 
  3. Corrected start/end timestamps: Restored normal chronological order.
- Root cause: Missing background logging tag setup causing volatile displa, combined with an inverted time axis range (`Start time` > `End time`).
- Solution: Configured Data Log and Logging tags(in historical data board), linked Trend View to the log source, and adjusted `Start time` to precede `End time`.
- Lesson learned: Persistent trends require Data Logs, and time axis bounds must be strictly chronological.

### 2026-10-16 - OPC UA connectivity setup under WinCC Professional simulation environment

- Context: Feasibility test phase (initial 30-min limit extended) to evaluate replacing a legacy VB script CSV export with a data collection workflow via a Python client (asyncua) connected to the local OPC UA server. Development environment using TIA Portal V18 with an S7-1200 PLC configured in simulation.
- Symptom: Unable to connect to the OPC UA server. Diagnostic tools (uals, uaread) and the custom Python script returned Timeout errors, followed by a connection refusal: `[WinError 1225] The remote computer refused the network connection`. The target port remained closed during netstat checks.
- Attempts:
  1. Targeted the PLC OPC UA server port (Port 4840) under standard PLCSIM: The port responded but the connection failed with a `BadServiceUnsupported` error. PLCSIM Advanced was not used as it does not list the S7-1200 in its supported hardware documentation.
  2. Targeted the WinCC architecture port (Port 4861) using the integrated TIA Portal HMI simulation button: The connection was still refused with `WinError 1225`.
  3. Checked the TIA software inventory, which listed `SIMATIC WinCC Runtime Professional Simulation` instead of the standalone Runtime package. Installed the standalone WinCC Runtime Professional V18 setup.
  4. The installer package blocked at startup with the error message: "Check for IIS components failed!".
  5. Opened the WinCC Certificate Manager, which flagged "No CA configured". Created a local Certificate Authority (My_CA_WinCC) and generated a server certificate (.der).
- Root cause: The simulation environment running via the standard HMI simulation button did not open the network port. Activating the external OPC UA interface requires a specific sequence of local platform configurations (standalone Runtime components, operational IIS feature dependencies, and an active local certificate binding).
- Solution: Executed the following sequence to open the communication channel:
  1. Manually enabled the missing IIS Windows features flagged by the installer (including ASP.NET, IIS 6 Metabase Compatibility, and Windows/Anonymous Authentication).
  2. Created the server certificate in the WinCC Certificate Manager under the local CA.
  3. Performed a full hardware and software recompile (Rebuild all) of the HMI station within TIA Portal.
  4. Started the WinCC Runtime. Port 4861 shifted to `LISTENING` status in netstat, allowing the Python client to browse the address space (`ns=1;s=t|...`) and pull real-time process values.
- Lesson learned: Evaluating external industrial network interfaces (like OPC UA) in a local simulation environment requires verifying that the full standalone execution engine is deployed alongside its specific operating system dependencies (such as IIS components and valid local certificate paths), rather than relying solely on the default integrated HMI simulator.

