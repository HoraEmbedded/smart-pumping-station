"""Read the export tags from the WinCC OPC UA server and append new samples to a CSV file. Read only."""
import argparse
import asyncio
import csv
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from asyncua import Client

from dataset_schema import COLUMNS

PREFIX = "ns=1;s=t|DB_IIoTExport_"
NAMES = [c for c in COLUMNS if c != "Timestamp"]


def fmt(value):
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, float):
        return round(value, 4)
    return value


async def run(args):
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = missed = errors = 0
    last = None
    end = time.monotonic() + args.duration
    async with Client(url=args.url, timeout=10) as client:
        nodes = [client.get_node(PREFIX + name) for name in NAMES]
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            while time.monotonic() < end:
                try:
                    values = await client.read_values(nodes)
                except Exception as exc:
                    errors += 1
                    print(f"read error: {exc}")
                    await asyncio.sleep(args.poll)
                    continue
                row = {name: fmt(v) for name, v in zip(NAMES, values)}
                n = int(row["SampleCounter"])
                if n != last:
                    if last is not None and n - last > 1:
                        missed += n - last - 1
                    row["Timestamp"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
                    writer.writerow(row)
                    f.flush()
                    rows += 1
                    last = n
                await asyncio.sleep(args.poll)
    print(f"{rows} samples written to {out}, {missed} missed, {errors} read errors")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="opc.tcp://127.0.0.1:4861")
    parser.add_argument("--out", required=True)
    parser.add_argument("--duration", type=float, default=60.0)
    parser.add_argument("--poll", type=float, default=0.5)
    args = parser.parse_args()
    logging.getLogger("asyncua").setLevel(logging.ERROR)
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("stopped")


if __name__ == "__main__":
    main()