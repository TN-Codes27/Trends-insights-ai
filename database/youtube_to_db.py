from connection import get_engine
from models import posts, creators, metrics
from ingestion.youtube_ingest import fetch_recent_videos, fetch_video_details
from sqlalchemy import select, insert
from datetime import datetime

#CHANGE FROM PSYCOP2 TO SQLALCHEMY

#1. fetch youtube creators from db 
def youtube_sync_posts(): 
    engine = get_engine()
    try: 
        with engine.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, handle FROM creators WHERE platform = 'youtube'")
                print("The number of creators: ", cur.rowcount)
                row = cur.fetchone()

                while row is not None:
                    print(row)

                    row = cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    #2. loop through each creator and fetch recent videos




