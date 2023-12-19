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

    def __call__(self, eventargs: Any):
        for handler in self.eventhandler:
            handler(eventargs)
