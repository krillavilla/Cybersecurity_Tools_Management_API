# app.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import api_bp
from config import Config
from models import db
from dotenv import load_dotenv

def create_app(config_class=Config):
    load_dotenv()  # This will load the .env file

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Use environment variables from Config instead of hardcoded values
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Cybersecurity Tools Management API!"})

    # Error handlers for different status codes
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")

    return app

app = create_app()

if __name__ == '__main__':
    # Only enable debug mode in development environments
    # In production, this should be False to prevent information leakage
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode)
