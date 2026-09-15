create schema if not exists staging;
create table if not exists staging.videos(video_id varchar(20) primary key,title TEXT,
published_at timestamp, duration varchar(20), view_count bigint, like_count bigint, comment_count bigint)

