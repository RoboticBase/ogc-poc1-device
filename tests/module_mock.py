#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mock import MagicMock, patch

LED_PIN = 26
BTN_PIN = 5
HOST = 'test_host'
PORT = 1883
PUSHED_PAYLOAD = 'pushed'
DEVICE_TYPE = 'robot'
DEVICE_ID = 'robot01'

MockNeopixel = MagicMock()
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
    "neopixel": MockNeopixel,
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
    "time": MockTime,
    "argparse": MockArgparse,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()
