import os
import json
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

with open("data/playlist_videos.json", "r", encoding="utf-8") as file:
    videos = json.load(file)

print("Videos loaded:", len(videos))

video_ids = []

for video in videos:
    video_ids.append(video["video_id"])


url = "https://www.googleapis.com/youtube/v3/videos"

video_details = []

for i in range(0, len(video_ids), 50):

    # we take 50 IDs from the list
    batch = video_ids[i:i + 50]

    params = {
        # snippet       -> title, publication date, etc.
        # contentDetails -> duration
        # statistics    -> views, likes, comments
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(batch),
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    print(
        f"batch {i // 50 + 1} | "
        f"status: {response.status_code}"
    )

    data = response.json()

    for item in data.get("items", []):

        video = {
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "duration": item["contentDetails"]["duration"],
            "view_count": item["statistics"].get("viewCount"),
            "like_count": item["statistics"].get("likeCount"),
            "comment_count": item["statistics"].get("commentCount")
        }

        video_details.append(video)



today = date.today().isoformat()

filename = f"data/YT_data_{today}.json"

with open(filename, "w", encoding="utf-8") as file:
    json.dump(
        video_details,
        file,
        indent=4,
        ensure_ascii=False
    )

print(f"Raw JSON saved: {filename}")