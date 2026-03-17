import requests
from config import BOT_TOKEN

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def download_video(file_id: str, save_path: str = "video.mp4") -> str:
    res = requests.get(f"{TELEGRAM_API}/getFile", params={"file_id": file_id}).json()
    file_path = res["result"]["file_path"]
    video = requests.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}")
    with open(save_path, "wb") as f:
        f.write(video.content)
    return save_path

def send_message(chat_id: int, text: str):
    requests.get(f"{TELEGRAM_API}/sendMessage", params={"chat_id": chat_id, "text": text})
