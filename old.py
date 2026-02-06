from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_CREDIT = "🤖 دا بوټ د سالار خانو لخوا جوړ شوی"

# ========= START =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1️⃣ ترمیکس کمانډونه"],
        ["2️⃣ سالار کمانډ"],
        ["3️⃣ کورنا لیکنې"],
        ["4️⃣ چت روم"],
        ["5️⃣ ترمیکس ډاونلوډ"],
        ["6️⃣ د سالار واتساف"],
        ["7️⃣ د مړ شوي شخص Facebook ID"]
    ]
    await update.message.reply_text(
        f"👋 سلام!\nیو انتخاب وټاکه 👇\n\n{BOT_CREDIT}",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ========= TERMUX COMMANDS =========
async def termux_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📌 Termux Commands:

pkg update
pkg upgrade
pkg install python
pkg install git
pip install requests
pip install mechanize
pip install bs4 futures
pip install rich
termux-setup-storage
pip install pycurl
""")

# ========= SALAR COMMAND =========
async def salar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📌 Salar Command:

rm -rf SALAR
git clone --depth=1 https://github.com/SaLarKhAnOo2003/SALAR.git
cd SALAR
python SALAR.py
""")

# ========= CONDOLENCE =========
async def condolence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🕊️ کورنا لیکنې:

1️⃣ The news of your death came to my ears like a gunshot 😭
2️⃣ A good friend is a blessing of God...
3️⃣ I'm still in shock and disbelief...
4️⃣ May your soul rest in peace...
5️⃣ Rest in peace my brother 🌹🕊️
""")

# ========= CHAT ROOM =========
async def chat_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
💬 چت روم (ثابت پیغامونه):

1️⃣ سلام زه سالار خانو یم، ستاسو نوم څه دی؟
2️⃣ زه هر وخت قهرمان یم او د افغانستان یم 🇦🇫
3️⃣ زه کندهاری یم، ته د کوم ځای یې؟
4️⃣ هر ځای زه زنداباد، ته څوک یې؟
""")

# ========= TERMUX DOWNLOAD =========
async def termux_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📥 Termux Download Links:

1️⃣ https://f-droid.org/packages/com.termux/
2️⃣ https://github.com/termux/termux-app/releases
3️⃣ https://apkpure.com/termux/com.termux
4️⃣ https://apkcombo.com/termux/com.termux/
5️⃣ https://uptodown.com/android/termux
""")

# ========= WHATSAPP =========
async def whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
💬 د سالار واتساف ګروپ:

https://chat.whatsapp.com/Lk71RwA3sny9m63fIElBKV?mode=ac_t
""")

# ========= MEMORIAL FB =========
async def memorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🕊️ د مړ شوي شخص Facebook Memorial

📌 لازم معلومات:
1️⃣ بشپړ نوم
2️⃣ د مړ شوي شخص ایمیل
3️⃣ د مرګ سند (Death Certificate)
4️⃣ ستا ایمیل

🔗 رسمي فورم:
https://www.facebook.com/help/contact/228813257197480

ℹ️ دا یوازې د حقیقي مړ شوي شخص لپاره دی.
""" + BOT_CREDIT)

# ========= HANDLER =========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "1️⃣ ترمیکس کمانډونه":
        await termux_commands(update, context)
    elif text == "2️⃣ سالار کمانډ":
        await salar_command(update, context)
    elif text == "3️⃣ کورنا لیکنې":
        await condolence(update, context)
    elif text == "4️⃣ چت روم":
        await chat_room(update, context)
    elif text == "5️⃣ ترمیکس ډاونلوډ":
        await termux_download(update, context)
    elif text == "6️⃣ د سالار واتساف":
        await whatsapp(update, context)
    elif text == "7️⃣ د مړ شوي شخص Facebook ID":
        await memorial(update, context)
    else:
        await update.message.reply_text("❌ مهرباني وکړئ له مینو څخه انتخاب وکړئ")

# ========= MAIN =========
def main():
    BOT_TOKEN = "8104728401:AAHztsToQBEROX5y1_V8E88lohvlZ96YyCU"

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
