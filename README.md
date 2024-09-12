## Arduino Home climate display

---

### The goal of this project is to create an indoor and outdoor climate monitor.
#### The monitor will be build using Arduino and various sensors to display the following:

- **Temperature**
- **Humidity** 
- **Pressure** 
- **Wind Speed**
- **Direction**
- **Rainfall**


#### This readings will be sent real time via a wireless protocol to a Raspberry Pi which will then give a live display of the readings in a GUI

---

### Progress

The project at its starting point consists of an Arduino UNO and a DHT11 sensor and can display the temperature in C (or F) and the humidity in %.<br>
It displays the readings on a 16x2 LCD screen in the format:<br><br>Temp: 20.0 C<br>Humidity 60.00%<br>


It also uses a HC-SR04 ultrasonic turn the LCD on and off depending on if somebody is present to see it. This is to safe on battery life.


--- 

### Current Equipment 

- **Arduino UNO**
- **HC-SR04 Ultrasonic Sensor**
- **DHT11 Temperature and Humidity Sensor**
- **I2C 16x2 Arduino LCD** 
---

### Future Equipment

- **Raspberry Pi Model 4B**
- **BME688**<br>This is to replace the DHT11 and handle the Temperature, Humidity, and pressure parts of the project
- **SparkFun Arduino IoT Weather Station**<br> This includes the wind and rain hardware also a ESP22 board for wireless communication 
- **4.26" E-Paper Display HAT (800x480)**
---

### Communication

The data from the outdoor weather station will need to be sent to the Pi inside over a short distance, the ideal protocols for this are Zigbee, MQTT, Bluetooth, Wi-Fi and LoRa. <br> if using an ESP22 board I can set up the Pi as MQTT broker and the ESP as a client. Another way I could do is set the Pi up as a router and create a private network over Wi-Fi.

---

### Display

The RasPi will process the data from outside and also inside from a second Arduino taking indoor data. The choice to use an E-Paper display is to reduce power consumption and improve battery life. This display will be made to very simple and have a section for inside consisting of Temperature and Humidity then a second for outside consisting of Temperature, Humidity, Pressure, Wind Speed, Wind Direction and Rainfall level
