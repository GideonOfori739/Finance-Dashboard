
from database import create_table, create_connection
from models import Expense
from tracker import Tracker


create_table()

conn = create_connection()

conn.execute(
    "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
    ("test_user", "password123")
)
conn.commit()

user = conn.execute(
    "SELECT * FROM users WHERE username = ?",
    ("test_user",)
).fetchone()
user_id = user["id"]
conn.close()

tracker = Tracker()

expense = Expense(
    25,
    "Food",
    "Waakye",
    "2026-10-14"
)

tracker.add_expense(user_id= 1, expense=expense)



conn = create_connection()

rows = conn.execute(
    "SELECT * FROM expenses WHERE user_id = ?",
    (user_id,)
).fetchall()

for row in rows:
    print(dict(row))

conn.close()
