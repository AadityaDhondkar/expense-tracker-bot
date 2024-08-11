from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from apscheduler.schedulers.background import BackgroundScheduler
from database import init_db, add_expense, get_expenses, get_total_expenses, clear_all_expenses, add_user, get_user_id, set_reminder_status, get_reminder_status
import datetime
import sqlite3

# Initialize the database
init_db()

# Handler functions
async def start(update: Update, context):
    chat_id = update.message.chat_id
    add_user(chat_id)  # Store the chat ID when the user starts
    await update.message.reply_text(
        "Welcome! You can track your expenses here. Use '/add <item> - <cost> - <category>' to add expenses, '/report' to get reports, '/reminder' to set reminders, and '/clear' to clear all expenses."
    )

async def add_expense_handler(update: Update, context):
    chat_id = update.message.chat_id
    user_id = get_user_id(chat_id)
    if not user_id:
        await update.message.reply_text("User not found. Please use /start to initialize.")
        return

    message = update.message.text.strip()
    try:
        # Split the message using the hyphen as a delimiter, handling any extra spaces
        parts = [part.strip() for part in message.split('-')]

        if len(parts) != 3:
            raise ValueError("Invalid format")

        item = parts[0]
        cost = int(parts[1])
        category = parts[2]
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        add_expense(user_id, item, cost, category, date)
        await update.message.reply_text(f"Added: {item} - {cost}rs - {category}")
    except ValueError:
        await update.message.reply_text("Please use the format: Item - Cost - Category")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def report(update: Update, context):
    chat_id = update.message.chat_id
    user_id = get_user_id(chat_id)
    if not user_id:
        await update.message.reply_text("User not found. Please use /start to initialize.")
        return

    today = datetime.datetime.now()
    start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    
    expenses = get_expenses(user_id, start_date, end_date)
    total = get_total_expenses(user_id, start_date, end_date)
    
    report_msg = "Expense Report (Last 30 Days):\n\n"
    for item, cost, category, date in expenses:
        report_msg += f"{date} - {item} - {cost}rs - {category}\n"
    report_msg += f"\nTotal Expenses: {total}rs"

    await update.message.reply_text(report_msg)

async def set_reminder(update: Update, context):
    chat_id = update.message.chat_id
    user_id = get_user_id(chat_id)
    if not user_id:
        await update.message.reply_text("User not found. Please use /start to initialize.")
        return

    set_reminder_status(user_id, "enabled")  # Enable reminders
    await update.message.reply_text("Reminder set! I'll remind you daily to log your expenses.")

async def clear_all(update: Update, context):
    chat_id = update.message.chat_id
    user_id = get_user_id(chat_id)
    if not user_id:
        await update.message.reply_text("User not found. Please use /start to initialize.")
        return

    clear_all_expenses(user_id)  # Clear all expenses and disable reminders
    set_reminder_status(user_id, "disabled")
    await update.message.reply_text("All expenses have been cleared and reminders are disabled.")

def send_daily_reminder():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT user_id FROM reminder_status WHERE status = 'enabled'")
    user_ids = c.fetchall()
    conn.close()

    for user_id in user_ids:
        message = "Reminder: Please log your expenses for today!"
        application.bot.send_message(chat_id=user_id[0], text=message)

def main():
    global application
    application = Application.builder().token("7306549702:AAEnPWhtGU-4DVRjloPW-g1Z-4kRc_oAu0I").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense_handler))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("reminder", set_reminder))
    application.add_handler(CommandHandler("clear", clear_all))

    # Set up the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_reminder, 'interval', days=1)
    scheduler.start()

    application.run_polling()

if __name__ == '__main__':
    main()
