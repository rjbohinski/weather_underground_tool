#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `weather_underground_tool` package."""

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import pytest

from weather_underground_tool.weather_underground_tool import WU


DEFAULT_FILE_NAME = 'secret.txt'


def load_key(file_name=DEFAULT_FILE_NAME):
    """Load the API key from the file.

    :param str file_name: The key file name.
    :return: The key.
    :rtype: str
    :raises IOError: If the file could not be read or is empty.
    """
    key = None
    with open(file_name, 'r') as key_file:
        key = key_file.read().strip()

    if key is None:
        raise IOError()
    return key


@pytest.mark.key
def test_api():
    """Test the API call."""
    api = WU(load_key())
    json = api.call_api(['conditions'], 'PA/Philadelphia')
    assert json['current_observation']['display_location']['full'] == \
        'Philadelphia, PA'


def test_api_bad_key():
    """Test the API call with a bad key."""
    api = WU('0')
    json = api.call_api(['conditions'], 'PA/Philadelphia')
    assert json['response']['error']['type'] == \
        'keynotfound'


@pytest.mark.key
def test_template():
    """Test the template function."""
    api = WU(load_key())
    output = api.format_data(
        ['conditions'],
        'PA/Philadelphia',
        'Test [display_location_full]')
    assert 'Test Philadelphia, PA' in output
    assert '[' not in output
