from database.db_operations import DataBaseConnector

db = DataBaseConnector()


class Refuel:
    def __init__(self, ID) -> None:
        self.ID = ID

    def show_info(self):
        self.date, self.km, self.liters, self.cost = db.get_refuel_info(self.ID)
        print(self.date)
        print(self.km)
        print(self.liters)
        print(self.cost)


if __name__ == "__main__":
    new_id = db.count_length("tank")
    # db.add_refuel(new_id,'11.02.2023',400,50,260)
    rf = Refuel(2)
    rf.show_info()
