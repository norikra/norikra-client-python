#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import sys

from . overhttp import MsgPackClientOverHttp

RPC_DEFAULT_PORT = 26571


class Client(object):

    def __init__(self, host="localhost", port=RPC_DEFAULT_PORT, opts={}):
        addr = "http://{}:{}/".format(host, port)
        self.client = MsgPackClientOverHttp(addr)

        if 'connection_timeout' in opts:
            self.client.connection_timeout = opts['connection_timeout']
        if 'send_timeout' in opts:
            self.client.send_timeout = opts['send_timeout']
        if 'receive_timeout' in opts:
            self.client.receive_timeout = opts['receive_timeout']

    def targets(self):
        return self.client.call("targets")

    def open(self, target, fields=None, auto_field=True):
        return self.client.call("open", target, fields, auto_field)

    def close(self, target):
        return self.client.call("close", target)

    def modify(self, target, auto_field):
        return self.client.call("modify", target, auto_field)

    def queries(self):
        return self.client.call("queries")

    def register(self, query_name, query_group, query_expression):
        return self.client.call("register", query_name,
                                query_group, query_expression)

    def deregister(self, query_name):
        return self.client.call("deregister", query_name)

    def fields(self, target):
        return self.client.call("fields", target)

    def reserve(self, target, field, type):
        return self.client.call("reserve", target, field, type)

    def send(self, target, events):
        return self.client.call("send", target, events)

    # [ [time, event], ... ]
    def event(self, query_name):
        return self.client.call("event", query_name)

    # [ [time, event], ... ]
    def see(self, query_name):
        return self.client.call('see', query_name)

    # {'query_name' => [ [time, event], ... ]}
    def sweep(self, query_group=None):
        return self.client.call('sweep', query_group)

if __name__ == '__main__':
    pass