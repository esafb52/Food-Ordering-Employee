from FoodyAuth.model import Section
from FoodyAuth.model import User


def get_all_section_wtf_select():
    total = Section.query.all()
    dt = []
    for each in total:
        dt.append((each.PublicKey, each.Name,))
    return dt



def Search_In_Users(option:str, data:str) -> User:
    """
        this function take a search option and search Data and
        search in users by base on option that passed
    :param option:
    :param data:
    :return:
    """
    match option:
        case"NationalCode":
            return User.query.filter(User.NationalCode == data).all() or None

        case "PhoneNumber":
            return User.query.filter(User.PhoneNumber == data).all() or None

        case _:
            return None



