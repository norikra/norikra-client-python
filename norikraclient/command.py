#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import sys
import itertools
import json

from . client import Client
from . option_parser import parse_commands


class EventCmd(object):
    def send(self, nclient, args):
        buffer = []
        for line in sys.stdin:
            if len(buffer) >= args['batch_size']:
                nclient.send(args['target'], buffer)
                buffer = []
                buffer.append(json.loads(line))
            if len(buffer) > 0:
                nclient.send(args['target'], buffer)

    def fetch(self, nclient, args):
        print(nclient.event(args['query_name']))

class TargetCmd(object):
    def list(self, nclient, args):
        if args['simple'] is False:
            print("{}\t{}".format("TARGET", "AUTO_FIELD"))
        targets = nclient.targets()
        for t in targets:
            print("{}\t{}".format(t['name'], t['auto_field']))
        if args['simple'] is False:
            print("{} target(s) found.".format(len(targets)))

    def open(self, nclient, args):
        field_defs = args['field_defs']
        fields = None
        if len(field_defs) > 0:
            fields = {}
            for s in field_defs:
                fname, ftype = s.split(':')
                fields[fname] = ftype

        auto_field = True
        if args['suppress_auto_field']:
            auto_field = False

        nclient.open(args['target'][0], fields, auto_field)

def main(argv=sys.argv):
    """norikra-client-py main command-line entry"""

    # parse commands include sub commands, and return all as dict
    args = parse_commands(argv)

    # start handling
    nclient = Client(host=args['host'], port=args['port'])

    command = args['command']
    sub = args['sub']
    if command == 'event':
        c = EventCmd()
        if sub == 'send':
            c.send(nclient, args)
        elif sub == 'fetch':
            c.fetch(nclient, args)
    elif command == 'target':
        c = TargetCmd()
        if sub == 'list':
            c.list(nclient, args)
        elif sub == 'open':
            c.open(nclient, args)



    return True

if __name__ == '__main__':
    sys.exit(main(sys.argv))
