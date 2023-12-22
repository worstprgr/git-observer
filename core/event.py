from datetime import datetime
from typing import Any, Callable


class Event(object):
    """
    Event like object to contribute information to a
    subscribers list
    """

    eventhandler: list[Callable]

    def __init__(self):
        self.eventhandler = []

    def __iadd__(self, handler: Callable[[Any], None]):
        self.eventhandler.append(handler)
        return self

    def __isub__(self, handler: Callable):
        self.eventhandler.remove(handler)
        return self

    def __call__(self, eventargs: Any = None):
        for handler in self.eventhandler:
            if eventargs:
                handler(eventargs)
            else:
                handler()


class StatusEventArgs:
    status: str
    status_date: datetime

    def __init__(self, status_message: str) -> None:
        self.status = status_message
        self.status_date = datetime.now()


class StatusEvent(Event):
    def __init__(self):
        super().__init__()
        self.eventhandler: list[Callable[[str], None]] = []

    def __call__(self, eventargs: Any = None):
        return super().__call__(StatusEventArgs(eventargs))
