#!/usr/bin/env python3
import time
import ssl
import paho.mqtt.client as mqtt
import neopixel
import argparse

parser = argparse.ArgumentParser(description="LED controller")
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
parser.add_argument("--username",
                    help="MQTT Username",
                    default='')
parser.add_argument("--password",
                    help="MQTT Password",
                    default='')
parser.add_argument("--key_file",
                    help="Select the SSL keyfile")
parser.add_argument("--device_type",
                    help="Device Type",
                    required=True)
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
device_type = args.device_type
device_id = args.device_id
topic_sub = '/{}/{}/cmd'.format(device_type, device_id)
topic_pub = '/{}/{}/cmdexe'.format(device_type, device_id)
username = args.username
password = args.password
cacrt = args.key_file
client = mqtt.Client(protocol=mqtt.MQTTv311)
Connected = False
wait_sec = 5

#####################
#   LED Parameter   #
#####################
LED_COUNT = 72
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
strip = neopixel.Adafruit_NeoPixel(LED_COUNT,
                                   LED_PIN,
                                   LED_FREQ_HZ,
                                   LED_DMA,
                                   LED_INVERT,
                                   LED_BRIGHTNESS,
                                   LED_CHANNEL)

#####################
#   LED Functions   #
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
        colorOn(strip, neopixel.Color(0, 0, 0), wait_ms1)


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
        return neopixel.Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return neopixel.Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return neopixel.Color(0, pos * 3, 255 - pos * 3)


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
            color = wheel((int(i * 256 / strip.numPixels()) + j) & 255)
            strip.setPixelColor(i, color)
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
#   MQTT Functions   #
######################
def on_message(client, userdata, message):
    s = message.payload.decode('utf-8').split('|')
    print(s[-1])
    if s[-1] == 'on':
        print('light on!!')
        colorWipe(strip, neopixel.Color(0, 0, 255), 10)
        time.sleep(0.5)
        client.publish(topic_pub, str(device_id)+'@action|success')
    elif s[-1] == 'off':
        print('light off!!')
        colorWipe(strip, neopixel.Color(0, 0, 0), 10)
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


def on_disconnect(client, userdata, rc=0):
    colorWipe(strip, neopixel.Color(0, 0, 0), 10)
    client.loop_stop()


def setup():
    client.username_pw_set(username, password=password)
    if args.ssl:
        client.tls_set(cacrt, tls_version=ssl.PROTOCOL_TLSv1_1)
        client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message


def main():
    print('mosquitto_pub -t ' + topic_sub + '-m on or off')
    strip.begin()
    client.connect(host, port=port, keepalive=60)
    client.loop_start()
    while not Connected:
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
