#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
autodomain
'''

import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from ruamel import yaml

from utils.format import fmt

sys.dont_write_bytecode = True
FILE = os.path.realpath(__file__)
SCRIPTNAME = os.path.splitext(FILE)[0]
SCRIPTPATH = os.path.dirname(os.path.abspath(FILE))

def command_subparsers(parser):
    subparsers = parser.add_subparsers(
        dest='command',
        title='commands',
        description='choose a command to run')
    return subparsers

def ls_parser(subparsers):
    parser = subparsers.add_parser('ls')
    parser.add_argument(
        '--ls-arg',
        help='ls arg')
    return parser

def create_parser(subparsers):
    parser = subparsers.add_parser('create')
    parser.add_argument(
        '--create-arg',
        help='create arg')

def change_parser(subparsers):
    parser = subparsers.add_parser('change')
    parser.add_argument(
        '--change-arg',
        help='change arg')

def main(args):
#    parser = ArgumentParser(
#        description=__doc__,
#        formatter_class=RawDescriptionHelpFormatter,
#        add_help=False)
    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        '--config',
        metavar='FILEPATH',
        default='%(SCRIPTPATH)s/config.yml' % globals(),
        help='default="%(default)s"; config filepath')
    ns, rem = parser.parse_known_args(args)
    try:
        config = yaml.safe_load(open(ns.config))
    except FileNotFoundError as er:
        config = dict()
    parser = ArgumentParser(
        parents=[parser],
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter)

    parser.set_defaults(**config)
    parser.add_argument(
        '--firstname',
        help='default="%(default)s"; first name')
    parser.add_argument(
        '--lastname',
        help='default="%(default)s"; last name')
    parser.add_argument(
        '--age',
        help='default="%(default)s"; age')

    subparsers = command_subparsers(parser)
    ls_parser(subparsers)
    create_parser(subparsers)
    change_parser(subparsers)

    ns = parser.parse_args(rem)
    print(ns)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
