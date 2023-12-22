#!/usr/bin/env python
import argparse

from core.paths import Paths


c_paths = Paths()


class ManagementFactory:
    def __init__(self):
        self.config_defaults: dict = {
            'origin': 'https://github.com/worstprgr/git-observer/commit/',
            'filepath': c_paths.BASE_DIR,
            'logfolders': ['.'],
            'ignore': [],
            'show_viewer': False,
            'descending': False
        }

    @staticmethod
    def cmp_inp_vs_out(arg_parser: argparse.PARSER, test_parse: list[list], test_args: list,
                       available_args_cmp: list) -> bool:
        """
        Compares the provided arguments vs the output from argparse.

        :param arg_parser: The argument parser object.
        :param test_parse: A nested list, with [option, argument(s)].
        :param test_args: A static list, with test arguments to compare with.
        :param available_args_cmp: A list, with all available options.
        :return: True, if every output matches the input from `test_args`.
        """
        for index, t_args in enumerate(test_parse):
            namespace_result = arg_parser.parse_args(t_args).__dict__[available_args_cmp[index]]
            if not namespace_result == test_args[index]:
                return False
        return True

    @staticmethod
    def zip_options_with_args(test_args: list, available_args: list) -> list[list]:
        """
        Zips two lists together. In that case it combines options and arguments.

        :param test_args: A static list with test arguments.
        :param available_args: A list, with all available options (With hyphens prepended).
        :return: A nested list, with options and arguments combined.
        """
        tmp_list: list = []
        for index, x in enumerate(test_args):
            if type(x) is list:
                arg = [available_args[index]] + x
            elif x is True:
                arg = [available_args[index]]
            else:
                arg = [available_args[index], x]
            tmp_list.append(arg)
        return tmp_list
