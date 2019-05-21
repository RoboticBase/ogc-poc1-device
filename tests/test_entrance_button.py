#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import freezegun
import datetime


from mock import patch

from parameterized import parameterized

from module_mock import (LED_PIN, BTN_PIN,
                         DEVICE_ID, DEVICE_TYPE, MockTime)

from src import entrance_button


@patch('src.entrance_button.GPIO')
@patch('src.entrance_button.client')
class TestEntranceButton(unittest.TestCase):

    def test_setup(self, mocked_client, mocked_GPIO):
        entrance_button.setup()
        mocked_GPIO.setwarnings.assert_called_once_with(False)
        mocked_GPIO.setmode.assert_called_once_with(mocked_GPIO.BCM)
        mocked_GPIO.setup.assert_any_call(LED_PIN, mocked_GPIO.OUT)
        mocked_GPIO.setup.assert_any_call(BTN_PIN, mocked_GPIO.IN)
        self.assertEqual(mocked_client.on_connect, entrance_button.on_connect)
        self.assertEqual(mocked_client.on_disconnect,
                         entrance_button.on_disconnect)

    @parameterized.expand([(1, False), (0, True)])
    def test_on_connect(self, mocked_client, mocked_GPIO, rc, is_connected):
        entrance_button.on_connect(mocked_client, None, 0, rc)
        self.assertEqual(entrance_button.Connected, is_connected)

    def test_on_disconnect(self, mocked_client, mocked_GPIO):
        entrance_button.on_disconnect(mocked_client, None)
        mocked_client.loop_stop.assert_called_once()
        self.assertFalse(entrance_button.Connected)

    def test_sensor(self, mocked_client, mocked_GPIO):
        mocked_GPIO.input.return_value = 1
        mocked_GPIO.HIGH = 1
        mocked_GPIO.LOW = 0
        topic = '/{}/{}/attrs'.format(DEVICE_TYPE, DEVICE_ID)

        with freezegun.freeze_time('2018-01-02T03:04:05.000000+0900'):
            tzinfo = datetime.timezone(datetime.timedelta(hours=9))
            date = datetime.datetime.now().replace(tzinfo=tzinfo).isoformat()
            payload = '{}|state|on'.format(date)
            entrance_button.sensor()
        mocked_GPIO.input.assert_called_once_with(BTN_PIN)
        mocked_client.publish.assert_called_once_with(topic, payload)
        MockTime.sleep.assert_any_call(1)
        mocked_GPIO.output.assert_any_call(LED_PIN, mocked_GPIO.HIGH)
        mocked_GPIO.output.assert_any_call(LED_PIN, mocked_GPIO.LOW)
