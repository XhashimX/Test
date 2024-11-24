import subprocess
import os

def download_and_send():
    URL = "https://vm.tiktok.com/ZNe3hDFKa/"
    BOT_TOKEN = "7749324996:AAFSpsRIyPCQ9dxzOuShUATSm3V9MP1goD4"
    CHAT_ID = "421777948"

    yt_dlp_command = [
        "yt-dlp", 
        "-o", "-", 
        URL
    ]

    curl_command = [
        "curl", 
        "-F", f"chat_id={CHAT_ID}", 
        "-F", "video=@-;filename=video.mp4", 
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    ]

    yt_dlp_process = subprocess.Popen(yt_dlp_command, stdout=subprocess.PIPE)
    curl_process = subprocess.Popen(curl_command, stdin=yt_dlp_process.stdout)
    yt_dlp_process.stdout.close()
    curl_process.communicate()

    return "Video sent to Telegram bot successfully!"

if __name__ == "__main__":
    download_and_send()
