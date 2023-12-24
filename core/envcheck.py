#!/usr/bin/env python
import pathlib
import sys
import subprocess
from datetime import datetime

from core.paths import Paths
from core.utils import PathUtils


class EnvironmentCheck:
    """
    This class performs a check, if the core elements of this program are
    present or not. If one condition fails, the program gets terminated.

    Temporary files are ignored in the check.
    """
    def __init__(self, disable_logging: bool = False):
        """
        If you want to create folders, add the path object to `self.create_folders`.
        If you want to create files, add the path object to `self.create:files`.
        """
        self.c_paths = Paths()
        self.c_paths_mod = Paths()
        self.c_path_utils = PathUtils()
        self.disable_logging: bool = disable_logging
        self.check_list: list[bool] = []
        self.create_folders: list = [self.c_paths.LOG_DIR]
        self.create_files: list = []

        # If you want to add files or folders to the ignore variable,
        # use the variable names from core.paths.Paths().__init__
        self.ignore_temp_files: list = [
            'CONFIG_INI',
            'BUNNY_FILE',
            'LOG_FILE_DUMMY',
            'CONF_INI_DUMMY'
        ]

    def env_check(self, terminate: bool = True) -> bool | None:
        """
        Checking, if essential files and folders are existing, and if the
        Git client is present on the user's machine.

        :param terminate: (Optional) If False, it won't terminate the program, just return `False`.
        :return: A boolean or None, based on the given parameter.
        """
        self.env_log(1, 'Starting environment check ...')

        self.create_folders_or_files()

        self.env_log(1, 'Checking Git client ...')
        self.check_list += [self.git_client_exists()]

        self.env_log(1, 'Checking the presence of program files and folders ...')
        self.check_list += [self.folders_exists()]

        for check in self.check_list:
            if check is False:
                self.env_log(4, 'Environment check failed, quitting program.')
                if terminate:
                    sys.exit(1)
                else:
                    return False
        self.env_log(1, 'All files and folders are existing')
        return True

    def create_folders_or_files(self):
        if self.create_folders:
            for folder in self.create_folders:
                pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        if self.create_files:
            for file in self.create_files:
                pathlib.Path(file).touch(exist_ok=True)

    def folders_exists(self) -> bool:
        all_files_folders = self.c_paths_mod.__dict__

        for x in self.ignore_temp_files:
            del all_files_folders[x]

        for x in all_files_folders.keys():
            exists = self.c_path_utils.file_or_folder_exists(all_files_folders[x])
            if not exists:
                self.env_log(4, f'Can not find "{all_files_folders[x]}"')
                return False
        return True

    def git_client_exists(self) -> bool:
        str_to_cmp: str = 'git version'
        git_cmd: list[str] = ['git', '--version']
        console_out: str = subprocess.check_output(git_cmd, text=True)

        if console_out.startswith(str_to_cmp):
            return True
        self.env_log(4, 'Git client does not exist. Please check if Git is proper installed.')
        return False

    def env_log(self, level: int, message: str) -> str:
        if not self.disable_logging:
            # Separate logging, because the logging module want's to create a file inside
            # the log folder, that maybe don't exist yet.
            levels = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
            if level > 2:
                stream = sys.stderr
            else:
                stream = sys.stdout
            print(f'{datetime.now()} [{levels[level]}]: Environment Check: {message}', file=stream)
