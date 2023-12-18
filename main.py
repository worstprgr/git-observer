#!/bin/env python
import datetime
from argparse import Namespace

from core.config.management import ConfigManager
from core.transport import ObservationEventArgs
from observer import GitObserverThread
from viewer import GitObserverViewer
from core.utils import SignalUtils
from core.logger import Logger

sig_utl = SignalUtils()
log = Logger(__name__).log_init


def observer_loaded(e: ObservationEventArgs) -> None:
    """
    Event handler that handles newly loaded observations by
    presenting them to the shell
    :return: None
    """
    for observation in e.observations:
        print(f"#### Observation {observation.name} ({e.update_time}) ####")
        for cmt in observation.commits:
            print(f"{cmt.author} ({cmt.date}): {cmt.message}\n" +
                  f"{cmt.branch}\n" +
                  f"{cmt.origin}{cmt.sha1}\n")


def call_shell(config: Namespace) -> None:
    """
    Calls the command line tool GitObserver using
    passed config in an endless loop paused for 60s per run
    :param config: configuration of command line tool
    :return: None
    """
    observer = GitObserverThread(config)
    observer.OnLoaded += observer_loaded
    observer.start()
    print(f'{datetime.datetime.now()}: GitObserver for shell started')

    while True:
        if sig_utl.term_status:
            observer.run_thread = False
            log.info('SIGTERM / SIGINT received. Shutting down program.')
            break


if __name__ == '__main__':
    app_config = ConfigManager.get_config()
    if app_config.show_viewer:
        GitObserverViewer(app_config).run()
    else:
        call_shell(app_config)
