import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import date

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "data")

DB_HOST=os.getenv("POSTGRES_CONN_HOST")
DB_PORT = os.getenv("POSTGRES_CONN_PORT")
DB_NAME = os.getenv("ELT_DATABASE_NAME")
DB_USER = os.getenv("ELT_DATABASE_USERNAME")
DB_PASSWORD = os.getenv("ELT_DATABASE_PASSWORD")

JSON_FILE = os.path.join(DATA_DIR, f"YT_data_{date.today().isoformat()}.json")


with open(JSON_FILE,'r',encoding='utf-8') as file:
    videos=json.load(file)

print("Videos loaded from JSON:", len(videos))

connection=psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor=connection.cursor()

sql = """
insert into staging.videos (
    video_id,
    title,
    published_at,
    duration,
    view_count,
    like_count,
    comment_count
)
values (%s, %s, %s, %s, %s, %s, %s)
on conflict (video_id)
do update set
    title = EXCLUDED.title,
    published_at = EXCLUDED.published_at,
    duration = EXCLUDED.duration,
    view_count = EXCLUDED.view_count,
    like_count = EXCLUDED.like_count,
    comment_count = EXCLUDED.comment_count;
"""

for video in videos:
    cursor.execute(
        sql,
        (
            video["video_id"],
            video["title"],
            video["published_at"],
            video["duration"],
            video["view_count"],
            video["like_count"],
            video["comment_count"]
        )
    )


source_ids = [video["video_id"] for video in videos]

if source_ids:
    placeholders = ",".join(["%s"] * len(source_ids))

    delete_sql = f"""
        DELETE FROM staging.videos
        WHERE video_id NOT IN ({placeholders});
    """

    cursor.execute(delete_sql, source_ids)

    print("Deleted rows from staging:", cursor.rowcount)

connection.commit()

cursor.close()
connection.close()

print("Staging table updated successfully.")
