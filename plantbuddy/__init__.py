from flask import Flask, session
from flask_mail import Mail
from flask_login import LoginManager
from .config import init_app
import os
from .database.db import Customer


mail = Mail()
login_manager = LoginManager()

def create_app():
    print("create app")
    app = Flask(__name__, instance_relative_config=True)
    print("init app")
    init_app(app)

    # Set environment variable for development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    from .database import db
    print("dbinit")
    db.init_app(app)
    mail.init_app(app)
    print("loginit")
    login_manager.init_app(app)
    print("r")

    
    print("dbimp")
    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))
    
    print("2")

    with app.app_context():
        db.create_all()

    print("3")

    from .site.auth import auth_bp
    print("31")
    app.register_blueprint(auth_bp)
    print("32")

    from .site.plant_management import plants_bp
    app.register_blueprint(plants_bp)

    from .site.routes import main_bp
    app.register_blueprint(main_bp)

    print("4")

    # Add the clear_flashes function to Jinja globals
    app.jinja_env.globals.update(clear_flashes=clear_flashes)

    print("Returning app")

    return app

def clear_flashes():
    if '_flashes' in session:
        del session['_flashes']
