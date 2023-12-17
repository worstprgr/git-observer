#!/usr/bin/env python 
"""
This tool checks, if a Git author, and it's email address matches
with the white listed entry.

Note: This isn't an OpSec tool, it's intended as an additional quality gate.
"""
import pathlib
import subprocess
import sys
import argparse


class GitLog:
    def __init__(self):
        self.author_email: str = str

        # Checking only the latest commit
        self.git_command: list = ['git', 'log', '-1', '--pretty=format:%an %ae']

    def get_author_email(self) -> None:
        # No error handling intended, because when it crashes, it crashes ¯\_(ツ)_/¯
        # Or in other words: If Git isn't reachable, this script should terminate here anyway
        git_response: str = subprocess.check_output(self.git_command, stderr=subprocess.STDOUT, text=True)

        self.author_email: str = git_response.strip().lower()


class FetchWhitelist:
    def __init__(self, wl_path: pathlib.Path):
        self.whitelist_file: pathlib.Path = wl_path
        self.author_email: list = []
        self.ignore_symbol: str = '#'

    def open_parse_whitelist(self) -> None:
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
        if path: self.whitelist_file = self.conv_path(path)

    @staticmethod
    def conv_path(path: str) -> pathlib.Path:
        if type(path) == str: return pathlib.Path(path)
        return path


class ArgHandler:
    def __init__(self):
        # Parser
        self.path_help = 'A custom path to the whitelist file.'
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-p', '--path', action='store')

        # Args
        self.args = self.parser.parse_args()
        self.custom_path = self.args.path


class Main:
    def __init__(self, whitelist_path):
        # Init
        self.fw = FetchWhitelist(whitelist_path)
        self.gl = GitLog()
        self.error: bool = True

    def run_check(self):
        # Run actions
        self.fw.open_parse_whitelist()
        self.gl.get_author_email()

        # Data to compare
        git_log_author_email: str = self.gl.author_email
        whitelist_author_email: list[str] = self.fw.author_email

        # Compare author and email address
        self.cmp(git_log_author_email, whitelist_author_email)

        if not self.error:
            print('[OK]: Author & E-Mail address is matching with whitelist')

    def cmp(self, from_git: str, from_whitelist: list) -> None or Exception:
        if not (from_git in from_whitelist):
            print(f'[ERROR]: "{from_git}" not found in whitelist', file=sys.stderr)
            sys.exit(1)
        self.error = False


if __name__ == '__main__':
    ap = ArgHandler()
    p = FilePaths(ap.custom_path)
    m = Main(p.whitelist_file)
    m.run_check()
