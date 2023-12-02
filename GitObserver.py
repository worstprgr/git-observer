#!/bin/env python
import datetime
import subprocess

import core.paths as cpaths
import core.utils as cutils
from core.transport import Commit
from core.transport import Observation

# Init utils
FileUtils = cutils.FileUtils()


class GitObserver:
    known_hashes: list[str] = []

    def __init__(self, config):
        # May encapsulate config in exclusive var
        self.origin = config.origin
        self.filepath = config.filepath
        self.logfolders = config.logfolders
        self.ignore = config.ignore
        self.descending = config.descending
        self.since: str = '1 week ago'
        self.git_fetch = [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'fetch',
            '--all'
        ]

        # Paths
        self.gitlog_dummy_file: str = cpaths.GITLOG_DUMMY

        # Git relevant
        self.filepath = config.filepath
        self.logfolders = config.logfolders
        self.ignore = config.ignore
        self.origin = config.origin
        self.since: str = '1 week ago'
        self.git_fetch: list = [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'fetch',
            '--all'
        ]

    def get_git_log_cmd(self, path: str) -> list[str]:
        sort_flag = '--date-order'
        if self.descending:
            sort_flag = '--reverse'
        return [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'log',
            f'--since={self.since}',
            "--pretty=format:%cn|%cI|%s|%h|%D",
            '--all',
            sort_flag,
            f'{self.filepath}/{path}'
        ]

    def run(self, test: bool = False) -> list[Observation]:
        observations: list[Observation] = []
        subprocess.run(self.git_fetch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for path in self.logfolders:
            response = self.get_log_response(path, test)
            messages = self.handle_log_response(response)
            observations.append(Observation(path, messages))
        return observations

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

    def handle_log_response(self, response: str) -> list[Commit]:
        messages = self.collect_commit_messages(response)

        if len(messages) == 0:
            return []

        self.log_message(">>>")
        self.log_message("Found changes:")
        for cmt in messages:
            print(f"{cmt.author} ({cmt.date}): {cmt.message}\n" +
                  f"{cmt.branch}" +
                  f"{self.origin}{cmt.sha1}\n")
        return messages

    def collect_commit_messages(self, response) -> list[Commit]:
        lines = response.split("\n")
        messages = []
        for line in lines:
            lineinfo = line.split('|')

            author = lineinfo[0]
            date = datetime.datetime.fromisoformat(lineinfo[1])
            message = lineinfo[2]
            commit_hash = lineinfo[3]
            branch = ''
            if lineinfo[4]:
                branch = lineinfo[4] + "\n"

            if commit_hash in self.known_hashes:
                continue
            self.known_hashes.append(commit_hash)

            if self.ignore_author(author):
                continue
            cmt = Commit(author, date, message, commit_hash, branch)
            messages.append(cmt)

        if len(messages) > 0:
            messages.reverse()
        return messages

    def ignore_author(self, author: str) -> bool:
        if self.ignore is None:
            return False

        for author_ignore in self.ignore:
            if author == author_ignore:
                return True
        return False

    def get_git_show_cmd(self, sha1: str) -> list[str]:
        """
        Builds a list of arguments passed to subprocess,
        that represent a call of git show on configured directory
        using specific SHA1 identifier
        :param sha1: SHA1
        :return: git show arguments
        """
        return [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'show',
            '--pretty=medium',
            '-s',
            sha1
        ]

    def get_git_show(self, sha1: str) -> str:
        """
        Returns single commit identified by param SHA1
        using git command line
        :param sha1: SHA1
        :return: git show result
        """
        git_show_cmd = self.get_git_show_cmd(sha1)
        # Should be a utility for external calls instead of redundant
        response = subprocess.run(git_show_cmd, stdout=subprocess.PIPE)
        return response.stdout.decode("utf-8")

    @staticmethod
    def log_message(message: str):
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} - {message}")
