from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'plantbuddy.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='key_var'  # Add a unique and secret key here
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    from .plant_management import plants_bp  # Relative import
    app.register_blueprint(plants_bp, url_prefix='/plants')

    return app
