#!/bin/bash
adb shell "su -c 'mkdir /data/local/tmp/$1 2>/dev/null; cp -rf /data/data/$1/* /data/local/tmp/$1/ && chmod -R 777 /data/local/tmp/$1'" && adb pull /data/local/tmp/$1 && adb shell "su -c 'rm -rf /data/local/tmp/$1'"
