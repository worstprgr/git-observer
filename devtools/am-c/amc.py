#!/usr/bin/env python
"""
This tool compares the Git author and e-mail address of the latest commit, against a custom white list.

If it found a match, it prints a success message to stdout.
Else, it prints an error message to stderr and terminates with an exit code 1.

This tool isn't meant for OpSec, only for an additional quality gate.

Copyright (C) 2023  worstprgr <adam@seishin.io> GPG Key: key.seishin.io

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import pathlib
import subprocess
import sys
import argparse
import os


class GitLog:
    def __init__(self):
        self.author_email: str = str

        # Checking only the latest commit
        self.git_command: list = ['git', 'log', '-1', '--pretty=format:%an %ae']

    def get_author_email(self) -> None:
        try:
            git_response: str = subprocess.check_output(self.git_command, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError:
            print('[ERROR]: No Git installed or no Git repository available')
            sys.exit(1)

        self.author_email: str = git_response.strip().lower()


class FetchSecretEnvVariable:
    def __init__(self):
        self.whitelist_env: str = 'WHITELIST_AMC'

    def get_env(self) -> list[str]:
        env: str = os.environ.get(self.whitelist_env)
        if env is None or env == '':
            print('Secret environment variable not found')
            sys.exit(1)
        else:
            env: list = env.strip().split('\n')
            return env


class FetchWhitelist(FetchSecretEnvVariable):
    def __init__(self, wl_path: pathlib.Path, secret_env: bool):
        super().__init__()
        self.whitelist_file: pathlib.Path = wl_path
        self.author_email: list = []
        self.ignore_symbol: str = '#'
        self.secret_env = secret_env

    def fetch(self):
        if self.secret_env:
            self.parse_whitelist_env()
        else:
            self.parse_whitelist_file()

    def parse_whitelist_env(self) -> None:
        self.author_email += self.get_env()

    def parse_whitelist_file(self) -> None:
        try:
            with open(self.whitelist_file, 'r', encoding='utf8') as f:
                whitelist: list = f.readlines()
        except FileNotFoundError:
            print(f'[ERROR]: Can not find "{self.whitelist_file}"', file=sys.stderr)
            sys.exit(1)

        item: str

        for item in whitelist:
            if item.startswith('\n') or item.startswith(' ') or item.startswith(self.ignore_symbol):
                continue
            user_pair = item.strip().lower()
            self.author_email.append(user_pair)


class FilePaths:
    def __init__(self, path: str = None):
        self.whitelist_file: pathlib.Path = self.conv_path('whitelist.amc')
        if path:
            self.whitelist_file = self.conv_path(path)

    @staticmethod
    def conv_path(path: str) -> pathlib.Path:
        if type(path) is str:
            return pathlib.Path(path)
        return path


class ArgHandler:
    def __init__(self):
        # Parser
        self.path_help = 'A custom path to the whitelist file. Usage: -p <Your Path>'
        self.secret_help = 'Enables the checking via a secret variable, setup in your CI pipeline ' \
                           '-> README.md for more information'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-p', '--path', action='store', help=self.path_help)
        self.parser.add_argument('-s', '--secret', action='store_true', help=self.secret_help)

        # Args
        self.args = self.parser.parse_args()
        self.custom_path = self.args.path
        self.secret = self.args.secret


class Main:
    def __init__(self, whitelist_path, secret_env: bool):
        # Init
        self.fw = FetchWhitelist(whitelist_path, secret_env)
        self.gl = GitLog()
        self.error: bool = True
        self.secret_mode: bool = secret_env

    def run_check(self):
        # Run actions
        self.fw.fetch()
        self.gl.get_author_email()

        # Data to compare
        git_log_author_email: str = self.gl.author_email
        whitelist_author_email: list[str] = self.fw.author_email

        # Compare author and email address
        self.cmp(git_log_author_email, whitelist_author_email)

        if not self.error:
            print('[OK]: Authors & E-Mail addresses are matching with whitelist')

    def cmp(self, from_git: str, from_whitelist: list) -> None or Exception:
        if not (from_git in from_whitelist):
            if self.secret_mode:
                print('[ERROR]: Author(s) and E-Mail addresses not found in whitelist', file=sys.stderr)
            else:
                print(f'[ERROR]: "{from_git}" not found in whitelist', file=sys.stderr)
            sys.exit(1)
        self.error = False


if __name__ == '__main__':
    ap = ArgHandler()
    p = FilePaths(ap.custom_path)
    m = Main(p.whitelist_file, ap.secret)
    m.run_check()
