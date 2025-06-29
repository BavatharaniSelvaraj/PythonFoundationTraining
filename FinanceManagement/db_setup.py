import mysql.connector

def create_tables():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Tharani@25"
        )
        cursor = conn.cursor()

        # Create database and use it
        cursor.execute("CREATE DATABASE IF NOT EXISTS finance_db")
        cursor.execute("USE finance_db")

        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100),
                password VARCHAR(100),
                email VARCHAR(100)
            )
        """)

        # Create ExpenseCategories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ExpenseCategories (
                category_id INT PRIMARY KEY,
                category_name VARCHAR(100) UNIQUE
            )
        """)

        # Create Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                expense_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                amount DECIMAL(10,2),
                category_id INT,
                date DATE,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES Users(user_id),
                FOREIGN KEY(category_id) REFERENCES ExpenseCategories(category_id)
            )
        """)

        # Insert default categories with known IDs
        default_categories = [
            ( 3, 'Food'),
            ( 6, 'Transportation'),
            (4, 'Medical'),
            ( 5, 'Shopping'),
            ( 2, 'Education'),
            ( 1, 'Child Care'),
        ]

        for category in default_categories:
            try:
                cursor.execute("""
                    INSERT INTO ExpenseCategories (category_id, category_name) 
                    VALUES (%s, %s)
                """, category)
            except mysql.connector.errors.IntegrityError:
                # Skip if already exists (duplicate entry)
                continue

        conn.commit()
        print("Database, tables, and default categories created successfully.")

    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    create_tables()
