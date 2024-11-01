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
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np
import re
import datetime as dt

pressures = []
times = []
ax = None 
topic = None  
max_mins = 5

def start_pressure_plotting(ax_in, broker="localhost", port=1883, topic_in="sensor/pressure", max_points=24):
    global ax, topic
    ax = ax_in  
    topic = topic_in 

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker, port, 60)
    client.loop_start()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic) 

def on_message(client, userdata, msg):
    current_time = dt.datetime.now()
    message = msg.payload.decode().strip()
    match = re.search(r"[-+]?\d*\.\d+|\d+", message)
    
    if match:
        pressure = float(match.group())
        print(f"Received pressure: {pressure}")

        times.append(current_time.strftime('%H:%M:%S'))
        pressures.append(pressure)
        
        if len(times) > max_mins:
            times.pop(0)
            pressures.pop(0)

        update_pressure_plot() 

def update_pressure_plot():
    if ax is not None:
        ax.clear()
        ax.plot(times, pressures, marker='o', label="Pressure", color='blue')
        
        ax.set_xlabel("Time")
        ax.set_ylabel("Pressure (Pa)")
        ax.set_title("Pressure Over Time")
        ax.legend(loc="upper left")
        ax.set_ylim(101000.0, 103000.0)
        ax.grid(True)

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.draw()
