#!/usr/bin/env python
import pathlib

import core.unittestutils

ut_utils = core.unittestutils.UTUtils()


class UtilsFactory:
    @staticmethod
    def create_bunny_file(fp: str | pathlib.Path):
        bunny = r"""
               ((`\
            ___ \\ '--._
         .'`   `'    o  )
        /    \   '. __.'
       _|    /_  \ \_\_
jgs   {_\______\-'\__\_\
"""
        file = ut_utils.lazy_path_obj(fp)

        with open(file, 'w+', encoding='utf8') as f:
            f.write(bunny)
