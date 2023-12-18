#!/bin/env python
from argparse import Namespace
from time import sleep

from core.config.management import ConfigManager
from core.transport import Observation, ObservationUtil
from observer import GitObserver
from viewer import GitObserverViewer
from core.utils import SignalReceiver
from core.logger import Logger

log = Logger(__name__).log_init
__run_main = True


def global_sigterm():
    """
    Event handler to receive exit signals by system, provided
    by SignalReceiver.  
    Sets the main thread flag __run_main to False
    :return: None
    """
    global __run_main
    log.info("SIGTERM called")
    __run_main = False


def call_shell(config: Namespace, interval_ms: int) -> None:
    """
    Calls the command line tool GitObserver using
    passed config
    :param config: configuration of command line tool
    :param interval_ms: Milliseconds describing the length of one iteration
    :return: None
    """
    global __run_main

    log.info("Starting GitObserver shell")
    observer = GitObserver(config)
    ms_since_last_iteration = 0
    while __run_main:
        if ms_since_last_iteration % interval_ms == 0:
            observations: list[Observation] = observer.load_observations()
            if not ObservationUtil.is_empty(observations):
                for folder in observations:
                    print(f'--- {folder} ---')
                    for cmt in folder.commits:
                        branch = f'{cmt.branch}\n' if cmt.branch else ''
                        print(f"{cmt.author} ({cmt.date}): {cmt.message}\n" +
                              f"{branch}" +
                              f"{cmt.origin}{cmt.sha1}\n")
                ms_since_last_iteration = 0
        sleep(0.1)
        ms_since_last_iteration += 100


def call_viewer(config: Namespace, sig_recv: SignalReceiver) -> None:
    """
    Calls the viewer tool GitObserverViewer using
    passed config.
    Commonly used in a separate thread
    :param config: configuration of command line tool
    :param sig_recv: SignalReceiver which should be bound to exit gracefully
    :return: None
    """
    viewer = GitObserverViewer(config)
    sig_recv.OnTerminate += viewer.root_delete
    viewer.mainloop()


if __name__ == '__main__':
    app_config = ConfigManager.get_config()

    # React to SIGTERM/-INIT
    signal_receiver = SignalReceiver()
    signal_receiver.OnTerminate += global_sigterm

    if app_config.show_viewer:
        call_viewer(app_config, signal_receiver)
    else:
        # Calc interval duration
        interval_dur_s = 60
        interval_dur_ms = interval_dur_s * 1000
        call_shell(app_config, interval_dur_ms)
