#!/bin/bash
echo "discover cpu arch"
echo adb shell getprop ro.product.cpu.abi
echo "updating frida"
pip install frida-tools --upgrade
echo "uploading frida"
adb push /data/local/tmp/frida-server
adb push cert.crt /data/local/tmp/cert.crt
echo "------- run the following -------"
echo adb shell 
echo su root
echo chmod 755 /data/local/tmp/frida-server
echo /data/local/tmp/frida-server
