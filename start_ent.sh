#!/bin/sh
nohup /usr/bin/python3 /home/pi/ogc-poc1-device/entrance_button.py --host 'mqtt.tech-sketch.jp' --port 8883 --ssl --key_file '/home/pi/ogc-poc1-device/ssl/DST_Root_CA_X3.pem' --device_id button_sensor_000000000000000X &
