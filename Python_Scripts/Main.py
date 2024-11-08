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
import Wind

def display_all_graphs():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    Pressure.start_pressure_monitoring(axes[0, 0], broker="localhost", port=1883, topic="sensor/pressure", max_mins=5)
    Temperature.start_temperature_monitoring(axes[0, 1], broker="localhost", port=1883, topic="sensor/temperature", max_mins=5)
    Humidity.start_humidity_monitoring(axes[1, 0], broker="localhost", port=1883, topic="sensor/humidity", max_mins=5)
    axes[1, 1] = fig.add_subplot(2, 2, 4, projection='polar')
    Wind.start_wind_rose_plot(axes[1, 1], broker="localhost", port=1883, max_data_points=50)

    text_box = fig.text(0.5, 0.02, "", ha='center', va='bottom', fontsize=12, color="black")

    def update_all(frame):
        Pressure.update_pressure_barchart()
        Temperature.update_temperature_plot()
        Humidity.update_humidity_plot()
        Wind.update_wind_rose(frame)

        current_pressure = Pressure.current_reading(Pressure.live_reading)
        current_temperature = Temperature.current_reading(Temperature.live_reading)
        current_humidity = Humidity.current_reading(Humidity.live_reading)
        current_wind = Wind.current_reading(Wind.live_reading)

        text_box.set_text(
            f"Temperature is:   {current_temperature if current_temperature is not None else 'N/A'}\n"
            f"Humidity is:      {current_humidity if current_humidity is not None else 'N/A'}\n"
            f"Pressure is:      {current_pressure if current_pressure is not None else 'N/A'}\n"
            f"Wind speed is:    {current_wind if current_wind is not None else 'N/A'}"
        )

    fig.ani = FuncAnimation(fig, update_all, interval=1000)
    fig.tight_layout(pad=7.0)

    return fig
