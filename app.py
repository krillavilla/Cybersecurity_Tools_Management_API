# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import api_bp
from config import Config
from models import db
from dotenv import load_dotenv

def create_app():
    load_dotenv()  # This will load the .env file

    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Cybersecurity Tools Management API!"})

    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)