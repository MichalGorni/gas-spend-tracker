from tkinter import END, CENTER
from tkinter import ttk
from ttkthemes import ThemedTk
import pandas as pd
import sys

from database.db_operations import DataBaseConnector

db = DataBaseConnector()


class RefuelSummary(ThemedTk):
    def __init__(self, theme: str = "arc"):
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.set_theme(theme)
        self._window_config()
        self.prepare_tree()
        # self.chart()

    def _window_config(self):
        self.geometry("700x300")
        self.title("Refuel Summary")
        self.resizable(False, False)

    def prepare_tree(self):
        columns = (
            "ID",
            "Date",
            "Kilometers",
            "Total Cost",
            "Gas cost",
            "Cost per km",
            "Liters refueled",
            "Avg Consumption",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.place(x=10, y=10)
        self.tree.tag_configure("odd", background="#E8E8E8")
        self.tree.tag_configure("even", background="#DFDFDF")
        data = db.get_refuel_info()
        for row in data:
            self.tree.insert("", END, values=row)
        for column in columns:
            self.tree.heading(column, text=column)
            if column == "ID":
                self.tree.column(column, anchor=CENTER, width=20)
            elif column == "Avg Consumption":
                self.tree.column(column, anchor=CENTER, width=110)
            else:
                self.tree.column(column, anchor=CENTER, width=80)


if __name__ == "__main__":
    rs = RefuelSummary()
    rs.mainloop()
