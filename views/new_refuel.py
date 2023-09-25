from tkinter import *
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
import sys

from database.db_operations import DataBaseConnector
from validation.validation import NewRefValidation
from calculations.RefuelCalc import RefuelCalc

from user import User

db = DataBaseConnector()


class NewRefuel(ThemedTk):
    """
    Class creates a window allowing user passing information about latest refuel.
    """

    def __init__(self, theme="arc") -> None:
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.set_theme(theme)
        self._window_config()
        self.refuel_panel()
        summary = ttk.Button(self, text="Create Summary", command=self.summary)
        summary.place(x=250, y=300)
        self.up = UserPanel(window=self)
        self.val = NewRefValidation()

    def _window_config(self) -> None:
        """
        Window configuration.
        """
        self.title("New Refuel")
        self.geometry("700x350")
        self.resizable(False, False)

    def refuel_panel(self) -> None:
        """
        Creates panel for passing refuel details
        """
        frame = ttk.Labelframe(self, text="Refuel Details")
        frame.place(x=10, y=10, width=300, height=250)
        self.cal = DateEntry(
            frame,
            width=12,
            background="green",
            foreground="white",
            borderwidth=2,
            date_pattern="dd-mm-y",
        )
        self.cal.place(x=150, y=5)
        header0 = ttk.Label(frame, text="Date of refueling:")
        header0.place(x=10, y=5)
        # self.ref_date = ttk.Entry(frame)
        # self.ref_date.place(x=150,y=5,width=80)
        header1 = ttk.Label(frame, text="Kilometers:")
        header1.place(x=10, y=40)
        self.ref_km = ttk.Entry(
            frame,
        )
        self.ref_km.place(x=150, y=40, width=80)
        header2 = ttk.Label(frame, text="Total Cost:")
        header2.place(x=10, y=75)
        self.ref_cost = ttk.Entry(frame)
        self.ref_cost.place(x=150, y=75, width=80)
        header2 = ttk.Label(frame, text="Gas cost per liter:")
        header2.place(x=10, y=110)
        self.gas_cost = ttk.Entry(frame)
        self.gas_cost.place(x=150, y=110, width=80)

    def get_ref_info(self) -> list:
        """
        Function extracts information provided by user in a form.
        """
        date = self.cal.get_date()
        kilometers = self.ref_km.get()
        cost = self.ref_cost.get()
        gas_price = self.gas_cost.get()
        info = [
            date,
            kilometers,
            cost,
            gas_price,
        ]
        for item in info:
            print(type(item))
        val = NewRefValidation()
        errors, data = val.validate_refuel(info)
        if len(errors) > 0:
            text = "\n".join(errors)
            # messagebox.showerror(title='Błąd wprowadzania',message=text)
            return 0
        return data

    def validation(self) -> tuple[list, list]:
        """
        Function valides data provided by user.
        Returnes refuel details and users' details.
        """
        ref_info = self.get_ref_info()
        users = self.up.pass_entries()

        if ref_info == 0:
            messagebox.showerror(title="Error", message="Review Refuel Details!")
        elif type(users) == str:
            messagebox.showerror(title="Error", message=users)
        elif self.val.check_kilometers(ref_info[1], users) == 0:
            messagebox.showerror(
                title="Error", message="Amount of kilometers does not sum up!"
            )
        return ref_info, users

    def summary(self) -> None:
        """
        Function aggretes data validation and calculations.
        Creates window with refuel summary.
        """
        ref_info, users = self.validation()
        calc = RefuelCalc(ref_info, users)
        route_info = calc.route_info()
        user_info = calc.users_info()
        print(user_info)
        SummaryWindow(route_info, user_info)


class UserPanel:
    """
    Class stands for user panel in refuel window interface.
    """

    def __init__(self, window) -> None:
        self.window = window
        self.users = []
        self.kms = []
        self.objects = []
        self.frame = ttk.Labelframe(window, text="Users Details")
        self.frame.place(x=350, y=10, width=300, height=250)
        self.y = 40
        self.index = 0
        # ad_user = ttk.Button(
        #     self.window,
        #     text='Dodaj użytkownika',
        #     command=lambda:self.add_user_entry(self.y)
        #     )
        # ad_user.place(x=530,y=5)
        header0 = ttk.Label(self.frame, text="User Name:")
        header0.place(x=30, y=10)
        header1 = ttk.Label(self.frame, text="Kilometers:")
        header1.place(x=170, y=10)
        self.user_entry(self.y)

    def user_entry(self, row, name="", kmval="") -> None:
        """
        Creates form for passing user details.
        """
        counta = 1
        for _ in range(0, 6):
            count = ttk.Label(self.frame, text=counta)
            count.place(x=5, y=self.y)

            user = ttk.Entry(self.frame)
            user.place(x=30, y=self.y)
            user.insert(0, name)

            km = ttk.Entry(self.frame)
            km.place(x=170, y=self.y, width=80)
            km.insert(0, kmval)
            self.users.append([user, km])
            self.y += 30
            counta += 1
        self.users[0][0].focus()

    def __data_validation(self, data: list) -> None:
        """
        Function validates user data.
        """
        Valid = NewRefValidation()
        errors, users = Valid.user_validation(data)
        if len(errors) > 0:
            text = "\n".join(errors)
            # messagebox.showerror(title='Coś poszło nie tak',message=text)
            return text

            # messagebox.showinfo(title='Sukces',message='Wszystkie pola poprawnie')
        return users

    def pass_entries(self) -> None:
        """
        Extracts data from user form, passes to the validation function.
        Returns a list with user data.
        """
        users = []
        for row in self.users:
            users.append((row[0].get(), row[1].get()))
            print(users)
        users = self.__data_validation(users)
        return users

    def remove_button(self):  # to be removed
        self.user.destroy()
        self.km.destroy()
        self.delete.destroy()
        for item in self.rows.values():
            try:
                for it in item:
                    print(it.get())
            except:
                print(f"{it} not in scope")


class SummaryWindow(ThemedTk):
    """
    GUI showing user summary of provided data.
    Class inheritates from ThemedTk object.
    """

    def __init__(self, route_info: list, users_info: list, theme="arc") -> None:
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.route_info = route_info
        self.users_info = users_info
        self.set_theme(theme)
        self.__window_config()
        self.__route_display()
        self.users_display()
        self.save = ttk.Button(self, text="Save", command=self.save_data)
        self.save.place(x=5, y=5)

    def __window_config(self) -> None:
        """
        Window properties configuration.
        """
        self.title("Summary")
        self.geometry("800x500")
        self.resizable(False, False)

    def __route_display(self) -> None:
        """
        Displays route details in a labaled frame.
        """
        frame = ttk.Labelframe(self, text="Route Details")
        frame.place(x=10, y=40, width=200, height=450)
        header_font = ("Helvetica bold", 11)
        text_font = ("Helvetica", 12)
        x = 10
        y = 10
        headers = [
            "Date of refuel",
            "Kilometers",
            "Total Cost",
            "Gas cost per liter",
            "Cost per 1km",
            "Liters refueled",
            "Average Consumption",
        ]

        for header, info in zip(headers, self.route_info):
            ttk.Label(frame, text=header, font=header_font).place(x=x, y=y)
            y += 20
            ttk.Label(frame, text=info, font=text_font).place(x=x, y=y)
            y += 40

    def users_display(self) -> None:
        """
        Display user details in a labeled frame with a table.
        """
        frame = ttk.Labelframe(self, text="User Details")
        frame.place(x=250, y=40, width=450, height=300)
        columns = ("Name", "Kilometers", "Share (%)", "Spend (zł)")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.place(x=10, y=10)
        for col in columns:
            tree.heading(col, text=col)
        for user in self.users_info:
            tree.insert("", END, values=user)
        for column in columns:
            tree.column(column, anchor=W, width=100)

    def save_data(self) -> None:
        """
        Loads data to the database.
        """
        db.add_refuel(self.route_info)
        refid = db.get_newest_id()
        for user in self.users_info:
            check = db.get_user_by_name(user[0])
            if check == None:
                ms = messagebox.askquestion(
                    title="Warning!",
                    message=f'There is no "{user[0]}" in database, do you want to add {user[0]} to the database?',
                )
                if ms == "yes":
                    db.add_user(name=user[0])
            us = User(name=user[0])
            us.update(km=user[1], spend=user[3])
            usid = db.get_user_id(user[0])
            db.add_ref_con(refid, usid, user[1], user[2], user[3])

        self.save["state"] = DISABLED
        messagebox.showinfo(title="Congratulaions!", message="Refuel Saved!")


if __name__ == "__main__":
    r = NewRefuel()
    r.mainloop()
