import sqlite3

conn = sqlite3.connect("chat.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (sender TEXT, message TEXT)")

def register_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

def save_message(sender, message):
    c.execute("INSERT INTO messages VALUES (?, ?)", (sender, message))
    conn.commit()
