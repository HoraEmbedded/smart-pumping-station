"""Tests to rerun after a change: list the tests linked to a block or file in the traceability matrix."""
import csv
import sys
from pathlib import Path

MATRIX = Path(__file__).resolve().parents[1] / "01_requirements" / "requirements_traceability_matrix.csv"


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: impact.py <block or file name> [more names]")
    keys = [k.lower() for k in sys.argv[1:]]
    tests, reqs = set(), []
    with MATRIX.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            refs = row["Design_Ref"].lower().split(";")
            if any(k in ref for k in keys for ref in refs):
                reqs.append(row["Req_ID"])
                tests.update(t for t in row["Test_IDs"].split(";") if t)
    print("requirements:", ", ".join(reqs) or "none")
    print("tests to rerun:", ", ".join(sorted(tests)) or "none")
    print("Shared blocks (OB1, DB_Parameters, DB_HMI): rerun every level 1 test as well.")


if __name__ == "__main__":
    main()