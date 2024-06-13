#!/bin/bash

echo "Initiated the plug & play mode installation..."
apt update
pip install picamera
apt install nginx

mv startup.services /etc/systemd/system/
sytemctl enable startup.services
systemctl start startup.services

sleep 1

echo "done"

