#!/bin/env python
import datetime
import subprocess
from typing import IO

import core.paths as cpaths
import core.utils as cutils
from core.transport import Commit
from core.transport import Observation
from core.logger import Logger

# Init utils
FileUtils = cutils.FileUtils()


class GitObserver:
    """
    Controller to get access to git log messages including
    filtering for ignored authors and specific folders to observe
    """
    known_hashes: list[str] = []

    def __init__(self, config, is_test_instance: bool = False):
        """
        Initializes a new instance of GitObserver controller class
        according to given configuration. May be started in testing mode by passing
        optional parameter is_test_instance
        :param config: Configuration provided by caller
        :param is_test_instance: [Optional] flag if test mode
        """
        self.logger = Logger(__name__).log_init
        self.is_test = is_test_instance
        if is_test_instance:
            self.logger.info("Initialized for testing")

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
        self.log_config()

    def log_config(self):
        """
        Logs the given configuration to current instance log
        :return: None
        """
        self.logger.info(f'Origin: "{self.origin}"')
        self.logger.info(f'Git root: "{self.filepath}"')
        self.logger.info(f'Descending: {self.descending}')
        if self.logfolders and len(self.logfolders) > 0:
            self.logger.info(f'Observed folders: {str.join(", ", self.logfolders)}')
        if self.ignore and len(self.ignore) > 0:
            self.logger.info(f'Ignored authors: {str.join(", ", self.ignore)}')

    def get_git_log_cmd(self, path: str) -> list[str]:
        """
        Build tha log command according given folder
        which should get observed
        :param path: relative folder to receive log info for
        :return: argument list to be used when calling external git executable
        """
        sort_flag = '--date-order'
        if self.descending:
            sort_flag = '--reverse'
        return [
            'git',
            f'--git-dir={self.filepath}/.git/',
            f'--work-tree={self.filepath}',
            'log',
            f'--since="{self.since}"',
            '--pretty=format:"%cn|%cI|%s|%h|%D"',
            '--all',
            sort_flag,
            f'{self.filepath}/{path}'
        ]

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

    def run(self) -> list[Observation]:
        """
        Iterates over all configured observation folders
        and collect their (filtered) log info which then is returned
        :return: log info
        """
        observations: list[Observation] = []
        if not self.is_test:
            subprocess.run(self.git_fetch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for path in self.logfolders:
            messages = self.handle_observed_path(path)
            observations.append(Observation(path, messages))
        return observations

    def read_git_commits(self, path: str) -> list[Commit]:
        """
        Returns the Git log as a string.
        If the test param is true, it returns the content of a .txt file instead,
        that represents a mockup of a gitlog.

        :param path: Git-Paths from a repo.
        :return: The whole Git log as string.
        """
        git_log = []
        with self.get_git_log_bytes(path) as response_stream:
            while True:
                line = response_stream.readline()
                if not line:
                    break
                commit_line = line.decode("utf-8").rstrip()[1:-1]
                commit = self.parse_commit_formatted(commit_line)
                if commit:
                    git_log.append(commit)
        return git_log

    def get_git_log_bytes(self, path: str) -> IO:
        """
        Gets an IO stream of bytes representing the git log result.
        Is a common file stream reading from static dummy in test case.

        PLEASE NOTE: the stream has to be closed by caller
        :param path: observed folder
        :return: IO byte stream to read from
        """
        if not self.is_test:
            cmd = self.get_git_log_cmd(path)
            return subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
        return open(self.gitlog_dummy_file, mode='rb', buffering=-1, errors=None, closefd=True)

    @staticmethod
    def parse_commit_formatted(commit_msg: str) -> Commit | None:
        """
        Parses one commit line given by git log
        to transport data object Commit
        :param commit_msg: one string that represents one commit in pre-defined format (see init)
        :return: Newly created instance of Commit representing the commit
        """
        if not commit_msg:
            return

        lineinfo = commit_msg.split('|')
        author = lineinfo[0]
        date = datetime.datetime.fromisoformat(lineinfo[1])
        message = lineinfo[2]
        commit_hash = lineinfo[3]
        branch = ''
        if lineinfo[4]:
            branch = lineinfo[4] + "\n"
        return Commit(author, date, message, commit_hash, branch)

    def handle_observed_path(self, path: str) -> list[Commit]:
        """
        Handles one observed path by calling git log command
        corresponding to given path parameter
        :param path: observed path
        :return: list of parsed and filtered commits
        """
        response = self.read_git_commits(path)
        messages = self.filter_commit_result(response)
        if len(messages) == 0:
            return []

        self.logger.info("Found actual changes, will present now")
        for cmt in messages:
            print(f"{cmt.author} ({cmt.date}): {cmt.message}\n" +
                  f"{cmt.branch}" +
                  f"{self.origin}{cmt.sha1}\n")
        return messages

    def filter_commit_result(self, commits: list[Commit]) -> list[Commit]:
        """
        Filters parsed commit messages by configured criteria
        and removes already shown commits
        :param commits: list of parsed commits
        :return: filtered and sorted list
        """
        messages = []
        if len(commits) <= 0:
            return messages

        for commit in commits:
            if not commit:
                continue

            if commit.sha1 in self.known_hashes:
                continue
            self.known_hashes.append(commit.sha1)

            if self.ignore_author(commit.author):
                continue
            messages.append(commit)

        if len(messages) > 0:
            messages.reverse()
        return messages

    def ignore_author(self, author: str) -> bool:
        """
        Determines if the given author name is to be ignored.
        If no ignore list is given by config, all authors are relevant
        :param author: committer
        :return: TRUE if author needs to be ignored
        """
        if self.ignore is None:
            return False

        for author_ignore in self.ignore:
            if author == author_ignore:
                return True
        return False

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
