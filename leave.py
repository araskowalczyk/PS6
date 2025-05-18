from database import get_connection
from datetime import datetime

def submit_leave_request(user_id, start_date, end_date, reason):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        if start > end:
            return False
    except ValueError:
        return False

    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO leave_requests (user_id, start_date, end_date, reason, status) VALUES (?, ?, ?, ?, ?)",
        (user_id, start_date, end_date, reason, "oczekujacy")
    )
    conn.commit()
    conn.close()
    return True

def approve_leave_request(request_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT status FROM leave_requests WHERE id = ?", (request_id,))
    result = c.fetchone()
    if not result or result[0] != "oczekujacy":
        conn.close()
        return False
    c.execute("UPDATE leave_requests SET status = 'zatwierdzony' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()
    return True

def reject_leave_request(request_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT status FROM leave_requests WHERE id = ?", (request_id,))
    result = c.fetchone()
    if not result or result[0] != "oczekujacy":
        conn.close()
        return False
    c.execute("UPDATE leave_requests SET status = 'odrzucony' WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()
    return True
