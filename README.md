SysLight - Visual RAM/CPU Usage Monitor

This project uses an ESP32 microcontroller and six LEDs to show a computer's system performance in real time. A Python script running on a Windows PC reads the system's RAM usage once per second and sends the percentage value to the ESP32 over a USB serial connection.

The ESP32 receives the percentage and lights the LEDs based on the usage level:

- Green LEDs indicate low usage
- Yellow LEDs indicate medium usage
- Red LEDs indicate high usage

A button added to the circuit along with a Blue and White LED allow for 
switching between CPU and RAM usage.

Blue for CPU and White for RAM.
