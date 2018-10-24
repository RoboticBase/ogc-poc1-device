#!/bin/sh
nohup /usr/bin/python3 /home/pi/ogc-poc1-device/dest_button.py --host 'mqtt.tech-sketch.jp' --port 8883 --ssl --key_file '/home/pi/ogc-poc1-device/ssl/DST_Root_CA_X3.pem' --device_id dest_human_sensor_000000000000000X &
nohup sudo /usr/bin/python3 /home/pi/ogc-poc1-device/dest_led.py --host 'mqtt.tech-sketch.jp' --port 8883 --ssl --key_file '/home/pi/ogc-poc1-device/ssl/DST_Root_CA_X3.pem' --device_id dest_led_000000000000000X &
