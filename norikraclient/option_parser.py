#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import argparse


def parse_event(origargs):
    parser = argparse.ArgumentParser(add_help=False)
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


def parse_target(origargs):
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(help='sub commands', dest='sub')

    # list
    parser_list = subparsers.add_parser('list',
                                        help="show list of targets")
    parser_list.add_argument('-s', '--simple', action='store_true',
                             help="suppress header/footer")

    # open
    parser_open = subparsers.add_parser('open',
                                        help="create new target (and define its fields)")
    parser_open.add_argument('-x', '--suppress_auto_field', action='store_true',
                             help="suppress to define fields automatically")
    parser_open.add_argument('target', nargs=1)
    parser_open.add_argument('field_defs', nargs="*")

    # close
    parser_close = subparsers.add_parser('close',
                                         help="close existing target and all its queries")
    parser_close.add_argument('target', nargs=1)

    # modify
    parser_modify = subparsers.add_parser('modify',
                                          help="modify target to do define fields automatically or not")
    parser_modify.add_argument('target', nargs=1)
    parser_modify.add_argument('bool_value', nargs=1)

    args = parser.parse_args(origargs.rest)

    # convert to dict in order to merge all args
    dict_orig = vars(origargs)
    dict_orig['command'] = 'target'
    dict_args = vars(args)
    dict_orig.update(dict_args)

    return dict_orig


def parse_admin(origargs):
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers(help='sub commands', dest='sub')

    # stats
    parser_stats = subparsers.add_parser('stats',
                                         help="dump stats json: same with norikra server's --stats option")

    args = parser.parse_args(origargs.rest)

    # convert to dict in order to merge all args
    dict_orig = vars(origargs)
    dict_orig['command'] = 'admin'
    dict_args = vars(args)
    dict_orig.update(dict_args)

    return dict_orig


def parse_commands(argv):
    '''This is parent parser which parses subcommands.'''
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
    parser_query.add_argument('rest', nargs='*')
#    parser_query.set_defaults(func=parse_query)

    parser_target = subparsers.add_parser('target', help='manage targets')
    parser_target.add_argument('rest', nargs='*')
    parser_target.set_defaults(func=parse_target)

    parser_admin = subparsers.add_parser('admin', help='manage admins')
    parser_admin.add_argument('rest', nargs='*')
    parser_admin.set_defaults(func=parse_admin)

    args = parser.parse_args()
    args = args.func(args)

    return args
