#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import argparse

def parse_event(origargs):
    parser = argparse.ArgumentParser(description='event',
                                     prog='norikra-client-py', add_help=False)
    subparsers = parser.add_subparsers(help='sub commands', dest='sub')

    # fetch
    parser_fetch = subparsers.add_parser('fetch',
                                         help="fetch events from specified query")
    parser_fetch.add_argument('query_name', nargs='*',
                              help="fetch events from specified query")

    # send
    parser_send = subparsers.add_parser('send', help="send data into targets")
    parser_send.add_argument('--batch_size', action='store', type=int, default=10000,
                             help="records sent in once transferring (default: 10000)")
    parser_send.add_argument('target')

    args = parser.parse_args(origargs.rest)

    # convert to dict in order to merge all args
    dict_orig = vars(origargs)
    dict_orig['command'] = 'event'
    dict_args = vars(args)
    dict_orig.update(dict_args)

    return dict_orig

def parse_commands(argv):
    parser = argparse.ArgumentParser(description='norikra client for python',
                                     prog='norikra-client-py')
    parser.add_argument('--host', action='store', help='HOST',
                        default='localhost')
    parser.add_argument('--port', action='store', help='PORT',
                        type=int, default=26571)
    subparsers = parser.add_subparsers(help='sub commands')

    parser_event = subparsers.add_parser('event', help='send/fetch events')
    parser_event.add_argument('rest', nargs='*')
    parser_event.set_defaults(func=parse_event)

    parser_query = subparsers.add_parser('query', help='manage queries')
    parser_target = subparsers.add_parser('target', help='manage targets')

    args = parser.parse_args()
    args = args.func(args)

    return args

