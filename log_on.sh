#!/bin/bash

mkdir /home/pi/log_on

echo "$(date) @ $(hostname)" >> /home/pi/log_on/log_on.log
echo >> /home/pi/log_on/log_on.log
