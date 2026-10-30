from datetime import date, timedelta
import pandas as pd


def calculate_streak(habits, habit_name, today=None):
    if today is None:
        today = date.today()
    elif isinstance(today, str):
        today = date.fromisoformat(today)

    completed_dates = set()

    for habit in habits:
        if habit["name"] == habit_name and habit["completed"]:
            try:
                completed_date = date.fromisoformat(habit["date"])
            except (ValueError, TypeError):
                continue

            completed_dates.add(completed_date)

    if not completed_dates:
        return 0

    # A streak may end today or yesterday.
    current_day = (
        today if today in completed_dates
        else today - timedelta(days=1)
    )

    streak = 0

    while current_day in completed_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


def weekly_habit_report(habits):
    """Calculate weekly habit completion statistics."""

    if not habits:
        return {}

    data = pd.DataFrame(habits)

    data["date"] = pd.to_datetime(
        data["date"], errors="coerce"
    )

    data = data.dropna(subset=["date"])

    if data.empty:
        return {}

    data["completed"] = data["completed"].astype(bool)

    data["week"] = (
        data["date"]
        .dt.to_period("W")
        .astype(str)
    )

    report = data.groupby("week").agg(
        total_habits=("completed", "count"),
        completed_habits=("completed", "sum")
    )

    report["completion_rate"] = (
        report["completed_habits"]
        / report["total_habits"]
        * 100
    ).round(1)

    return report.to_dict("index")
