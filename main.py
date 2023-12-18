#!/bin/env python
import datetime
from argparse import Namespace

from core.config.management import ConfigManager
from core.transport import ObservationEventArgs
from observer import GitObserverThread
from viewer import GitObserverViewer


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

    # Keeping the child thread alive
    while observer.is_alive():
        observer.join(1)


if __name__ == '__main__':
    app_config = ConfigManager.get_config()
    if app_config.show_viewer:
        GitObserverViewer(app_config).run()
    else:
        call_shell(app_config)
