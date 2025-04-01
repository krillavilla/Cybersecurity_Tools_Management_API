# config.py
import os
from datetime import timedelta


class Config:
    """
    Base configuration class with default settings for the application.
    """
    # Critical security settings - will raise error if not set
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. This is a required environment variable.")

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for Flask application. This is a required environment variable.")

    # Database URI without hardcoded credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL set. This is a required environment variable.")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ['headers']  # or wherever you want to look for the JWT token (e.g., cookies, headers)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # 1 hour
    JWT_HEADER_NAME = "Authorization"


class TestConfig(Config):
    """
    Configuration class for testing with a separate database.
    """
    # Override the database URI validation from parent class
    # For testing, we'll use a SQLite in-memory database if TEST_DATABASE_URL is not set
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL', 'sqlite:///:memory:')
    TESTING = True


class SQLiteTestConfig:
    """
    Configuration class for testing with an in-memory SQLite database.
    This is useful for unit tests that should not interact with the actual database.

    Note: This class does not inherit from Config to avoid the environment variable
    validation, as it's specifically designed for isolated testing.
    """
    # Use secure random values for testing only
    SECRET_KEY = os.environ.get('SECRET_KEY', 'test-secret-key-' + os.urandom(24).hex())
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'test-jwt-key-' + os.urandom(24).hex())

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Testing configuration
    TESTING = True
    WTF_CSRF_ENABLED = False

    # JWT configuration
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_HEADER_NAME = "Authorization"
