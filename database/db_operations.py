import os
import sqlite3


class DataBaseConnector:
    """Database operator class, which provides database connection"""

    def __init__(self) -> None:
        self.conn = sqlite3.connect(rf"database\gastracker.db")
        self.c = self.conn.cursor()

    def create_users_table(self):
        """Creates database"""
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

    def create_refuel_table(self):
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

    def count_length(self, table_name):
        self.c.execute(f"SELECT COUNT(*) FROM {table_name}")
        length = self.c.fetchone()[0]
        return length + 1

    def add_user(self, name):
        # id = self.count_length('users')
        with self.conn:
            self.c.execute(
                f"INSERT INTO users (name, km, spend) VALUES (:name, :km, :spend)",
                {"name": name, "km": 0, "spend": 0},
            )
        print("User added")

    def get_user_id(self, name):
        with self.conn:
            self.c.execute(
                f"SELECT user_ID FROM users WHERE name=:name", {"name": name}
            )
        user_id = self.c.fetchone()
        return user_id[0]

    def get_user_by_name(self, name):
        with self.conn:
            self.c.execute(
                f"SELECT km, spend FROM users WHERE name=:name", {"name": name}
            )

        user = self.c.fetchone()
        # km = user[0]
        # spend = user[1]
        # return km, spend
        return user

    def get_user(self, ID):
        with self.conn:
            self.c.execute(
                "SELECT * FROM users WHERE user_ID=:user_ID", {"user_ID": ID}
            )
        return self.c.fetchone()

    def update_user(self, name, km, spend):
        with self.conn:
            self.c.execute(
                "UPDATE users SET km=:km,spend=:spend WHERE name=:name",
                {"km": km, "spend": spend, "name": name},
            )

    def add_refuel(self, list):
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
                    "date": list[0],
                    "km": list[1],
                    "total_cost": list[2],
                    "cost_per_liter": list[3],
                    "cost_per_km": list[4],
                    "liters": list[5],
                    "avg_cons": list[6],
                },
            )
        print("Refuel added")

    def get_refuel_info(self, *arg: int):
        if arg:
            with self.conn:
                self.c.execute(
                    "SELECT * FROM refuel WHERE refuel_ID=:ID ORDER BY date ASC;",
                    {"ID": arg[0]},
                )
            inf = self.c.fetchall()
        else:
            with self.conn:
                self.c.execute("SELECT * FROM refuel ORDER BY date ASC;")
            inf = self.c.fetchall()
        return inf

    def delete_col(self, table, column_name):
        with self.conn:
            self.c.execute(f"ALTER TABLE {table} DROP COLUMN {column_name}")

    def get_newest_id(self):
        with self.conn:
            self.c.execute(f"SELECT MAX(refuel_ID) FROM refuel")
        id = self.c.fetchone()
        return id[0]

    def add_ref_con(self, refid, usid, userkm, usershare, userspend):
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

    def get_all_users(self):
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

    def historical(self, user_ID):
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
                {"user_ID": user_ID},
            )
        return self.c.fetchall()


if __name__ == "__main__":
    d = DataBaseConnector()
    # d.add_user('Dorota')
    # # d.create_users_table()
    # id = d.get_user_id('Michał')
    # print(id + 2)
    data = d.get_refuel_info()
    print(data)
