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
        ["6️⃣ دسالار واتساف"],
        ["7️⃣ دکورنا سوی ایدی جوړول"]
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

The news of your death came to my ears like a gun shot😭. He died during the bomb blast in Palestine 🇰🇼 R.I.P bro @  you will be in our hearts forever😭💔 pls remember my brother's account
Date of Death 21/10/2025 Time 12:55 AM
---------------------------------------------------

2️⃣

() May your soul rest in peace and may God bless you with paradise. 
I miss you so much. I see your Facebook messages every day. Every time I see your message, I cry.
My Facebook friend was a soldier in the country of afghanistan who.😭May the soul of those killed by Hamas group rest in peace😭😓💔
Dead Time 9:33 am 
Dead Date 13/7/2024
---------------------------------------------------

3️⃣

(@) was my best friends😭❤️‍🔥 He died yesterday. May god give him heaven, Rest in peace my brother. We will miss you so much. May god give strength to your family to accept this sad truth. I request to facebook so they make his account memorialize, as everyone can pray for him.🤚🏽😭💔
Rip my bro🌹🕊
---------------------------------------------------

4️⃣
Hello dear sir. Our soul is not permanent for living here but i am very sorry about my loss. My friend () has been died due to heart attack. He was well wisher for all humanity. I have never seen suck a kind person pls Facebook team help us to make memo my lovely friend's account. 
Pls give hearts prays and many memories to my dear..
Rest in peace 🕊️ dear 😭
---------------------------------------------------

5️⃣

I'm still in shock and disbelief that my best friend ( ) 💔😭 is gone. The pain of losing you is unbearable I miss you every second of every day I wish I could turn back the time and save you😭💐. rest in peace😭💐🕊️
Death date 22/1/2025 time 11:30pm
---------------------------------------------------
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

# ===== Whatsap Group =====
async def whatsap_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
💬 Whatsap Group Links:

https://chat.whatsapp.com/Lk71RwA3sny9m63fIElBKV?mode=ac_t
""")

# ===== MEMORIAL FACEBOOK =====
async def memorial_facebook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🕊️ د مړ شوي شخص Facebook Memorial ID

📌 لازم معلومات:
1️⃣ د مړ شوي کس بشپړ نوم
2️⃣ دوهم دمر سوی شخص جیمیل
3️⃣ دمری سوی شخص داسنادو دفیدایشت نیته
4️⃣ دمر سوی شخص اسناد یادونه دفیدایشت نیته باید داسنادو فه رکم یی  او دایدی نوم او فیدایشت نیته هم باید داسنادو فه رکم وی


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
        
    elif text == "6️⃣ دسالار واتساف":
        await whatsap_group(update, context)

    elif text == "7️⃣ دکورنا سوی ایدی جوړول":
        await memorial_facebook(update, context)

    elif text == "1️⃣ چت روم":
        await update.message.reply_text("Ich, der Anführer von ISIS‼️🔪🗡💪🏿(@), sage dir, nachdem du jedes Kind gesehen hast, wo immer‼️🔪🗡💪🏿 es war, töte es auf die gleiche Weise, dies ist mein Fluch 💪🏿🗡🔪‼️auf dir, oh Geschwätz, höre in deine Ohren und das vor dreißig Tagen (6/2/2026) Eine unserer Gruppen namens Jahani tötete 8 Kinder im Zentrum 🔪💪🏿💪🏿💪🏿‼️von Syrien, Damaskus, und dies ist eine der guten 🔪💪🏿‼️Taten unserer Gruppe, die Jahani heißt, und nach allem, 🔪🗡‼️💪🏿was Sie tun, sollte es jedes Kind und jede Person, die Sie sehen, tun werde💪🏿💪🏿‼️ bestraft Ziehe den meisten Harnstoff, das ist mein Befehl, das ist die neue Idee deines Anführers 👇🏿👇🏿
Ich, der Anführer von ISIS‼️🔪🗡💪(@) sage dir, nachdem du jedes Kind gesehen hast, wo immer‼️🔪🗡💪🏿 es war, töte es auf die gleiche Weise, dies ist mein Fluch 💪🏿🗡🔪‼️auf dir, oh Geschwätz, höre in deine Ohren und das vor dreißig Tagen(6/2/2026) Eine unserer Gruppen namens Jahani tötete 8 Kinder im Zentrum 🔪💪🏿💪🏿💪🏿‼️von Syrien, Dam.
👇🏻😋
https://www.facebook.com/")

    elif text == "2️⃣ چت روم":
        await update.message.reply_text("‼️Bommenwerpers staan ​​klaar ‼️Gooi over de stad Charkov, bommenwerpers zijn klaar om aan te vallen ❗️🗡 Bereid lichte en zware wapens voor, we gaan oorlog voeren ⚔️❗️Bommenwerpers, helikopters, wees klaar ⚰️🗡 Gooi giftige bommen boven de vijand ⚔️🚫 we moeten win deze oorlog, lang leve ISIS‼️⚔️ ISIS vernietigt zijn vijanden ⚔️ gooi bommen richting Kharkiv‼️🗡 aanvalsaanval❗️ bombardeer deze aanval, we moeten de aanval winnen❗️ ISIS lang leve ISIS ⚔️‼️‼️Bommenwerpers staan ​​klaar ‼️Gooi over de stad Charkov, bommenwerpers zijn klaar om aan te vallen ❗️🗡 Bereid lichte en zware wapens voor, we gaan oorlog voeren ⚔️❗️Bommenwerpers, helikopters, wees klaar ⚰️🗡 Gooi giftige bommen boven de vijand ⚔️🚫 we moeten win deze oorlog, lang leve ISIS‼️⚔️ ISIS vernietigt zijn vijanden ⚔️ gooi bommen richting Kharkiv‼️🗡 aanvalsaanval❗️ bombardeer deze aanval, we moeten de aanval winnen❗️ ISIS lang leve ISIS ⚔️‼️‼️Bommenwerpers staan ​​klaar ‼️Gooi over de stad Charkov, bommenwerpers zijn klaar om aan te vallen ❗️🗡 Bereid lichte en zware wapens voor, we gaan oorlog voeren ⚔️❗️Bommenwerpers, helikopters, wees klaar ⚰️🗡 Gooi giftige bommen boven de vijand ⚔️🚫 we moeten win deze oorlog, lang leve ISIS‼️⚔️ ISIS vernietigt zijn vijanden ⚔️ gooi bommen richting Kharkiv‼️🗡 aanvalsaanval❗️ bombardeer deze aanval, we moeten de aanval winnen❗️ ISIS lang leve ISIS ⚔️‼️‼️Bommenwerpers staan ​​klaar ‼️Gooi over de stad Charkov, bommenwerpers zijn klaar om aan te vallen ❗️🗡 Bereid lichte en zware wapens voor, we gaan oorlog voeren ⚔️❗️Bommenwerpers, helikopters, wees klaar ⚰️🗡 Gooi giftige bommen boven de vijand ⚔️🚫 we moeten win deze oorlog, lang leve ISIS‼️⚔️ ISIS vernietigt zijn vijanden ⚔️ gooi bommen richting Kharkiv‼️🗡 aanvalsaanval❗️ bombardeer deze aanval, we moeten de aanval winnen❗️ ISIS lang leve ISIS ⚔️‼️")

    elif text == "3️⃣ چت روم":
        await update.message.reply_text("نیک نیم 😼👇🏻

Troorism😭☝

نوم د گروپ ☹️👇

I am a terrorist, I am an ISIS terrorist, I am a criminal, I am a murderer. I am the one who killed

داغه کزاریش دی کورف کی فورته کی یادونه کورفان باید لس دانی وی👇

😭🔪😭🔪😭🔪😭🔪😭🔪👇👇👇
Ich bin gegen die türkische Regierung. Ich wurde geschlachtet Dann haben sie mich abgeschlachte t. Ich bin gegen die türkische Regierung. Sein Vater wurde abgeschnitten. Isis Isis Isis Isis a Troosti - Organisation Ich bin eine ISIS - 
Regierung.🔪❌❌❌❌❌🔪🔪🔪🔪🔪⚔️
হ্যালো মেইন ফ্রুন্ডে, ডয়েচল্যান্ডে আইচ বিন এইন মিটগ্লিড ডেস ভার্ট্রাউয়েন্স গেজেন ডাই রুসিশে রেজিরং।،🔪🔪🔪❌🚫❌
Hallo Freunde, ich bin Mitglied der Stiftung gegen die russische Regierung in Deutschland. Ich bin gegen die türkische Regierung. Ich wurde geschlachtet Dann wurde ich von ISIS 🚫🚫🚫🚫🚫🚫🔪🔪🔪🔪🔪🔪🔪 abgeschlachtet. Ich bin gegen die türkische Regierung. Sein Vater wurde abgeschnitten. Isis Isis Isis Isis a Troosti - Organizasyon I am an ISIS - Govt.☝☝☝
ISIS ISIS Ich bin eine Treuhandorganisation. Ich bin gegen die türkische Regierung. Ich wurde geschlachtet Dann haben sie mich abgeschlachtet. Ich bin gegen die türkische Regierung. Sein Vater wurde abgeschnitten. Isis Isis Isis Isis a Troosti - Organisation Ich bin ein ISIS - Regierung.🔪❌🚫🚫🗡⚔️🗡⚔️🗡⚔️🗡⚔️❌,
Ich bin gegen die türkische Regierung. Ich wurde geschlachtet Dann haben sie mich abgeschlachtet. Ich bin gegen die türkische Regierung. Sein Vater wurde abgeschnitten. Isis Isis Isis Isis a Troosti - Organisation Ich bin eine ISIS - Regierung.🔪🗡⚔️🗡⚔️🗡❌❌❌❌❌
Hallo Freunde, ich bin Mitglied der Stiftung gegen die russische Regierung in Deutschland. Ich bin gegen die türkische Regierung. Ich wurde geschlachtet Dann wurde ich von ISIS 🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫🚫 abgeschlachtet. Ich bin gegen die türkische Regierung. Sein Vater wurde abgeschnitten. Isis Isis Isis Isis a Troosti - Organizasyon I am an ISIS - Govt.☝☝☝
ISIS ISIS Ich bin eine Treuhandorganisation. Ich bin gegen die türkische Regierung. Ich wurde geschlachtet Dann haben sie mich abgeschlachtet. Ich bin gegen die türkische Regierung. Sein Vater wurde abgeschnitten. Isis Isis Isis Isis a Troosti - Organisation Ich bin ein ISIS - Regierung.🔪⚔️⚔️⚔️⚔️⚔️❌❌❌❌,
হ্যালো মেইন ফ্রুন্ডে, ডয়েচল্যান্ডে আইচ বিন এইন মিটগ্লিড ডেস ভার্ট্রাউয়েন্স গেজেন ডাই ،রুসিশে রেজিরং।
They slaughtered my father, they are planning to kill my family, ISIS, I am against the American government, I am against the Turkish government, the government threatened to kill me, ISIS 👈, I was sexually harassed, I was raped 👈 ISIS 👉, Hello Mei,
I am the murderer of your father 👉ISIS👈, then I killed them with bullets, tears were falling 🔪😭☝, ISIS slaughtered me, I confess that I was involved in the suicide terrorist attack on September 11, 2001 ☝🇺🇸🔪I am above the girls I raped you, then I slaughtered them, I burned the bodies of dozens of people of the Turkish government 🇹🇷🔪☝, I am against the Turkish government, I am the killer of Shiite youth, I slaughtered the Shiites, I slaughtered the Shiites 
alive with a knife.
হ্যালো মেইন ফ্রুন্ডে, ডয়েচল্যান্ডে আইচ বিন এইন মিটগ্লিড ডেস ভার্ট্রাউয়েন্স গেজেন ডাই রুসিশে রেজিরং।،
They slaughtered my father, they are planning to kill my family, ISIS, I am against the American government, I am against the Turkish government, the government threatened to kill me, ISIS 👈, I was sexually harassed, I was raped 👈 ISIS 👉, Hello Mei,
I am the murderer of your father 👉ISIS👈, then I killed them with bullets, tears were falling 🔪😭☝, ISIS slaughtered me, I confess that I was involved in the suicide terrorist attack on September 10, 1991👈 ☝🇺🇸🔪I am above the girls I raped you, then I slaughtered them, I burned the bodies of dozens of people of the Turkish government 🇹🇷🔪☝, I am against the Turkish government, I am the killer of Shiite youth, I slaughtered the Shiites, I slaughtered the Shiites alive with a knife.
হ্যালো মেইন ফ্রুন্ডে, ডয়েচল্যান্ডে আইচ বিন এইন মিটগ্লিড ডেস ভার্ট্রাউয়েন্স গেজেন ডাই রুসিশে রেজিরং।،
")

    elif text == "4️⃣ دچت روم نیک نیم":
        await update.message.reply_text("私はコロナウイルス❌🚫感染者です 🚫🧟‍♀️🧟‍♀️🧟‍♀️🧟‍♂️🧟‍♂️")

    elif text == "⬅️ شاته":
        await start(update, context)

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token("8104728401:AAFWHpJ-mWLhc881Cktk_huE8v7Vkcwj8HE").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
