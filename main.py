#!/bin/env python
import datetime
import time
from argparse import Namespace

from GitObserver import GitObserver
from GitObserverViewer import GitObserverViewer
from core.config import ConfigHandler


def call_commandline(config: Namespace):
    """
    Calls the command line tool GitObserver using
    passed config in an endless loop paused for 60s per run
    :param config: configuration of command line tool
    :return: None
    """
    # TODO: Replace this line with the logger
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Starting git log observer...")
    observer = GitObserver(config)
    while 1:
        observer.run()
        time.sleep(60)


if __name__ == '__main__':
    app_config = ConfigHandler.get_app_config()
    if app_config.show_viewer:
        GitObserverViewer(app_config).run()
    else:
        call_commandline(app_config)
