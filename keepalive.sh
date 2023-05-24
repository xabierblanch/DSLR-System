#!/bin/bash
'''
This code is responsible for activating the relay connected to pin 23 of the Raspberry Pi.
The activation of this relay connects GPIO4 with GND in the WittyPi, allowing the automatic system shutdown to be disabled.
Thanks to this, the system remains powered on.
To activate it, execute "sh keepalive.sh" in the command line.
To shutdown the system, simply activate "sh shutdown.sh".
'''

gpio -g mode 23 out
gpio -g write 23 1
