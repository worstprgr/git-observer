import webbrowser as wb
from datetime import datetime
from tkinter import BOTH, BOTTOM, RIGHT, X, Y, ttk, PhotoImage
from tkinter import Frame
from tkinter import Scrollbar
from tkinter import Tk

from GitObserver import GitObserver
from core.transport import Observation
from core.utils import TkUtils


def is_empty(observations: list[Observation]):
    """
    Checks if given list of Observation is
    either null or empty. Empty is defined by
    all nested lists of Commit are empty as well
    :param observations:
    :return:
    """
    if observations is None or len(observations) == 0:
        return True
    for folder in observations:
        if observations is None:
            continue
        if len(folder.commits) > 0:
            return False
    return True


class GitObserverViewer:
    """
    TKinter based form to show a TreeView containing
    observations column wise
    """

    def __init__(self, app_config):
        self.config = app_config
        """"
        Instantiates a new instance and passes given
        config further down to GitObserver doing the observations
        """
        # Force use of descending log output
        self.config.descending = True
        # Instantiate GitObserver with received conf
        self.observer = GitObserver(self.config)

        # Create root window
        self.root = Tk()
        # Open PhotoImage to be passed to created form
        icon = PhotoImage(file="static/favicon.png")
        self.root.iconphoto(True, icon)
        self.root.title('Git Log Observer')
        geo = TkUtils.calculate_form_geometry(self.root, 0.7, 0.5)
        self.root.geometry(geo)

        self.view_frame = Frame(self.root)
        self.view_frame.pack(fill=BOTH, expand=True)

        # scrollbar
        self.view_scroll_y = Scrollbar(self.view_frame, orient='vertical')
        self.view_scroll_y.pack(side=RIGHT, fill=Y)
        self.view_scroll_x = Scrollbar(self.view_frame, orient='horizontal')
        self.view_scroll_x.pack(side=BOTTOM, fill=X)

        self.tv_commits = ttk.Treeview(self.view_frame, show="headings",
                                       yscrollcommand=self.view_scroll_y.set, xscrollcommand=self.view_scroll_x.set)
        # Bind cell click event to open_link
        self.tv_commits.bind('<Double-1>', self.cell_double_click)
        self.tv_commits.pack(fill=X, expand=True)
        self.view_scroll_y.config(command=self.tv_commits.yview)
        self.view_scroll_x.config(command=self.tv_commits.xview)

    def update_observation(self):
        """
        Update routine to trigger observation and
        bring results to the end of shown table
        :return: None
        """
        observations = self.observer.run()
        self.update_view(observations)
        self.root.after(60 * 1000, self.update_observation)

    def update_view(self, observations: list[Observation]):
        """
        Update routine to get a list of Observation
        at the end of currently shown table.
        Won't do anything if given list is empty (see is_empty)
        :param observations: New observation results that should be appended
        :return: None
        """
        if is_empty(observations):
            # ToDo: may we extract STDOUT to a actual log file
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Nothing changed")
            return

        self.create_columns(observations)

        # add data
        row_count = 0
        for folder in observations:
            commit_count = len(folder.commits)
            if commit_count > row_count:
                row_count = commit_count

        for row_idx in range(0, row_count):
            row_values = []
            if row_idx == 0:
                row_values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                row_values.append('')

            for folder in observations:
                if row_idx >= len(folder.commits):
                    row_values.append('')
                    row_values.append('')
                    continue
                commit = folder.commits[row_idx]
                value = f"{commit.author}: {commit.message} ({commit.date.strftime('%Y-%m-%d %H:%M:%S')})"
                row_values.append(value)
                row_values.append(commit.sha1)
            self.tv_commits.insert(parent='', index='end', values=row_values)

        self.tv_commits.pack(fill=BOTH, expand=True)

    def create_columns(self, observations: list[Observation]):
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
            column_names.append(f'{folder.name}')
            column_names.append('Link')

        # define our column
        self.tv_commits['columns'] = column_names

        self.tv_commits.heading(0, anchor="nw", text=column_names[0])
        self.tv_commits.column(0, anchor="nw", minwidth=145, stretch=False, width=145)

        # format our column
        for col_idx in range(1, len(column_names) - 1):
            min_width = 150
            is_meta = col_idx % 2 != 0
            if is_meta:
                min_width = 75
            self.tv_commits.heading(col_idx, anchor="nw", text=column_names[col_idx])
            self.tv_commits.column(col_idx, anchor="nw", minwidth=min_width, stretch=True, width=min_width)

    def cell_double_click(self, event):
        """
        Event handler for TreeView purpose.
        Will expect third and then every second column value to represent
        a web link.
        Does nothing when different column is hit or link is empty
        :param event: Mouse click event
        :return: None
        """
        # Get the associated TreeView widget
        tree = event.widget
        # Try to get region by mouse event args
        region = tree.identify_region(event.x, event.y)
        col = tree.identify_column(event.x)
        iid = tree.identify('item', event.x, event.y)
        col_num = int(col.split('#')[1])
        # Return on Date click
        if col_num <= 1:
            return

        # Minus first column (last update), then every second col is a link col
        if not region == 'cell':
            return

        if (col_num - 1) % 2 == 0:
            # Extract link from clicked and found cell
            sha1 = tree.item(iid)['values'][col_num - 1]
            link = f"{self.config.origin}{sha1}"
            if len(link) > 0:
                # open the link in default browser
                wb.open_new_tab(link)
        else:
            # Extract link from next cell of clicked cell
            sha1 = tree.item(iid)['values'][col_num]
            if len(sha1) > 0:
                git_medium_info = self.observer.get_git_show(sha1)
                TkUtils.show_dialog(self.root, git_medium_info)

    def run(self):
        """
        Initially updates observations and starts
        the main application loop
        :return:
        """
        self.update_observation()
        self.root.mainloop()
