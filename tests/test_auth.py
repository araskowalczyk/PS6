import unittest
from auth import register_user, users

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
