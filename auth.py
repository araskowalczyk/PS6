users = []

def register_user(username, password, role):
    if not username or not password or role not in ["pracownik", "kierownik"]:
        return False
    for user in users:
        if user.username == username:
            return False
    new_user = User(len(users) + 1, username, password, role)
    users.append(new_user)
    return True
