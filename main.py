#!/bin/env python
from GitObserver import GitObserver
from GitObserverViewer import GitObserverViewer
import datetime
import time
from argparse import ArgumentParser
from core.paths import BASE_DIR

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
    parser.add_argument('-o', '--origin', metavar='origin',
                        default='https://github.com/worstprgr/git-observer/commit/',  # Default to repo at GitHub
                        help='Origin path to build commit link for output', required=False)
    parser.add_argument('-f', '--filepath', action='store', default=BASE_DIR,
                        help='Git root to be observed', required=False)
    parser.add_argument('-lf', '--logfolders', metavar='Folder', type=str, nargs='+',
                        default='.', help='Folder(s) to be observed', required=False)
    parser.add_argument('-ig', '--ignore', metavar='Author', type=str, nargs='+',
                        help='Author name to be ignored')
    parser.add_argument('-ui', '--show-viewer', action='store_true', default=False,
                        help='Flag to determine if application should open a grid in UI')
    parser.add_argument('-desc', '--descending', action='store_true', default=False,
                        help='Flag if output should be descending. DEFAULT for --use-viewer')
    return parser.parse_args()


if __name__ == '__main__':
    parsed_config = parse_arguments()
    if parsed_config.show_viewer:
        GitObserverViewer(parsed_config).run()
    else:
        call_commandline(parsed_config)
