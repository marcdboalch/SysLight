# syslight.py - Host script for Visual RAM/CPU Usage Monitor with mode button
# Uses average per-core CPU usage with a configurable scale factor
# Runs on Windows 11 with Python 3

import psutil
import serial
import time

# ================== USER CONFIG ==================
PORT = "COM4"           # <-- change to your actual COM port (e.g. COM3, COM5)
BAUDRATE = 115200

UPDATE_INTERVAL = 1   # seconds between updates (0.5 = 2x/sec, 1.0 = 1x/sec)

# Scale factor to compensate for under-reporting on your system.
# If Task Manager says ~20% while this script says ~4%, try CPU_SCALE = 5.0.
CPU_SCALE = 7
# =================================================


def get_metrics():
    """
    Return integer percentages for "effective" CPU usage and RAM usage.

    CPU:
      - Get per-core usage list over UPDATE_INTERVAL
      - Take the average across all cores
      - Apply CPU_SCALE, clamp to 0–100

    This gives you a tunable approximation that you can visually line up with
    Task Manager by adjusting CPU_SCALE.
    """
    per_core = psutil.cpu_percent(interval=UPDATE_INTERVAL, percpu=True)

    if not per_core:
        cpu_avg = 0.0
    else:
        cpu_avg = sum(per_core) / len(per_core)

    # Apply scale factor
    cpu_value = cpu_avg * CPU_SCALE

    # Clamp 0–100
    if cpu_value < 0:
        cpu_value = 0.0
    if cpu_value > 100:
        cpu_value = 100.0

    ram_value = psutil.virtual_memory().percent

    return int(round(cpu_value)), int(round(ram_value))


def main():
    print(f"Opening serial port {PORT} at {BAUDRATE}...")
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)

    # Warm-up (initial call not strictly necessary here, but harmless)
    _ = psutil.cpu_percent(interval=None, percpu=True)

    try:
        while True:
            cpu, ram = get_metrics()

            line = f"CPU:{cpu},RAM:{ram}\n"
            ser.write(line.encode("ascii"))

            # Debug print so you can tweak CPU_SCALE
            print(line.strip())

    except KeyboardInterrupt:
        print("\nExiting.")

    finally:
        ser.close()
        print("Serial port closed.")


if __name__ == "__main__":
    main()
