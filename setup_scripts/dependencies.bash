#!/bin/bash

#This script will install any necessary dependencies before 
#running initial-setup.bash

#required for swatchdog
#Swatchdog is useful for cloud, usb, and wifi attacks, but not required

#apt install -y libdate-manip-perl 
#apt install -y python-setuptools
#apt install -y libdate-calc-perl
#apt install -y libfile-tail-perl

#required for pymetasploit
apt install -y python-setuptools

apt install -y metasploit-framework

#Packages for Wi-Fi attacks

#apt install -y hostapd
#apt install -y dnsmasq

#get adb using this package, or use the adb from platform-tools android-sdk, make sure to include the binary
#location in your path

#apt install -y adb

#Packages for odroid 16x2 lcd screen
#required for wiringpi2-python
#apt install -y python-dev
#apt install -y swig3.0
