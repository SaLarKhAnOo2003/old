from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ BOT TOKEN
TOKEN = "7975528068:AAGRjVzq88d4I7pz-cJiqr_f4wcy97gk34k"

# ✅ ADMIN (ته)
ADMIN_ID = 5887665463

users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text(
        "سلام 👋\n"
        "دا FakeSalarGmailBot دی ✅\n"
        "بوت فعال شو"
    )

async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(f"ټول یوزران: {len(users)}")
    else:
        await update.message.reply_text("اجازه نه لرې ❌")

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        try:
            uid = int(context.args[0])
            users.discard(uid)
            await update.message.reply_text("یوزر ریموف شو ✅")
        except:
            await update.message.reply_text("سم ID ولیکه")
    else:
        await update.message.reply_text("اجازه نه لرې ❌")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", all_users))
app.add_handler(CommandHandler("remove", remove_user))

app.run_polling()
