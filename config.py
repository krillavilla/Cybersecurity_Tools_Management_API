# config.py
import os
from datetime import timedelta


class Config:
    """
    Base configuration class with default settings for the application.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:newpassword@localhost:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['headers']  # or wherever you want to look for the JWT token (e.g., cookies, headers)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 1 hour
    JWT_HEADER_NAME = "Authorization"
