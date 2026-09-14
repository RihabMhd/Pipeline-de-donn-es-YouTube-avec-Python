import json

with open("data/playlist_videos.json", "r", encoding="utf-8") as file:
    videos = json.load(file)

print("Videos loaded:", len(videos))

video_ids = []

for video in videos:
    video_ids.append(video["video_id"])
