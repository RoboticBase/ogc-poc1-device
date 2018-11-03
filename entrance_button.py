#!/usr/bin/env python3
import time
import datetime
import ssl
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import argparse

parser = argparse.ArgumentParser(description="Button controller in entrance")
parser.add_argument("--host",
                    help="MQTT Address(Default:localhost)",
                    default='localhost')
parser.add_argument("--port",
                    type=int,
                    help="MQTT Port(Default:1883)",
                    default=1883)
parser.add_argument("--ssl",
                    help="Use SSL connection",
                    action='store_true')
parser.add_argument("--key_file",
                    help="Select the SSL keyfile")
parser.add_argument("--device_id",
                    help="Device ID",
                    required=True)
args = parser.parse_args()
print("Connecting to " + args.host + ":" + str(args.port))
if args.ssl:
    print("SSL:" + args.key_file)

######################
#   MQTT Parameter   #
######################
host = args.host
port = args.port
device_id = args.device_id
topic = '/button_sensor/'+str(device_id)+'/attrs'
username = 'button_sensor'
password = 'button_sensor_0GC'
cacrt = args.key_file
client = mqtt.Client(protocol=mqtt.MQTTv311)
Connected = False

########################
#   Sensor Parameter   #
########################
LED_PIN = 26
BTN_PIN = 5
Pushed = False

######################
#   MQTT Functions   #
######################


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected')
        global Connected
        Connected = True
    elif rc == 1:
        print('Connection Failed')


def on_disconnect(client, userdata, rc=0):
    global Connected
    Connected = False
    print('network is disconnect')
    client.loop_stop()


def sensor():
    if GPIO.input(BTN_PIN) == GPIO.HIGH:
        tzinfo = datetime.timezone(datetime.timedelta(hours=9))
        date = datetime.datetime.now().replace(tzinfo=tzinfo).isoformat()
        payload = date+'|state|on'
        client.publish(topic, payload)
        print("pushed")
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BTN_PIN, GPIO.IN)
    if args.ssl:
        client.username_pw_set(username, password=password)
        client.tls_set(cacrt, tls_version=ssl.PROTOCOL_TLSv1_1)
        client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect


def main():
    global Connected
    print('mosquitto_sub -t ' + topic)
    client.connect(host, port=port, keepalive=60)
    client.loop_start()
    while not Connected:
        time.sleep(1)
    while True:
        sensor()


if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        client.disconnect()
        GPIO.cleanup()
