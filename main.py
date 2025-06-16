import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

# توکن ربات (هاردکد)
BOT_TOKEN = "8166245312:AAHS577hLSkHSIGaaI4d0rBBfNuwGSYTldU"

# لیست کاربران یکتا
unique_users = set()

# ----------------------------
# تنظیمات بات تلگرام
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    unique_users.add(user_id)
    await update.message.reply_text("سلام! متن انگلیسی بفرست تا برات ترجمه کنم.")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = GoogleTranslator(source='en', target='fa').translate(text)
    await update.message.reply_text(translated)

async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"تعداد کاربران یکتا: {len(unique_users)}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("count", count))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    app.run_polling()

# ----------------------------
# وب‌سرور Flask برای زنده نگه‌داشتن
# ----------------------------
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "🤖 ربات تلگرام آنلاین است!"

# ----------------------------
# اجرای موازی بات + وب‌سرور
# ----------------------------
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    web_app.run(host="0.0.0.0", port=8080)
