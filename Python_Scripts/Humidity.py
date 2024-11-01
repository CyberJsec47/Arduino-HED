#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Humidity.py
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
import datetime as dt
import re

x_data = []
y_data = []
ax = None

def start_humidity_monitoring(ax_in, broker="localhost", port=1883, topic="sensor/humidity", max_mins=5):
    global ax
    ax = ax_in
    client = mqtt.Client()

    def on_message(client, userdata, msg):
        global x_data, y_data
        message = msg.payload.decode().strip()
        match = re.search(r"[-+]?\d*\.\d+|\d+", message)
        if match:
            humidity = float(match.group())
            x_data.append(dt.datetime.now().strftime('%H:%M:%S'))
            y_data.append(humidity)
            if len(x_data) > max_mins:
                x_data.pop(0)
                y_data.pop(0)

    client.on_message = on_message

    def on_connect(client, userdata, flags, rc):
        client.subscribe(topic)

    client.on_connect = on_connect
    client.connect(broker, port, 60)
    client.loop_start()

def update_humidity_plot():
    if ax and x_data and y_data:
        ax.clear()
        ax.plot(x_data, y_data, marker='o', color='green', label="Humidity (%)")
        ax.set_xticks(x_data)
        ax.set_xticklabels(x_data, rotation=45)
 
