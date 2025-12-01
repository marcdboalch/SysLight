# main.py - ESP32 Visual RAM/CPU Usage Monitor with half-steps
# Runs on ESP32 with MicroPython

import sys
from machine import Pin

# LED order: [G0, G1, Y0, Y1, R0, R1]
# Make sure your wiring matches these pins.
LED_PINS = [2, 4, 5, 18, 19, 23]

# Percentage ranges for how many LEDs to light.
# You can adjust these if you want different breakpoints.
def leds_for_percent(percent):
    """
    Map usage percentage to a number of LEDs (0–6).

    0%          -> 0 LEDs (all off)
    1–10%       -> 1 LED   (1 green)
    11–30%      -> 2 LEDs  (2 green)
    31–50%      -> 3 LEDs  (2 green + 1 yellow)
    51–70%      -> 4 LEDs  (2 green + 2 yellow)
    71–90%      -> 5 LEDs  (2 green + 2 yellow + 1 red)
    91–100%     -> 6 LEDs  (all: 2 green + 2 yellow + 2 red)
    """
    if percent <= 0:
        return 0
    elif percent <= 10:
        return 1
    elif percent <= 30:
        return 2
    elif percent <= 50:
        return 3
    elif percent <= 70:
        return 4
    elif percent <= 90:
        return 5
    else:
        return 6

# --- INITIALIZE LED OBJECTS ---
leds = [Pin(pin_num, Pin.OUT) for pin_num in LED_PINS]

def clear_leds():
    """Turn all LEDs off."""
    for led in leds:
        led.value(0)

def set_usage_level(percent):
    """
    Light LEDs based on usage percentage using the half-step scheme.
    """
    # clamp to 0–100
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100

    clear_leds()

    count = leds_for_percent(percent)

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
    # read one line from USB serial (blocking)
    line = sys.stdin.readline()

    if not line:
        continue

    value = parse_line(line)
    if value is not None:
        set_usage_level(value)
