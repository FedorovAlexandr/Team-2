#!/usr/bin/python

import argparse

def parser():
    """Parses command-line"""

    parser = argparse.ArgumentParser(description='Parser')
    parser.add_argument('-P', action='store_true', help='Equivalent to --partial --progress')
    parser.add_argument('-S', action='store_true', help='Handle sparse files efficiently')
    parser.add_argument('-a', action='store_true', help='Archive mode')
    parser.add_argument('-e', action='store', help='Specify the remote shell to use')
    parser.add_argument('-q', action='store_true', help='Decrease verbosity')
    parser.add_argument('-v', action='store_true', help='Increase verbosity')
    parser.add_argument('-z', action='store_true', help='Compress file data during the transfer')
    parser.add_argument('-pass', action='store', dest='passwd', help='Get password')
    parser.add_argument('-progress', action='store_true', help='Show progress during transfer')
    parser.add_argument('paths', nargs='*', help='Get sources and destinations')
    args = parser.parse_args()
    paths = args.paths
    return paths
