import requests
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =====================
# 🔐 BOT TOKEN (خپل نوی TOKEN دلته واچوه)
# =====================
TOKEN = "7975528068:AAGH-zHSVwc0xkUg9h0ePHK2nxYpcx99U4g"

# =====================
# 🌐 DOMAINS
# =====================
DOMAINS = ["1secmail.com", "1secmail.org", "1secmail.net"]

# =====================
# 💾 DATABASE (Permanent)
# =====================
db = sqlite3.connect("emails.db", check_same_thread=False)
cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS emails (
    user_id INTEGER,
    email TEXT
)
""")
db.commit()

# =====================
# 🧠 HELPERS
# =====================
def save_email(user_id, email):
    cur.execute("INSERT INTO emails (user_id, email) VALUES (?, ?)", (user_id, email))
    db.commit()

def get_user_emails(user_id):
    cur.execute("SELECT email FROM emails WHERE user_id = ?", (user_id,))
    return [row[0] for row in cur.fetchall()]

# =====================
# ▶️ START
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📧 Generate Email"],
        ["📂 My Emails"]
    ]
    await update.message.reply_text(
        "👋 سلام!\n"
        "FakeSalarGmailBot ته ښه راغلې ✅\n\n"
        "👇 له Menu څخه انتخاب وکړه",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =====================
# 📧 GENERATE MENU
# =====================
async def generate_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[d] for d in DOMAINS]
    await update.message.reply_text(
        "🌐 domain انتخاب کړه 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =====================
# 🌐 HANDLE DOMAIN
# =====================
async def handle_domain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domain = update.message.text
    user_id = update.effective_user.id

    if domain not in DOMAINS:
        return

    url = f"https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1&domain={domain}"
    email = requests.get(url, timeout=15).json()[0]

    save_email(user_id, email)

    await update.message.reply_text(
        f"✅ ایمیل جوړ شو:\n\n📧 {email}\n\n"
        "📥 inbox لپاره ولیکه:\n/inbox 1"
    )

# =====================
# 📂 SHOW EMAILS
# =====================
async def show_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    emails = get_user_emails(user_id)

    if not emails:
        await update.message.reply_text("❌ ته تر اوسه ایمیل نه لرې")
        return

    text = "📂 ستا ایمیلونه:\n\n"
    for i, mail in enumerate(emails, start=1):
        text += f"{i}. {mail}\n"

    text += "\n📥 inbox مثال:\n/inbox 1"
    await update.message.reply_text(text)

# =====================
# 📥 INBOX
# =====================
async def inbox(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    emails = get_user_emails(user_id)

    if not context.args:
        await update.message.reply_text("❌ کارول: /inbox 1")
        return

    try:
        index = int(context.args[0]) - 1
    except:
        await update.message.reply_text("❌ ناسم نمبر")
        return

    if index < 0 or index >= len(emails):
        await update.message.reply_text("❌ ناسم ایمیل نمبر")
        return

    email = emails[index]
    login, domain = email.split("@")

    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    messages = requests.get(url, timeout=15).json()

    if not messages:
        await update.message.reply_text("📭 inbox خالي دی")
        return

    text = "📥 Inbox:\n\n"
    for m in messages:
        text += f"🆔 {m['id']} | {m['from']}\n📌 {m['subject']}\n\n"

    text += "📖 لوستلو لپاره:\n/read MESSAGE_ID"
    await update.message.reply_text(text)

# =====================
# 📖 READ EMAIL
# =====================
async def read_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ کارول: /read ID")
        return

    msg_id = context.args[0]

    cur.execute("SELECT email FROM emails")
    all_emails = [row[0] for row in cur.fetchall()]

    for email in all_emails:
        login, domain = email.split("@")
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200 and "subject" in r.text:
            data = r.json()
            body = data.get("textBody") or data.get("htmlBody") or ""
            await update.message.reply_text(
                f"📧 From: {data['from']}\n"
                f"📌 Subject: {data['subject']}\n\n"
                f"{body}"
            )
            return

    await update.message.reply_text("❌ ایمیل ونه موندل شو")

# =====================
# 🧭 TEXT ROUTER (ONE HANDLER ONLY)
# =====================
async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📧 Generate Email":
        await generate_menu(update, context)
        return

    if text == "📂 My Emails":
        await show_ids(update, context)
        return

    if text in DOMAINS:
        await handle_domain(update, context)
        return

# =====================
# 🚀 MAIN
# =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", show_ids))
    app.add_handler(CommandHandler("inbox", inbox))
    app.add_handler(CommandHandler("read", read_email))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    print("✅ FakeSalarGmailBot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
