from sqlalchemy import Table, Integer, String, Text, ForeignKey, BigInteger, Float, Boolean, DateTime, UniqueConstraint
from sqlalchemy import MetaData
from sqlalchemy import Column

metadata = MetaData()
from datetime import datetime

# 1. table for the creators 

creators = Table(
    'creators', 
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('platform', String(50), nullable=False),
    Column('name', String(255), nullable=False),
    Column('handle', String(255), nullable=False),
    Column('created_at', String(50), default=datetime.now), 
    Column('follower_count', BigInteger, default=0),
    UniqueConstraint("platform", "handle", name="uix_platform_handle")
)

# 2. table for the posts

posts = Table(
    'posts',
    metadata, 
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('creator_id', Integer, ForeignKey('creators.id'), nullable=False), 
    Column('platform', String(50), nullable=False), 
    Column('post_id', String(255), nullable=False, unique=True),
    Column('title', String, nullable=True),
    Column('caption', String, nullable=True),
    Column('published_at', DateTime),
    Column('view_count', BigInteger, default=0),
    Column('thumbnail_url', String, nullable=True),
    Column('created_at', String(50), default=datetime.now)
)

#3. metrics table 

metrics = Table(
'metrics',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('post_id', Integer, ForeignKey('posts.id'), nullable=False),
    Column('view_count', BigInteger, default=0),
    Column('like_count', BigInteger, default=0),
    Column('comment_count', BigInteger, default=0),
    Column('share_count', BigInteger, default=0)
)