#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  LiveTempTest.py
#  
#  Copyright 2024  <josh@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt

# MQTT Settings
broker = "localhost"
port = 1883
topic = "sensor/temperature"

# only have 100 (mins) of data in the graph
max_mins = 100


# Data for graph
x_data = []
y_data = []

def on_message(client, userdata, msg):
    message = msg.payload.decode().strip()
    print(f"Message received: '{message}'")
    
    x_data.append(dt.datetime.now().strftime('%H:%M:%S'))
    y_data.append(message)
    
    if len(x_data) > max_mins:
        x_data.pop(0)
        y_data.pop(0)
        
        
# Set up MQTT client
client  = mqtt.Client()
client.on_message = on_message

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)
    
    
client.on_connect = on_connect

def update_graph(frame):
    plt.cla()
    plt.plot(x_data, y_data, label="Temperature")
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Temperature C")
    plt.title("Live Temperature Test")
    plt.legend(loc="upper left")
    plt.tight_layout
    
    
plt.style.use('fivethirtyeight')
fig = plt.figure()

client.connect(broker, port, 60)
client.loop_start()

ani = FuncAnimation(fig, update_graph, interval=1000)

plt.show()

client.loop_stop()
