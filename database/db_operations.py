import os
import sqlite3


class DataBaseConnector:
    """
    Class enables connectio to the database.
    Provides set of query function allowing accessing data.
    """

    def __init__(self) -> None:
        self.conn = sqlite3.connect(
            rf"C:\Users\gorni\OneDrive\Pulpit\PYTHON\gas_spend_tracker\database\gastracker.db"
        )
        self.c = self.conn.cursor()

    def create_users_table(self) -> None:
        """
        Creates table "user"
        """
        self.c.execute(
            f"""CREATE TABLE users (
                user_ID INTEGER PRIMARY KEY,
                name STRING,
                km FLOAT,
                spend FLOAT,
            )"""
        )
        self.conn.commit()
        self.conn.close()

    def create_refuel_table(self) -> None:
        """
        Creates table "refuel"
        """
        self.c.execute(
            f"""CREATE TABLE refuel (
                refuel_ID PRIMARY KEY,
                date DATE,
                km FLOAT,
                total_cost FLOAT,
                cost_per_liter FLOAT,
                cost_per_km FLOAT,
                liters FLOAT,
                avg_cons FLOAT
            )"""
        )
        self.conn.commit()
        self.conn.close()

    def count_length(self, table_name: str) -> int:
        """
        Checks number of rows in a given table.
        Returns integer with a number of rows in a table + 1
        :param table_name - name of table to be checked
        """
        self.c.execute(f"SELECT COUNT(*) FROM {table_name}")
        length = self.c.fetchone()[0]
        return length + 1

    def add_user(self, name: str):
        """ "
        Adds new user to the table "users"
        """
        # id = self.count_length('users')
        with self.conn:
            self.c.execute(
                f"INSERT INTO users (name, km, spend) VALUES (:name, :km, :spend)",
                {"name": name, "km": 0, "spend": 0},
            )
        print("User added")

    def get_user_id(self, name: str) -> int:
        """
        Fetches user id from table "users" by given name
        """
        with self.conn:
            self.c.execute(
                f"SELECT user_ID FROM users WHERE name=:name", {"name": name}
            )
        user_id = self.c.fetchone()
        return user_id[0]

    def get_user_by_name(self, name: str) -> tuple:
        """
        Fetches user data by it's name from the "users" table.
        Returns tuple with user data
        """
        with self.conn:
            self.c.execute(
                f"SELECT km, spend FROM users WHERE name=:name", {"name": name}
            )

        user = self.c.fetchone()
        # km = user[0]
        # spend = user[1]
        # return km, spend
        return user

    def get_user(self, id: int) -> tuple:
        """
        Gets user data by given id number.
        Returns tuple with user data.
        """
        with self.conn:
            self.c.execute(
                "SELECT * FROM users WHERE user_ID=:user_ID", {"user_ID": id}
            )
        return self.c.fetchone()

    def update_user(self, name: str, km: float, spend: float) -> None:
        """
        Updates user info in the table "users".
        """
        with self.conn:
            self.c.execute(
                "UPDATE users SET km=:km,spend=:spend WHERE name=:name",
                {"km": km, "spend": spend, "name": name},
            )

    def add_refuel(self, data: list) -> None:
        """
        Inserts new refuel data into the "refuel" table.
        """
        with self.conn:
            self.c.execute(
                f"""INSERT INTO refuel (
            date,
            km,
            total_cost,
            cost_per_liter,
            cost_per_km,
            liters,
            avg_cons
            )
            VALUES (
                :date, 
                :km, 
                :total_cost, 
                :cost_per_liter,
                :cost_per_km, 
                :liters,
                :avg_cons)
                """,
                {
                    "date": data[0],
                    "km": data[1],
                    "total_cost": data[2],
                    "cost_per_liter": data[3],
                    "cost_per_km": data[4],
                    "liters": data[5],
                    "avg_cons": data[6],
                },
            )
        print("Refuel added")

    def get_refuel_info(self, refuel_id: int | None = None) -> tuple:
        """
        Fetches data from the "refuel" table.
        Optional param "refuel_id" - if passed then only data for a given refuel is fetched.
        If "refuel_id" is not passed, then all data will be fetched.
        """
        if refuel_id:
            with self.conn:
                self.c.execute(
                    "SELECT * FROM refuel WHERE refuel_ID=:ID ORDER BY date ASC;",
                    {"ID": refuel_id[0]},
                )
            inf = self.c.fetchall()
        else:
            with self.conn:
                self.c.execute("SELECT * FROM refuel ORDER BY date ASC;")
            inf = self.c.fetchall()
        return inf

    def delete_col(self, table: str, column_name: str) -> None:
        """
        Deletes selected column from a given table.
        """
        with self.conn:
            self.c.execute(f"ALTER TABLE {table} DROP COLUMN {column_name}")

    def get_newest_id(self) -> int:
        """
        Gets newest id from the "refuel" table.
        Returns integer.
        """
        with self.conn:
            self.c.execute(f"SELECT MAX(refuel_ID) FROM refuel")
        id = self.c.fetchone()
        return id[0]

    def add_ref_con(
        self, refid: int, usid: int, userkm: float, usershare: float, userspend: float
    ) -> None:
        """
        Inserts new record into "ref_us_con" table
        """
        with self.conn:
            self.c.execute(
                f"""INSERT INTO ref_us_con (
            refuel_ID, 
            user_ID, 
            user_km, 
            user_share, 
            user_spend
            ) 
            VALUES(
                :refuel_ID,
                :user_ID,
                :user_km,
                :user_share,
                :user_spend)
                """,
                {
                    "refuel_ID": refid,
                    "user_ID": usid,
                    "user_km": userkm,
                    "user_share": usershare,
                    "user_spend": userspend,
                },
            )

    def get_all_users(self) -> list:
        """
        Fetches all user data from the "users" table
        """
        with self.conn:
            self.c.execute("SELECT * FROM users")
        user_list = self.c.fetchall()
        return user_list

    def users_summary(self):
        users = self.get_all_users()
        km = []
        spend = []
        for user in users:
            km.append(user[1])
            spend.append(user[2])

    def historical(self, user_id: int) -> tuple:
        """
        Returns historical data of an user by given user id.
        Data is feched from tables "refule" and "ref_us_con"
        """
        with self.conn:
            self.c.execute(
                """SELECT refuel.date, ref_us_con.user_km,ref_us_con.user_share,ref_us_con.user_spend
                            FROM 
                                refuel
                            JOIN ref_us_con ON
                                refuel.refuel_ID=ref_us_con.refuel_ID
                            WHERE user_ID=:user_ID
                            ORDER BY
                                refuel.date ASC;""",
                {"user_ID": user_id},
            )
        return self.c.fetchall()


if __name__ == "__main__":
    d = DataBaseConnector()
    # d.add_user('Dorota')
    # # d.create_users_table()
    # id = d.get_user_id('Michał')
    # print(id + 2)
    # d.create_refuel_table()
    d.create_users_table()
