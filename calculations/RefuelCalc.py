class RefuelCalc:
    def __init__(self,ref_info,users):
        self.ref_info = ref_info
        self.users = users

    #srednie spalanie,koszt per km
    #udział km kierowcy, koszt per kierowca

    def route_info(self):
        self.km = self.ref_info[1]
        self.cost = self.ref_info[2]
        self.price = self.ref_info[3]

        cost_per_km = round((self.cost/self.km),2)
        liters = round((self.cost/self.price),1)
        average_consumption = round(((liters/self.km)*100),2)

        self.ref_info.append(cost_per_km)
        self.ref_info.append(liters)
        self.ref_info.append(average_consumption)

        return self.ref_info

    def users_info(self):
        users = []
        for row in self.users:
            share = round(((row[1]/self.km)*100 ),2)
            user_cost = round((self.cost*share)/100,2)
            row = (row[0],row[1],share,user_cost)
            users.append(row)
        return users


