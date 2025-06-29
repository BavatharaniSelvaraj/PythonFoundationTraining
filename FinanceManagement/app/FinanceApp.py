import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.FinanceRepositoryImpl import FinanceRepositoryImpl
from entity.User import User
from entity.Expense import Expense
from exception.UserNotFoundException import UserNotFoundException
from exception.ExpenseNotFoundException import ExpenseNotFoundException

def main():
    repo = FinanceRepositoryImpl()
    logged_in_user_id = None

    while True:
        print("\n===== Finance Management System =====")
        print("1. Register (Add User)")
        print("2. Login")
        print("3. Add Expense")
        print("4. Delete User")
        print("5. Delete Expense")
        print("6. Update Expense")
        print("7. View All Expenses")
        print("8. Generate Expense Report")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                email = input("Enter email: ")
                user = User(None, username, password, email)
                user_id = repo.createUser(user)
                if user_id:
                    print(f"User registered successfully! Your user ID is: {user_id}")
                else:
                    print("Failed to register user.")

            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user_id = repo.loginUser(username, password)
                if user_id:
                    logged_in_user_id = user_id
                    print(f"Login successful! Welcome, {username}.")
                else:
                    print("Invalid username or password.")

            elif choice == "3":
                if not logged_in_user_id:
                    print("Please login first.")
                    continue

                print("Available Categories:")
                for cat in repo.getAllCategories():
                    print(f"{cat[0]}. {cat[1]}")

                amount = float(input("Enter amount: "))
                category_id = int(input("Enter category ID: "))
                date = input("Enter date (YYYY-MM-DD): ")
                desc = input("Enter description: ")

                exp = Expense(None, logged_in_user_id, amount, category_id, date, desc)
                if repo.createExpense(exp):
                    print("Expense added successfully!")
                else:
                    print("Failed to add expense.")

            elif choice == "4":
                uid = int(input("Enter user ID to delete: "))
                if repo.deleteUser(uid):
                    print("User deleted.")
                    if logged_in_user_id == uid:
                        logged_in_user_id = None
                else:
                    print("User deletion failed.")

            elif choice == "5":
                eid = int(input("Enter expense ID to delete: "))
                if repo.deleteExpense(eid):
                    print("Expense deleted.")
                else:
                    print("Expense deletion failed.")

            elif choice == "6":
                if not logged_in_user_id:
                    print("Please login first.")
                    continue

                eid = int(input("Enter expense ID to update: "))
                amt = float(input("Enter new amount: "))
                print("Available Categories:")
                for cat in repo.getAllCategories():
                    print(f"{cat[0]}. {cat[1]}")
                cid = int(input("Enter new category ID: "))
                date = input("Enter new date: ")
                desc = input("Enter new description: ")

                exp = Expense(eid, logged_in_user_id, amt, cid, date, desc)
                if repo.updateExpense(logged_in_user_id, exp):
                    print("Expense updated.")
                else:
                    print("Update failed.")

            elif choice == "7":
                if not logged_in_user_id:
                    print("Please login first.")
                    continue

                expenses = repo.getAllExpenses(logged_in_user_id)
                if expenses:
                    print("\nID | Amount | Category | Date | Description")
                    print("-"*50)
                    for e in expenses:
                        print(f"{e[0]} | {e[1]} | {e[2]} | {e[3]} | {e[4]}")
                else:
                    print("No expenses found.")

            elif choice == "8":
                if not logged_in_user_id:
                    print("Please login first.")
                    continue

                from_date = input("Enter start date (YYYY-MM-DD): ")
                to_date = input("Enter end date (YYYY-MM-DD): ")
                report = repo.getExpenseReport(logged_in_user_id, from_date, to_date)
                if report:
                    print("\nID | Amount | Date | Description")
                    print("-"*50)
                    for r in report:
                        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
                else:
                    print("No expenses found in the selected range.")

            elif choice == "0":
                print("Thank you for using Finance Management System!")
                break

            else:
                print("Invalid choice.")

        except (UserNotFoundException, ExpenseNotFoundException) as e:
            print(e)
        except Exception as ex:
            print(f"Unexpected error: {ex}")

if __name__ == "__main__":
    main()
