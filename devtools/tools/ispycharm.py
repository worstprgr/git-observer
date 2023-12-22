#!/usr/bin/env python
import os


def is_pycharm_active():
    if 'PYCHARM_HOSTED' in os.environ:
        return True
    else:
        return False
