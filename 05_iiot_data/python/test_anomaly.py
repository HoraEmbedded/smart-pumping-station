"""Tests of the anomaly rules on constructed values."""
import inspect
import unittest

import anomaly_rules
from anomaly_rules import (PARAMS, ano_01, ano_02, ano_03, ano_04, ano_05, ano_06, periods)


def rows_of(n, **series):
    """n samples, counter plus 1 and simulated time plus 60 s per sample (acceleration 60)."""
    base = {"SampleCounter": 0.0, "SimTime_s": 0.0, "TankLevel_pct": 50.0, "SourceLevel_pct": 80.0,
            "Flow_m3h": 0.0, "Pressure_bar": 0.0, "P1_Current_A": 0.0, "P2_Current_A": 0.0,
            "P1_RunCmd": 0.0, "P2_RunCmd": 0.0, "P1_RunFeedback": 0.0, "P2_RunFeedback": 0.0,
            "P1_StartCount": 0.0, "P2_StartCount": 0.0}
    rows = []
    for i in range(n):
        row = dict(base, SampleCounter=float(i), SimTime_s=60.0 * i)
        for key, value in series.items():
            row[key] = value[i] if isinstance(value, (list, tuple)) else value
        rows.append(row)
    return rows


def window(n, a, b):
    return [1.0 if a <= i < b else 0.0 for i in range(n)]


class RuleTests(unittest.TestCase):
    def test_ano_01_after_the_delay_only(self):
        run = window(15, 2, 14)
        flags = ano_01(rows_of(15, P1_RunFeedback=run, P1_Current_A=[10.0 * x for x in run]), PARAMS)
        self.assertIsNone(flags[6])
        self.assertIn("normal", flags[7])
        self.assertIsNotNone(flags[13])
        self.assertIsNone(flags[14])

    def test_ano_01_current_orients_the_hint(self):
        run = window(15, 2, 14)
        flags = ano_01(rows_of(15, P1_RunFeedback=run, P1_Current_A=[13.0 * x for x in run]), PARAMS)
        self.assertIn("blockage", flags[7])

    def test_ano_01_quiet_with_normal_flow(self):
        run = window(15, 2, 14)
        flags = ano_01(rows_of(15, P1_RunFeedback=run, Flow_m3h=12.0), PARAMS)
        self.assertTrue(all(f is None for f in flags))

    def test_ano_03_needs_high_current(self):
        run = window(15, 2, 14)
        high = ano_03(rows_of(15, P1_RunFeedback=run, P1_Current_A=[13.0 * x for x in run]), PARAMS)
        normal = ano_03(rows_of(15, P1_RunFeedback=run, P1_Current_A=[10.0 * x for x in run]), PARAMS)
        self.assertIsNotNone(high[7])
        self.assertTrue(all(f is None for f in normal))

    def test_ano_02_flat_level_is_flagged_after_the_window(self):
        flags = ano_02(rows_of(20, P1_RunFeedback=window(20, 2, 18), Flow_m3h=12.0, TankLevel_pct=40.0), PARAMS)
        self.assertIsNone(flags[6])
        self.assertIsNotNone(flags[7])
        self.assertIsNotNone(flags[17])

    def test_ano_02_rising_level_is_quiet(self):
        level = [30.0 + 1.5 * i for i in range(20)]
        flags = ano_02(rows_of(20, P1_RunFeedback=window(20, 2, 18), Flow_m3h=12.0, TankLevel_pct=level), PARAMS)
        self.assertTrue(all(f is None for f in flags))

    def test_ano_02_window_restarts_when_the_pump_changes(self):
        flags = ano_02(rows_of(20, P1_RunFeedback=window(20, 2, 7), P2_RunFeedback=window(20, 7, 17),
                               Flow_m3h=12.0, TankLevel_pct=40.0), PARAMS)
        self.assertIsNone(flags[11])
        self.assertIsNotNone(flags[12])

    def test_ano_04_four_starts_in_a_short_time(self):
        counts = [float(sum(i >= s for s in (2, 6, 10, 14))) for i in range(30)]
        flags = ano_04(rows_of(30, P1_StartCount=counts), PARAMS)
        self.assertIsNone(flags[13])
        self.assertIsNotNone(flags[14])

    def test_ano_04_spread_starts_are_quiet(self):
        counts = [float(i // 40) for i in range(170)]
        flags = ano_04(rows_of(170, P1_StartCount=counts), PARAMS)
        self.assertTrue(all(f is None for f in flags))

    def test_ano_05_flow_without_pump_needs_persistence(self):
        steady = ano_05(rows_of(10, Flow_m3h=[0, 0, 5, 5, 5, 0, 0, 0, 0, 0]), PARAMS)
        single = ano_05(rows_of(10, Flow_m3h=[0, 0, 5, 0, 0, 0, 0, 0, 0, 0]), PARAMS)
        self.assertIsNone(steady[3])
        self.assertIn("flow", steady[4].lower())
        self.assertTrue(all(f is None for f in single))

    def test_ano_05_range_is_immediate(self):
        flags = ano_05(rows_of(6, TankLevel_pct=[50, 50, 120, 50, 50, 50]), PARAMS)
        self.assertIsNotNone(flags[2])

    def test_ano_05_current_and_feedback_inconsistencies(self):
        current = ano_05(rows_of(10, P1_Current_A=[0, 0, 5, 5, 5, 0, 0, 0, 0, 0]), PARAMS)
        feedback = ano_05(rows_of(10, P1_RunFeedback=[0, 0, 1, 1, 1, 0, 0, 0, 0, 0], Flow_m3h=12.0), PARAMS)
        self.assertIn("current", current[4])
        self.assertIn("feedback", feedback[4])

    def test_ano_06_flags_the_pump_drawing_more(self):
        n = 24
        p2, p1 = window(n, 2, 10), window(n, 12, 22)
        flow = [12.0 if p1[i] or p2[i] else 0.0 for i in range(n)]
        rows = rows_of(n, P1_RunFeedback=p1, P2_RunFeedback=p2, Flow_m3h=flow,
                       P1_Current_A=[13.0 * x for x in p1], P2_Current_A=[10.0 * x for x in p2])
        flags = ano_06(rows, PARAMS)
        self.assertIsNone(flags[13])
        self.assertIn("30 percent", flags[14])
        self.assertTrue(all(f is None for f in flags[:12]))

    def test_ano_06_needs_a_reference_and_a_real_gap(self):
        n = 24
        first, second = window(n, 2, 10), window(n, 12, 22)
        flow = [12.0 if first[i] or second[i] else 0.0 for i in range(n)]
        high_first = ano_06(rows_of(n, P1_RunFeedback=first, P2_RunFeedback=second, Flow_m3h=flow,
                                    P1_Current_A=[13.0 * x for x in first],
                                    P2_Current_A=[10.0 * x for x in second]), PARAMS)
        small_gap = ano_06(rows_of(n, P2_RunFeedback=first, P1_RunFeedback=second, Flow_m3h=flow,
                                   P2_Current_A=[10.0 * x for x in first],
                                   P1_Current_A=[10.5 * x for x in second]), PARAMS)
        self.assertTrue(all(f is None for f in high_first))
        self.assertTrue(all(f is None for f in small_gap))

    def test_ano_06_ignores_unlike_operating_points(self):
        n = 24
        p2, p1 = window(n, 2, 10), window(n, 12, 22)
        flow = [12.0 if p2[i] else (6.0 if p1[i] else 0.0) for i in range(n)]
        rows = rows_of(n, P1_RunFeedback=p1, P2_RunFeedback=p2, Flow_m3h=flow,
                       P1_Current_A=[13.0 * x for x in p1], P2_Current_A=[10.0 * x for x in p2])
        self.assertTrue(all(f is None for f in ano_06(rows, PARAMS)))

    def test_periods_group_close_flags(self):
        flags = [None, None, None, "a", "a", None, "a"] + [None] * 5 + ["b"]
        found = periods(rows_of(len(flags)), flags)
        self.assertEqual([(q["start"], q["end"]) for q in found], [(3, 6), (12, 12)])

    def test_rules_never_name_the_injection_columns(self):
        self.assertNotIn("GT_", inspect.getsource(anomaly_rules))


if __name__ == "__main__":
    unittest.main()