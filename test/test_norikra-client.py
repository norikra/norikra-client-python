#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import sys
import os
import datetime
from pprint import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from norikraclient.client import Client

class TestNorikraClient(object):
    def test_targets(self):
        n = Client()

        print(n.targets())