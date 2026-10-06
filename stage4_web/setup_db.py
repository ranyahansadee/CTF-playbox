import sqlite3

conn = sqlite3.connect("company.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS employees")
cur.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    email TEXT
)
""")

cur.execute("DROP TABLE IF EXISTS admin_sessions")
cur.execute("""
CREATE TABLE admin_sessions (
    id INTEGER PRIMARY KEY,
    username TEXT,
    session_token TEXT
)
""")

employees = [
    (1, "David Perera", "Engineering", "david@easycloud.com"),
    (2, "Priyani Fernando", "Engineering", "pfernando@easycloud.com"),
    (3, "Dinesh Peris", "IT Support", "dperis@easycloud.com"),
    (4, "Amaya Silva", "HR", "asilva@easycloud.com"),
]
cur.executemany("INSERT INTO employees VALUES (?,?,?,?)", employees)

cur.execute("INSERT INTO admin_sessions VALUES (?,?,?)",
            (1, "admin", "sess_8f3a1c9e2b7d4f60"))

conn.commit()
conn.close()
print("Database created.")
