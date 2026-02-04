import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================
# 🔐 BOT TOKEN
# =====================
TOKEN = "7975528068:AAGYqgmVZAA6MO63vleJjVvxavfXC5Trkto"

# =====================
# DOMAINS
# =====================
DOMAINS = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net"
]

# =====================
# USER DATA (RAM)
# =====================
USER_EMAILS = {}  # {user_id: [email1, email2...]}

# =====================
# START
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📧 Generate Email"],
        ["📂 My Emails"]
    ]
    await update.message.reply_text(
        "👋 سلام!\n"
        "FakeSalarGmailBot ته ښه راغلې ✅\n\n"
        "له Menu څخه انتخاب وکړه 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =====================
# GENERATE MENU
# =====================
async def generate_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[d] for d in DOMAINS]
    await update.message.reply_text(
        "🌐 domain انتخاب کړه 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =====================
# HANDLE DOMAIN
# =====================
async def handle_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domain = update.message.text
    user_id = update.effective_user.id

    if domain not in DOMAINS:
        return

    url = f"https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1&domain={domain}"
    email = requests.get(url).json()[0]

    USER_EMAILS.setdefault(user_id, []).append(email)

    await update.message.reply_text(
        f"✅ ایمیل جوړ شو:\n\n📧 {email}\n\n"
        "📥 Inbox لپاره ولیکه:\n/inbox 1"
    )

# =====================
# SHOW EMAIL LIST
# =====================
async def show_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in USER_EMAILS or not USER_EMAILS[user_id]:
        await update.message.reply_text("❌ ته تر اوسه ایمیل نه لرې")
        return

    text = "📂 ستا ټول ایمیلونه:\n\n"
    for i, mail in enumerate(USER_EMAILS[user_id], start=1):
        text += f"{i}. {mail}\n"

    text += "\n📥 Inbox مثال:\n/inbox 1"
    await update.message.reply_text(text)

# =====================
# INBOX
# =====================
async def inbox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not context.args:
        await update.message.reply_text("❌ کارول: /inbox 1")
        return

    idx = int(context.args[0]) - 1

    if user_id not in USER_EMAILS or idx >= len(USER_EMAILS[user_id]):
        await update.message.reply_text("❌ ناسم ایمیل نمبر")
        return

    email = USER_EMAILS[user_id][idx]
    login, domain = email.split("@")

    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    messages = requests.get(url).json()

    if not messages:
        await update.message.reply_text("📭 Inbox خالي دی")
        return

    text = "📥 Inbox:\n\n"
    for m in messages:
        text += f"🆔 {m['id']}\nFrom: {m['from']}\n📌 {m['subject']}\n\n"

    text += "📖 لوستلو لپاره:\n/read MESSAGE_ID"
    await update.message.reply_text(text)

# =====================
# READ EMAIL
# =====================
async def read_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ کارول: /read ID")
        return

    msg_id = context.args[0]

    for emails in USER_EMAILS.values():
        for email in emails:
            login, domain = email.split("@")
            url = (
                "https://www.1secmail.com/api/v1/"
                f"?action=readMessage&login={login}&domain={domain}&id={msg_id}"
            )
            r = requests.get(url)
            if r.status_code == 200 and "subject" in r.text:
                data = r.json()
                body = data.get("textBody") or data.get("htmlBody")
                await update.message.reply_text(
                    f"📧 From: {data['from']}\n"
                    f"📌 Subject: {data['subject']}\n\n{body}"
                )
                return

    await update.message.reply_text("❌ ایمیل ونه موندل شو")

# =====================
# MENU HANDLER
# =====================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "📧 Generate Email":
        await generate_menu(update, context)
    elif update.message.text == "📂 My Emails":
        await show_ids(update, context)

# =====================
# MAIN
# =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", show_ids))
    app.add_handler(CommandHandler("inbox", inbox))
    app.add_handler(CommandHandler("read", read_email))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_domain))

    print("✅ Fake Mail Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
