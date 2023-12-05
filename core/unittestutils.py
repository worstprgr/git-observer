#!/usr/bin/env python
import os
import time
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

    def delete_file(self, fp: str | pathlib.Path) -> None:
        time.sleep(0.05)
        os.remove(self.lazy_path_obj(fp))
        print('Removed:', fp)

    def file_exists(self, fp: str | pathlib.Path) -> bool:
        file: pathlib.Path = self.lazy_path_obj(fp)
        file_exists: bool = os.path.exists(file)
        if file_exists:
            return True
        return False
