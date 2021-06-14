#!/bin/bash

echo >> /home/pi/logs/log_RasPi.log
echo "************** XBG HRCam PUIGCERCOS logs **************" >> /home/pi/logs/log_RasPi.log
echo "$(date) @ $(hostname)" >> /home/pi/logs/log_RasPi.log
echo >> /home/pi/logs/log_RasPi.log
echo "Memoria total disponible" >> /home/pi/logs/log_RasPi.log
echo "$(df -P --total -Bg -h)" >> /home/pi/logs/log_RasPi.log
echo >> /home/pi/logs/log_RasPi.log
sudo iwconfig wlan0 >> /home/pi/logs/log_RasPi.log
cp /home/pi/wittypi/schedule.log /home/pi/wittypi/wittyPi.log /home/pi/logs
