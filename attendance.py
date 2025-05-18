from models import Attendance
from datetime import datetime

attendance_records = []

def view_attendance(user_id, date_range):
    start, end = date_range
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if start_date > end_date:
            return []
    except ValueError:
        return []

    return [
        record for record in attendance_records
        if record.user_id == user_id and start <= record.date <= end
    ]
