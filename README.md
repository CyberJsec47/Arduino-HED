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


These readings will be sent real time wirelessly to a Raspberry Pi which will then give a live display of the readings in a GUI interface. 

---

### Progress

Currently I the SparkFun MicroMod board is set up with the ESP32 prossesor attached and is taking various readings at 10 second intervals and dispaying on a serial printout in the Arduino IDE. <br>Currently I have set up all sensors on the station to take readings.<br><br><img src="Images/Data_On_Serial.jpg" width="400" height="400"><br> They all are published to an MQTT broker and the Pi is able to subscribe to the topics to display the data.<br>Using a Bash script I can test all the data comes through<br><br><img src="Images/RasPi_Bash_Display.jpg"><br>
I started to work on the Python part of this project which is how I am displaying the data.<br> I had one script which took the MQTT message and printing to terminal similar to the Bash script, next I started to work on collecting a live updating feed. 

For this I made a script which collected temperature data and created a animated Matplot chart which updates every 10 seconds showing the temperature over the timeframe of about 16 minutes until it starts to rewrite.<br>Today's progress I made a graph for each of the readings and used Matplotlib Sub plot function to bring them all together in one display<br><br><img src="Images/live_graph.jpg"> 


One issue that has come up is powering the device. Using a 2000mAh LiPoly battery it lasts around a day until its drained and paired with a 6W solar panel this proves unable to charge the battery quicker than the board drains it.<br> For this I am going to try add in the ESP light sleep mode and change the message intervals to every hour or 30 mins with the board in a sleep mode inbetween with the hope this gives the battery enough time to charge to re transmit messages.<br>

--- 

### Current Equipment 

- **Arduino UNO**
- **Arduino Nano ESP32**
- **Raspberry Pi 5**
- **SparkFun IoT Weather Kit**
- **DHT11 Temperature and Humidity Sensor**<br>
<br><img src="Images/Station.jpg"><br>
---

### Communication

The data from the outdoor weather station will need to be sent to the Pi inside over a short distance.<br> The [SparkFun](https://thepihut.com/products/sparkfun-arduino-iot-weather-station) Comes with an ESP32 board so I can use its WiFi capabilities to send the data with the MQTT protocol by setting the the board as publisher and the RaspPi and a subscriber.<br> To do this I am using the Mosquitto MQTT broker on the Pi. 

---
### Display


Using Tkinter I have created a executable desktop icon that runs the Tkinter GUI module which is connected to the Matplot graphs creating one intergrated display.<br> To do this I created a desktop entry in a bash script which points to another bash script where which opens the GUI.py module in my WeatherStation directory. This might be an overly complicated way to open from an icon but it works for what I need.

---
### Finished main project

At its current stage I am saying this project is finished. The main goals of creating an IoT weather station to display the temperature, humidity, wind speed and direction is complete alongside a live text display and charts for some weather trends and patterns.<br>


### **Issues**
- **Power**
When I finished the project and was happy with the Python and C++ side of it I started to look into external power. I've settled with a 2000mAh Lipoly battery and a 6W solar panel with a Adafruit bq24074 charging board. This powered the board via the battery and the solar panel keeps the battery topped up.<br> The first issues was the solar panel is not the greatest and with cloudy and dark weather it can't charge the battery as fast as the battery drains to power the board.<br> This I found was the ESP was sending the messages every 10 seconds using a lot of power, I changed this to every 60 seconds the power issues carried on.<br>
- **Resolve**
To fix this I looked into ESP low power mode functions. As using modem mode or sleep mode caused connection issues or still battery draining issues I opted to use light power mode on a rolling cycle of sleeping for a set time, waking up for a set time and back to sleep.<br><br>
- **Power connection**
Looking into external power for this board SparkFun dont have a well documented way it can be easily done. The main power for this board is a USB-C port which can be plugged into a 5V plug as it has a built in 5v to 3.3v regultor. But once this is outside in a weather proof box it wont be practical to run a cable from the box into the house or other means of power unless I install an external power socket outside which is just not needed.<br>Another issues with this board is it only has pin holes for external wires, when searched they advertise it as coming with a 2 pin JST connection so I bought a JST wire to go from the charging board to the carrier board which was a wrong fit.
- **Resolve**
To fix this physical power issue I stripped the JST pins and soldered the wires directly into the 3.3v pin and gnd on the board. The 2000mAh Lipoly battery runs as 3.7v so this is find to directly attach and this has solved the power issues.<br><br>

- **Watchdog timers**
There was issues with connection to wifi not being established which ended in a constant loop of attempting connection, to solve this I looked into setting up a WDT to catch the failed attempt and restart the code. This started to become complicated and the WDT event was being triggered but not restarting the code. I found the WDT was being trigged in a set up loop so as it reset the code it would catch this loop and crash out.<br>
- **Resovle**
As the board isn't saving any data itself I have no issue with a reset as it would react to the physical button being pressed so in times where the wifi connection cant be establised within a 60 second timeout the ESP uses a reset function on the  whole board and starts the process all over again.
  

---
### **Next steps**



