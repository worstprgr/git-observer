from tkinter import Button, NONE, BOTH, DISABLED, VERTICAL, Text, Scrollbar, Frame, Tk, Toplevel
from tkinter.constants import RIGHT, Y
from core.logger import Logger


class ToplevelModal(Toplevel):
    """
    A Toplevel that disables given parent and
    only resumes parent activity when closed
    """

    def __init__(self, root: Tk):
        """
        Initializes a new modal instance of this
        class inherited from Toplevel
        :param root: root Tk
        """
        self.logger = Logger(__name__).log_init
        # Please note: this is to have a standalone form beside root (I guess)
        super().__init__(None)
        self.root = root
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.resizable(width=False, height=False)
        geo_loc = TkUtil.calculate_form_geometry(root, 0.35, 0.2)
        self.geometry(geo_loc)
        self.wait_visibility()
        self.grab_set()

    def close(self):
        """
        Closes this instance by calling destroy and releases
        root for resuming its activity
        :return:
        """
        self.destroy()
        self.root.deiconify()


class TkUtil:

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
        width = TkUtil.calculate_width(root, width_percent=width_percent)
        height = TkUtil.calculate_height(root, height_percent=height_percent)

        root_maximized = bool(('-zoomed' in root.attributes() and root.attributes('-zoomed'))
                              or (root.wm_state() == 'zoomed'))
        # get screen width and height
        if root_maximized:
            # When in full screen we can tell that geo of root is related to selected monitor
            width_screen = root.winfo_x() + root.winfo_width()
            height_screen = root.winfo_y() + root.winfo_height()
        else:
            # This may work or may not (always primary screen)
            width_screen = root.winfo_screenwidth()
            height_screen = root.winfo_screenheight()
        return TkUtil.__calculate_geometry__(width_screen, height_screen, width, height)

    @staticmethod
    def __calculate_geometry__(screen_w: int, screen_h: int, form_w: int, form_h) -> str:
        # calculate position to start from
        x = (screen_w / 2) - (form_w / 2)
        y = (screen_h / 2) - (form_h / 2)

        # TODO: currently not respecting roots screen, it reproducible opens on primary screen
        # print(f"{root.winfo_screen()}: {int(root.winfo_x())}x{int(root.winfo_y())}
        # +{int(root.winfo_screenwidth ())}+{int(root.winfo_screenheight())}")

        # return calculations to root in order to get right geometry and pos
        return f"{int(form_w)}x{int(form_h)}+{int(x)}+{int(y)}"

    @staticmethod
    def show_message_dialog(root: Tk, message_text: str):
        """
        Creates a Toplevel window based on given Tk root that shows
        passed message and a button "OK" to close dialog again
        :param root: Tk root
        :param message_text: message to be shown
        :return: None
        """
        dialog = ToplevelModal(root)
        default_bg = root.cget('bg')
        message_root = Frame(dialog, bg=default_bg)
        scroll_y = Scrollbar(message_root, orient=VERTICAL)
        scroll_y.pack(side=RIGHT, fill=Y)

        message = Text(master=message_root, bg=default_bg, height=10, yscrollcommand=scroll_y.set)
        message.insert(index=1.0, chars=message_text)
        message.config(state=DISABLED, highlightthickness=0, borderwidth=0)
        message_root.pack(fill=BOTH, expand=True, padx=10, pady=5)
        message.pack(anchor='nw', expand=True, fill=BOTH)

        btn_close = Button(master=dialog, width=8, text='OK', command=dialog.close)
        btn_close.pack(anchor='s', padx=12, pady=5, fill=NONE)
