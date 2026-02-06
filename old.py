import threading
from flask import Flask, request, render_template_string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =========================
# CONFIG
# =========================
BOT_TOKEN = "7975528068:AAHaP1gI5PzkkpjaOoI3Qu2p8QGSQp9j4PE"
PUBLIC_BASE_URL = "https://salar-demo-bot.onrender.com"

# =========================
# TELEGRAM BOT
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        ["📘 Facebook Demo"],
        ["🎮 PUBG Demo"],
        ["🎲 Ludo Demo"],
        ["📷 Camera Demo"]
    ]
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "This bot provides **LEGAL DEMO pages only**.\n"
        "⚠️ Never enter real credentials.\n\n"
        "Choose a demo:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    pages = {
        "📘 Facebook Demo": "facebook",
        "🎮 PUBG Demo": "pubg",
        "🎲 Ludo Demo": "ludo",
        "📷 Camera Demo": "camera"
    }

    if text in pages:
        link = f"{PUBLIC_BASE_URL}/{pages[text]}?uid={uid}"
        await update.message.reply_text(
            f"🔗 Demo Link:\n{link}\n\n"
            "⚠️ DEMO ONLY – Do NOT use real data."
        )

# =========================
# FLASK WEB APP
# =========================
app = Flask(__name__)

BASE_HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{title}}</title>
<style>
body{font-family:system-ui;background:#f3f4f6;padding:16px}
.card{background:#fff;border-radius:16px;padding:16px;max-width:420px;margin:auto;
box-shadow:0 10px 30px rgba(0,0,0,.08)}
.badge{display:inline-block;background:#eef2ff;color:#1877f2;
padding:6px 10px;border-radius:999px;font-weight:700}
.warn{background:#fff1f2;color:#7f1d1d;padding:12px;border-radius:12px;margin:12px 0}
input,textarea{width:100%;padding:12px;border-radius:12px;border:1px solid #e5e7eb}
button{width:100%;padding:12px;border-radius:14px;border:0;
background:#1877f2;color:#fff;font-weight:700;margin-top:10px}
.note{font-size:12px;color:#6b7280;text-align:center;margin-top:10px}
</style>
</head>
<body>
<div class="card">
<span class="badge">DEMO</span>
<h2>{{title}}</h2>
<div class="warn">
⚠️ This is a DEMO page.<br>
❌ Do NOT enter real credentials.<br>
✅ Use dummy/test text only.
</div>
{{body}}
<div class="note">Legal Demo UI • No data is stored</div>
</div>
</body>
</html>
"""

def demo_form(title, labels):
    inputs = ""
    for l in labels:
        inputs += f"<label>{l}</label><input placeholder='demo_{l.lower()}'><br>"
    inputs += "<button>Submit (Demo)</button>"
    return render_template_string(
        BASE_HTML,
        title=title,
        body=inputs
    )

@app.route("/facebook")
def facebook():
    return demo_form("Facebook Demo", ["Username", "Password"])

@app.route("/pubg")
def pubg():
    return demo_form("PUBG Demo", ["Player ID", "Region"])

@app.route("/ludo")
def ludo():
    return demo_form("Ludo Demo", ["Player Name"])

@app.route("/camera")
def camera():
    body = """
    <p>📷 Camera Demo UI</p>
    <div class="warn">
    Camera access is NOT enabled.<br>
    This is a visual demo only.
    </div>
    <button disabled>Open Camera (Disabled)</button>
    """
    return render_template_string(BASE_HTML, title="Camera Demo", body=body)

# =========================
# RUN BOTH
# =========================
def run_flask():
    app.run(host="0.0.0.0", port=8081)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))
    bot.run_polling()

if __name__ == "__main__":
    main()
