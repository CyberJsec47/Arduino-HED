#!/bin/bash


TOPICS=(
       "sensor/temperature"
       "sensor/humidity"
       "sensor/pressure"
       "sensor/altitude"
       "sensor/wind_dir"
       "sensor/wind_speed"
       "sensor/rainfall"
)

for topic in "$TOPICS[@]"; do
        mosquitto_sub -h localhost -t "$topic" -v & done

while true; do
      sleep 1 
done