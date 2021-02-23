from datetime import datetime
from datetime import date


def sex_pair_num(num):
    return 1 if num == 2 else num + 1


def sex_pair(num):
    if num == 0:
        num = int(input("""
                        Пожалуйста укажите Ваш пол:
                                            1 - мужской
                                            2 - женский
                        """)
                  )
        return sex_pair_num(num)
    else:
        return sex_pair_num(num)


def calculate_age(date_born):
    born = [int(i) for i in date_born.split('.')]
    born = datetime(born[2], born[1], born[0])
    today = date.today()
    return today.year - born.year - (
            (today.month, today.day) < (born.month, born.day)
    )
