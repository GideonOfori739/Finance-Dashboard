
from database import create_connection, DATABASE_URL
from models import Expense, Habit


# SQLite uses ?, PostgreSQL uses %s
PLACEHOLDER = "%s" if DATABASE_URL else "?"


class Tracker:
    def __init__(self):
        self.expenses = []
        self.habits = []

    def get_expenses(self, user_id):
        conn = create_connection()

        try:
            rows = conn.execute(
                f"""
                SELECT id, amount, category, description, date
                FROM expenses
                WHERE user_id = {PLACEHOLDER}
                ORDER BY date DESC, id DESC
                """,
                (user_id,)
            ).fetchall()

            expenses = []

            for row in rows:
                expense = Expense(
                    id=row["id"],
                    amount=row["amount"],
                    category=row["category"],
                    description=row["description"],
                    date=row["date"]
                )
                expenses.append(expense)

            return expenses

        finally:
            conn.close()

    def add_expense(self, user_id, expense):
        conn = create_connection()

        try:
            conn.execute(
                f"""
                INSERT INTO expenses
                (user_id, amount, category, description, date)
                VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER},
                        {PLACEHOLDER}, {PLACEHOLDER})
                """,
                (
                    user_id,
                    expense.amount,
                    expense.category,
                    expense.description,
                    expense.date
                )
            )
            conn.commit()

        finally:
            conn.close()

    def remove_expense(self, expense_id, user_id):
        conn = create_connection()

        try:
            cursor = conn.execute(
                f"""
                DELETE FROM expenses
                WHERE id = {PLACEHOLDER} AND user_id = {PLACEHOLDER}
                """,
                (expense_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def summarise_by_category(self, user_id):
        conn = create_connection()

        try:
            rows = conn.execute(
                f"""
                SELECT category, SUM(amount) AS total
                FROM expenses
                WHERE user_id = {PLACEHOLDER}
                GROUP BY category
                ORDER BY total DESC
                """,
                (user_id,)
            ).fetchall()

            return {
                row["category"]: row["total"]
                for row in rows
            }

        finally:
            conn.close()

    def add_habit(self, user_id, habit):
        conn = create_connection()

        try:
            conn.execute(
                f"""
                INSERT INTO habits (user_id, name, date, completed)
                VALUES ({PLACEHOLDER}, {PLACEHOLDER},
                        {PLACEHOLDER}, {PLACEHOLDER})
                """,
                (
                    user_id,
                    habit.name,
                    habit.date,
                    habit.completed
                )
            )
            conn.commit()

        finally:
            conn.close()

    def get_habits(self, user_id):
        conn = create_connection()

        try:
            rows = conn.execute(
                f"""
                SELECT id, name, date, completed
                FROM habits
                WHERE user_id = {PLACEHOLDER}
                ORDER BY date DESC
                """,
                (user_id,)
            ).fetchall()

            return [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "date": row["date"],
                    "completed": bool(row["completed"])
                }
                for row in rows
            ]

        finally:
            conn.close()

    def mark_habit_completed(self, habit_id, user_id):
        conn = create_connection()

        try:
            cursor = conn.execute(
                f"""
                UPDATE habits
                SET completed = {PLACEHOLDER}
                WHERE id = {PLACEHOLDER}
                AND user_id = {PLACEHOLDER}
                """,
                (True, habit_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()

    def remove_habit(self, habit_id, user_id):
        conn = create_connection()

        try:
            cursor = conn.execute(
                f"""
                DELETE FROM habits
                WHERE id = {PLACEHOLDER}
                AND user_id = {PLACEHOLDER}
                """,
                (habit_id, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

        finally:
            conn.close()
