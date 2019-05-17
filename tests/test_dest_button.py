#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from mock import patch, MagicMock

from parameterized import parameterized, param

MockRPi = MagicMock()
MockArgparse = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
    "argparse": MockArgparse,
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from src import dest_button


@patch('RPi.GPIO')
@patch('src.dest_button.args')
@patch('src.dest_button.client')
class TestDestButton(unittest.TestCase):

    def test_setup(self, mocked_client, mocked_args, mocked_GPIO):
        dest_button.setup()
        
