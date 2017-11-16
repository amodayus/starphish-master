#!/bin/bash

#Running this script installs pymetasploit with a couple fixes of our own and made by community in other 
#github repos
#Downloads signing scripts, swatchdog, python adb, blacklists
#a module from loading that could insert junk characters into
#our lcd screen, and installs WiringPi2-Python

#By default the uncommented lines should get you up and running a basic C2

#You want this
git clone https://github.com/allfro/pymetasploit.git pymsf

#add in our own msfrpc.py with disable payload handler and functionality fix

cp msfrpc.py pymsf/src/metasploit/msfrpc.py

cd pymsf/ && python setup.py install

cd ../

#Use swatchdog to run an automation script, could be an automated version of C2
#to take an action when a certain regex in a log file has been matched
#git clone https://github.com/ToddAtkins/swatchdog.git swdog

#cd swdog/ && perl Makefile.PL && make && make test && make install && make realclean

#cd ../

#Python adb, another adb option useful for automating things in python, not necessary
#git clone https://github.com/ardevd/pyand.git pyand

#cd pyand/ && python setup.py build && python setup.py install

#cd ../

#LCD Character display package setup, do this on an ODROID-C2
#git clone https://github.com/hardkernel/WiringPi2-Python.git

#cd WiringPi2-Python && git submodule init && git submodule update && ./build.sh

#cd ../

#Good repo, used for converting python3 ipaddress module to python2
#git clone https://github.com/phihag/ipaddress.git

#cd ipaddress && python setup.py install

#cd ../

#Good repo, used mainly to sign apps with debug certificates
#cd ../ && git clone https://github.com/appium/sign.git 

#In the future we may add interfaces files to create a Wireless AP
#cp configure/interfaces /etc/network/interfaces

#Remove junk characters for ODROID, only do this if you are using an ODROID-C2
#echo "blacklist w1_gpio" > /etc/modprobe.d/w1_gpio.conf 
