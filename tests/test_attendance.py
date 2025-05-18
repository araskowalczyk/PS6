import unittest
from database import init_db, get_connection
from auth import register_user
from attendance import view_attendance

class TestViewAttendance(unittest.TestCase):

    def setUp(self):
        init_db()
        conn = get_connection()
        c = conn.cursor()
        # Czyścimy dane
        c.execute("DELETE FROM attendance")
        c.execute("DELETE FROM users")
        conn.commit()
        conn.close()

        # Dodaj użytkownika i dane obecności
        register_user("jan", "haslo123", "pracownik")
        self.user_id = self.get_user_id("jan")
        self.insert_attendance_data()

    def get_user_id(self, username):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def insert_attendance_data(self):
        conn = get_connection()
        c = conn.cursor()
        data = [
            (self.user_id, "2024-06-01", "obecny"),
            (self.user_id, "2024-06-02", "urlop"),
            (self.user_id, "2024-06-03", "nieobecny")
        ]
        c.executemany("INSERT INTO attendance (user_id, date, status) VALUES (?, ?, ?)", data)
        conn.commit()
        conn.close()

    def test_view_attendance_valid_range(self):
        records = view_attendance(self.user_id, ("2024-06-01", "2024-06-03"))
        self.assertEqual(len(records), 3)

    def test_view_attendance_partial_range(self):
        records = view_attendance(self.user_id, ("2024-06-02", "2024-06-02"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][3], "urlop")  # status znajduje się na pozycji 3

    def test_view_attendance_other_user(self):
        register_user("adam", "haslo456", "pracownik")
        other_user_id = self.get_user_id("adam")
        records = view_attendance(other_user_id, ("2024-06-01", "2024-06-03"))
        self.assertEqual(len(records), 0)

    def test_invalid_date_range(self):
        records = view_attendance(self.user_id, ("2024-06-05", "2024-06-01"))
        self.assertEqual(records, [])

if __name__ == '__main__':
    unittest.main()
