class Expense:
    def __init__(self, amount, category, description, date):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __str__(self):
        return f"{self.category}: {self.amount} - {self.description} ({self.date})"

class Habit:
    def __init__(self, name, date, completed=False):
        self.name = name
        self.date = date
        self.completed = completed

    def __str__(self):
        return f"{self.name} - {self.date} (Completed: {self.completed})"