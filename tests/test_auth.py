import unittest
from auth import register_user, users
from auth import login_user
from leave import submit_leave_request, leave_requests
from leave import approve_leave_request, reject_leave_request
from attendance import view_attendance, attendance_records
from models import Attendance

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

class TestSubmitLeaveRequest(unittest.TestCase):

    def setUp(self):
        leave_requests.clear()

    def test_valid_leave_request(self):
        result = submit_leave_request(1, "2024-06-01", "2024-06-05", "urlop wypoczynkowy")
        self.assertTrue(result)
        self.assertEqual(len(leave_requests), 1)

    def test_invalid_date_order(self):
        result = submit_leave_request(1, "2024-06-10", "2024-06-05", "bledne daty")
        self.assertFalse(result)

    def test_invalid_date_format(self):
        result = submit_leave_request(1, "2024/06/01", "2024-06-05", "format bledu")
        self.assertFalse(result)

    def test_empty_reason(self):
        result = submit_leave_request(1, "2024-06-01", "2024-06-05", "")
        self.assertTrue(result) 

class TestApproveRejectLeave(unittest.TestCase):

    def setUp(self):
        leave_requests.clear()
        submit_leave_request(1, "2024-06-01", "2024-06-05", "urlop")

    def test_approve_pending_request(self):
        result = approve_leave_request(1)
        self.assertTrue(result)
        self.assertEqual(leave_requests[0].status, "zatwierdzony")

    def test_reject_pending_request(self):
        leave_requests.clear()
        submit_leave_request(1, "2024-06-01", "2024-06-05", "urlop")
        result = reject_leave_request(1)
        self.assertTrue(result)
        self.assertEqual(leave_requests[0].status, "odrzucony")

    def test_approve_nonexistent_request(self):
        result = approve_leave_request(999)
        self.assertFalse(result)

    def test_approve_already_processed(self):
        approve_leave_request(1)
        result = approve_leave_request(1)
        self.assertFalse(result)

class TestViewAttendance(unittest.TestCase):

    def setUp(self):
        attendance_records.clear()
        attendance_records.append(Attendance(1, 1, "2024-06-01", "obecny"))
        attendance_records.append(Attendance(2, 1, "2024-06-02", "urlop"))
        attendance_records.append(Attendance(3, 1, "2024-06-03", "nieobecny"))
        attendance_records.append(Attendance(4, 2, "2024-06-02", "obecny"))

    def test_view_attendance_valid_range(self):
        result = view_attendance(1, ("2024-06-01", "2024-06-03"))
        self.assertEqual(len(result), 3)

    def test_view_attendance_partial_range(self):
        result = view_attendance(1, ("2024-06-02", "2024-06-02"))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status, "urlop")

    def test_view_attendance_other_user(self):
        result = view_attendance(2, ("2024-06-01", "2024-06-03"))
        self.assertEqual(len(result), 1)

    def test_invalid_date_range(self):
        result = view_attendance(1, ("2024-06-05", "2024-06-01"))
        self.assertEqual(result, [])