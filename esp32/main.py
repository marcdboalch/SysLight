# main.py - ESP32 Visual System Resource Usage Monitor

import sys
from machine import Pin

# --- CONFIGURABLE LED PIN LIST (order matters: G0, G1, Y0, Y1, R0, R1) ---
LED_PINS = [16, 17, 18, 19, 21, 22]

# Thresholds (percentages) - adjust if you want different ranges
LOW_MAX = 33      # 0 - 33%  -> 2 green LEDs
MED_MAX = 66      # 34 - 66% -> 2 green + 2 yellow
# 67 - 100%       -> all 6 LEDs

# --- INITIALIZE LED OBJECTS ---
leds = [Pin(pin_num, Pin.OUT) for pin_num in LED_PINS]

def clear_leds():
    """Turn all LEDs off."""
    for led in leds:
        led.value(0)

def set_usage_level(percent):
    """
    Light LEDs based on usage percentage.
    0%      -> all OFF
    1-33%   -> 2 green
    34-66%  -> 2 green + 2 yellow
    67-100% -> all 6 (green + yellow + red)
    """
    # clamp to 0-100
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100

    clear_leds()

    if percent == 0:
        return  # leave everything off

    # Decide how many LEDs to light
    if percent <= LOW_MAX:
        count = 2   # green only
    elif percent <= MED_MAX:
        count = 4   # green + yellow
    else:
        count = 6   # all

    for i in range(count):
        leds[i].value(1)

def parse_line(line):
    """
    Accepts lines like:
        'RAM:57'
        'CPU:42'
        '75'
    Returns integer percentage or None if invalid.
    """
    try:
        s = line.strip()
        if not s:
            return None

        if ":" in s:
            _, num = s.split(":", 1)
        else:
            num = s

        value = int(num)
        # basic sanity clamp
        if value < 0:
            value = 0
        if value > 100:
            value = 100
        return value
    except:
        return None

# --- MAIN LOOP ---
clear_leds()

while True:
    # read one line from USB serial (this is blocking)
    line = sys.stdin.readline()

    if not line:
        continue

    value = parse_line(line)
    if value is not None:
        set_usage_level(value)
