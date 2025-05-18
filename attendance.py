from database import get_connection
from datetime import datetime

def view_attendance(user_id, date_range):
    start, end = date_range
    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if start_date > end_date:
            return []
    except ValueError:
        return []

    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, user_id, date, status FROM attendance WHERE user_id = ? AND date BETWEEN ? AND ?",
        (user_id, start, end)
    )
    records = c.fetchall()
    conn.close()

    return records  # lista krotek: (id, user_id, date, status)
