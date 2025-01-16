from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .routes import main as main_blueprint

# Initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprint
    app.register_blueprint(main_blueprint)

    return app
