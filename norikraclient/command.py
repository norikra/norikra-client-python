#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import sys
import itertools
import json

from . client import Client
from . option_parser import parse_commands


def main(argv=sys.argv):
    """norikra-client-py main command-line entry"""

    # parse commands include sub commands, and return all as dict
    args = parse_commands(argv)

    # start handling
    nclient = Client(host=args['host'], port=args['port'])

    command = args['command']
    sub = args['sub']
    if command == 'event':
        if sub == 'send':
            buffer = []
            for line in sys.stdin:
                if len(buffer) >= args.batch_size:
                    nclient.send(args.target, buffer)
                    buffer = []
                    buffer.append(json.loads(line))

            if len(buffer) > 0:
                nclient.send(args.target, buffer)

        elif sub == 'fetch':
            print(nclient.event(args.query_name))

    return True

if __name__ == '__main__':
    sys.exit(main(sys.argv))
