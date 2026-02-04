import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# 🔐 خپل BOT TOKEN دلته واچوه
# =========================
TOKEN = "7975528068:AAGRjVzq88d4I7pz-cJiqr_f4wcy97gk34k"

# =========================
# DATA STORAGE (per user)
# =========================
USER_EMAILS = {}

DOMAINS = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net"
]

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[d] for d in DOMAINS]
    await update.message.reply_text(
        "سلام 👋\n"
        "FakeSalarGmailBot ته ښه راغلې ✅\n\n"
        "د ایمیل جوړولو لپاره domain انتخاب کړه 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =========================
# GENERATE EMAIL
# =========================
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[d] for d in DOMAINS]
    await update.message.reply_text(
        "domain انتخاب کړه 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =========================
# HANDLE DOMAIN SELECTION
# =========================
async def handle_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domain = update.message.text
    user_id = update.message.from_user.id

    if domain not in DOMAINS:
        await update.message.reply_text("❌ ناسم domain")
        return

    url = f"https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1&domain={domain}"
    email = requests.get(url).json()[0]

    if user_id not in USER_EMAILS:
        USER_EMAILS[user_id] = []

    USER_EMAILS[user_id].append(email)

    await update.message.reply_text(
        f"📧 ایمیل جوړ شو:\n\n{email}"
    )

# =========================
# SHOW USER EMAIL IDS
# =========================
async def show_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in USER_EMAILS or not USER_EMAILS[user_id]:
        await update.message.reply_text("❌ ته تر اوسه هیڅ ایمیل نه لرې")
        return

    text = "📂 ستا ټول ایمیلونه:\n\n"
    for i, mail in enumerate(USER_EMAILS[user_id], start=1):
        text += f"{i}. {mail}\n"

    await update.message.reply_text(text)

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("id", show_ids))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_domain))

    print("✅ Fake Mail Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
