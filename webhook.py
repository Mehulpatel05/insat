import os
from flask import Flask, request, jsonify
from telegram import download_video, send_message
from upload_reel import upload_reel

app = Flask(__name__)

# NOTE: Instagram Graph API requires a PUBLIC video URL, not a local file.
# For production, upload the video to S3/Cloudinary and use that URL.
# Here we simulate with a placeholder public URL after download.

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"status": "ignored"}), 200

    message = data["message"]
    chat_id = message["chat"]["id"]

    # Only handle video messages
    if "video" not in message:
        send_message(chat_id, "❌ Please send a video to upload as Reel.")
        return jsonify({"status": "no_video"}), 200

    file_id = message["video"]["file_id"]
    caption = message.get("caption", "")

    send_message(chat_id, "⏳ Downloading video...")
    local_path = download_video(file_id)

    # TODO: Upload local_path to a public host (S3, Cloudinary, etc.)
    # and replace the line below with the actual public URL.
    public_video_url = f"https://your-public-host.com/{os.path.basename(local_path)}"

    send_message(chat_id, "📤 Uploading to Instagram...")
    result = upload_reel(public_video_url, caption)

    if result["success"]:
        send_message(chat_id, f"✅ Reel Uploaded Successfully! Post ID: {result['post_id']}")
    else:
        send_message(chat_id, f"❌ Upload Failed: {result['error']}")

    # Cleanup local file
    if os.path.exists(local_path):
        os.remove(local_path)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
