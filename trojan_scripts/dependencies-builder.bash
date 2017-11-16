#!/bin/bash

sudo apt install maven rename openjdk-8-jdk zipalign

sudo dpkg --add-architecture i386
sudo apt update
sudo apt install libncurses5:i386 libstdc++6:i386 zlib1g:i386

#Generate a keystore with this example command:

#keytool -genkey -v -keystore example.keystore -alias example-alias -keyalg RSA -keysize 2048 -validity 10000

#Do not forget to zipalign your trojanized APK's
