# Transport objects for representing commit per folder
from datetime import datetime


class Commit:
    """
    Representation of one single commit
    at time point with given author and title
    """
    author: str
    date: datetime
    message: str
    sha1: str
    branch: str

    def __init__(self, author: str, date: datetime, message: str, commit_hash: str = None, branch: str = None):
        """
        Instantiates a new instance of Commit
        :param author: committer name
        :param date: time stamp
        :param message: summary text
        :param commit_hash: generated link using commit hash and argument 'origin'
        :param branch: branch name, if given
        """
        self.author = author
        self.date = date
        self.message = message
        self.sha1 = commit_hash
        self.branch = branch


class Observation:
    """
    Representation of one observation topic (e.g. given folder name) and
    associated commits
    """
    name: str
    commits: list[Commit]

    def __init__(self, name: str, observation_commits: list[Commit]):
        """
        Instantiates a new instance of Observation
        :param name: associated topic
        :param observation_commits: associated commits
        """
        self.name = name
        self.commits = observation_commits
