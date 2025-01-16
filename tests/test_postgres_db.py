from sqlalchemy import create_engine

DATABASE_URL = 'postgresql://postgres:newpassword@localhost:5432/postgres'

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Connected to the database successfully!")
    connection.close()
except Exception as e:
    print(f"Failed to connect: {e}")
