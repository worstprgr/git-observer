# Transport objects for representing commit per folder
from datetime import datetime
from typing import Callable

from core.event import Event


class Commit:
    """
    Representation of one single commit
    at time point with given author and title
    """
    origin: str
    author: str
    date: datetime
    message: str
    sha1: str
    branch: str

    def __init__(self, author: str, date: datetime, message: str,
                 commit_hash: str = None, branch: str = None, origin: str = None):
        """
        Instantiates a new instance of Commit
        :param author: committer name
        :param date: time stamp
        :param message: summary text
        :param commit_hash: generated link using commit hash and argument 'origin'
        :param branch: branch name, if given
        """
        self.origin = origin
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


class ObservationEventArgs:
    """
    Event handler arguments to
    hold a datetime giving information how old given data is
    and list of Observation representing loaded data
    """
    observations: list[Observation]
    """
    Observations represented by current event
    """

    update_time: datetime
    """
    Time point, when event occurred
    """

    def __init__(self, load_result: list[Observation]):
        """
        Initializes a new instance of event handler args.
        The timestamp will be time point of initialisation
        """
        self.update_time = datetime.now()
        self.observations = load_result


class ObservationEvent(Event):
    """
    Event like object to contribute a list of Observation
    to subscribers interested in them
    """

    __eventhandler: list[Callable[[ObservationEventArgs], None]] = []
    """
    INTERNAL
    Overridden list of subscribed handler fulfilling the required Callable signature
    """

    def raise_observation_event(self, target_observations: list[Observation]) -> None:
        """
        Public function to raise event with given transport data
        :return: None
        """
        eventargs = ObservationEventArgs(target_observations)
        self.__call__(eventargs)


class ObservationUtil:
    @staticmethod
    def is_empty(observations: list[Observation]):
        """
        Checks if given list of Observation is
        either null or empty. Empty is defined by
        all nested lists of Commit are empty as well
        :param observations:
        :return:
        """
        if observations is None or len(observations) == 0:
            return True

        for folder in observations:
            if observations is None:
                continue
            if len(folder.commits) > 0:
                return False
        return True

    @staticmethod
    def parse_commit_formatted(commit_msg: str, origin: str = None) -> Commit | None:
        """
        Parses one commit line given by git log
        to transport data object Commit
        :param commit_msg: one string that represents one commit in pre-defined format (see init)
        :param origin: optional parameter that describes origin
        :return: Newly created instance of Commit representing the commit
        """
        if not commit_msg:
            return

        lineinfo = commit_msg.split('|')
        if lineinfo is None or len(lineinfo) < 4:
            raise ValueError('Expected format "author|date|message|SHA1|[branch]"')

        author = lineinfo[0]
        date = datetime.fromisoformat(lineinfo[1])
        message = lineinfo[2]
        commit_hash = lineinfo[3]
        branch = ''
        if lineinfo[4]:
            branch = lineinfo[4]
        return Commit(author, date, message, commit_hash, branch, origin)
