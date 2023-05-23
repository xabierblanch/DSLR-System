#!/bin/bash

# Sleep for 25 seconds (wait for WiFi connection)
sleep 25

#create logs folder
mkdir -p /home/pi/logs

#run main script
python3 /home/pi/scripts/main.py >> /home/pi/logs/script.log

#move and upload logs
python3 /home/pi/scripts/logs.py

#shutdown RPi (WittyPi function)
gpio -g mode 4 out
gpio -g write 4 0
