import subprocess
import os

def download_and_send():
    URL = "https://www.tiktok.com/@ibu1b/video/7345634652016610565"
    BOT_TOKEN = "your_telegram_bot_token"
    CHAT_ID = "your_chat_id"

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

    try:
        yt_dlp_process = subprocess.Popen(yt_dlp_command, stdout=subprocess.PIPE)
        curl_process = subprocess.Popen(curl_command, stdin=yt_dlp_process.stdout)
        yt_dlp_process.stdout.close()
        curl_process.communicate()
        print("Video sent to Telegram bot successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Create a flag file to prevent re-sending
        with open("video_sent_flag.txt", "w") as flag_file:
            flag_file.write("Video sent")

if __name__ == "__main__":
    if not os.path.exists("video_sent_flag.txt"):
        download_and_send()
