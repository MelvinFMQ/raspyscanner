#!/bin/sh
#launcher.sh
#navigate to home directory, then to this directory, then execute python scirpt, then back home

cd /
cd home/pi/piserver
sudo python raspserver.py
cd / 
