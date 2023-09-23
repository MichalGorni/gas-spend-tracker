from datetime import date


class NewRefValidation:
    """
    Class used for validating data entries
    """

    def __init__(self) -> None:
        pass

    def validate_refuel(self, data: list) -> tuple[list, list]:
        """
        Checks if all required data has been provided.
        Normalizes float inputs.
        """
        errors = []
        info = []
        if type(data[0]) != date or len(str(data[0])) == 0:
            errors.append("Wrong Date!")
        else:
            info.append(data[0])
        for item in data[1:]:
            if len(str(item)) != 0:
                if "," in item:
                    item = item.replace(",", ".")

                item = float(item)
                info.append(item)
            else:
                errors.append("Check fields: Kilometers, Total Cost, Gas Price")
        print(info)
        return list(dict.fromkeys(errors)), info

    def check_kilometers(self, total: float, users_list: list) -> int:
        """
        Checks if total kiloemeters matches sum of kilometers per user.
        """
        lista = []
        for item in users_list:
            lista.append(item[1])
        if total == sum(lista):
            return 1
        else:
            return 0

    def user_validation(self, data: list) -> tuple[list, list]:
        """
        Validates weather user name has been provided.
        """
        print("Validating data...")
        error = []
        correct_list = []
        for entry in data:
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
