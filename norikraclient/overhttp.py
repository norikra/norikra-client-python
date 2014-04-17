#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import msgpack
import requests

REQUEST = 0  # [0, msgid, method, param]
RESPONSE = 1  # [1, msgid, error, result]
NOTIFY = 2  # [2, method, param]

NO_METHOD_ERROR = 0x01
ARGUMENT_ERROR = 0x02

HEADER = {"Content-Type": 'application/x-msgpack'}


class MsgPackClientOverHttp(object):
    def __init__(self, url):
        self.url = url
        self.seqid = 0
        self.client = None

        self.connection_timeout = 1
        self.send_timeout = 1
        self.receive_timeout = 1

    def call(self, method, *args, **kwargs):
        return self.send_request(method, args)

    def send_request(self, method, param):
        data = self.create_request_body(method, param)

        r = requests.post(self.url, data=data, headers=HEADER,
                          timeout=self.connection_timeout)

        if r.status_code != 200:
            raise Exception(r.status_code)
        return self.get_result(r.content)

    def create_request_body(self, method, param):
        method = str(method)
        msgid = self.seqid
        self.seqid += 1
        if self.seqid >= (1 << 31):
            self.seqid = 0

        data = msgpack.packb([REQUEST, msgid, str(method), param])

        return data

    def get_result(self, body):
        type, msgid, err, res = msgpack.unpackb(body, encoding='utf-8')
        if type != RESPONSE:
            raise "Unknown message type {}".format(type)

        if err is None:
            return res
        else:
            raise Exception(err)


if __name__ == '__main__':
    pass
