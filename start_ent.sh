#!/bin/sh
nohup python ./entrance_button.py --host 'mqtt.tech-sketch.jp' --port 8883 --ssl --key_file './ssl/DST_Root_CA_X3.pem' --device_id button_sensor_0000000000000001 &
