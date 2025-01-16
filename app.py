from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import os

# Initialize db and migrate
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.route('/')
    def index():
        return 'Welcome to the Cybersecurity Tools Management API!'

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
