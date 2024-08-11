from telegram.ext import Updater, MessageHandler, filters

def get_chat_id(update, context):
    chat_id = update.message.chat_id
    print(f"Chat ID: {chat_id}")

if __name__ == "__main__":
    updater = Updater("7306549702:AAEnPWhtGU-4DVRjloPW-g1Z-4kRc_oAu0I", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_chat_id))
    updater.start_polling()
    updater.idle()
