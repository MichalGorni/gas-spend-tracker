from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import sys


from database.db_operations import DataBaseConnector

db = DataBaseConnector()


class UserOverwiev(ThemedTk):
    """
    Class provides GUI for overview of all users.
    Inheritates from ThemedTk object.
    """

    def __init__(self, theme: str = "arc") -> None:
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.set_theme(theme)
        self._window_config()
        self._prepare_treeview()
        self.users_summary()
        ttk.Label(
            self,
            text="Double click on to see details",
            font=("Helvetica", 8),
        ).place(x=20, y=5)

    def _window_config(self) -> None:
        """
        Window's properties configuration.
        """
        self.geometry("600x300")
        self.title("Users Summary")

    def _prepare_treeview(self) -> None:
        """
        Retreives data from database and creates a treeview.
        """
        columns = ("ID", "Name", "Kilometers", "Spend")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.place(x=20, y=30)
        self.users_data = db.get_all_users()
        for user in self.users_data:
            self.tree.insert("", END, values=user)
        for column in columns:
            self.tree.heading(column, text=column)
            if column == "ID":
                self.tree.column(column, anchor=CENTER, width=20)
            elif column == "Name":
                self.tree.column(column, anchor=W, width=80)
            else:
                self.tree.column(column, anchor=CENTER, width=70)
        self.tree.bind("<Double-1>", self.double_click)

    def users_summary(self) -> None:
        """
        Provides a specific user overview.
        """
        km = []
        spend = []
        for user in self.users_data:
            km.append(user[2])
            spend.append(user[3])
        ttk.Label(self, text="Sum of Kilometers:", font=("Helvetica", 12)).place(
            x=350, y=20
        )
        ttk.Label(self, text=f"{sum(km)} km", font=("Helvetica", 18)).place(x=350, y=60)
        ttk.Label(self, text="Total Gas Spend:", font=("Helvetica", 12)).place(
            x=350, y=120
        )
        ttk.Label(self, text=f"{sum(spend)} zł", font=("Helvetica", 18)).place(
            x=350, y=160
        )

    def double_click(self, event) -> None:
        """
        Event command opening invoking UserSummary object.
        """
        item = self.tree.selection()
        user_id = self.tree.item(item, "values")[0]
        summary = UserSummary(user_id)
        # summary.mainloop()


class UserSummary(ThemedTk):
    """
    Class provides GUI for specific user datails.
    """

    def __init__(self, user_id: int, theme: str = "arc") -> None:
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.user_id = int(user_id)
        self.set_theme(theme)
        self.get_user_basics()
        self._window_config()
        self.historical_view()
        self.mainloop()

    def _window_config(self) -> None:
        """
        Window's properties config.
        """
        self.geometry("600x300")
        self.title(rf"Summary - {self.username}")

    def get_user_basics(self) -> None:
        """
        Retreives user data from a database.
        Creates GUI elements.
        """
        data = db.get_user(self.user_id)
        self.username = data[1]
        headers = ["Sum of Kilometers:", "Sum of Spend:"]
        y = 20
        for entry, head in zip(data[2:], headers):
            ttk.Label(self, text=head, font=("Helvetica", 12)).place(x=400, y=y)
            y += 20
            ttk.Label(self, text=entry, font=("Healvetica", 15)).place(x=400, y=y)
            y += 40

    def historical_view(self) -> None:
        """
        Retreives user's historical data from a database.
        Creates a tree widget and inserts data.
        """
        data = db.historical(self.user_id)
        columns = ("Date", "Kilometers", "Share (%)", "Spend (zł)")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        tree.place(x=10, y=10)
        for row in data:
            tree.insert("", END, values=row)
        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor=W, width=80)


if __name__ == "__main__":
    w = UserOverwiev()
    w.mainloop()
    # ov = UserSummary(1)
    # ov.mainloop()
    # data = db.historical(1)
    # print(data)
