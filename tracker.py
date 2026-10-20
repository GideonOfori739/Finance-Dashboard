from database import create_connection
from models import Expense, Habit


class Tracker:
    def __init__(self):
        self.expenses = []
        self.habits = []

    def add_expense(self, user_id, expense):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
            (user_id, expense.amount, expense.category, expense.description, expense.date)
        )
        conn.commit()
        conn.close()

    def remove_expense(self, expense_id, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?",
            (expense_id, user_id)
        )
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        return deleted_count > 0

    def summarise_by_category(self, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT category, SUM(amount)AS total 
            FROM expenses 
            WHERE user_id = ? 
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return {row["category"]: row["total"] for row in rows}

    def add_habit(self, user_id, habit):
        conn =  create_connection()

        conn.execute("""
        INSERT INTO habits (user_id, name, date, completed)
          VALUES (?, ?, ?, ?)
        """, (user_id, habit.name, habit.date, habit.completed))
        conn.commit()
        conn.close()


    def get_habits(self, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT id, name, date, completed FROM habits
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,)).fetchall()
        conn.close()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "date": row["date"],
                "completed": bool(row["completed"])
            }
            for row in rows
        ]
    

    def mark_habit_completed(self, habit_id, user_id):
        conn = create_connection()

        cursor = conn.execute("""
            UPDATE habits
            SET completed = 1
            WHERE id = ? AND user_id = ?
        """, (habit_id, user_id))
        conn.commit()
        updated = cursor.rowcount
        conn.close()
        return updated > 0



    def remove_habit(self, habit_id, user_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM habits
            WHERE id = ? AND user_id = ?
        """, (habit_id, user_id))
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        return deleted_count > 0

if __name__ == "__main__":
    from models import Expense
    tracker = Tracker()
    expense = Expense(25, "Food", "Waakye", "2026-10-14")

    tracker.add_expense(
        user_id=1,
        expense=expense
    )

    
    print(tracker.expenses)
    print(tracker.summarise_by_category(user_id=1))