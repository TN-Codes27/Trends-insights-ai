import requests
from database.connection import get_engine
from database.models import posts, metrics, creators
from sqlalchemy import select, insert
from datetime import datetime


def extract_tiktok_post(url):
    """
    Extract TikTok metadata using the official oEmbed endpoint.
    This bypasses TikTok's dynamic JS and anti-scraping blocks.
    """

    oembed_url = f"https://www.tiktok.com/oembed?url={url}"
    response = requests.get(oembed_url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        raise ValueError(f"oEmbed request failed with status {response.status_code}")

    data = response.json()

    caption = data.get("title")
    thumbnail = data.get("thumbnail_url")

    # Extract post_id from URL
    try:
        post_id = url.split("/video/")[1].split("?")[0]
    except:
        raise ValueError("Could not extract post_id from URL. Ensure it is a correct TikTok URL.")

    return {
        "caption": caption,
        "post_id": post_id,
        "thumbnail": thumbnail,
        "publish_datetime": None,  # TikTok oEmbed does NOT provide this; added in Stage 4 Extended
        "like_count": None,
        "comment_count": None,
        "share_count": None
    }


def get_creator_id_for_tiktok(name):
    """
    Fetch the creator_id for a TikTok creator by name.
    """

    engine = get_engine()
    with engine.connect() as conn:
        row = conn.execute(
            select(creators).where(
                creators.c.platform == "tiktok",
                creators.c.name == name
            )
        ).fetchone()

        if not row:
            raise ValueError(f"No TikTok creator found with name '{name}'.")

        return row.id


def insert_tiktok_post(data, creator_id):
    """
    Insert the TikTok post into the posts and metrics tables.
    """

    engine = get_engine()

    with engine.connect() as conn:

        # Check if the post already exists
        existing = conn.execute(
            select(posts).where(posts.c.post_id == data["post_id"])
        ).fetchone()

        if existing:
            print(f"Post {data['post_id']} already exists. Skipping.")
            return

        # Insert into posts table
        ins_post = insert(posts).values(
            creator_id=creator_id,
            platform="tiktok",
            post_id=data["post_id"],
            title=None,
            caption=data["caption"],
            published_at=data["publish_datetime"],   # correct column name
            thumbnail_url=data["thumbnail"],
            created_at=datetime.now()
        )


        result_post = conn.execute(ins_post)
        new_post_id = result_post.inserted_primary_key[0]

        # Insert into metrics table (initial snapshot)
        ins_metric = insert(metrics).values(
            post_id=new_post_id,
            timestamp_collected=datetime.now(),
            view_count=None,
            like_count=data["like_count"],
            comment_count=data["comment_count"],
            share_count=data["share_count"]
        )

        conn.execute(ins_metric)
        conn.commit()

        print(f"Inserted TikTok post {data['post_id']} successfully.")


if __name__ == "__main__":
    print("Paste a TikTok video URL:")
    url = input("> ").strip()

    print("Extracting metadata...")
    data = extract_tiktok_post(url)
    print("Extracted data:", data)

    creator_name = input("Enter creator name (must match DB): ").strip()
    creator_id = get_creator_id_for_tiktok(creator_name)

    insert_tiktok_post(data, creator_id)

    print("TikTok ingestion test complete.")
