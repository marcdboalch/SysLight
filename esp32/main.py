# main.py - ESP32 Visual RAM/CPU Usage Monitor with mode button
# Runs on ESP32 with MicroPython

import sys
from machine import Pin

# Bar graph LED order: [G0, G1, Y0, Y1, R0, R1]
BAR_LED_PINS = [2, 4, 5, 18, 19, 23]

# Mode indicator LEDs
CPU_LED_PIN = 25   # Blue LED
RAM_LED_PIN = 26   # Clear/White LED

# Mode button
BUTTON_PIN = 27

# --- INITIALIZE HARDWARE ---

bar_leds = [Pin(pin_num, Pin.OUT) for pin_num in BAR_LED_PINS]
cpu_led = Pin(CPU_LED_PIN, Pin.OUT)
ram_led = Pin(RAM_LED_PIN, Pin.OUT)

# Button with internal pull-up: pressed -> 0, released -> 1
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Current mode: "RAM" or "CPU"
mode = "RAM"

# Remember last values so we can redraw when mode changes
last_cpu = 0
last_ram = 0

def clear_bar():
    """Turn all bar graph LEDs off."""
    for led in bar_leds:
        led.value(0)

def leds_for_percent(percent):
    """
    Map usage percentage to a number of LEDs (0–6).

    0%          -> 0 LEDs
    1–10%       -> 1 LED   (1 green)
    11–30%      -> 2 LEDs  (2 green)
    31–50%      -> 3 LEDs  (2 green + 1 yellow)
    51–70%      -> 4 LEDs  (2 green + 2 yellow)
    71–90%      -> 5 LEDs  (2 green + 2 yellow + 1 red)
    91–100%     -> 6 LEDs  (2 green + 2 yellow + 2 red)
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

def set_bar_from_percent(percent):
    """Update bar LEDs for given percentage."""
    # clamp
    if percent < 0:
        percent = 0
    if percent > 100:
        percent = 100

    clear_bar()
    count = leds_for_percent(percent)

    for i in range(count):
        bar_leds[i].value(1)

def update_mode_leds():
    """Turn on the LED for the current mode."""
    if mode == "CPU":
        cpu_led.value(1)
        ram_led.value(0)
    else:  # "RAM"
        cpu_led.value(0)
        ram_led.value(1)

def parse_line(line):
    """
    Parse a line like:
        'CPU:37,RAM:62'
    or possibly only one of them:
        'CPU:37'
        'RAM:62'
    Returns (cpu_value, ram_value) where each may be None if missing.
    """
    s = line.strip()
    if not s:
        return (None, None)

    cpu_val = None
    ram_val = None

    parts = s.split(",")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            label, num = part.split(":", 1)
        else:
            # If no label, ignore in this version
            continue

        label = label.strip().upper()
        try:
            v = int(num.strip())
        except:
            continue

        # clamp
        if v < 0:
            v = 0
        if v > 100:
            v = 100

        if label == "CPU":
            cpu_val = v
        elif label == "RAM":
            ram_val = v

    return (cpu_val, ram_val)

# --- INITIAL SETUP ---
clear_bar()
update_mode_leds()

# For simple debounce
prev_button_state = button.value()

while True:
    # --- Check button for mode toggle (polled each cycle) ---
    current_button_state = button.value()

    # Button wired to pull-up: pressed = 0, released = 1
    if prev_button_state == 1 and current_button_state == 0:
        # Falling edge: button press detected
        # Toggle mode
        if mode == "RAM":
            mode = "CPU"
        else:
            mode = "RAM"

        update_mode_leds()

        # Redraw bar graph using the new mode
        if mode == "CPU":
            set_bar_from_percent(last_cpu)
        else:
            set_bar_from_percent(last_ram)

    prev_button_state = current_button_state

    # --- Read one line from USB serial (blocking) ---
    line = sys.stdin.readline()
    if not line:
        continue

    cpu_val, ram_val = parse_line(line)

    # Update stored values if present
    if cpu_val is not None:
        last_cpu = cpu_val
    if ram_val is not None:
        last_ram = ram_val

    # Update bar graph based on current mode
    if mode == "CPU":
        set_bar_from_percent(last_cpu)
    else:
        set_bar_from_percent(last_ram)
