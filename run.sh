#!/bin/bash

sleep 25

sh /home/pi/Scripts/log_on.sh

python3 /home/pi/Scripts/upload_log_on.py

sh /home/pi/Scripts/logs_RasPi.sh

python3 /home/pi/Scripts/upload_logs.py

sudo python3 /home/pi/Scripts/HRCam_UB_v4.py >> /home/pi/logs/log_Script.log

python3 /home/pi/Scripts/upload_log_on.py

sh /home/pi/Scripts/logs_RasPi.sh

python3 /home/pi/Scripts/upload_logs.py

gpio -g mode 4 out
gpio -g write 4 0
