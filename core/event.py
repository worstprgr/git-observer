from typing import Any, Callable


class Event:
    """
    Event like object to contribute information to a
    subscribers list
    """

    __eventhandler: list[Callable[[Any], None]] = []
    """
    INTERNAL
    List of subscribed handler fulfilling the required Callable signature
    """

    def __iadd__(self, handler: Callable[[Any], None]):
        self.__eventhandler.append(handler)
        return self

    def __isub__(self, handler: Callable):
        self.__eventhandler.remove(handler)
        return self

    def __call__(self, eventargs: Any):
        for eventhandler in self.__eventhandler:
            eventhandler(eventargs)
