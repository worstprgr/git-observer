#!/usr/bin/env python 


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
