from datetime import date


class NewRefValidation:
    def __init__(self) -> None:
        pass

    def validate_refuel(self, lista):
        errors = []
        info = []
        if type(lista[0]) != date or len(str(lista[0])) == 0:
            errors.append("Wrong Date!")
        else:
            info.append(lista[0])
        for item in lista[1:]:
            if len(str(item)) != 0:
                if "," in item:
                    item = item.replace(",", ".")

                item = float(item)
                info.append(item)
            else:
                errors.append("Check fields: Kilometers, Total Cost, Gas Price")
        print(info)
        return list(dict.fromkeys(errors)), info

    def check_kilometers(self, value, users_list):
        lista = []
        for item in users_list:
            lista.append(item[1])
        if value == sum(lista):
            return 1
        else:
            return 0

    def user_validation(self, lista):
        print("Validating data...")
        error = []
        correct_list = []
        for entry in lista:
            if len(entry[0]) > 0 and len(str(entry[1])) > 0:
                print(f"{entry} is correct")
                correct_list.append((entry[0], float(entry[1])))
            elif len(entry[0]) == 0 and len(str(entry[1])) > 0:
                error.append("Fill all name fields!")
            elif len(entry[0]) > 0 and len(str(entry[1])) == 0:
                error.append("Fill all kilometers fields!")
            elif len(entry[0]) == 0 and len(str(entry[1])) == 0:
                print(f"{entry} to be removed")

        return error, correct_list


if __name__ == "__main__":
    dict1 = ["asda", "assa"]
    dict2 = [0, ""]

    v = NewRefValidation()
    er = v.check_entries(dict1, dict2)
    print(er)
