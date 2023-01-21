import sqlite3 as db

conn = db.connect("oakridge-codefest/oakridge-codefest.db")
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS user_credentials (
        username TEXT NOT NULL PRIMARY KEY,
        password TEXT NOT NULL
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

c.close()
conn.close()