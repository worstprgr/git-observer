#!/usr/bin/env python
import argparse
import os
import pathlib


class UTUtils:
    @staticmethod
    def lazy_path_obj(fp: str | pathlib.Path) -> pathlib.Path:
        """
        Converting a string to a path-like object.
        :param fp: Filepath as string or path-like object.
        :return: The path as path-like object.
        """
        if type(fp) is str:
            fp = pathlib.Path(fp)
        return fp

    def create_file(self, fp: str | pathlib.Path) -> None:
        file: pathlib.Path = self.lazy_path_obj(fp)
        file.touch()
        print('Created:', file)

    def delete_file(self, fp: str | pathlib.Path) -> None:
        file: pathlib.Path = self.lazy_path_obj(fp)
        os.remove(file)
        print('Removed:', file)

    def file_exists(self, fp: str | pathlib.Path) -> bool:
        file: pathlib.Path = self.lazy_path_obj(fp)
        file_exists: bool = os.path.exists(file)
        if file_exists:
            return True
        return False

    @staticmethod
    def cmp_types(obj: any, check_type: type) -> bool:
        if type(obj) is check_type:
            return True
        return False

    def if_all_lines_begin_with(self, fp: str | pathlib.Path = None, namespace: argparse.Namespace = None,
                                keywords: list | dict = None) -> bool:
        """
        Checks if items in the text file are existing.
        Note: It only checks, if the line begins with the desired keyword.

        Using the param `namespace`, the `keyword` lists gets truncated by one item (keywords[1:]),
        since theres no "[Default]" decorator in a namespace.

        :param fp: Filepath as string or path-like-object.
        :param namespace: Namespace from argparse.
        :param keywords: Keywords to check against as a list. If dict is provided, it converts the keys to a list.
        :return: True, if every keyword exists. False, if one or more keywords are missing.
        """
        if type(keywords) is dict:
            keywords: dict
            keywords: list = [_key for _key in keywords.keys()]

        _content: list = []

        if fp and not namespace:
            file: pathlib.Path = self.lazy_path_obj(fp)
            with open(file, 'r', encoding='utf8') as f:
                content = f.readlines()

            # remove empty lines and strip newlines
            for x in content:
                if x != '\n':
                    _content.append(x.strip())
        elif namespace and not fp:
            for key in namespace.__dict__:
                _content.append(key)
        else:
            raise TypeError('No filepath or namespace provided.')

        # check, if a line begins with the current keyword
        for index, x in enumerate(_content):
            if not x.startswith(keywords[index]):
                return False
        return True


class DummyNamespace:
    """
    Generic namespace container for a dictionary.
    """
    def __init__(self, data):
        self.__dict__.update(data)
