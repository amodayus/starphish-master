#!/bin/bash

#Enable port forwarding for WiFi attacks
#echo "1" > /proc/sys/net/ipv4/ip_forward

#start msfrpcd
#Socat is used to redirect postgresql on 5433 to 5432
sudo socat tcp-l:5432,fork,reuseaddr tcp:127.0.0.1:5433 &
#Did not have to use sudo to start msfrpcd 
#You can use the ds-control script directly on the Amazon EC2
#Or port forward port 55553
sudo msfrpcd -f -a 127.0.0.1 -P <passwordvalue> &
# Example: msfrpcd -f -a 127.0.0.1 -P thematrixhasyouneo &

#start swatchdog
#swatchdog --config-file configure/swatch-usb --tail-file /var/log/messages >> /var/log/starphish-swatch-usb.log 2>&1 &
