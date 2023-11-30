#!/usr/bin/env python
"""
Note on `pathlib.Path().resolve()` - it gets the current working directory,
but it depends on where the file got executed. So if you call this file
from one directory above, it shows you the (same) directory above.
"""
import pathlib


# Folders
BASE_DIR: str = str(pathlib.Path().resolve())
CORE_DIR: str = BASE_DIR + '/core'
STATIC_DIR: str = BASE_DIR + '/static'

# Files
GITLOG_DUMMY: str = STATIC_DIR + '/gitlog-dummy.txt'
