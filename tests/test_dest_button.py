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
PUSHED_PAYLOAD = 'pushed'
DEVICE_TYPE = 'robot'
DEVICE_ID = 'robot01'

MockRPi = MagicMock()
MockTime = MagicMock()
MockArgparse = MagicMock()
MockArgumentParser = MagicMock()
MockArg = MagicMock()
MockArg.host = HOST
MockArg.port = PORT
MockArg.device_type = DEVICE_TYPE
MockArg.device_id = DEVICE_ID
MockArg.pushed_payload = PUSHED_PAYLOAD

MockArgparse.ArgumentParser.return_value = MockArgumentParser
MockArgumentParser.parse_args.return_value = MockArg

modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
    "time": MockTime,
    "argparse": MockArgparse,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from src import dest_button


@patch('src.dest_button.GPIO')
@patch('src.dest_button.client')
class TestDestButton(unittest.TestCase):

    def test_setup(self, mocked_client, mocked_GPIO):
        dest_button.setup()
        mocked_GPIO.setwarnings.assert_called_once_with(False)
        mocked_GPIO.setmode.assert_called_once_with(mocked_GPIO.BCM)
        mocked_GPIO.setup.assert_any_call(LED_PIN, mocked_GPIO.OUT)
        mocked_GPIO.setup.assert_any_call(BTN_PIN, mocked_GPIO.IN)
        self.assertEqual(mocked_client.on_connect, dest_button.on_connect)
        self.assertEqual(mocked_client.on_disconnect, dest_button.on_disconnect)
       
    @parameterized.expand([(1, False), (0, True)])
    def test_on_connect(self, mocked_client, mocked_GPIO, rc, is_connected):
        dest_button.on_connect(mocked_client, None, 0, rc)
        self.assertEqual(dest_button.Connected, is_connected)

    def test_on_disconnect(self, mocked_client, mocked_GPIO):
        dest_button.on_disconnect(mocked_client, None)
        mocked_client.loop_stop.assert_called_once()
        self.assertFalse(dest_button.Connected)

    def test_sensor(self, mocked_client, mocked_GPIO):
        mocked_GPIO.input.return_value = 1
        mocked_GPIO.HIGH = 1
        mocked_GPIO.LOW = 0
        topic = '/{}/{}/attrs'.format(DEVICE_TYPE, DEVICE_ID)

        with freezegun.freeze_time('2018-01-02T03:04:05.000000+0900'):
            tzinfo = datetime.timezone(datetime.timedelta(hours=9))
            date = datetime.datetime.now().replace(tzinfo=tzinfo).isoformat()
            payload = '{}|{}|{}'.format(date, PUSHED_PAYLOAD, date)
            dest_button.sensor()
        mocked_GPIO.input.assert_called_once_with(BTN_PIN)
        mocked_client.publish.assert_called_once_with(topic, payload)
        MockTime.sleep.assert_called_once_with(1)
        mocked_GPIO.output.assert_any_call(LED_PIN, mocked_GPIO.HIGH)
        mocked_GPIO.output.assert_any_call(LED_PIN, mocked_GPIO.LOW)
