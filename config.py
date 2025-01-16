import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Use environment variable or fallback
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://postgres:newpassword@localhost:5432/postgres')  # Use environment variable or fallback
    SQLALCHEMY_TRACK_MODIFICATIONS = False
