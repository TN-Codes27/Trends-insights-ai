from connection import get_engine
from models import creators

def insert_initial_creators():
    engine = get_engine()

    creator_data = [
        {'platform': 'youtube', 'name': 'Natalie Oneill', 'handle': 'UCvaL9hWV_pqLZjaixtL01Fg'},
        {'platform': 'youtube', 'name': 'Madaleine Argy', 'handle': 'UCw24-aQvuVMP3C8gAduidPg'},
        {'platform': 'instagram', 'name': 'Natalie Oneill', 'handle': 'natalieoneilll'},
        {'platform': 'tiktok', 'name': 'Natalie Oneill', 'handle': 'natalieoneilll'},
        {'platform': 'instagram', 'name': 'Madaleine Argy', 'handle': 'madaleineargy'},
        {'platform': 'tiktok', 'name': 'Madaleine Argy', 'handle': 'madaleineargy'}
    ]

    # THIS PART IS REQUIRED TO INSERT DATA
    with engine.connect() as conn:
        for creator in creator_data:
            conn.execute(creators.insert().values(**creator))
        conn.commit()

if __name__ == "__main__":
    insert_initial_creators()
    print("Initial creators inserted successfully.")
