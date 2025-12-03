SysLight - Visual RAM/CPU Usage Monitor

This project uses an ESP32 microcontroller and six LEDs to show a computer's system performance in real time. A Python script running on a Windows PC reads the system's RAM usage once per second and sends the percentage value to the ESP32 over a USB serial connection.

The ESP32 receives the percentage and lights the LEDs based on the usage level:

- Green LEDs indicate low usage
- Yellow LEDs indicate medium usage
- Red LEDs indicate high usage

A button added to the circuit along with a Blue and White LED allow for 
switching between CPU and RAM usage.

Blue for CPU and White for RAM.


Required Components:
- 2 Green LEDs
- 2 Yellow LEDs
- 2 Red LEDs
- 1 Blue and white (color doesn't really matter) LED
- 1 Button
- 8 220 Ohm resistors
- 1 breadboard
- Various Jumper Cables
- ESP32 Microcontroller flashed with MicroPython

Setup:
Place each Green, Yellow, and Red LED into the board on different rails of the breadboard. Connect the anode (long leg) to a leg of a 220 Ohm resistor and connect the other leg of the resistor to a GPIO pin of the ESP32 using a jumper cable. Connect the cathode (short leg) of the LEDs to the ground rail of the breadboard and connect the ground rail to the ground of the ESP32 using another jumper cable. Make sure to keep note of which pins you are connecting the LEDs to, as that is imporant to change in the code.
Connect one half of the button to another GPIO pin on the ESP32 and the other half to the ground rail.

In my setup, going from green to red, I used pin 2, 4, 5, 18, 19, 23. For the CPU LED, pin 25. RAM LED, 26. And button, pin 27. As some of the pins can have other uses that disrupt the circuit, I found these to be the most consistant. In the main.py code, make sure your pin values match to the ones used on your board. 

Connect to the board using a USB-C cable, making sure you are connected to the right COM port.

Save main.py to the ESP32 and save Syslight.py to a location you know. Make sure any program using the COM port is closed. Open command prompt, change directories till you get to the one with Syslight.py and run the program (python syslight.py). If done correctly, you should see side by side values of CPU and RAM usage. 

(NOTE: It is possible that you will need to change the scaling value of the CPU usage in Syslight.py if it deson't match what you see in task manager. I believe psutil is looking at individual CPU core usage rather than overall usage. So some tweaking may be required. During my testing, I found a scale of 7 to be fairly accurate for my machine.)
