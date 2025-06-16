from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

# لیست ساده برای ذخیره شناسه یکتای کاربران
unique_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    unique_users.add(user_id)
    
    await update.message.reply_text("سلام! متن انگلیسی بفرست تا برات ترجمه کنم.")
    # await update.message.reply_text(f"تعداد کاربرانی که تاکنون بات را استارت زده‌اند: {len(unique_users)}")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = GoogleTranslator(source='en', target='fa').translate(text)
    await update.message.reply_text(translated)

# توکن به صورت هاردکد شده
BOT_TOKEN = "8166245312:AAHS577hLSkHSIGaaI4d0rBBfNuwGSYTldU"

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

app.run_polling()
