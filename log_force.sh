#!/bin/bash

mkdir /home/pi/log_force

echo "Desconexió forçada" >> /home/pi/log_force/log_force.log
echo "$(date) @ $(hostname)" >> /home/pi/log_force/log_force.log
echo >> /home/pi/log_force/log_force.log
