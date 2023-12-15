#!/usr/bin/env python
import pathlib
from datetime import datetime

import core.paths as c_paths


class LoggerFactory:
    @staticmethod
    def create_log_file_path():
        dt_now: datetime = datetime.now()
        date_initial_strf: str = dt_now.strftime('%Y-%m-%d')
        log_file_name = pathlib.Path(c_paths.LOG_FILE(date_initial_strf))
        return log_file_name
