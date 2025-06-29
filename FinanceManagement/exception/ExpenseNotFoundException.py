class ExpenseNotFoundException(Exception):
    def __init__(self, message="Expense not found"):
        super().__init__(message)
