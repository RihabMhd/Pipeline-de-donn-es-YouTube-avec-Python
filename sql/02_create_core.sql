create schema if not exists core;
create table if not exists core.videos(video_id varchar(20) primary key,title TEXT,
published_at timestamp, duration_seconds varchar(20), view_count bigint, like_count bigint, comment_count bigint)