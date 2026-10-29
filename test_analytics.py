
from analytics import category_totals, weekly_spending
from models import Expense


def test_category_totals():
    expenses = [
        Expense(50, "Food", "Lunch", "2026-10-26"),
        Expense(30, "Transport", "Taxi", "2026-10-27"),
        Expense(20, "Food", "Breakfast", "2026-10-27"),
    ]

    result = category_totals(expenses)

    assert result["Food"] == 70
    assert result["Transport"] == 30


def test_weekly_spending():
    expenses = [
        Expense(50, "Food", "Lunch", "2026-10-26"),
        Expense(30, "Transport", "Taxi", "2026-10-27"),
    ]

    result = weekly_spending(expenses)

    assert sum(result.values()) == 80
