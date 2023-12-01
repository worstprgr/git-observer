#!/bin/env python
from GitObserver import GitObserver
import datetime
import time
from argparse import ArgumentParser

def call_commandline(args):
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Starting git log observer...")
    observer = GitObserver(args)
    while 1:
        observer.run()
        time.sleep(60)

def parse_arguments():
     parser = ArgumentParser(allow_abbrev=True)
     parser.add_argument('-o', '--origin', metavar='origin', help='Origin path to build commit link for output', required=True)
     parser.add_argument('-f', '--filepath', help='Git root to be observed', action='store', required=True)
     parser.add_argument('-lf', '--logfolders', metavar='Folder', type=str, nargs='+', help='Folder(s) to be observed', required=True)
     parser.add_argument('-ig', '--ignore', metavar='Author', type=str, nargs='+', help='Author name to be ignored')
     return parser.parse_args()

if __name__ == '__main__':
       args = parse_arguments()
       call_commandline(args)
