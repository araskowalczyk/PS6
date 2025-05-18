import unittest
from auth import register_user, users
from auth import login_user

class TestRegisterUser(unittest.TestCase):

    def setUp(self):
        users.clear()

    def test_successful_registration(self):
        self.assertTrue(register_user("jan", "haslo123", "pracownik"))

    def test_duplicate_username(self):
        register_user("jan", "haslo123", "pracownik")
        self.assertFalse(register_user("jan", "innehaslo", "kierownik"))

    def test_invalid_role(self):
        self.assertFalse(register_user("anna", "haslo123", "admin"))

    def test_empty_fields(self):
        self.assertFalse(register_user("", "", "pracownik"))

if __name__ == '__main__':
    unittest.main()


class TestLoginUser(unittest.TestCase):

    def setUp(self):
        users.clear()
        register_user("jan", "haslo123", "pracownik")

    def test_login_success(self):
        user = login_user("jan", "haslo123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "jan")

    def test_login_wrong_password(self):
        user = login_user("jan", "zlehaslo")
        self.assertIsNone(user)

    def test_login_nonexistent_user(self):
        user = login_user("adam", "haslo123")
        self.assertIsNone(user)

    def test_login_empty_fields(self):
        user = login_user("", "")
        self.assertIsNone(user)