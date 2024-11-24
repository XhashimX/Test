import os
import requests
import yt_dlp
from flask import Flask, request

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # ادخل توكن البوت الخاص بك هنا
CHAT_ID = os.environ.get("CHAT_ID")  # ادخل معرف المحادثة الخاص بك هنا

app = Flask(__name__)

@app.route('/', methods=['POST'])
def download_tiktok():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        if text.startswith('/download'):
            url = text.split('/download ', 1)[1]
            try:
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # اعطاء الأولوية لـ mp4
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info_dict)
                    send_video(filename)
                    os.remove(filename)  # حذف الملف بعد الإرسال
                    return 'OK'
            except Exception as e:
                send_message(f"حدث خطأ: {e}")
                return 'Error'

    return 'OK'

def send_video(filename):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    files = {'video': open(filename, 'rb')}
    data = {'chat_id': CHAT_ID}
    requests.post(url, files=files, data=data)

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
