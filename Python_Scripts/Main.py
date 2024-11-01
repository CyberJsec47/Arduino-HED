#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Main.py
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
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Pressure
import Temperature
import Humidity
import DirSpeed

def display_all_graphs():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    Pressure.start_pressure_plotting(axes[0, 0], broker="localhost", port=1883, topic_in="sensor/pressure", max_points=24)
    Temperature.start_temperature_monitoring(axes[0, 1], broker="localhost", port=1883, topic="sensor/temperature", max_mins=5)
    Humidity.start_humidity_monitoring(axes[1, 0], broker="localhost", port=1883, topic="sensor/humidity", max_mins=5)

    fig.delaxes(axes[1, 1]) 
    axes[1, 1] = fig.add_subplot(2, 2, 4, projection='polar') 

    DirSpeed.start_wind_rose_plot(axes[1, 1], broker="localhost", port=1883, max_data_points=50)

    def update_pressure(frame):
        Pressure.update_pressure_plot()

    def update_temperature(frame):
        Temperature.update_temperature_plot()

    def update_humidity(frame):
        Humidity.update_humidity_plot()

    def update_dirspeed(frame):
        DirSpeed.update_wind_rose_plot()

    anim_pressure = FuncAnimation(fig, update_pressure, interval=1000)
    anim_temperature = FuncAnimation(fig, update_temperature, interval=1000)
    anim_humidity = FuncAnimation(fig, update_humidity, interval=1000)
    anim_dirspeed = FuncAnimation(fig, update_dirspeed, interval=1000)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    display_all_graphs()
