#Script goals: 
# 1. Connect to the Youtube API 
# 2. Pull the latest videos from the specified accounts in accounts_to_track.json
# 3. Print/store the basic metadata

#TO DO: ADD IN THE VIDEO DURATIO LESS THAN MEANS ITS A SHORT OR LIVE STREAM ETC!!!
import os
from attr import define
from dotenv import get_key, load_dotenv, find_dotenv
from pathlib import Path
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.discovery import build
#code to complete next time: 

#1. load env variables 
def load_api_key():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY not found in environment variables")
    return api_key

    
# 2. get youtube client 
def get_youtube_client(api_key):
    youtube = build(
    serviceName="youtube",
    version="v3",
    developerKey=api_key
) 
    return youtube

# 3. Fetch the most recent videos for a given channel ID
def fetch_recent_videos(youtube, channel_id, max_results=10):
    # call search().list(...)
    response = youtube.search().list(
    part="snippet",
    channelId=channel_id,
    maxResults=max_results,
    order="date",
    type="video"
    ).execute()
    # extract video IDs
    video_ids = [item['id']['videoId'] for item in response.get('items', [])]
    # return list of video IDs
    return video_ids


# 4. Fetch video details (views, likes, comments, title, etc.)
def fetch_video_details(youtube, video_ids):
    # call videos().list(...)
    response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()
    # loop over response["items"] and for each item
    
    video_metadata = []
    for item in response.get("items", []):
        vid_id = item["id"]
        title = item["snippet"]["title"]
        published_at = item["snippet"]["publishedAt"]
        stats = item["statistics"]  
        views = stats.get("viewCount", "0")
        likes = stats.get("likeCount", "0")
        comments = stats.get("commentCount", "0") 

        dict = {
            "video_id": vid_id,
            "title": title,
            "published_at": published_at,
            "view_count": views,
            "like_count": likes,
            "comment_count": comments
        }

        video_metadata.append(dict)
    return video_metadata


# 5. Main function to test the pipeline
if __name__ == "__main__":
    # 1. load API key
    api_key = load_api_key()
    # 2. create client
    youtube = get_youtube_client(api_key)
    # 3. fetch videos 
    channel_id = "UCvaL9hWV_pqLZjaixtL01Fg"  
    # 4. print the returned metadata
    video_ids = fetch_recent_videos(youtube, channel_id, max_results=5)
    details = fetch_video_details(youtube, video_ids)
    print(details)

    