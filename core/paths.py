#!/usr/bin/env python
import core.utils


# Init
path_utils = core.utils.PathUtils()


# Folders
BASE_DIR: str = path_utils.get_base_dir()
CORE_DIR: str = BASE_DIR + '/core'
STATIC_DIR: str = BASE_DIR + '/static'
LOG_DIR: str = BASE_DIR + '/logs'
STATIC_UT_DIR: str = STATIC_DIR + '/unittest'

# Files
CONFIG_INI: str = BASE_DIR + '/conf.ini'
LOG_FILE = lambda a: LOG_DIR + f'/log_{a}.log'

# Unittest
BUNNY_FILE: str = STATIC_UT_DIR + '/bunny.txt'
LOG_FILE_DUMMY: str = STATIC_UT_DIR + '/dummy-log.txt'
GITLOG_DUMMY: str = STATIC_UT_DIR + '/gitlog-dummy.txt'
GITLOG_DUMMY_REDUNDANT: str = STATIC_UT_DIR + '/gitlog-dummy-redundant.txt'
CONF_INI_DUMMY: str = STATIC_UT_DIR + '/conf_dummy.ini'
