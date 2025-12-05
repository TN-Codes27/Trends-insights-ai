from connection import get_engine
from models import metadata

def create_all_tables():
    engine = get_engine()
    metadata.create_all(engine)
    print("All tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
