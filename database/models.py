from sqlalchemy import (
    Table, Column, Integer, String, Text, ForeignKey, BigInteger, DateTime, UniqueConstraint
)
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy import Enum
metadata = MetaData()

# 1. creators table
creators = Table(
    'creators',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('platform', String(50), nullable=False),
    Column('name', String(255), nullable=False),
    Column('handle', String(255), nullable=False),
    Column('created_at', DateTime, default=datetime.now),
    Column('follower_count', BigInteger, default=0),
    UniqueConstraint("platform", "handle", name="uix_platform_handle")
)

# 2. posts table (static post info ONLY)
posts = Table(
    'posts',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('creator_id', Integer, ForeignKey('creators.id'), nullable=False),
    Column('platform', String(50), nullable=False),
    Column('post_id', String(255), nullable=False, unique=True),  # YouTube/TikTok/IG ID
    Column('title', String, nullable=True),
    Column('caption', String, nullable=True),
    Column('published_at', DateTime),       # correct name + type
    Column('thumbnail_url', String, nullable=True),
    Column('created_at', DateTime, default=datetime.now),
    Column("video_type", Enum("video", "short", "live", "reel", "post", name="video_type_enum"), nullable=False, default="video")
)

# 3. metrics table (time-series)
metrics = Table(
    'metrics',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('post_id', Integer, ForeignKey('posts.id'), nullable=False),
    Column('view_count', BigInteger, default=0),
    Column('like_count', BigInteger, default=0),
    Column('comment_count', BigInteger, default=0),
    Column('share_count', BigInteger, default=0),
    Column('timestamp_collected', DateTime, default=datetime.now)
)
