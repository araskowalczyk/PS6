class User:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

class LeaveRequest:
    def __init__(self, request_id, user_id, start_date, end_date, reason, status):
        self.request_id = request_id
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        self.reason = reason
        self.status = status

class Attendance:
    def __init__(self, attendance_id, user_id, date, status):
        self.attendance_id = attendance_id
        self.user_id = user_id
        self.date = date
        self.status = status  # "obecny", "nieobecny", "urlop"
