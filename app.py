from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from models import db
from routes import api_bp
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Add the JWT secret key or flask secret key here
    app.config[
        'JWT_SECRET_KEY'] = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVxTm1OSTl0TllYME91UlM3V1U5RCJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktY29mc2hwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJkWWZZOWZMVFBsZ1ZFM2tnWHVIUUZHS0xwN01meGd5SEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9zZWN1cml0eWFwcC8iLCJpYXQiOjE3MzcyODExOTcsImV4cCI6MTczNzM2NzU5Nywic2NvcGUiOiJyZWFkOnRvb2xzIGNyZWF0ZTp0b29scyB1cGRhdGU6dG9vbHMgZGVsZXRlOnRvb2xzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiZFlmWTlmTFRQbGdWRTNrZ1h1SFFGR0tMcDdNZnhneUgifQ.FBNZXjTD2A79NxbhjlQDcwsLtMzJc1l-IoCZkwuQISDgnCvyLUQG2VskpxEUvEifPQFYTbGT-6ySMVquEaucAcQloGPyX2l7ZDriUxV7TqJlpzIRgoLB3G4dFCZqdlsOr1YjOJQCKIyRyKjoF_6okXYuFn_qBNER-XS76c_abJyAw81Pj3w23fxcjKnY2-zAdhZDyrN0nGSom-Zd3khQBvBhq6Rnv9ghyFVUMK_q6xiyt_ipkfrTCr79eAjUyNvYF8vuyyn1DRJFW9Q1dRW30-1OmNyVpCGm8dV1sodu6sAQMDteplzLqdE6OgZVMriwIzN-WnX9R76JglLz5WrpCg'  # Replace with a secure secret key
    app.config['SECRET_KEY'] = 'your_secret_key'  # This is the Flask secret key used for sessions and cookies

    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    # Initialize the JWTManager
    jwt = JWTManager(app)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (if any)
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
