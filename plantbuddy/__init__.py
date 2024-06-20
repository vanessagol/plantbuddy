from flask import Flask, session
from flask_mail import Mail
from flask_login import LoginManager
from .config import init_app
import os
from .database.db import Customer
from .database.seeds import populate_db


mail = Mail()
login_manager = LoginManager()

def create_app():
    print("create app")
    app = Flask(__name__, instance_relative_config=True)
    init_app(app)

    # Set environment variable for development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    from .database import db
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))


    with app.app_context():
        db.create_all()
        # Check if every Table is empty
        NEW_DB = all(db.session.query(table).first()
                     is None for table in db.metadata.sorted_tables)

        if NEW_DB:
            print("All tables are empty. Seeding database...")
            populate_db()


    from .site.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .site.plant_management import plants_bp
    app.register_blueprint(plants_bp)

    from .site.routes import main_bp
    app.register_blueprint(main_bp)

    # Add the clear_flashes function to Jinja globals
    app.jinja_env.globals.update(clear_flashes=clear_flashes)


    return app

def clear_flashes():
    if '_flashes' in session:
        del session['_flashes']
