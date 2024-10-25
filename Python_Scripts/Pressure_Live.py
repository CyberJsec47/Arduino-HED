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
import re
import numpy as np

broker = "localhost"
port = 1883
topic = "sensor/pressure"

max_points = 24  

angles = []
pressures = []

def on_message(client, userdata, msg):
    if dt.datetime.now().minute % 30 == 0:
        message = msg.payload.decode().strip()
        match = re.search(r"[-+]?\d*\.\d+|\d+", message)
        if match:
            pressure = float(match.group())
            print(pressure)
        
        hours = current_time.hour % 12
        minutes = current_time.minute
        angle = (hours * 2 + minutes // 30) * (np.pi / 6) 
        
        angles.append(angle)
        pressures.append(pressure)

        if len(angles) > max_points:
            angles.pop(0)
            pressures.pop(0)

client  = mqtt.Client()
client.on_message = on_message

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

client.on_connect = on_connect

def update_graph(frame):
    plt.cla()
    
    if angles and pressures:
        ax = plt.subplot(111, projection="polar")  
        ax.plot(angles, pressures, marker='o', label="Pressure")
        ax.fill(angles, pressures, alpha=0.3) 
        ax.set_theta_zero_location("N")  
        ax.set_theta_direction(-1) 
        ax.set_ylim(101200.0, 101300.0)

        half_hour_labels = [
            "12:00", "12:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", 
            "4:00", "4:30", "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", 
            "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30"
        ]
        
        ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
        ax.set_xticklabels(half_hour_labels)
        plt.title("12-Hour Pressure Polar Plot")
        plt.legend(loc="upper right")
        
plt.style.use('ggplot')
fig = plt.figure()

client.connect(broker, port, 60)
client.loop_start()

ani = FuncAnimation(fig, update_graph, interval=1000)
plt.show()

client.loop_stop()
