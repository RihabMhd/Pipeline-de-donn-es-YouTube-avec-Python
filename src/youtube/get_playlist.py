import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")

url = "https://www.googleapis.com/youtube/v3/playlistItems"

videos = []

next_page_token = None

while True:

    params = {
        "part": "snippet",
        "playlistId": PLAYLIST_ID,
        "maxResults": 50,
        "key": API_KEY
    }

    if next_page_token:
        params["pageToken"] = next_page_token

    response = requests.get(url, params=params)

    print("Playlist status:", response.status_code)

    data = response.json()

    for item in data.get("items", []):

        video = {
            "video_id": item["snippet"]["resourceId"]["videoId"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"]
        }

        videos.append(video)

    next_page_token = data.get("nextPageToken")

    if not next_page_token:
        break


with open("data/playlist_videos.json", "w", encoding="utf-8") as file:
    json.dump(videos, file, indent=4, ensure_ascii=False)

print("Total videos:", len(videos))
print("Playlist data saved.")