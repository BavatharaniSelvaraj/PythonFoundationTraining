import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from dao.FinanceRepositoryImpl import FinanceRepositoryImpl
from entity.User import User
from entity.Expense import Expense
from exception.UserNotFoundException import UserNotFoundException
from exception.ExpenseNotFoundException import ExpenseNotFoundException
import datetime

class TestFinanceApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.repo = FinanceRepositoryImpl()

        # Add a test user before running tests
        cls.test_user = User(None, "unit_test_user", "pass123", "unit@test.com")
        cls.repo.createUser(cls.test_user)

        # Manually retrieve the user_id (assuming auto-increment)
        # You can implement a get_user_by_email() in your repo for real use
        users = cls.repo.getAllExpenses(1)
        cls.test_user_id = 1  # Update this appropriately if needed

    def test_user_creation(self):
        user = User(None, "demo_test_user", "pass456", "demo@test.com")
        result = self.repo.createUser(user)
        self.assertTrue(result)

    def test_expense_creation(self):
        expense = Expense(
            None,
            self.test_user_id,
            100.0,
            1,
            datetime.date.today().strftime("%Y-%m-%d"),
            "Unit test expense"
        )
        result = self.repo.createExpense(expense)
        self.assertTrue(result)

    def test_get_expenses_list(self):
        expenses = self.repo.getAllExpenses(self.test_user_id)
        self.assertIsInstance(expenses, list)

    def test_delete_invalid_user(self):
        with self.assertRaises(UserNotFoundException):
            self.repo.deleteUser(99999)  # Non-existent user

    def test_delete_invalid_expense(self):
        with self.assertRaises(ExpenseNotFoundException):
            self.repo.deleteExpense(99999)  # Non-existent expense

if __name__ == '__main__':
    unittest.main()
