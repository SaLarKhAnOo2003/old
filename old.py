from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# =====================
# BOT TOKEN
# =====================
TOKEN = "7975528068:AAF9QdOGpQ8HmgJy90oxksnXg32lvEOo-1k"

# =====================
# APK FILE (same folder)
# =====================
APK_FILE = "LiteSocial.apk"   # <-- APK دې همدلته کیږده

# =====================
# START
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📱 Download Lite Facebook App"],
        ["ℹ️ About"]
    ]
    await update.message.reply_text(
        "👋 سلام!\n\n"
        "دا یو قانوني Lite Social App دی ✅\n"
        "هیڅ معلومات نه اخلي ❌\n\n"
        "👇 انتخاب وکړه:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =====================
# MENU
# =====================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📱 Download Lite Facebook App":
        if os.path.exists(APK_FILE):
            await update.message.reply_document(
                document=open(APK_FILE, "rb"),
                caption=(
                    "📦 Lite Social App\n\n"
                    "⚠️ DEMO / WEBVIEW ONLY\n"
                    "دا اپ یوازې اصلي Facebook ویب خلاصوي.\n"
                    "Meta سره تړاو نه لري."
                )
            )
        else:
            await update.message.reply_text("❌ APK فایل ونه موندل شو")

    elif text == "ℹ️ About":
        await update.message.reply_text(
            "ℹ️ معلومات:\n\n"
            "✅ قانوني WebView App\n"
            "✅ هیڅ لاګین یا صلفي نه اخلي\n"
            "❌ جعلي پاڼې نه لري\n\n"
            "دا اپ یوازې ویب‌سایټ خلاصوي."
        )

# =====================
# MAIN
# =====================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu))
    print("✅ Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
