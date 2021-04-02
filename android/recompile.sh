#!/bin/bash
# to create keystore: keytool -keystore clientkeystore -genkey -alias client

echo "usage: ./recompile.sh <modified.apk>"
echo "uninstall preivous app firs!!!"

echo run this first: apktool b gaiainvaders/ -o modified-1.apk
echo " password is 111111"
jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore clientkeystore $1 mykey
echo "isntalling"
echo "press enter to install after you've unisntalled from emulator"
read
adb install $1

