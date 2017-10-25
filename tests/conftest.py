#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Add keyword to skip tests if a key is required. Useful for Travis tests."""

from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import pytest


def pytest_addoption(parser):
    parser.addoption("--runkey", action="store_true",
                     default=False, help="run tests that require keys")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runkey"):
        # --runkey given in cli: do not skip slow tests
        return
    skip_key = pytest.mark.skip(reason="need --runkey option to run")
    for item in items:
        if "key" in item.keywords:
            item.add_marker(skip_key)
