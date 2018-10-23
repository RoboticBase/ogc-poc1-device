#!/usr/bin/env python3
import time
import datetime
import ssl
import paho.mqtt.client as mqtt
from neopixel import *
import argparse

parser = argparse.ArgumentParser(prog="dest_led.py", description="LED controller in destination", add_help = True)
parser.add_argument("--host", help="MQTT Address(Default:localhost)", default = 'localhost')
parser.add_argument("--port", type=int, help="MQTT Port(Default:1883)", default = 1883)
parser.add_argument("--ssl", help="Use SSL connection", action = 'store_true')
parser.add_argument("--key_file", help="Use SSL connection(Default:./ssl/DST_Root_CA_X3.pem)", default = './ssl/DST_Root_CA_X3.pem')
parser.add_argument("--device_id", help="(Default:dest_led_0000000000000001)", required = True)
args = parser.parse_args()
print("Connecting to " + args.host + ":" + str(args.port))
if args.ssl:
    print("SSL:" + args.key_file)


######################
### MQTT Parameter ###
######################
host=args.host
port=args.port
device_id=args.device_id

topic_sub='/dest_led/'+str(device_id)+'/cmd'
topic_pub='/dest_led/'+str(device_id)+'/cmdexe'
username='dest_led'
password='dest_led_0GC'
cacrt=args.key_file
client = mqtt.Client(protocol=mqtt.MQTTv311)
Connected = False
wait_sec=5

#####################
### LED Parameter ###
#####################
LED_COUNT      = 72      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

#####################
### LED Functions ###
#####################
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
def colorFlash(strip, color, wait_ms1=50, wait_ms2=50):
    for i in range(5):
        colorOn(strip, color, wait_ms1)
        colorOn(strip, Color(0,0,0), wait_ms1)
def colorOn(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000)
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(25):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

######################
### MQTT Functions ###
######################
def on_message(client, userdata, message):
    s = message.payload.decode('utf-8').split('|')
    print(s[-1])
    if s[-1] == 'on':
        print('light on!!')
        colorWipe(strip, Color(0, 0, 255), 10)
        time.sleep(0.5)
        client.publish(topic_pub, str(device_id)+'@action|success')
    elif s[-1] == 'off':
        print('light off!!')
        colorWipe(strip, Color(0,0,0), 10)
        time.sleep(0.5)
        client.publish(topic_pub, str(device_id)+'@action|success')
    else:
        print(s[-1])
        print('The message is none')


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected')
        global Connected
        Connected = True
    if rc == 1:
        print('Connection Failed')


def on_disconnect(client, userdata,rc=0):
    colorWipe(strip, Color(0,0,0), 10)
    client.loop_stop()

def setup():
    if args.ssl:
        client.username_pw_set(username, password=password)
        client.tls_set(cacrt, tls_version = ssl.PROTOCOL_TLSv1_1)
        client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_disconnect= on_disconnect
    client.on_message= on_message

def main():
    print('mosquitto_pub -t ' + topic_sub + '-m on or off')
    strip.begin()
    client.connect(host, port=port, keepalive=60)
    client.loop_start()
    while Connected != True:
        time.sleep(0.1)
    client.subscribe(topic_sub)
    while(True):
        time.sleep(1)

if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        client.disconnect()
