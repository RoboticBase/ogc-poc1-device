#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import freezegun
import datetime


from mock import patch, MagicMock

from parameterized import parameterized, param

LED_PIN = 26
BTN_PIN = 5
HOST = 'test_host'
PORT = 1883
DEVICE_TYPE = 'robot'
DEVICE_ID = 'robot01'

LED_COUNT = 72
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

MockNeopixel = MagicMock()
MockTime = MagicMock()
MockArgparse = MagicMock()
MockArgumentParser = MagicMock()
MockArg = MagicMock()
MockArg.host = HOST
MockArg.port = PORT
MockArg.device_type = DEVICE_TYPE
MockArg.device_id = DEVICE_ID

MockArgparse.ArgumentParser.return_value = MockArgumentParser
MockArgumentParser.parse_args.return_value = MockArg

modules = {
    "neopixel": MockNeopixel,
    "time": MockTime,
    "argparse": MockArgparse,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from src import dest_led


@patch('src.dest_led.client')
class TestDestLed(unittest.TestCase):

    def test_setup(self, mocked_client):
        dest_led.setup()
        self.assertEqual(mocked_client.on_connect, dest_led.on_connect)
        self.assertEqual(mocked_client.on_disconnect, dest_led.on_disconnect)
        self.assertEqual(mocked_client.on_message, dest_led.on_message)
       
    @parameterized.expand([(1, False), (0, True)])
    def test_on_connect(self, mocked_client, rc, is_connected):
        dest_led.on_connect(mocked_client, None, 0, rc)
        self.assertEqual(dest_led.Connected, is_connected)

    @parameterized.expand([(b'xxxx|xxxx|on', 255), (b'xxxx|xxxx|off', 0)])
    def test_on_message(self, mocked_client, payload, color):
        mocked_message = MagicMock()
        mocked_message.payload = payload

        dest_led.on_message(mocked_client, None, mocked_message)
        MockNeopixel.Color.assert_any_call(0, 0, color)
        MockNeopixel.Color.assert_any_call(0, 0, 0)
        MockTime.sleep.assert_any_call(0.5)
        MockTime.sleep.assert_any_call(0.01)
        topic_pub = '/{}/{}/cmdexe'.format(DEVICE_TYPE, DEVICE_ID)
        pub_message = '{}@action|success'.format(DEVICE_ID)
        mocked_client.publish.assert_called_once_with(topic_pub, pub_message)

    def test_on_disconnect(self, mocked_client):
        dest_led.on_disconnect(mocked_client, None)
        mocked_client.loop_stop.assert_called_once()

