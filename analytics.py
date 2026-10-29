
import pandas as pd


def category_totals(expenses):
    """Calculate total spending for each expense category."""
    if not expenses:
        return {}

    data = pd.DataFrame([
        {
            "category": expense.category,
            "amount": expense.amount
        }
        for expense in expenses
    ])

    totals = data.groupby("category")["amount"].sum()
    return totals.sort_values(ascending=False).to_dict()


def weekly_spending(expenses):
    """Calculate total spending for each week."""
    if not expenses:
        return {}

    data = pd.DataFrame([
        {
            "date": expense.date,
            "amount": expense.amount
        }
        for expense in expenses
    ])

    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data = data.dropna(subset=["date"])

    if data.empty:
        return {}

    data["week"] = (
        data["date"]
        .dt.to_period("W")
        .astype(str)
    )

    totals = data.groupby("week")["amount"].sum()
    return totals.to_dict()
