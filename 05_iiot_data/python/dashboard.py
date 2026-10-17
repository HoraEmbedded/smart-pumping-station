"""Local read-only dashboard: serves one HTML page and a JSON view of a CSV dataset on 127.0.0.1."""
import argparse
import json
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from kpi import compute, load_rows

PAGE = Path(__file__).resolve().parents[1] / "dashboard" / "index.html"
LOCK = threading.Lock()
CACHE = {"sig": None, "rows": [], "kpi": {}}
CONFIG = {"csv": None, "replay": False, "window": 600}


def refresh():
    """Reload the dataset only when the file changed."""
    try:
        stat = CONFIG["csv"].stat()
    except OSError:
        return
    sig = (stat.st_size, stat.st_mtime)
    if sig != CACHE["sig"]:
        rows = load_rows(CONFIG["csv"])
        CACHE.update(sig=sig, rows=rows, kpi=compute(rows))


def series(rows):
    tail = rows[-CONFIG["window"]:]
    pts = tail[::max(1, len(tail) // 300)]
    if pts[-1] is not tail[-1]:
        pts.append(tail[-1])

    def col(name):
        return [round(r[name], 3) for r in pts]

    return {
        "t": [round(r["SimTime_s"] / 60.0, 2) for r in pts],
        "level": col("TankLevel_pct"), "source": col("SourceLevel_pct"),
        "flow": col("Flow_m3h"), "pressure": col("Pressure_bar"),
        "i1": col("P1_Current_A"), "i2": col("P2_Current_A"),
        "p1": col("P1_RunFeedback"), "p2": col("P2_RunFeedback"),
    }


def payload():
    with LOCK:
        refresh()
        rows, kpi = CACHE["rows"], CACHE["kpi"]
        if not rows:
            return {"rows": 0}
        last = rows[-1]
        data = series(rows)
    try:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(last["Timestamp"])).total_seconds()
    except ValueError:
        age = None
    return {
        "rows": len(rows),
        "file": CONFIG["csv"].name,
        "mode": "replay" if CONFIG["replay"] else "live",
        "age_s": age,
        "latest": {
            "state": int(last["StationState"]), "level": last["TankLevel_pct"],
            "source": last["SourceLevel_pct"], "flow": last["Flow_m3h"],
            "pressure": last["Pressure_bar"], "i1": last["P1_Current_A"], "i2": last["P2_Current_A"],
            "power": last["Power_kW"], "p1": int(last["P1_RunFeedback"]), "p2": int(last["P2_RunFeedback"]),
            "alarms": int(last["ActiveAlarmCount"]), "aw1": int(last["AlarmWord1"]),
            "aw2": int(last["AlarmWord2"]), "counter": int(last["SampleCounter"]),
            "sim_h": last["SimTime_s"] / 3600.0,
        },
        "kpi": kpi,
        "series": data,
    }


class Handler(BaseHTTPRequestHandler):
    """Only GET is implemented, any other method gets a 501 answer."""

    def do_GET(self):
        if self.path == "/":
            self.reply(200, "text/html; charset=utf-8", PAGE.read_bytes())
        elif self.path.startswith("/api"):
            self.reply(200, "application/json", json.dumps(payload()).encode("utf-8"))
        else:
            self.reply(404, "text/plain", b"not found")

    def reply(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", required=True, help="dataset file, written live by the collector or recorded")
    parser.add_argument("--port", type=int, default=8050)
    parser.add_argument("--window", type=int, default=600, help="number of samples shown in the trends")
    parser.add_argument("--replay", action="store_true", help="recorded dataset: no freshness check")
    args = parser.parse_args()
    CONFIG.update(csv=Path(args.csv), replay=args.replay, window=args.window)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"dashboard on http://127.0.0.1:{args.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()