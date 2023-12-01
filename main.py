#!/bin/env python
from GitObserver import GitObserver
import datetime
import time
from argparse import ArgumentParser


def call_commandline(config):
    """
    Calls the command line tool GitObserver using
    passed config in an endless loop paused for 60s per run
    :param config: configuration of command line tool
    :return: None
    """
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Starting git log observer...")
    observer = GitObserver(config)
    while 1:
        observer.run()
        time.sleep(60)


def parse_arguments():
    """
    Parses the given arguments passed by caller and
    returns the parsed result
    :return:
    """
    parser = ArgumentParser(allow_abbrev=True)
    parser.add_argument('-o', '--origin', metavar='origin', default='',
                        help='Origin path to build commit link for output', required=False)
    parser.add_argument('-f', '--filepath', action='store',
                        help='Git root to be observed', required=True)
    parser.add_argument('-lf', '--logfolders', metavar='Folder', type=str, nargs='+',
                        default='.', help='Folder(s) to be observed', required=False)
    parser.add_argument('-ig', '--ignore', metavar='Author', type=str, nargs='+',
                        help='Author name to be ignored')
    return parser.parse_args()


if __name__ == '__main__':
    parsed_config = parse_arguments()
    call_commandline(parsed_config)
