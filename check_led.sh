#!/bin/sh
nohup python ./dest_led.py --device_id dest_led_0000000000000001 &
watch -n 2 mosquitto_pub 
