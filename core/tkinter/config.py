import typing
from argparse import Namespace
from tkinter import Tk, Label, Frame, W, EW, Widget, Button, RIGHT, LEFT
from typing import Any

from core.config.management import ConfigManager
from core.tkinter.util import ToplevelModal, Checkbox, Textbox


class ConfigWindow(ToplevelModal):

    def __init__(self, root: Tk, config: Namespace):
        super().__init__(root, width_percent=0.25, height_percent=0.2)
        self.config = config
        self.conf_handler = ConfigManager()
        self.edit_widgets: dict[str, Widget] = dict()
        self.edit_values = self.conf_handler.get_simplified_config()
        self.__build_grid__()

        options = Frame(master=self)
        self.cancel = Button(master=options, text='Cancel', command=self.destroy)
        self.cancel.pack(side=LEFT)
        self.accept = Button(master=options, text='Save', command=self.on_save)
        self.accept.pack(padx=5, side=LEFT)
        options.pack(side=RIGHT, pady=5, padx=1)

    def __build_grid__(self):
        """
        Dynamically builds a grid with current settings input and
        differs between boolean and texts
        """
        row_idx = 0
        main_frame = Frame(master=self)
        for setting in self.edit_values.keys():
            current_val = self.edit_values.get(setting)

            label = Label(master=main_frame, width=30, text=setting, anchor=W)
            label.grid(row=row_idx, column=0, sticky=EW)

            edit: Widget
            if type(current_val) is bool:
                edit = Checkbox(init_val=current_val, master=main_frame, anchor=W, padx=0)
            else:
                text_edit = Textbox(text=current_val, master=main_frame, width=70)
                edit = text_edit
            edit.grid(row=row_idx, column=1, sticky=EW, padx=0)

            self.edit_widgets[setting] = edit
            row_idx += 1

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.pack(padx=10, expand=True)

    def on_save(self):
        for key in self.edit_widgets.keys():
            self.edit_values[key] = self.__get_widget_value(self.edit_widgets[key])
        self.conf_handler.apply_changes(self.edit_values)
        self.destroy()

    @staticmethod
    def __get_widget_value(widget: Widget) -> Any:
        if type(widget) is Checkbox:
            return typing.cast(type(Checkbox), widget).get()
        else:
            return typing.cast(type(Textbox), widget).get()
