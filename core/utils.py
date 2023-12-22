#!/usr/bin/env python
import math
import pathlib
import os
from collections import namedtuple
from signal import signal, Signals
from typing import Callable

from core.event import Event


class FileUtils:
    @staticmethod
    def simple_fopen(fp: str, read_mode: int = 0) -> str or list:
        """
        Opens a file as read only and with utf8 encoding.

        If `read_mode` is 0 - it returns the whole file as a string (Default).
        If `read_mode` is 1 - it returns every newline as an item in a list.

        :param fp: The file path.
        :param read_mode: 0 or 1.
        :exception: UserWarning, if read_mode contains an illegal integer.
        :return: String or list, depends on read mode.
        """
        with open(fp, 'r', encoding='utf8') as f:
            if read_mode == 0:
                file = f.read()
            elif read_mode == 1:
                file = f.readlines()
            else:
                raise UserWarning(f'Method: simple_fopen - Read Mode {read_mode} does not exist.')
        return file


class PathUtils:
    @staticmethod
    def get_base_dir() -> str:
        """
        Finds the root folder of the project, using the `root.init` as an anchor.
        :return: The root path, as a string.
        """
        root_init = "root.init"
        max_search_depth = 5
        current_dir = os.getcwd()

        for x in range(max_search_depth):
            if root_init in os.listdir(current_dir):
                return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir
        raise RuntimeError("Root directory not found within the specified search depth")

    @staticmethod
    def conv_to_path_object(fp: str) -> pathlib.Path:
        return pathlib.Path(fp)


class TypeUtil:
    """
    Utilities to handle several types
    """

    @staticmethod
    def parse_value(value: str, default_val):
        """
        Basically a string parser converting a string value
        to list, bool, int or string
        :param value: Input value that needs to be converted to Type of default_val
        :param default_val: default_val as template fpr output value
        :return: Any
        """
        if type(default_val) is list:
            return [item.strip() for item in value.split(',')]
        if type(default_val) is bool:
            return bool(value)
        if type(default_val) is int:
            return int(value)
        return value


class TimeUtil:
    """
    Helper class that implements functionalities
    in special cases required when working with time and date
    """

    @staticmethod
    def calculate_countdown(interval_ms: float, current_ms: float) -> namedtuple:
        """
        Calculates the difference of an interval based on its length and how
        much time is done currently, both in unit milliseconds.
        :param interval_ms: Total length of interval
        :param current_ms: Current ran milliseconds since interval start
        :return: namedtuple representing minutes, seconds and milliseconds left, until interval end is reached
        """
        result = namedtuple("int", "min, second, millisecond")

        # Calculate from millisecond to second
        delta_s = (interval_ms - current_ms) / 1000.0
        # Determine minute amount and rest representing seconds
        min_left, seconds_left = divmod(delta_s, 60.0)
        result.min = math.trunc(min_left)

        # Calculate rest seconds back to millisecond
        mod_ms = seconds_left * 1000.0

        # determine seconds and the rest representing milliseconds
        seconds_left, ms_left = divmod(mod_ms, 1000.0)
        result.second = math.trunc(seconds_left)
        result.millisecond = math.trunc(ms_left)
        return result


class SignalEvent(Event):
    """
    Event like object to contribute a received Signal
    """

    def __init__(self):
        super().__init__()
        self.eventhandler: list[Callable[[], None]] = []


class SignalReceiver:
    """
    If a 'signal interrupt' or a 'signal termination' is received,
    the variable 'term_status' changes its state.

    The variable is used to change the condition of the while-loop
    inside the main.py
    """

    OnTerminate: SignalEvent = SignalEvent()

    def __init__(self):
        signal(Signals.SIGINT, self.__terminate)
        signal(Signals.SIGTERM, self.__terminate)
        signal(Signals.SIGILL, self.__terminate)

    def __terminate(self, *args) -> None:
        self.OnTerminate()
