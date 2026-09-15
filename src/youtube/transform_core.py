import os
import re
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def duration_to_seconds(duration):
    hours = 0
    minutes = 0
    seconds = 0

    match = re.search(r"(\d+)H", duration)
    if match:
        hours = int(match.group(1))

    match = re.search(r"(\d+)M", duration)
    if match:
        minutes = int(match.group(1))

    match = re.search(r"(\d+)S", duration)
    if match:
        seconds = int(match.group(1))

    return hours * 3600 + minutes * 60 + seconds


connection = psycopg2.connect(
    host="localhost",
    port=os.getenv("POSTGRES_CONN_PORT"),
    database=os.getenv("ELT_DATABASE_NAME"),
    user=os.getenv("ELT_DATABASE_USERNAME"),
    password=os.getenv("ELT_DATABASE_PASSWORD")
)

cursor = connection.cursor()


cursor.execute("""
    SELECT
        video_id,
        title,
        published_at,
        duration,
        view_count,
        like_count,
        comment_count
    FROM staging.videos;
""")

videos = cursor.fetchall()

print("Videos loaded from staging:", len(videos))


for video in videos:

    video_id = video[0]
    title = video[1]
    published_at = video[2]
    duration = video[3]
    view_count = video[4]
    like_count = video[5]
    comment_count = video[6]

    duration_seconds = duration_to_seconds(duration)

    cursor.execute("""
        INSERT INTO core.videos (
            video_id,
            title,
            published_at,
            duration_seconds,
            view_count,
            like_count,
            comment_count
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)

        ON CONFLICT (video_id)
        DO UPDATE SET
            title = EXCLUDED.title,
            published_at = EXCLUDED.published_at,
            duration_seconds = EXCLUDED.duration_seconds,
            view_count = EXCLUDED.view_count,
            like_count = EXCLUDED.like_count,
            comment_count = EXCLUDED.comment_count;
    """, (
        video_id,
        title,
        published_at,
        duration_seconds,
        view_count,
        like_count,
        comment_count
    ))


connection.commit()

cursor.close()
connection.close()

print("Core table updated successfully.")
