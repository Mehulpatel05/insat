import threading
from flask import Flask, request, jsonify
from telegram import send_message, get_file_url
from upload_reel import upload_reel

app = Flask(__name__)

def process_video(chat_id, file_id, caption):
    send_message(chat_id, "⏳ Downloading video...")
    public_video_url = get_file_url(file_id)
    send_message(chat_id, "📤 Uploading to Instagram...")
    result = upload_reel(public_video_url, caption)
    if result["success"]:
        send_message(chat_id, f"✅ Reel Uploaded! Post ID: {result['post_id']}")
    else:
        send_message(chat_id, f"❌ Upload Failed: {result['error']}")

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"status": "ignored"}), 200

    message = data["message"]
    chat_id = message["chat"]["id"]

    if "video" not in message:
        send_message(chat_id, "❌ Please send a video to upload as Reel.")
        return jsonify({"status": "no_video"}), 200

    file_id = message["video"]["file_id"]
    caption = message.get("caption", "")

    threading.Thread(target=process_video, args=(chat_id, file_id, caption)).start()
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
