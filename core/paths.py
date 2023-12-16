#!/usr/bin/env python
import pathlib

import core.utils

# Init
path_utils = core.utils.PathUtils()


class Paths:
    """
    Converts all string paths to path like objects. \n\n

    **Usage** \n
    *import core.paths* \n\n

    *c_paths = core.paths.Paths()* \n\n

    *config_ini = c_paths.CONFIG_INI* \n
    *bunny_file = c_paths.BUNNY_FILE* \n\n
    """
    def __init__(self):
        """
        *Implementation of a new path*\n\n

        Concatenating a path like object with a string:\n
        *self.new_path = self.PATH_1, '/file.txt'*\n\n

        Concatenating two path like objects:\n
        *self.new_path = self.PATH_1, '/', self.PATH_2*\n\n

        Concatenating two path like objects and a file as string:\n
        *self.new_path = self.PATH_1, '/', self.PATH_2, '/file.txt'*
        """
        # Root directory of the project
        self.BASE_DIR: str = path_utils.get_base_dir()

        # Folders
        self.CORE_DIR = self.BASE_DIR, '/core'
        self.STATIC_DIR = self.BASE_DIR, '/static'
        self.LOG_DIR = self.BASE_DIR, '/logs'
        self.STATIC_UT_DIR = self.STATIC_DIR, '/unittest'

        # Files
        self.CONFIG_INI = self.BASE_DIR, '/conf.ini'

        # Unittest
        self.BUNNY_FILE = self.STATIC_UT_DIR, '/bunny.txt'
        self.LOG_FILE_DUMMY = self.STATIC_UT_DIR, '/dummy-log.txt'
        self.GITLOG_DUMMY = self.STATIC_UT_DIR, '/gitlog-dummy.txt'
        self.GITLOG_DUMMY_REDUNDANT = self.STATIC_UT_DIR, '/gitlog-dummy-redundant.txt'
        self.CONF_INI_DUMMY = self.STATIC_UT_DIR, '/conf_dummy.ini'

        for name in dir(self):
            if not name.startswith('__') and not callable(getattr(self, name)):
                nested_paths: tuple = getattr(self, name)
                nested_paths: str = self.flatten_tuple(nested_paths)
                setattr(self, name, pathlib.Path(nested_paths))

    def flatten_tuple(self, nested_tuple):
        result = ""
        for item in nested_tuple:
            if isinstance(item, tuple):
                result += self.flatten_tuple(item)
            else:
                result += item
        return result
