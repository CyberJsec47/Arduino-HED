#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DirSpeed.py
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
import numpy as np
import re

wind_directions = []
wind_speeds = []
ax = None

def start_wind_rose_plot(ax_in, broker="localhost", port=1883, max_data_points=50):
    global ax
    ax = ax_in  # Assign the provided polar plot Axes to ax

    client = mqtt.Client()

    def on_message(client, userdata, msg):
        global wind_directions, wind_speeds
        message = msg.payload.decode().strip()
        match = re.search(r"[-+]?\d*\.\d+|\d+", message)
        if match:
            value = float(match.group())
            if msg.topic == "sensor/direction":
                wind_directions.append(value)
            elif msg.topic == "sensor/speed":
                wind_speeds.append(value)

            wind_directions = wind_directions[-max_data_points:]
            wind_speeds = wind_speeds[-max_data_points:]

    client.on_message = on_message

    def on_connect(client, userdata, flags, rc):
        client.subscribe("sensor/direction")
        client.subscribe("sensor/speed")

    client.on_connect = on_connect
    client.connect(broker, port, 60)
    client.loop_start()

def update_wind_rose_plot():
    if ax and wind_directions and wind_speeds:
        ax.clear()
        num_bins = 8
        direction_bins = np.linspace(0, 360, num_bins + 1)
        hist, _ = np.histogram(wind_directions, bins=direction_bins, weights=wind_speeds)
        angles = np.radians((direction_bins[:-1] + direction_bins[1:]) / 2)
        bar_width = 2 * np.pi / num_bins
        ax.set_theta_offset(np.pi / 2) 
        ax.set_theta_direction(-1)     
        ax.bar(angles, hist, width=bar_width, color="skyblue", alpha=0.8, edgecolor="black")
        ax.set_ylim(0, max(hist) if np.any(hist) else 1)
