"""Layout of the PLC export block and of the CSV files."""

DB_SIZE = 70

REALS = ["TankLevel_pct", "SourceLevel_pct", "Flow_m3h", "Pressure_bar", "P1_Current_A",
         "P2_Current_A", "P1_RunHours", "P2_RunHours", "Power_kW", "GT_Drain_m3h"]
FLAGS = ["P1_RunCmd", "P2_RunCmd", "P1_RunFeedback", "P2_RunFeedback",
         "P1_Fault", "P2_Fault", "SourceOK", "Demand"]
TRUTH = ["GT_Inject_P1_LowFlow", "GT_Inject_P2_LowFlow", "GT_Inject_P1_NoFeedback",
         "GT_Inject_P2_NoFeedback", "GT_Inject_P1_HighCurrent", "GT_Inject_P2_HighCurrent"]

COLUMNS = (["Timestamp", "SampleCounter", "SimTime_s", "StationState",
            "TankLevel_pct", "SourceLevel_pct", "Flow_m3h", "Pressure_bar",
            "P1_Current_A", "P2_Current_A"] + FLAGS
           + ["ActiveAlarmCount", "AlarmWord1", "AlarmWord2", "P1_RunHours", "P2_RunHours",
              "P1_StartCount", "P2_StartCount", "Power_kW", "GT_Drain_m3h"] + TRUTH)

STATES = {0, 10, 20, 30, 40, 50, 90}

RANGES = {
    "TankLevel_pct": (0.0, 100.0),
    "SourceLevel_pct": (0.0, 100.0),
    "Flow_m3h": (0.0, 20.5),
    "Pressure_bar": (0.0, 10.0),
    "P1_Current_A": (0.0, 20.0),
    "P2_Current_A": (0.0, 20.0),
    "Power_kW": (0.0, 20.0),
    "GT_Drain_m3h": (0.0, 20.0),
}