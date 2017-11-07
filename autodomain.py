#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
sys.dont_write_bytecode = True

print('name: ', __file__)
print('args: ', ' '.join(sys.argv[1:]))


SCRIPTNAME = os.path.splitext(__file__)[0]
SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

from ruamel import yaml
from argparse import ArgumentParser, RawDescriptionHelpFormatter

if __name__ == '__main__':
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False)
    parser.add_argument(
        '--config',
        metavar='FILEPATH',
        default='%(SCRIPTPATH)s/config.yml' % globals(),
        help='default="%(default)s"; config filepath')
    ns, rem = parser.parse_known_args()
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
