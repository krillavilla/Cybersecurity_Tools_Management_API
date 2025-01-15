from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

# Configure database URI and secret keys
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tools.db'  # For simplicity, using SQLite here
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')  # Can be stored in .env file
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')  # Auth0

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

from . import routes  # Import routes after initializing app
