#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import sys
import itertools
import json

from . client import Client
from . option_parser import parse_commands


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

        auto_field = not args['suppress_auto_field']

        nclient.open(args['target'][0], fields, auto_field)

    def close(self, nclient, args):
        nclient.close(args['target'][0])

    def modify(self, nclient, args):
        auto_field = args['bool_value'][0] in ['yes', 'true', 'auto']

        nclient.modify(args['target'][0], auto_field)


class QueryCmd(object):
    def list(self, nclient, args):
        if args['simple'] is False:
            print("\t".join(["NAME", "GROUP", "TARGETS", "QUERY"]))
        queries = nclient.queries()
        queries = sorted(queries)
        for q in queries:
            print("{}\t{}\t{}\t{}".format(
                q['name'],
                'default' if q['group'] is None else q['group'],
                ','.join(q['targets']),
                " ".join([qe.strip() for qe in q['expression'].split("\n")]),
            ))

        if args['simple'] is False:
            print("{} queries found.".format(len(queries)))

    def add(self, nclient, args):
        q = args['query_name'][0]
        e = " ".join(args['expression'])
        group = 'default'  # TODO
        nclient.register(q, group, e)

    def remove(self, nclient, args):
        q = args['query_name'][0]
        nclient.deregister(q)


class FieldCmd(object):
    def list(self, nclient, args):
        if args['simple'] is False:
            print("{}\t{}".format("TARGET", "TYPE", "OPTIONAL"))

        target = args['target'][0]
        fields = nclient.fields(target)
        for f in fields:
            print("{}\t{}".format(f['name'], f['type'], f['optional']))
        if args['simple'] is False:
            print("{} field(s) found.".format(len(fields)))

    def add(self, nclient, args):
        target = args['target'][0]
        field = args['field'][0]
        type = args['type'][0]
        nclient.reserve(target, field, type)


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


class AdminCmd(object):
    def stats(self, nclient, args):
        targets = []
        queries = []

        queries = nclient.queries()
        for t in nclient.targets():
            fields = {}
            for f in nclient.fields(t['name']):
                if f['type'] == 'hash' or f['type'] == 'array':
                    continue
                fields[f['name']] = f
            targets.append({
                "name": t["name"],
                "fields": fields,
                "auto_field": t["auto_field"],
                })

        import json

        v = {
            "threads": {
                "engine": {"inbound": {},
                           "outbound": {},
                           "route_exec": {},
                           "timer_exec": {}
                },
                "rpc": {},
                "web": {},
            },
            "log": {},
            "targets": targets,
            "queries": queries,
        }

        print(json.dumps(v, sort_keys=True,
                         indent=4, separators=(',', ': ')))


def main(argv=sys.argv):
    """norikra-client-py main command-line entry"""

    # parse commands include sub commands, and return all as dict
    args = parse_commands(argv)

    # start handling
    nclient = Client(host=args['host'], port=args['port'])

    command = args['command']
    sub = args['sub']
    if command == 'target':
        c = TargetCmd()
        if sub == 'list':
            c.list(nclient, args)
        elif sub == 'open':
            c.open(nclient, args)
        elif sub == 'close':
            c.close(nclient, args)
        elif sub == 'modify':
            c.modify(nclient, args)
    elif command == 'query':
        c = QueryCmd()
        if sub == 'list':
            c.list(nclient, args)
        elif sub == 'add':
            c.add(nclient, args)
        elif sub == 'remove':
            c.remove(nclient, args)
    elif command == 'field':
        c = FieldCmd()
        if sub == 'list':
            c.list(nclient, args)
        elif sub == 'add':
            c.add(nclient, args)
    elif command == 'event':
        c = EventCmd()
        if sub == 'send':
            c.send(nclient, args)
        elif sub == 'fetch':
            c.fetch(nclient, args)
    elif command == 'admin':
        c = AdminCmd()
        if sub == 'stats':
            c.stats(nclient, args)

    return True

if __name__ == '__main__':
    sys.exit(main(sys.argv))
