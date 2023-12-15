#!/usr/bin/env python 
import logging
import os
import pathlib
from datetime import datetime

import core.utils as c_utils
import core.paths as c_paths


path_utils = c_utils.PathUtils()
file_utils = c_utils.FileUtils()


class Logger:
    """
    Usage:
        import core.logger as logger

        log = logger.Logger(__name__).log_init

        log.debug('Message')
        log.info('Message')
        log.warning('Message')
        log.error('Message')
        log.critical('Message')

    Logging an exception with traceback
        try:
            0/0
        except ZeroDivisionError as e:
            log.exception('Stop doing that.', exc_info=e)

    Logging an exception with traceback & stacktrace
        try:
            a = [1, 2]
            print(a[3])
        except IndexError as e:
            log.exception('Wrong Index', exc_info=e, stack_info=True)
    """

    def __init__(self, current_file):
        self.dt_now: datetime = datetime.now()
        self.date_initial_strf: str = self.dt_now.strftime('%Y-%m-%d')
        self.log_file_name = path_utils.conv_to_path_object(c_paths.LOG_FILE(self.date_initial_strf))

        # Create log file, if it doesn't exist
        self.if_log_exists_today(self.log_file_name)

        # Logger setup
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s.%(msecs)04d [%(levelname)s]: %(module)s -> %(funcName)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[
                                logging.FileHandler(self.log_file_name, 'a', encoding='utf8'),
                                logging.StreamHandler()
                            ])
        self.log_init = logging.getLogger(current_file)

    @staticmethod
    def if_log_exists_today(fp: pathlib.Path) -> bool:
        file_exists: bool = os.path.exists(fp)
        if not file_exists:
            fp.touch()
            return False
        return True

    @staticmethod
    def close_logger() -> None:
        """
        Looks after an instance from `logging.FileHandler` and closes it.
        """
        file_handler = next(
            (handler for handler in logging.getLogger().handlers if isinstance(handler, logging.FileHandler)), None)
        if file_handler:
            file_handler.close()
