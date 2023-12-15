#!/usr/bin/env python
"""
Since the discovery mode of the module `unittest` doesn't look deeper in
the project structure, this script kinda solves it.

Features:
    - Ignore folders, based on your .gitignore file
    - Ignore folders, based on your custom needs
"""
import subprocess
import os
import pathlib
import typing


class RunTests:
    def __init__(self):
        self.search_pattern: str = 'tests'
        self.root_dir: str = '.'
        self.root_dir_content: list = next(os.walk('.'))[1]
        self.git_ignore_file: str = self._conv_to_path('.gitignore')

        # Add more folders to ignore, that aren't in your .gitignore
        self.ignored_folders: list = ['.git', '.github']
        self.allowed_folders: list = []
        self.all_test_folders: list = []
        self.unit_test_cmd: list = lambda a: ['python', '-m', 'unittest', 'discover', '-s', a]

    def main(self, debug: bool = False) -> None:
        """
        Calls all needed methods, to execute found unit tests.
        :param debug: If true, it won't execute any UTs. Instead, it displays all found directories.
        :return: None
        """
        print('Gathering Unit Test Folders')
        self.load_git_ignore_folders()
        self.get_allowed_folders()
        self.walk_allowed_folders()

        if not debug:
            print('Running All Unit Tests')
            self.run_tests()
        else:
            print(self.all_test_folders)

    def load_git_ignore_folders(self):
        """
        Load the .gitignore file and extract all folder-names.
        :return: None
        """
        with open(self.git_ignore_file, 'r', encoding='utf8') as f:
            git_ignore_content = f.readlines()

        for x in git_ignore_content:
            if x.startswith('/'):
                self.ignored_folders.append(x.strip().strip('/'))

    def get_allowed_folders(self):
        """
        Compares the folders inside the root directory, with the ignored folders.
        :return: None
        """
        for x in self.root_dir_content:
            if x not in self.ignored_folders:
                self.allowed_folders.append(x)

    def walk_allowed_folders(self):
        """
        Searches for folders, that are named like in `search_pattern`.
        :return: None
        """
        def find_test_folders(folder: typing.Iterator) -> None:
            root: str
            for root, _, _ in folder:
                if root.endswith(self.search_pattern):
                    self.all_test_folders.append(self._conv_to_path(root))

        for x in self.allowed_folders:
            find_test_folders(os.walk(x))

    def run_tests(self):
        x: pathlib.Path
        for x in self.all_test_folders:
            subprocess.run(self.unit_test_cmd(str(x)))

    @staticmethod
    def _conv_to_path(fp: str) -> pathlib.Path:
        return pathlib.Path(fp)


if __name__ == '__main__':
    rt = RunTests()
    rt.main()
