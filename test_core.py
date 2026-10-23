
import pytest
import database

from database import create_table, create_connection
from models import Expense, Habit
from tracker import Tracker


@pytest.fixture
def setup_tracker(tmp_path, monkeypatch):
    # Give each test its own database
    test_db = tmp_path / "test_finance.db"
    monkeypatch.setattr(database, "DATABASE", str(test_db))

    create_table()

    conn = create_connection()
    conn.execute(
        """
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """,
        ("test_user", "test_password")
    )
    conn.commit()

    user = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        ("test_user",)
    ).fetchone()

    user_id = user["id"]
    conn.close()

    return Tracker(), user_id


def test_add_and_get_expense(setup_tracker):
    tracker, user_id = setup_tracker

    expense = Expense(
        25, "Food", "Waakye", "2026-10-20"
    )

    tracker.add_expense(user_id, expense)
    expenses = tracker.get_expenses(user_id)

    assert len(expenses) == 1
    assert expenses[0].amount == 25
    assert expenses[0].category == "Food"


def test_summarise_by_category(setup_tracker):
    tracker, user_id = setup_tracker

    tracker.add_expense(
        user_id,
        Expense(25, "Food", "Waakye", "2026-10-20")
    )
    tracker.add_expense(
        user_id,
        Expense(15, "Food", "Rice", "2026-10-20")
    )
    tracker.add_expense(
        user_id,
        Expense(20, "Transport", "Taxi", "2026-10-20")
    )

    summary = tracker.summarise_by_category(user_id)

    assert summary["Food"] == 40
    assert summary["Transport"] == 20


def test_remove_expense(setup_tracker):
    tracker, user_id = setup_tracker

    tracker.add_expense(
        user_id,
        Expense(25, "Food", "Waakye", "2026-10-20")
    )

    conn = create_connection()
    row = conn.execute(
        "SELECT id FROM expenses WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()

    assert tracker.remove_expense(row["id"], user_id) is True
    assert tracker.get_expenses(user_id) == []


def test_add_and_complete_habit(setup_tracker):
    tracker, user_id = setup_tracker

    habit = Habit("Study Python", "2026-10-20")
    tracker.add_habit(user_id, habit)

    habits = tracker.get_habits(user_id)

    assert len(habits) == 1
    assert habits[0]["name"] == "Study Python"
    assert habits[0]["completed"] is False

    result = tracker.mark_habit_completed(
        habits[0]["id"], user_id
    )

    assert result is True
    assert tracker.get_habits(user_id)[0]["completed"] is True
