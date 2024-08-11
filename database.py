import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT,
                    cost INTEGER,
                    category TEXT,
                    date TEXT)''')
    conn.commit()
    conn.close()

def add_expense(item, cost, category, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (item, cost, category, date) VALUES (?, ?, ?, ?)",
              (item, cost, category, date))
    conn.commit()
    conn.close()

def get_expenses(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT item, cost, category, date FROM expenses WHERE date BETWEEN ? AND ?",
              (start_date, end_date))
    expenses = c.fetchall()
    conn.close()
    return expenses

def get_total_expenses(start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT SUM(cost) FROM expenses WHERE date BETWEEN ? AND ?",
              (start_date, end_date))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0
def clear_all_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
def add_user(chat_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY)")
    c.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT chat_id FROM users")
    users = c.fetchall()
    conn.close()
    return [user[0] for user in users]