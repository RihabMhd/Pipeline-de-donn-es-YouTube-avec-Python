import os
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

    print("status:", response.status_code)

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

print("Total videos:", len(videos))

for video in videos:
    print(video)