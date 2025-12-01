# syslight.py - Host script for Visual RAM/CPU Usage Monitor
# Runs on Windows 11 with Python 3

import time
import csv
from datetime import datetime

import psutil
import serial

# ================== USER CONFIG ==================
PORT = "COM4"          # <-- change this to your ESP32 port (e.g. COM4, COM5)
BAUDRATE = 115200

# Choose which metric to send: "RAM" or "CPU"
METRIC = "RAM"

INTERVAL_SEC = 1.0     # how often to send updates (seconds)

# Optional CSV logging
LOG_TO_CSV = False
CSV_PATH = "metrics.csv"
# =================================================

def get_metric_value():
    """
    Return an integer percentage for RAM or CPU usage.
    """
    metric = METRIC.upper()
    if metric == "CPU":
        # First call can be 0.0, but that's fine for this project.
        value = psutil.cpu_percent(interval=None)
    else:
        # Default to RAM
        mem = psutil.virtual_memory()
        value = mem.percent

    return int(round(value)), metric

def main():
    print(f"Opening serial port {PORT} at {BAUDRATE}...")
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)

    csv_file = None
    csv_writer = None
    if LOG_TO_CSV:
        csv_file = open(CSV_PATH, "a", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "metric", "value"])

    try:
        while True:
            value, metric_label = get_metric_value()
            line = f"{metric_label}:{value}\n"
            # send to ESP32
            ser.write(line.encode("ascii"))

            # optional logging
            if csv_writer is not None:
                csv_writer.writerow([
                    datetime.now().isoformat(timespec="seconds"),
                    metric_label,
                    value
                ])
                csv_file.flush()

            # simple console feedback
            print(line.strip())

            time.sleep(INTERVAL_SEC)

    except KeyboardInterrupt:
        print("\nExiting (Ctrl+C pressed).")

    finally:
        if csv_file is not None:
            csv_file.close()
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
