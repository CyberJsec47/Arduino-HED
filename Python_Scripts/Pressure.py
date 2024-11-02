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

def start_pressure_monitoring(ax_in, broker="localhost", port=1883, topic="sensor/pressure", max_mins=5):
    global ax
    ax = ax_in 
    client = mqtt.Client()

    def on_message(client, userdata, msg):
        global x_data, y_data, live_reading
        message = msg.payload.decode().strip()
        match = re.search(r"[-+]?\d*\.\d+|\d+", message)
        if match:
            pressure = float(match.group())
            x_data.append(dt.datetime.now().strftime('%H:%M:%S'))
            y_data.append(pressure)
            live_reading.append(message)
            if len(y_data) > max_mins:
                x_data.pop(0)
                y_data.pop(0)
 
            update_pressure_barchart()

    client.on_message = on_message

    def on_connect(client, userdata, flags, rc):
        client.subscribe(topic)

    client.on_connect = on_connect
    client.connect(broker, port, 60)
    client.loop_start()

def update_pressure_barchart():
    if ax is not None:
        ax.clear()
        
        ax.bar(x_data, y_data, color='blue', edgecolor='black', alpha=0.7)
        
        ax.set_xticks(range(len(x_data)))
        ax.set_xticklabels(x_data, rotation=45, ha="right")
        ax.set_ylim([102000.00, 104000.00])
        ax.set_xlabel("Time")
        ax.set_ylabel("Pressure (Pa)")
        ax.set_title("Atmospheric Pressure")
        ax.legend(["Pressure (Pa)"], loc="upper left")
        ax.grid(True)

        plt.draw()
