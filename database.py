import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    # Create users table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 chat_id INTEGER UNIQUE)''')

    # Create expenses table with a user_id column
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 item TEXT,
                 cost INTEGER,
                 category TEXT,
                 date TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')

    # Create a table to store reminder status for each user
    c.execute('''CREATE TABLE IF NOT EXISTS reminder_status (
                 user_id INTEGER PRIMARY KEY,
                 status TEXT,
                 FOREIGN KEY(user_id) REFERENCES users(id))''')

    conn.commit()
    conn.close()

def add_user(chat_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def get_user_id(chat_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT id FROM users WHERE chat_id = ?", (chat_id,))
    user_id = c.fetchone()

    conn.close()
    return user_id[0] if user_id else None

def add_expense(user_id, item, cost, category, date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("INSERT INTO expenses (user_id, item, cost, category, date) VALUES (?, ?, ?, ?, ?)",
              (user_id, item, cost, category, date))
    conn.commit()
    conn.close()

def get_expenses(user_id, start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT item, cost, category, date FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?",
              (user_id, start_date, end_date))
    expenses = c.fetchall()

    conn.close()
    return expenses

def get_total_expenses(user_id, start_date, end_date):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT SUM(cost) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?",
              (user_id, start_date, end_date))
    total = c.fetchone()[0]

    conn.close()
    return total if total else 0

def clear_all_expenses(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def set_reminder_status(user_id, status):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("INSERT OR REPLACE INTO reminder_status (user_id, status) VALUES (?, ?)", (user_id, status))
    conn.commit()
    conn.close()

def get_reminder_status(user_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    c.execute("SELECT status FROM reminder_status WHERE user_id = ?", (user_id,))
    status = c.fetchone()

    conn.close()
    return status[0] if status else None
