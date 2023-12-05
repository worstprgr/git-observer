#!/usr/bin/env python
import core.utils


# Init
path_utils = core.utils.PathUtils()


# Folders
BASE_DIR: str = path_utils.get_base_dir()
CORE_DIR: str = BASE_DIR + '/core'
STATIC_DIR: str = BASE_DIR + '/static'
LOG_DIR: str = BASE_DIR + '/logs'

# Files
GITLOG_DUMMY: str = STATIC_DIR + '/gitlog-dummy.txt'
LOG_FILE = lambda a: LOG_DIR + f'/log_{a}.log'
