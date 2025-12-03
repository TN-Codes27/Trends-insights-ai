from connection import get_engine

def test_connection():
    try: 
        engine = get_engine()
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print("Database connection failed:", e)

if __name__ == "__main__":
    test_connection()