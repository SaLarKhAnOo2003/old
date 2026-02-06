from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_CREDIT = "🤖 دا بوټ د سالار خانو لخوا جوړ شوی"

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1️⃣ ترمیکس کمانډونه"],
        ["2️⃣ سالار کمانډ"],
        ["3️⃣ کورنا لیکنې"],
        ["4️⃣ چت روم"],
        ["5️⃣ ترمیکس ډاونلوډ"],
        ["6️⃣ د مړ شوي شخص Facebook ID"]
    ]
    await update.message.reply_text(
        f"👋 سلام!\nمهرباني وکړئ یو انتخاب وکړئ 👇\n\n{BOT_CREDIT}",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ===== TERMUX COMMANDS =====
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

# ===== SALAR COMMAND =====
async def salar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📌 Salar Command:

rm -rf SALAR
git clone --depth=1 https://github.com/SaLarKhAnOo2003/SALAR.git
cd SALAR
python SALAR.py
""")

# ===== CONDOLENCE TEXTS =====
async def condolence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🕊️ کورنا لیکنې:

1️⃣
The news of your death came to my hearing as a gun shot😪.
He died during the protest in Nigeria 🇳🇬
R.I.P 😭 brother ()

---------------------

2️⃣
A good friend is blessing of God.
I am heartbroken to hear about () death in car accident.
Death date: 4/10/2024
Time: 3:31pm

---------------------

3️⃣
I'm still in shock that my best friend ()💔😭 is gone.
Death date: 28/10/2024
Time: 12:00pm

---------------------

4️⃣
() May your soul rest in peace.
Dead Date: 14/11/2024
Dead Time: 9:33 am
""")

# ===== CHAT ROOM MENU =====
async def chat_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1️⃣ چت روم"],
        ["2️⃣ چت روم"],
        ["3️⃣ چت روم"],
        ["4️⃣ چت روم"],
        ["⬅️ شاته"]
    ]
    await update.message.reply_text(
        "💬 چت روم انتخاب کړئ 👇",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ===== TERMUX DOWNLOAD =====
async def termux_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📥 Termux Download Links:

1️⃣ https://f-droid.org/packages/com.termux/
2️⃣ https://github.com/termux/termux-app/releases
3️⃣ https://apkpure.com/termux/com.termux
4️⃣ https://apkcombo.com/termux/com.termux/
5️⃣ https://uptodown.com/android/termux
""")

# ===== MEMORIAL FACEBOOK =====
async def memorial_facebook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🕊️ د مړ شوي شخص Facebook Memorial ID

📌 لازم معلومات:
1️⃣ د مړ شوي کس بشپړ نوم
2️⃣ د هغه د Facebook پروفایل لینک
3️⃣ د مرګ اسناد (Death Certificate / News)
4️⃣ ستا خپل ایمیل
5️⃣ ستا اړیکه له هغه شخص سره

🔗 د فیسبوک رسمي فورم:
https://www.facebook.com/help/contact/228813257197480

ℹ️ یادونه:
دا فورم یوازې د مړ شوي شخص د اکاونټ Memorial کولو لپاره دی،
د فېک اکاونټ لپاره نه دی.

""" + BOT_CREDIT)

# ===== MESSAGE HANDLER =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "1️⃣ ترمیکس کمانډونه":
        await termux_commands(update, context)

    elif text == "2️⃣ سالار کمانډ":
        await salar_command(update, context)

    elif text == "3️⃣ کورنا لیکنې":
        await condolence(update, context)

    elif text == "4️⃣ چت روم":
        await chat_menu(update, context)

    elif text == "5️⃣ ترمیکس ډاونلوډ":
        await termux_download(update, context)

    elif text == "6️⃣ د مړ شوي شخص Facebook ID":
        await memorial_facebook(update, context)

    elif text == "1️⃣ چت روم":
        await update.message.reply_text("سلام زه سالار خانو یم، ستاسو نوم څه دی؟")

    elif text == "2️⃣ چت روم":
        await update.message.reply_text("زه هر وخت قهرمان یم او د افغانستان یم 🇦🇫")

    elif text == "3️⃣ چت روم":
        await update.message.reply_text("زه کندهاری یم، ته د کوم ځای یې؟")

    elif text == "4️⃣ چت روم":
        await update.message.reply_text("هر ځای زه زنداباد، ته څوک یې؟")

    elif text == "⬅️ شاته":
        await start(update, context)

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token("8104728401:AAExuKzu-mSRW92ceF9BED406je0KmDp0xQ").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
