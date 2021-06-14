#!/bin/bash

sleep 600

sudo sh /home/pi/Scripts/log_force.sh

sudo python3 /home/pi/Scripts/upload_log_force.py

gpio -g mode 4 out
gpio -g write 4 0

