"""Для тестов нужен логин пароль от аккаунта ВК"""

import unittest
from main import User

login = ''
password = ''


class TestUser(unittest.TestCase):

    user = User(login=login, password=password)

    def setUp(self) -> None:
        self.user.get_user(577250478)

    def test_api(self):
        self.assertEqual(self.user.api.version, '5.92')

    def test_get_user(self):
        ids = self.user.user_id
        relation = self.user.relation
        self.assertTrue(ids)
        self.assertEqual(577250478, ids)
        self.assertEqual(1, relation)

    def test_find_pair(self):
        list_pair = self.user.find_pair()
        self.assertTrue(list_pair)
        self.assertIsInstance(list_pair, list)
        self.assertIsNotNone(list_pair[0], int)

    def test_target_user(self):
        user_photo = self.user.get_target_user(577250478)
        self.assertTrue(user_photo)
        self.assertIsInstance(user_photo, list)
        self.assertIsNotNone(user_photo[0], dict)
        self.assertEqual(user_photo[0]['album_id'], -6)


if __name__ == '__main__':
    unittest.main()
