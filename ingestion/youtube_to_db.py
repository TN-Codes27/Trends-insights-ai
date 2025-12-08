from database.connection import get_engine
from database.models import posts, creators, metrics
from sqlalchemy import select, insert
from datetime import datetime
from ingestion.youtube_ingest import (
    fetch_recent_videos,
    fetch_video_details,
    get_youtube_client,
    load_api_key,
)

def youtube_sync_posts():
    engine = get_engine()

    try:
        with engine.connect() as conn:

            youtube = get_youtube_client(load_api_key())

            # 1. Fetch creators on YouTube
            youtube_creators = conn.execute(
                select(creators).where(creators.c.platform == "youtube")
            ).fetchall()

            print(f"Found {len(youtube_creators)} YouTube creators.")

            for creator in youtube_creators:

                channel_id = creator.handle
                print(f"\nFetching videos for channel: {creator.name} ({channel_id})")

                # 2. Fetch video IDs + metadata
                video_ids = fetch_recent_videos(youtube, channel_id, max_results=5)
                video_details = fetch_video_details(youtube, video_ids)

                for video in video_details:

                    # Convert YouTube timestamp → datetime
                    dt = datetime.fromisoformat(video["published_at"].replace("Z", "+00:00"))

                    # 3. Check if post already exists
                    existing_post = conn.execute(
                        select(posts).where(posts.c.post_id == video["video_id"])
                    ).fetchone()

                    if existing_post:
                        print(f"Already exists → {video['video_id']}")
                        continue

                    # 4. Insert new post
                    ins_post = insert(posts).values(
                        creator_id=creator.id,
                        platform="youtube",
                        post_id=video["video_id"],
                        title=video["title"],
                        caption=None,
                        published_at=dt,
                        thumbnail_url=None,
                        created_at=datetime.now(),
                    )

                    result_post = conn.execute(ins_post)
                    post_row_id = result_post.inserted_primary_key[0]

                    print(f"Inserted new post: {video['video_id']}")

                    # 5. Insert initial metrics
                    ins_metric = insert(metrics).values(
                        post_id=post_row_id,
                        view_count=int(video["view_count"]),
                        like_count=int(video["like_count"]),
                        comment_count=int(video["comment_count"]),
                        share_count=0,
                        timestamp_collected=datetime.now(),
                    )

                    conn.execute(ins_metric)
                    print(f" → Metrics inserted for {video['video_id']}")

            # Commit after all inserts
            conn.commit()

    except Exception as error:
        print(" Error during YouTube sync:", error)


if __name__ == "__main__":
    youtube_sync_posts()
    print("\nYouTube posts synced successfully.")
