class Expense:
    def __init__(self, amount, category, description, date,  id=None):
        self.id = id if id is not None else self.generate_id()
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def generate_id(self):
        # Placeholder for ID generation logic
        pass

    def __str__(self):
        return f"{self.category}: {self.amount} - {self.description} ({self.date})"

class Habit:
    def __init__(self, name, date, completed=False):
        self.name = name
        self.date = date
        self.completed = completed

    def __str__(self):
        return f"{self.name} - {self.date} (Completed: {self.completed})"