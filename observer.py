#!/bin/env python
import subprocess
from argparse import Namespace
from logging import INFO
from threading import Thread
from time import sleep
from typing import IO

import core.paths
from core.transport import Commit, ObservationUtil, ObservationEvent
from core.transport import Observation
from core.logger import Logger

c_paths = core.paths.Paths()


class GitObserver:
    """
    Controller to get access to git log messages including
    filtering for ignored authors and specific folders to observe
    """

    def __init__(self, config: Namespace, is_test_instance: bool = False):
        """
        Initializes a new instance of GitObserver controller class
        according to given configuration. May be started in testing mode by passing
        optional parameter is_test_instance
        :param config: Configuration provided by caller
        :param is_test_instance: [Optional] flag if test mode
        """
        self.logger = Logger(__name__).log_init
        self.is_test = is_test_instance
        self.known_hashes: list[str] = []

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
        self.gitlog_dummy_file: str = c_paths.GITLOG_DUMMY
        self.log_config()

    def log_config(self):
        """
        Logs the given configuration to current instance log
        :return: None
        """
        # Only log when it's not a test
        if self.is_test:
            return
        self.log_info(f'Origin: "{self.origin}"')
        self.log_info(f'Git root: "{self.filepath}"')
        self.log_info(f'Descending: {self.descending}')
        if self.logfolders and len(self.logfolders) > 0:
            self.log_info(f'Observed folders: {str.join(", ", self.logfolders)}')
        if self.ignore and len(self.ignore) > 0:
            self.log_info(f'Ignored authors: {str.join(", ", self.ignore)}')

    def get_git_log_cmd(self, path: str) -> list[str]:
        """
        Build tha log command according given folder
        which should get observed
        :param path: relative folder to receive log info for
        :return: argument list to be used when calling external git executable
        """
        sort_flag = '--date-order'
        if not self.descending:
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
            '--pretty=fuller',
            '-s',
            sha1
        ]

    def load_observations(self) -> list[Observation]:
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
                commit = ObservationUtil.parse_commit_formatted(commit_line, self.origin)
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

    def log_info(self, message: str):
        """
        Logs on INFO respecting the is_test flag where logging
        produces nasty and useless output
        :param message: message to log
        :return: None
        """
        if not self.is_test:
            self.logger.log(INFO, message)


class GitObserverThread(Thread, GitObserver):
    """
    Thread based GitObserver that loads commits every
    minute and notifies all subscribers over changes using ObservationEvent
    """

    OnLoaded: ObservationEvent
    """
    Public event that can be subscribed.
    Will be called each minute and contribute loaded new observations
    """
    __run_thread: bool
    """
    Signal flag to tell, if loop is active
    """

    def __init__(self, config: Namespace, is_test_instance: bool = False):
        """
        Creates a new instance of this class wrapping GitObserver based
        on Thread and calls init methods of those parents
        :return: None
        """
        self.__run_thread = True
        self.OnLoaded = ObservationEvent()
        Thread.__init__(self, target=self.__observation_loop, daemon=True)
        GitObserver.__init__(self, config, is_test_instance)

    def __observation_loop(self):
        """
        Internal loop based on timer.sleep.
        Ever 60th second, the observations are collected
        and published using Event functionality
        :return: None
        """
        current_second = 0
        while self.__run_thread:
            if current_second % 60 == 0:
                current_second = 0
                result = self.load_observations()
                self.OnLoaded(result)
            current_second += 1
            sleep(1)

    def stop_observation(self):
        self.logger.info("Shutting down thread")
        self.__run_thread = False
