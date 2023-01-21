import sqlite3 as db

conn = db.connect("oakridge-codefest/oakridge-codefest.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS user_credentials (
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        title STRING NOT NULL,
        description STRING,
        date STRING NOT NULL,
        time STRING NOT NULL,
        location STRING,
        attendees STRING
    )
''')
conn.commit()

def user_login(username, password):
    conn = db.connect("oakridge-codefest/oakridge-codefest.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM user_credentials WHERE username = '{username}'")
    record = c.fetchone()
    if not record:
        return False
    elif password != record[1]:
        c.close()
        conn.close()
        return False
    c.close()
    conn.close()
    return True

def user_signup(username, password):
    conn = db.connect("oakridge-codefest/oakridge-codefest.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM user_credentials WHERE username = '{username}'")
    record = c.fetchone()
    if not record:
        c.execute(f"INSERT INTO user_credentials VALUES ('{username}', '{password}')")
        conn.commit()
        c.close()
        conn.close()
        return True
    c.close()
    conn.close()
    return False

def new_event(username, title, description, date, time, location):
    conn = db.connect("oakridge-codefest/oakridge-codefest.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO events (username, title, description, date, time, location) VALUES ('{username}', {title}, {description}, {date}, {time}, {location})")
    conn.commit()
    c.close()
    conn.close()

def get_event(id = None):
    conn = db.connect("oakridge-codefest/oakridge-codefest.db")
    c = conn.cursor()
    if not id:
        c.execute("SELECT * FROM events")
        data = c.fetchall()
    else:
        c.execute(f"SELECT * FROM events WHERE id = {id}")
        data = c.fetchone()
    c.close()
    conn.close()
    return data

def join_event(id, username):
    conn = db.connect("oakridge-codefest/oakridge-codefest.db")
    c = conn.cursor()
    c.execute(f"SELECT attendees FROM events WHERE id = {id}")
    attendees = c.fetchone()
    if attendees:
        attendees += f",{username}"
    else:
        attendees = username
    c.execute(f"UPDATE TABLE events SET attendees = '{attendees}'")
    conn.commit()
    c.close()
    conn.close()

c.close()
conn.close()