from scripts.class_user import User
from scripts.class_user import User_Main
from scripts.functions_find_people import sex_pair_num


import unittest

api = ''
name = ''


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(api)

    def test_version(self):
        self.assertTrue(type(self.user.version) == str,
                        'Версия приложения должна быть строкой!')


class TestUser_Main(unittest.TestCase):
    def setUp(self) -> None:
        self.test_user = User_Main(api)

    def test_user_id(self):
        self.test_user.get_user(name)
        self.assertTrue(type(self.test_user.user_id) == int,
                        'Не работает get_user')


class TestFunc(unittest.TestCase):
    def test_sex_pair_num(self):
        self.assertTrue(sex_pair_num(1) == 2, 'Ошибка')
        self.assertTrue(sex_pair_num(2) == 1, 'Ошибка')


if __name__ == '__main__':
    unittest.main()
