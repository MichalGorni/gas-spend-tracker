import os
from database.db_operations import DataBaseConnector
import time

BASE_DIR = os.path.dirname(__file__)

db = DataBaseConnector()


class User:
    def __init__(self, name):
        self.name = name
        try:
            self.get_user_info()
        except:
            print("User not found")
            print("Creating new user...")
            db.add_user(self.name)
            self.get_user_info()

    def check_user(self):
        try:
            db.get_user_by_name(self.name)
        except:
            return None

    def get_user_info(self):
        self.km, self.spend = db.get_user_by_name(self.name)
        return self.km, self.spend

    def show_info(self):
        self.get_user_info()
        print(f"User information for {self.name}")
        print(self.km, self.spend)

    def update(self, km, spend):
        self.km = self.km + km
        self.spend = self.spend + spend
        db.update_user(self.name, self.km, self.spend)


if __name__ == "__main__":
    Michal = User("Tomek")
    Michal.update(10, 70)
    Michal.show_info()
    # print(t)
    # db.get_all_users()
    # db.create_users_table()
