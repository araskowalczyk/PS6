import unittest
from leave import submit_leave_request
from database import init_db, get_connection
from auth import register_user

class TestSubmitLeaveRequest(unittest.TestCase):

    def setUp(self):
        init_db()
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM leave_requests")
        c.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        register_user("jan", "haslo123", "pracownik")

    def get_user_id(self, username):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def test_valid_leave_request(self):
        user_id = self.get_user_id("jan")
        result = submit_leave_request(user_id, "2024-06-01", "2024-06-05", "urlop wypoczynkowy")
        self.assertTrue(result)

    def test_invalid_date_order(self):
        user_id = self.get_user_id("jan")
        result = submit_leave_request(user_id, "2024-06-10", "2024-06-05", "bledne daty")
        self.assertFalse(result)

    def test_invalid_date_format(self):
        user_id = self.get_user_id("jan")
        result = submit_leave_request(user_id, "2024/06/01", "2024-06-05", "bledny format")
        self.assertFalse(result)

    def test_empty_reason(self):
        user_id = self.get_user_id("jan")
        result = submit_leave_request(user_id, "2024-06-01", "2024-06-05", "")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
