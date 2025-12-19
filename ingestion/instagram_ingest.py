import requests
from bs4 import BeautifulSoup
from database.connection import get_engine
from database.models import posts, metrics, creators
from sqlalchemy import select, insert
from datetime import datetime


def extract_instagram_post(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch URL: status code {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    caption_tag = soup.find("meta", property="og:title")
    caption = caption_tag["content"] if caption_tag else None

    thumb_tag = soup.find("meta", property="og:image")
    thumbnail = thumb_tag["content"] if thumb_tag else None

    clean_url = url.split("?")[0].rstrip("/")

    if "/p/" in clean_url:
        post_id = clean_url.split("/p/")[1].split("/")[0]
        video_type = "post"
    elif "/reel/" in clean_url:
        post_id = clean_url.split("/reel/")[1].split("/")[0]
        video_type = "reel"
    else:
        raise ValueError("URL must be an Instagram /p/ (post) or /reel/ URL.")

    return {
        "caption": caption,
        "post_id": post_id,
        "thumbnail": thumbnail,
        "publish_datetime": None,
        "like_count": None,
        "comment_count": None,
        "video_type": video_type,
    }


def get_creator_id_for_instagram(name):
    engine = get_engine()
    with engine.connect() as conn:
        creator = conn.execute(
            select(creators).where(
                (creators.c.platform == "instagram") &
                (creators.c.name == name)
            )
        ).fetchone()

        if not creator:
            raise ValueError(f"Creator '{name}' not found in DB.")

        return creator.id


def insert_instagram_post(data, creator_id):
    engine = get_engine()
    with engine.connect() as conn:
        existing_post = conn.execute(
            select(posts).where(posts.c.post_id == data["post_id"])
        ).fetchone()

        if existing_post:
            print(f"Post {data['post_id']} already exists in DB.")
            return

        ins_post = insert(posts).values(
            creator_id=creator_id,
            platform="instagram",
            post_id=data["post_id"],
            title=None,
            caption=data["caption"],
            published_at=data["publish_datetime"],
            thumbnail_url=data["thumbnail"],
            created_at=datetime.now(),
            video_type=data["video_type"],
        )

        result_post = conn.execute(ins_post)
        post_row_id = result_post.inserted_primary_key[0]

        ins_metric = insert(metrics).values(
            post_id=post_row_id,
            view_count=0,
            like_count=0,
            comment_count=0,
            share_count=0,
            timestamp_collected=datetime.now(),
        )

        conn.execute(ins_metric)
        conn.commit()

        print(f"Inserted Instagram post {data['post_id']} successfully.")


if __name__ == "__main__":
    print("Paste an Instagram post URL:")
    url = input("> ").strip()

    data = extract_instagram_post(url)
    print("Extracted data:", data)

    creator_name = input("Enter creator name (must match DB): ").strip()
    creator_id = get_creator_id_for_instagram(creator_name)

    insert_instagram_post(data, creator_id)

    print("Instagram ingestion test complete.")
