from tkinter import Menu
from tkinter import ttk
from ttkthemes import ThemedTk
import os

from views import new_refuel, refuel_summary, user_overview


class StarterWindow(ThemedTk):
    def __init__(self, theme: str = "arc"):
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.set_theme(theme)
        self.window_config()
        self.prepare_buttons()
        self.prepare_menu()

    def window_config(self):
        self.title("Gasoline tracker")
        self.geometry("400x300")
        self.resizable(False, False)

    def prepare_buttons(self):
        header = ttk.Label(text="GASOLINE TRACKER", font=("Helvetica", 20))
        header.place(x=50, y=20, width=300)

        tankowanie = ttk.Button(text="Add new refuel", command=self.open_new_ref)
        tankowanie.place(x=50, y=100, width=300)

        pod_user = ttk.Button(text="Users Summary", command=self.open_user_overwiev)
        pod_user.place(x=50, y=150, width=300)

        pod_tank = ttk.Button(text="Refuels Summary", command=self.open_refuel_summary)
        pod_tank.place(x=50, y=200, width=300)

    def prepare_menu(self):
        menu = Menu(self, tearoff=False)
        sub_menu = Menu(menu, tearoff=False)
        sub_menu.add_command(label="Exit", command=self.destroy)
        menu.add_cascade(menu=sub_menu, label="Menu")
        self.config(menu=menu)

    def open_new_ref(self):
        nr = new_refuel.NewRefuel()
        nr.mainloop()

    def open_user_overwiev(self):
        uv = user_overview.UserOverwiev()
        uv.mainloop()

    def open_refuel_summary(self):
        rs = refuel_summary.RefuelSummary()
        rs.mainloop()


if __name__ == "__main__":
    w = StarterWindow()
    # w.set_theme('arc')
    w.mainloop()
