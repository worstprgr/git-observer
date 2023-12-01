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
import typing


class RunTests:
    def __init__(self):
        self.search_pattern: str = 'tests'
        self.root_dir: str = '.'
        self.root_dir_content: list = next(os.walk('.'))[1]
        self.git_ignore_file: str = '.gitignore'
        self.ignored_folders: list = ['.git', '.github']  # Add more folders to ignore, that aren't in your .gitignore
        self.allowed_folders: list = []
        self.all_test_folders: list = []
        self.unit_test_cmd: list = lambda a: ['python', '-m', 'unittest', 'discover', '-s', a]

    def main(self):
        print('Gathering Unit Test Folders')
        self.load_git_ignore_folders()
        self.get_allowed_folders()
        self.walk_allowed_folders()
        print('Running All Unit Tests')
        self.run_tests()

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
        def replace_backslash(string: str) -> str:
            return string.replace('\\', '/') if '\\' in string else string

        def find_test_folders(folder: typing.Iterator) -> None:
            root: str
            for root, _, _ in folder:
                if root.endswith(self.search_pattern):
                    self.all_test_folders.append(replace_backslash(root))

        for x in self.allowed_folders:
            find_test_folders(os.walk(x))

    def run_tests(self):
        for x in self.all_test_folders:
            subprocess.run(self.unit_test_cmd(x))


if __name__ == '__main__':
    rt = RunTests()
    rt.main()
