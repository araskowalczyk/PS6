from models import LeaveRequest
from datetime import datetime

leave_requests = []

def submit_leave_request(user_id, start_date, end_date, reason):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        if start > end:
            return False
    except ValueError:
        return False

    new_request = LeaveRequest(
        request_id=len(leave_requests) + 1,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        status="oczekujacy"
    )
    leave_requests.append(new_request)
    return True

def approve_leave_request(request_id):
    for request in leave_requests:
        if request.request_id == request_id:
            if request.status == "oczekujacy":
                request.status = "zatwierdzony"
                return True
            return False  # nie można zatwierdzić już rozpatrzonego wniosku
    return False  # brak wniosku o podanym ID

def reject_leave_request(request_id):
    for request in leave_requests:
        if request.request_id == request_id:
            if request.status == "oczekujacy":
                request.status = "odrzucony"
                return True
            return False
    return False