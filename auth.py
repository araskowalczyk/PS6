from database import get_connection
from models import User

def register_user(username, password, role):
    if not username or not password or role not in ["pracownik", "kierownik"]:
        return False

    conn = get_connection()
    c = conn.cursor()

    # Sprawdzenie, czy użytkownik już istnieje
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False

    # Zapisanie nowego użytkownika do bazy
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              (username, password, role))
    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    row = c.fetchone()
    conn.close()

    if row:
        return User(*row)  # przekształć tuple w obiekt User
    return None
