import telebot
import config
import requests

bot = telebot.TeleBot(config.BOT_TOKEN)

# 🔹 عرض أزرار التحكم في البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    
    keyboard.row(
        telebot.types.InlineKeyboardButton("🔄 إعادة تشغيل", callback_data="reboot"),
        telebot.types.InlineKeyboardButton("⏳ مدة التشغيل", callback_data="uptime")
    )
    
    keyboard.row(
        telebot.types.InlineKeyboardButton("📂 الملفات", callback_data="files"),
        telebot.types.InlineKeyboardButton("📷 التقاط صورة", callback_data="photo")
    )
    
    keyboard.row(
        telebot.types.InlineKeyboardButton("📡 فحص الشبكة", callback_data="network"),
        telebot.types.InlineKeyboardButton("🛑 إيقاف التشغيل", callback_data="shutdown")
    )

    bot.send_message(message.chat.id, "🔹 تحكم في الجهاز المتصل:", reply_markup=keyboard)

# 🔹 تنفيذ الأوامر عند الضغط على الزر
@bot.callback_query_handler(func=lambda call: True)
def handle_command(call):
    commands = {
        "reboot": "reboot",
        "uptime": "uptime",
        "files": "ls /sdcard/",
        "photo": "termux-camera-photo /sdcard/photo.jpg",
        "network": "ifconfig",
        "shutdown": "shutdown"
    }

    if call.data in commands:
        url = f"https://your-server-url.onrender.com/command?cmd={commands[call.data]}"
        response = requests.get(url).json()
        
        if "output" in response:
            bot.send_message(call.message.chat.id, f"✅ تنفيذ `{call.data}`:\n```\n{response['output']}\n```", parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, f"❌ خطأ: {response.get('error', 'حدث خطأ غير معروف')}")

# تشغيل البوت
bot.polling()
