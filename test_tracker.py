
from database import create_table, create_connection
from models import Expense, Habit
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

print("Expenses:", tracker.add_expense(user_id=1, expense=expense))
print("Category Summary:", tracker.summarise_by_category(user_id=1))

conn = create_connection()
rows = conn.execute("""
    SELECT id FROM expenses
    WHERE user_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (user_id,)).fetchall()
conn.close()

if rows:
    deleted = tracker.remove_expense(rows[0]["id"], user_id)
    print("Expense removed:", deleted)

habit = Habit(
    "Exercise",
    "2026-10-14",
    
)
tracker.add_habit(user_id, habit)

habits = tracker.get_habits(user_id)
print("Habits:", habits)

if habits:
    habit_id = habits[0]["id"]
    result = tracker.mark_habit_completed(habit_id, user_id)
    print("Habit marked as completed:", result)

    removed = tracker.remove_habit(habit_id, user_id)
    print("Habit removed:", removed)