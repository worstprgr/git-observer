#!/usr/bin/env python
from tkinter import Button, NONE, BOTH, DISABLED, VERTICAL, Text, Scrollbar, Frame, Tk, Toplevel
from tkinter.constants import RIGHT, Y
import pathlib
import os


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


class TkUtils:

    @staticmethod
    def calculate_width(root: Tk, width_percent: float) -> int:
        """
        Calculates a percentual part of screen width.
        Uses root Tk to get access to window screen width
        :param root: root Tk for determination of screen width
        :param width_percent: percentual factor
        :return: int representing calculated width
        """
        return int(root.winfo_screenwidth() * width_percent)

    @staticmethod
    def calculate_height(root: Tk, height_percent: float) -> int:
        """
        Calculates a percentual part of screen height.
        Uses root Tk to get access to window screen height
        :param root: root Tk for determination of screen height
        :param height_percent: percentual factor
        :return: int representing calculated height
        """
        return int(root.winfo_screenheight() * height_percent)

    @staticmethod
    def calculate_form_geometry(root: Tk, width_percent: float, height_percent: float) -> str:
        """
        Calculates width and height based on given percentual factor and returns a
        string representing a geometry with dimensions at center point of screen
        :param root: Tk that provides info about screen
        :param width_percent: Percentual width
        :param height_percent: Percentual height
        :return:
        """
        width = TkUtils.calculate_width(root, width_percent=width_percent)
        height = TkUtils.calculate_height(root, height_percent=height_percent)

        # get screen width and height
        # This may get too big on 4K later
        width_screen = root.winfo_screenwidth()
        height_screen = root.winfo_screenheight()

        # calculate position to start from
        x = (width_screen / 2) - (width / 2)
        y = (height_screen / 2) - (height / 2)

        # TODO: currently not respecting roots screen, it reproducible opens on primary screen
        # print(f"{root.winfo_screen()}: {int(root.winfo_x())}x{int(root.winfo_y())}
        # +{int(root.winfo_screenwidth ())}+{int(root.winfo_screenheight())}")

        # return calculations to root in order to get right geometry and pos
        return f"{int(width)}x{int(height)}+{int(x)}+{int(y)}"

    @staticmethod
    def show_dialog(root: Tk, message_text: str):
        """
        Creates a Toplevel window based on given Tk root that shows
        passed message and a button "OK" to close dialog again
        :param root: Tk root
        :param message_text: message to be shown
        :return: None
        """
        dialog = Toplevel(root)
        dialog.resizable(width=False, height=False)
        geo_loc = TkUtils.calculate_form_geometry(root, 0.35, 0.2)
        dialog.geometry(geo_loc)

        default_bg = root.cget('bg')
        message_root = Frame(dialog, bg=default_bg)
        scroll_y = Scrollbar(message_root, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        message = Text(master=message_root, bg=default_bg, height=10, yscrollcommand=scroll_y.set)
        message.insert(index=1.0, chars=message_text)
        message.config(state=DISABLED, highlightthickness=0, borderwidth=0)
        message_root.pack(fill=BOTH, expand=True, padx=10, pady=5)
        message.pack(anchor='nw', expand=True, fill=BOTH)

        btn_close = Button(master=dialog, width=8, text='OK', command=dialog.destroy)
        btn_close.pack(anchor='s', padx=12, pady=5, fill=NONE)
