"""Compute the indicators of every dataset and write a summary CSV."""
import csv
from pathlib import Path

from kpi import KPI_KEYS, compute, load_rows

ROOT = Path(__file__).resolve().parents[1]


def cell(value, digits):
    return "n/a" if value is None else f"{value:.{digits}f}"


def main():
    files = sorted((ROOT / "datasets").glob("D0*.csv"))
    out_path = ROOT / "kpi_summary.csv"
    print(f"{'dataset':24}{'hours':>7}{'stn av%':>9}{'p1 av%':>8}{'starts/h':>9}"
          f"{'duty1%':>8}{'duty2%':>8}{'kWh/m3':>8}{'mttr1 h':>9}")
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset"] + KPI_KEYS)
        for path in files:
            k = compute(load_rows(path))
            writer.writerow([path.stem] + ["" if k[key] is None else k[key] for key in KPI_KEYS])
            print(f"{path.stem:24}{cell(k['sim_hours'], 1):>7}{cell(k['station_availability_pct'], 1):>9}"
                  f"{cell(k['pump1_availability_pct'], 1):>8}{cell(k['starts_per_hour'], 2):>9}"
                  f"{cell(k['duty_p1_pct'], 1):>8}{cell(k['duty_p2_pct'], 1):>8}"
                  f"{cell(k['specific_energy_kwh_m3'], 3):>8}{cell(k['mttr_p1_h'], 2):>9}")
    print(f"written to {out_path}")


if __name__ == "__main__":
    main()