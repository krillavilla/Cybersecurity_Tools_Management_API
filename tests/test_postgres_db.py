from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use TEST_DATABASE_URL for testing
# If not set, inform the user rather than using hardcoded credentials
DATABASE_URL = os.environ.get('TEST_DATABASE_URL')
if not DATABASE_URL:
    print("Warning: TEST_DATABASE_URL environment variable is not set.")
    print("For security reasons, this test requires a valid database URL.")
    print("Please set TEST_DATABASE_URL in your .env file or environment.")
    print("Example: postgresql://username:password@localhost:5432/test_db")
    exit(1)

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Connected to the database successfully!")
    connection.close()
except Exception as e:
    print(f"Failed to connect: {e}")
