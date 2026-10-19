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

    def remove_expense(self, expense):
        if expense in self.expenses:
            self.expenses.remove(expense)

    def summarise_by_category(self):
        categories = {
            expense.category
            for expense in self.expenses
        }
        summary = {
            category: sum(
                expense.amount
                for expense in self.expenses
                if expense.category == category
            )
            for category in categories
        }
        return summary

    def add_habit(self, habit):
        self.habits.append(habit)

    def remove_habit(self, habit):
        if habit in self.habits:
            self.habits.remove(habit)

if __name__ == "__main__":
    from models import Expense
    tracker = Tracker()
    expense = Expense(25, "Food", "Waakye", "2026-10-14")

    tracker.add_expense(
        user_id=1,
        expense=expense
    )
    
    print(tracker.expenses)
    print(tracker.summarise_by_category())