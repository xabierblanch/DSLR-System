#!/bin/bash

sleep 90

sudo sh /home/pi/Scripts/log_on.sh

sudo python3 /home/pi/Scripts/upload_log_on.py

sleep 2

sudo python3 /home/pi/Scripts/DSLR_UB_v2.py >> /home/pi/logs/log_Script.log

sudo sh /home/pi/Scripts/logs_RasPi.sh

sudo python3 /home/pi/Scripts/upload_logs.py

sleep 1

gpio -g mode 4 out
gpio -g write 4 0

