from dao.IFinanceRepository import IFinanceRepository
from entity.User import User
from entity.Expense import Expense
from util.DBConnUtil import getConnection
from exception.UserNotFoundException import UserNotFoundException
from exception.ExpenseNotFoundException import ExpenseNotFoundException

class FinanceRepositoryImpl(IFinanceRepository):

    def createUser(self, user: User) -> int:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)"
            values = (user.get_username(), user.get_password(), user.get_email())
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def loginUser(self, username: str, password: str) -> int:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM Users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Login error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def createExpense(self, expense: Expense) -> bool:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                INSERT INTO Expenses (user_id, amount, category_id, date, description)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                expense.get_user_id(),
                expense.get_amount(),
                expense.get_category_id(),
                expense.get_expense_date(),
                expense.get_description()
            )
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def getExpenseReport(self, user_id: int, from_date: str, to_date: str) -> list:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            query = """
                SELECT expense_id, amount, date, description
                FROM Expenses
                WHERE user_id = %s AND date BETWEEN %s AND %s
            """
            cursor.execute(query, (user_id, from_date, to_date))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error generating report: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def getAllCategories(self) -> list:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, category_name FROM ExpenseCategories")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def deleteUser(self, user_id: int) -> bool:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            if cursor.fetchone() is None:
                raise UserNotFoundException(user_id)

            cursor.execute("DELETE FROM Expenses WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            conn.commit()
            return True
        except UserNotFoundException as ue:
            raise ue
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def deleteExpense(self, expense_id: int) -> bool:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s", (expense_id,))
            if cursor.fetchone() is None:
                raise ExpenseNotFoundException(expense_id)

            cursor.execute("DELETE FROM Expenses WHERE expense_id = %s", (expense_id,))
            conn.commit()
            return True
        except ExpenseNotFoundException as ee:
            raise ee
        except Exception as e:
            print(f"Error deleting expense: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def getAllExpenses(self, user_id: int) -> list:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT expense_id, amount, category_id, date, description
                FROM Expenses
                WHERE user_id = %s
            """, (user_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching expenses: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def updateExpense(self, user_id: int, expense: Expense) -> bool:
        try:
            conn = getConnection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s AND user_id = %s",
                           (expense.get_expense_id(), user_id))
            if cursor.fetchone() is None:
                raise ExpenseNotFoundException(expense.get_expense_id())

            query = """
                UPDATE Expenses
                SET amount = %s, category_id = %s, date = %s, description = %s
                WHERE expense_id = %s AND user_id = %s
            """
            values = (
                expense.get_amount(),
                expense.get_category_id(),
                expense.get_expense_date(),
                expense.get_description(),
                expense.get_expense_id(),
                user_id
            )
            cursor.execute(query, values)
            conn.commit()
            return True
        except ExpenseNotFoundException as ee:
            raise ee
        except Exception as e:
            print(f"Error updating expense: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
