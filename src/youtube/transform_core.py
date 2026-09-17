import os
import psycopg2
from dotenv import load_dotenv
import isodate
from datetime import datetime
load_dotenv()


def duration_to_seconds(duration):
    parsed_duration=isodate.parse_duration(duration)
    seconds=int(parsed_duration.total_seconds())
    return seconds

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_date(date):
    if date is None:
        return None
    if isinstance(date, str):
        return datetime.fromisoformat(date.replace("Z", "+00:00"))
    return date  

def safe_title(title, default="Untitled"):
    if title is None or title.strip()=="":
        return default
    return title

def engagement_rate(like, comment, view, default=0):
    if view is None or view == 0:
        return default
    return (like + comment) / view

def like_view_ratio(like, view, default=0):
    if view is None or view==0:
        return default
    return like/view

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

    video_id=video[0]
    title = safe_title(video[1])
    published_at=safe_date(video[2])
    duration=video[3]
    view_count=safe_int(video[4])
    like_count=safe_int(video[5])
    comment_count=safe_int(video[6])

    er = round(engagement_rate(like_count, comment_count, view_count),6)
    lvr = round(like_view_ratio(like_count, view_count),6)

    duration_seconds=duration_to_seconds(duration)

    cursor.execute("""
        INSERT INTO core.videos (
            video_id, title, published_at, duration_seconds,
            view_count, like_count, comment_count,
            engagement_rate, like_view_ratio
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (video_id)
        DO UPDATE SET
            title=EXCLUDED.title,
            published_at=EXCLUDED.published_at,
            duration_seconds=EXCLUDED.duration_seconds,
            view_count=EXCLUDED.view_count,
            like_count=EXCLUDED.like_count,
            comment_count=EXCLUDED.comment_count,
            engagement_rate=EXCLUDED.engagement_rate,
            like_view_ratio=EXCLUDED.like_view_ratio;
    """, (
    video_id, title, published_at, duration_seconds,
    view_count, like_count, comment_count,
    er, lvr
    ))


cursor.execute("""
    DELETE FROM core.videos
    WHERE video_id NOT IN (
        SELECT video_id
        FROM staging.videos
    );
""")

print("Deleted rows from core:", cursor.rowcount)

connection.commit()

cursor.close()
connection.close()

print("Core table updated successfully.")
