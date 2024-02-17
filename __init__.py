from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys

sys.path.append('C:\\Users\\Admin\\PycharmProjects')

app = Flask(__name__, instance_relative_config=False)
app.url_map.strict_slashes = False
app.config.from_object('config.config.Config')
db = SQLAlchemy(app)


def create_app():
    """Construct the core application."""
    # db.init_app(app)

    with app.app_context():
        # Imports
        from models import models
        from routes import adminroutes, stream
        # Initialize Global db
        db.create_all()

        return app
