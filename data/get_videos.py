import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")
PLAYLIST_ID="UUfcQPMZg4tNk6tKUTHbAr0g"

url="https://www.googleapis.com/youtube/v3/playlistItems"

params={
    "part": "snippet",
    "playlistId": PLAYLIST_ID,
    "maxResults": 50,
    "key": API_KEY
}

response=requests.get(url, params=params)

print("status:",response.status_code)

data=response.json()

print(data)