from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def download_and_send(url):
    yt_dlp_command = [
        "yt-dlp",
        "-o", "-",
        url
    ]

    curl_command = [
        "curl",
        "-F", f"chat_id={CHAT_ID}",
        "-F", "video=@-;filename=video.mp4",
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    ]

    try:
        yt_dlp_process = subprocess.Popen(yt_dlp_command, stdout=subprocess.PIPE)
        curl_process = subprocess.Popen(curl_command, stdin=yt_dlp_process.stdout)
        yt_dlp_process.stdout.close()
        curl_process.communicate()
        return "Video sent to Telegram bot successfully!"
    except Exception as e:
        return f"Error: {e}"

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    return download_and_send(url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
