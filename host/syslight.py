# syslight.py - Host script for Visual RAM/CPU Usage Monitor with mode button
# Runs on Windows 11 with Python 3

import time
import csv
from datetime import datetime

import psutil
import serial

# ================== USER CONFIG ==================
PORT = "COM4"          # <-- change to your actual COM port (e.g. COM3, COM5)
BAUDRATE = 115200

INTERVAL_SEC = 1.0      # how often to send updates (seconds)

# Optional CSV logging
LOG_TO_CSV = False
CSV_PATH = "metrics.csv"
# =================================================

def get_metrics():
    """
    Return integer percentages for CPU and RAM usage.
    """
    cpu_value = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    ram_value = mem.percent

    return int(round(cpu_value)), int(round(ram_value))

def main():
    print(f"Opening serial port {PORT} at {BAUDRATE}...")
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)

    csv_file = None
    csv_writer = None
    if LOG_TO_CSV:
        csv_file = open(CSV_PATH, "a", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "cpu", "ram"])

    try:
        while True:
            cpu, ram = get_metrics()
            line = f"CPU:{cpu},RAM:{ram}\n"

            # send to ESP32
            ser.write(line.encode("ascii"))

            # optional logging
            if csv_writer is not None:
                csv_writer.writerow([
                    datetime.now().isoformat(timespec="seconds"),
                    cpu,
                    ram
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
