
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def create_category_chart(expenses):
    """Create and save a chart of spending by category."""
    totals = category_totals(expenses)

    # Create the folder if it does not exist.
    os.makedirs("static", exist_ok=True)

    chart_path = os.path.join("static", "category_chart.png")

    if not totals:
        if os.path.exists(chart_path):
            os.remove(chart_path)
        return None

    categories = list(totals.keys())
    amounts = list(totals.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts)
    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (GHS)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(chart_path)
    plt.close()

    return chart_path



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
