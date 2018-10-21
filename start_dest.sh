#!/bin/sh
nohup python ./dest_button.py --host 'mqtt.tech-sketch.jp' --port 8883 --ssl --key_file './ssl/DST_Root_CA_X3.pem' --device_id dest_human_sensor_0000000000000001 &
nohup python ./dest_led.py --host 'mqtt.tech-sketch.jp' --port 8883 --ssl --key_file './ssl/DST_Root_CA_X3.pem' --device_id dest_led_0000000000000001 &
