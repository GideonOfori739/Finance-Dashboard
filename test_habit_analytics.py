
from habit_analytics import calculate_streak


def test_three_day_streak():
    habits = [
        {"name": "Study Python", "date": "2026-10-27", "completed": True},
        {"name": "Study Python", "date": "2026-10-28", "completed": True},
        {"name": "Study Python", "date": "2026-10-29", "completed": True},
        {"name": "Exercise", "date": "2026-10-29", "completed": True},
    ]

    assert calculate_streak(
        habits, "Study Python", today="2026-10-29"
    ) == 3


def test_streak_can_end_yesterday():
    habits = [
        {"name": "Study Python", "date": "2026-10-27", "completed": True},
        {"name": "Study Python", "date": "2026-10-28", "completed": True},
    ]

    assert calculate_streak(
        habits, "Study Python", today="2026-10-29"
    ) == 2


def test_no_completed_habits():
    habits = [
        {"name": "Study Python", "date": "2026-10-29", "completed": False},
    ]

    assert calculate_streak(
        habits, "Study Python", today="2026-10-29"
    ) == 0



def test_weekly_habit_report():
    from habit_analytics import weekly_habit_report

    habits = [
        {"name": "Study", "date": "2026-10-26", "completed": True},
        {"name": "Exercise", "date": "2026-10-27", "completed": True},
        {"name": "Reading", "date": "2026-10-28", "completed": False},
        {"name": "Coding", "date": "2026-10-29", "completed": True},
    ]

    result = weekly_habit_report(habits)

    week_data = list(result.values())[0]

    assert week_data["total_habits"] == 4
    assert week_data["completed_habits"] == 3
    assert week_data["completion_rate"] == 75.0
