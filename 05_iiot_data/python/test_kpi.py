"""Hand-checkable tests of the indicator computation."""
import unittest

from kpi import compute


def dataset():
    """Eleven samples 60 s apart, ten intervals of 600 s in total.

    Pump 1 runs in intervals 1 to 5, is unavailable in intervals 6 and 7,
    the station is in FAULT in intervals 8 and 9.
    """
    rows = []
    for i in range(11):
        running = 1 <= i <= 5
        rows.append({
            "SimTime_s": 60.0 * i,
            "StationState": 90.0 if i >= 8 else 30.0,
            "P1_RunFeedback": 1.0 if running else 0.0,
            "P2_RunFeedback": 0.0,
            "AlarmWord1": 32.0 if i in (6, 7) else 0.0,
            "Flow_m3h": 12.0 if running else 0.0,
            "Power_kW": 6.0 if running else 0.0,
            "P1_StartCount": 0.0 if i == 0 else 1.0,
            "P2_StartCount": 0.0,
        })
    return rows


EXPECTED = {
    "sim_hours": 0.167,
    "run_hours_p1": 0.0833, "run_hours_p2": 0.0,
    "duty_p1_pct": 50.0, "duty_p2_pct": 0.0,
    "starts_p1": 1, "starts_p2": 0, "starts_per_hour": 6.0,
    "station_availability_pct": 80.0, "fault_share_pct": 20.0,
    "pump1_availability_pct": 80.0, "pump2_availability_pct": 100.0,
    "failures_p1": 1, "failures_p2": 0,
    "mtbf_p1_h": 0.0833, "mttr_p1_h": 0.0333,
    "mean_flow_pumping_m3h": 12.0, "volume_m3": 1.0,
    "energy_kwh": 0.5, "specific_energy_kwh_m3": 0.5,
}


class IndicatorTests(unittest.TestCase):
    def test_known_values(self):
        result = compute(dataset())
        for key, value in EXPECTED.items():
            with self.subTest(key=key):
                self.assertAlmostEqual(result[key], value, places=3)
        self.assertIsNone(result["mtbf_p2_h"])
        self.assertIsNone(result["mttr_p2_h"])

    def test_stopped_clock_has_no_weight(self):
        rows = dataset()
        rows.insert(4, dict(rows[3]))  # same simulated time as the previous sample
        reference = compute(dataset())
        result = compute(rows)
        reference.pop("rows")
        result.pop("rows")
        self.assertEqual(result, reference)

    def test_too_short_input(self):
        result = compute(dataset()[:1])
        self.assertIsNone(result["station_availability_pct"])


if __name__ == "__main__":
    unittest.main()