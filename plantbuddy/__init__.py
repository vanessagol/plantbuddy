from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from .config import init_app
import os

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    init_app(app)

    # Set environment variable for development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .models import Customer
    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .plant_management import plants_bp
    app.register_blueprint(plants_bp, url_prefix='/plants')

    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Add the clear_flashes function to Jinja globals
    app.jinja_env.globals.update(clear_flashes=clear_flashes)

    return app

def clear_flashes():
    if '_flashes' in session:
        del session['_flashes']
