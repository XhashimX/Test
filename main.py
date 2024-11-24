import subprocess
import os
import sys

def download_and_send(url):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

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
        print("Video sent to Telegram bot successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        download_and_send(video_url)
    else:
        print("Please provide the TikTok video URL as an argument.")
