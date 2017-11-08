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

def main(args):
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False)
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
        parents=[parser])
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
    ns = parser.parse_args(rem)
    print(ns)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
