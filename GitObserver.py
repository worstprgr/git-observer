#!/bin/env python
import datetime
import time
import subprocess
import argparse
from time import gmtime, strftime

import core.paths as cpaths
import core.utils as cutils


# Init utils
FileUtils = cutils.FileUtils()


class Commit:
    author: str
    date: datetime
    message: str
    hash: str
    branch: str


global known_hashes
global ignore_counter
known_hashes = []


class GitObserver:
    def __init__(self):
        # Argparse: Parser
        self.parser = argparse.ArgumentParser(allow_abbrev=True)
        self.parser.add_argument('-o', '--origin', metavar='origin', help='Origin path to build commit link for output')
        self.parser.add_argument('-f', '--filepath', action='store')
        self.parser.add_argument('-lf', '--logfolders', metavar='Path', type=str, nargs='+',
                                 help='a path to be observed')
        self.parser.add_argument('-ig', '--ignore', metavar='Author', type=str, nargs='+',
                                 help='Author name to be ignored')
        # Argparse: Args
        self.args = self.parser.parse_args()

        # Paths
        self.gitlog_dummy_file: str = cpaths.GITLOG_DUMMY

        # Git relevant
        self.filepath = self.args.filepath
        self.logfolders = self.args.logfolders
        self.ignore = self.args.ignore
        self.origin = self.args.origin
        self.since: str = '1 week ago'
        self.git_fetch: list = [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'fetch',
            '--all'
        ]
        subprocess.run(self.git_fetch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # DEBUG print('Command:', self.git_command)

    def get_git_log_cmd(self, path: str) -> list:
        return [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'log',
            f'--since={self.since}',
            "--pretty=format:%cn|%cI|%s|%h|%D",
            '--all',
            '--date-order',
            f'{self.filepath}/{path}'
        ]

    def run(self, test: bool = False) -> str:
        for path in self.logfolders:
            response = self.get_log_response(path, test)
            self.handle_log_response(response)

    def get_log_response(self, path: str, test: bool = False) -> str:
        """
        Returns the Git log as a string.
        If the test param is true, it returns the content of a .txt file instead,
        that represents a mockup of a gitlog.

        :param path: Git-Paths from a repo.
        :param test: (Optional) True -> Returns a dummy git log. False (Default) -> Returns a real git log.
        :return: The whole Git log as string.
        """
        if not test:
            response = subprocess.run(self.get_git_log_cmd(path), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            return response.stdout.decode("utf-8")
        else:
            # Task @ adam: Fill the static/gitlog-dummy.txt with data (anonymize it before committing)
            return FileUtils.simple_fopen(self.gitlog_dummy_file)

    def handle_log_response(self, response: str):
        messages = self.collect_commit_messages(response)

        if len(messages) == 0:
            return

        self.log_message(">>>")
        self.log_message("Found changes:")
        for cmt in messages:
            print(f"{cmt.author} ({cmt.date}): {cmt.message}\n" +
                  f"{cmt.branch}" +
                  f"{self.origin}{cmt.hash}\n")

    def collect_commit_messages(self, response):
        global known_hashes, ignore_counter
        ignore_counter = 0
        lines = response.split("\n")
        messages = []
        for line in lines:
            lineinfo = line.split('|')

            cmt = Commit()
            cmt.author = lineinfo[0]
            cmt.date = datetime.datetime.fromisoformat(lineinfo[1])
            cmt.message = lineinfo[2]
            cmt.hash = lineinfo[3]
            cmt.branch = ''
            if lineinfo[4]:
                cmt.branch = lineinfo[4] + "\n"

            if cmt.hash in known_hashes:
                continue
            known_hashes.append(cmt.hash)

            if self.ignore_author(cmt.author):
                continue
            messages.append(cmt)

        if len(messages) > 0:
            messages.reverse()
        return messages

    def ignore_author(self, author: str) -> bool:
        for author_ignore in self.ignore:
            if author == author_ignore:
                return 1
        return 0

    @staticmethod
    def log_message(message: str):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} - {message}")
