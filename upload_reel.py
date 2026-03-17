import time
import requests
from config import INSTAGRAM_USER_ID, INSTAGRAM_ACCESS_TOKEN

GRAPH_API = f"https://graph.facebook.com/v19.0/{INSTAGRAM_USER_ID}"

def upload_reel(video_url: str, caption: str = "") -> dict:
    # Step 1: Create media container
    res = requests.post(f"{GRAPH_API}/media", params={
        "video_url": video_url,
        "media_type": "REELS",
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }).json()

    if "id" not in res:
        return {"success": False, "error": res}

    creation_id = res["id"]

    # Wait for video to be processed
    time.sleep(10)

    # Step 2: Publish reel
    pub = requests.post(f"{GRAPH_API}/media_publish", params={
        "creation_id": creation_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }).json()

    if "id" in pub:
        return {"success": True, "post_id": pub["id"]}
    return {"success": False, "error": pub}
