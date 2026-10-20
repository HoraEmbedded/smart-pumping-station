"""Consistency checks on collected datasets. Exit code 1 if a check fails."""
import csv
import glob
import sys
from datetime import datetime

from dataset_schema import COLUMNS, RANGES, STATES


def check(path):
    errors = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            return ["header differs from the schema"], 0, 0
        rows = list(reader)
    if not rows:
        return ["no rows"], 0, 0
    missed = 0
    prev = None
    for line, r in enumerate(rows, start=2):
        if any(v == "" for v in r.values()):
            errors.append(f"line {line}: empty value")
            continue
        n, t, sim = int(r["SampleCounter"]), datetime.fromisoformat(r["Timestamp"]), float(r["SimTime_s"])
        if prev:
            if n <= prev[0]:
                errors.append(f"line {line}: sample counter not increasing")
            else:
                missed += n - prev[0] - 1
            if t <= prev[1]:
                errors.append(f"line {line}: timestamp not increasing")
            if sim < prev[2]:
                errors.append(f"line {line}: simulated time decreases")
        prev = (n, t, sim)
        for col, (lo, hi) in RANGES.items():
            if not lo <= float(r[col]) <= hi:
                errors.append(f"line {line}: {col} out of range")
        if int(r["StationState"]) not in STATES:
            errors.append(f"line {line}: unknown station state")
    if missed > 0.05 * len(rows):
        errors.append(f"{missed} missed samples")
    return errors, len(rows), missed


def main():
    failed = False
    paths = [p for arg in sys.argv[1:] for p in glob.glob(arg)]
    for path in sorted(paths):
        errors, count, missed = check(path)
        status = "OK  " if not errors else "FAIL"
        print(f"{status} {path}: {count} rows, {missed} missed")
        for e in errors[:10]:
            print(f"     {e}")
        failed = failed or bool(errors)
    sys.exit(1 if failed or not paths else 0)


if __name__ == "__main__":
    main()