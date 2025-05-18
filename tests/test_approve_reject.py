import unittest
from auth import register_user
from leave import submit_leave_request, approve_leave_request, reject_leave_request
from database import init_db, get_connection

class TestApproveRejectLeave(unittest.TestCase):

    def setUp(self):
        # Inicjalizacja bazy i czyszczenie danych
        init_db()
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM leave_requests")
        c.execute("DELETE FROM users")
        conn.commit()
        conn.close()

        # Rejestracja użytkownika i dodanie wniosku
        register_user("jan", "haslo123", "pracownik")
        self.user_id = self.get_user_id("jan")
        submit_leave_request(self.user_id, "2024-06-01", "2024-06-05", "urlop")
        self.request_id = self.get_request_id(self.user_id)

    def get_user_id(self, username):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def get_request_id(self, user_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM leave_requests WHERE user_id = ?", (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def get_request_status(self, request_id):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT status FROM leave_requests WHERE id = ?", (request_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def test_approve_pending_request(self):
        print("request_id =", self.request_id)
        status_before = self.get_request_status(self.request_id)
        print("status before:", status_before)

        result = approve_leave_request(self.request_id)
        print("approve result:", result)

        self.assertTrue(result)
        status_after = self.get_request_status(self.request_id)
        self.assertEqual(status_after, "zatwierdzony")

    def test_reject_pending_request(self):
        # Dodajemy nowego użytkownika z wnioskiem
        register_user("anna", "haslo456", "pracownik")
        anna_id = self.get_user_id("anna")
        submit_leave_request(anna_id, "2024-06-10", "2024-06-15", "wolne")
        anna_request_id = self.get_request_id(anna_id)

        result = reject_leave_request(anna_request_id)
        self.assertTrue(result)
        status = self.get_request_status(anna_request_id)
        self.assertEqual(status, "odrzucony")

    def test_approve_nonexistent_request(self):
        result = approve_leave_request(9999)
        self.assertFalse(result)

    def test_reapprove_already_processed(self):
        approve_leave_request(self.request_id)
        result = approve_leave_request(self.request_id)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
