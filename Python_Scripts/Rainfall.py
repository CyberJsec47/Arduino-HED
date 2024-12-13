#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rainfall.py
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

# This file is same as others and displays rainfall levels but due to matlabs graph layout I couldnt add in a third row or colum to display
# the graph without messing up format, as of now I am just using it to update the live text box, maybe in future I will pllace the live
# graph in the GUI, or add another sensor to make a 3, 3 plot.

import paho.mqtt.client as mqtt
import datetime as dt
import matplotlib.pyplot as plt
import re

x_data = []
y_data = []
ax = None
live_reading = []

def current_reading(live_reading):
    if live_reading:
        current_value = live_reading[0]
        if len(live_reading) > 1:
            live_reading.pop(0)
        return current_value
    return None

def add_reading(value):
    live_reading.append(value)

def start_rainfall_monitoring(broker="localhost", port=1883, topic="sensor/rainfall", max_mins=5):
    global ax
    client = mqtt.Client()

    def on_message(client, userdata, msg):
        global x_data, y_data
        message = msg.payload.decode().strip()
        match = re.search(r"[-+]?\d*\.\d+|\d+", message)
        if match:
            rain = float(match.group())
            x_data.append(dt.datetime.now().strftime('%H:%M:%S'))
            y_data.append(rain)
            live_reading.append(message)
            if len(x_data) > max_mins:
                x_data.pop(0)
                y_data.pop(0)

    client.on_message = on_message

    def on_connect(client, userdata, flags, rc):
        client.subscribe(topic)

    client.on_connect = on_connect
    client.connect(broker, port, 60)
    client.loop_start()

def update_rain_plot():
    if ax and x_data and y_data:
        ax.clear()
        ax.stem(x_data, y_data, linefmt='blue', markerfmt='D', label="Rainfall")
        ax.set_xticks(x_data)
        ax.set_xticklabels(x_data, rotation=45)
        ax.set_xlabel("Time")
        ax.set_ylabel("Rainfall (mm)")
        ax.set_title("Rainfall levels")
        ax.set_ylim([15.0, 35.0])
        ax.fill_between(x_data, y_data, 15.0, step="pre", alpha=0.5, color='lightsteelblue')
