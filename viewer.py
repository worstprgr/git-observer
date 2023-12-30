import webbrowser as wb
from collections import namedtuple
from datetime import datetime
from tkinter import BOTH, BOTTOM, NORMAL, NW, RIGHT, TOP, X, Y, ttk, PhotoImage, LEFT
from tkinter import Tk, Frame, Scrollbar, Label
from tkinter.ttk import Sizegrip
from core.event import StatusEventArgs

from observer import GitObserverThread
from core.tkinter.TkUtil import TkUtil
from core.transport import Observation, ObservationEventArgs, Commit
from core.transport import ObservationUtil
from core.paths import Paths


c_paths = Paths()
Point = namedtuple("Point", "x y")
"""
namedtuple representing X and Y coordinates
"""


class GitObserverViewer(Tk):
    """
    TKinter based form to show a TreeView containing
    observations column wise
    """

    def __init__(self, app_config):
        """"
        Instantiates a new instance and passes given
        config further down to GitObserver doing the observations
        """
        super().__init__()

        # Force use of descending log output
        self.config = app_config
        self.config.descending = True

        # Instance wide store row number and two-dimensional rows and their commits (columns)
        self.row_count: int = 0
        self.grid_data: list[list[Commit | None]] = list()

        # Get notified when closed
        self.protocol("WM_DELETE_WINDOW", self.root_delete)

        # Open PhotoImage to be passed to created form
        icon = PhotoImage(file=c_paths.FAVICON)
        self.iconphoto(True, icon)
        self.title('Git Log Observer')
        geo = TkUtil.calculate_form_geometry(self, 0.7, 0.5)
        self.geometry(geo)

        self.view_frame = Frame(self)
        self.view_frame.pack(fill=BOTH, expand=True)

        # scrollbar
        # H-Scroll container since contains a scroll bar and a sizegrip
        self.h_scroll_stack = Frame(self.view_frame, background='lightgray')
        self.sizegrip = Sizegrip(self.h_scroll_stack)
        self.sizegrip.pack(side=RIGHT, fill=Y)

        self.status_bar = Label(self.h_scroll_stack, text="Initializing...", background='lightgray')
        self.status_bar.pack(side=TOP, anchor=NW, padx=3)

        self.view_scroll_x = Scrollbar(self.h_scroll_stack, orient='horizontal')
        self.view_scroll_x.pack(side=LEFT, fill=X, expand=True)
        self.h_scroll_stack.pack(side=BOTTOM, fill=X)

        self.view_scroll_y = Scrollbar(self.view_frame, orient='vertical')
        self.view_scroll_y.pack(side=RIGHT, fill=Y)

        self.tv_commits = ttk.Treeview(self.view_frame, show="headings",
                                       yscrollcommand=self.view_scroll_y.set, xscrollcommand=self.view_scroll_x.set)
        # Bind cell click event to open_link
        self.tv_commits.bind('<Double-1>', self.cell_double_click)
        self.tv_commits.bind('<Control-Button-1>', self.control_click)
        self.tv_commits.pack(fill=X, expand=True)
        self.view_scroll_y.config(command=self.tv_commits.yview)
        self.view_scroll_x.config(command=self.tv_commits.xview)
        self.create_columns(app_config.logfolders)

        # Finally instantiate GitObserver with received conf
        self.observer = GitObserverThread(self.config)
        self.observer.OnLoaded += self.observer_loaded
        self.observer.OnStatus += self.observer_status
        self.observer.start()

    def root_delete(self):
        """
        Handler which is called when window is about to get deleted
        (Shutdown)
        :return: None
        """
        # Notify observer thread that its about to die
        self.observer.stop_observation()
        self.destroy()

    def observer_loaded(self, observation_args: ObservationEventArgs):
        """
        Event handler that reacts on external event
        of successfully loaded observations
        :return: None
        """
        if observation_args is None:
            return
        self.update_view(observation_args.observations)

    def observer_status(self, status_args: StatusEventArgs):
        if self.wm_state() == NORMAL:
            status_text = f'Status: {status_args.status}'
            self.status_bar.config(text=status_text)

    def update_view(self, observations: list[Observation]):
        """
        Update routine to get a list of Observation
        at the end of currently shown table.
        Won't do anything if given list is empty (see is_empty)
        :param observations: New observation results that should be appended
        :return: None
        """
        if ObservationUtil.is_empty(observations):
            return

        # add data
        update_row_count = 0
        for folder in observations:
            commit_count = len(folder.commits)
            if commit_count > update_row_count:
                update_row_count = commit_count

        for row_idx in range(0, update_row_count):
            row_values = []
            row_commits: list[Commit | None] = list()
            if row_idx == (update_row_count - 1):
                row_values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                row_values.append('')

            for folder in observations:
                if row_idx >= len(folder.commits):
                    row_values.append('')
                    row_commits.append(None)
                    continue
                commit = folder.commits[row_idx]
                value = f"{commit.author}: {commit.message} ({commit.date.strftime('%Y-%m-%d %H:%M:%S')})"
                row_values.append(value)
                row_commits.append(commit)
            self.grid_data.insert(0, row_commits)
            self.tv_commits.insert(parent='', index=0, values=row_values)
            self.row_count += 1

        self.tv_commits.pack_forget()
        self.tv_commits.pack(fill=BOTH, expand=True)

    def create_columns(self, observations: list[str]):
        """
        Initially creates columns based on first found
        Observation list.
        Won't do anything if columns already present
        :param observations: first ever loaded observation result
        :return: None
        """
        if len(self.tv_commits['columns']) > 0:
            return

        column_names = ['Last updated']
        for folder in observations:
            column_names.append(f'{folder}')

        # define our column
        self.tv_commits['columns'] = column_names

        self.tv_commits.heading(0, anchor="nw", text=column_names[0])
        self.tv_commits.column(0, anchor="nw", minwidth=145, stretch=False, width=145)

        # format our column
        for col_idx in range(1, len(column_names)):
            self.tv_commits.heading(col_idx, anchor="nw", text=column_names[col_idx])
            self.tv_commits.column(col_idx, anchor="nw", minwidth=150, stretch=True, width=150)
        self.tv_commits.pack(fill=BOTH, expand=True)

    def control_click(self, event):
        """
        Event handler for TreeView purpose when clicking with Ctrl clicked.
        Will get currently selected Commit and opens web browser leading to [origin]/[SHA1]
        :param event: Mouse click event
        :return: None
        """
        commit = self.get_row_on_position(Point(event.x, event.y))
        if not commit:
            return

        sha1 = commit.sha1
        if len(sha1) > 0:
            # Extract link from clicked and found cell
            link = f"{self.config.origin}{sha1}"
            # open the link in default browser
            wb.open_new_tab(link)
        for item in self.tv_commits.selection():
            self.tv_commits.selection_remove(item)

    def cell_double_click(self, event):
        """
        Event handler for TreeView purpose when double-clicking.
        Will get currently selected Commit and opens a detail form for whole commit info
        :param event: Mouse click event
        :return: None
        """
        commit = self.get_row_on_position(Point(event.x, event.y))
        if not commit:
            return
        # Extract link from next cell of clicked cell
        sha1 = commit.sha1
        if len(sha1) > 0:
            git_medium_info = self.observer.get_git_show(sha1)
            TkUtil.show_message_dialog(self, git_medium_info)

    def get_row_on_position(self, pos: Point) -> Commit | None:
        """
        Gets the currently selected row found by coordinates x and y
        and returns corresponding Commit or None
        :param pos: Point with X and Y coordinates
        :return: Commit or None
        """
        # Get the associated TreeView widget
        tree = self.tv_commits
        # Try to get region by position
        region = tree.identify_region(pos.x, pos.y)
        col = tree.identify_column(pos.x)
        iid = tree.identify('item', pos.x, pos.y)
        row_idx = tree.index(iid)
        # The identifier of columns has a trailing '#' which needs to be removed
        col_num = int(col.split('#')[1])
        # Return on Date click
        if col_num <= 1:
            return None

        # Adjust number to ignore first date column (e.g. col 2 is col 1 in data)
        col_num -= 1

        if not region == 'cell':
            return None

        return self.grid_data[row_idx][col_num - 1]
