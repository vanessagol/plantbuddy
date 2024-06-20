import os
from dotenv import load_dotenv
from itsdangerous import URLSafeTimedSerializer
from oauthlib.oauth2 import WebApplicationClient

# Load environment variables from a .env file
load_dotenv()

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(INSTANCE_PATH, "plantbuddy.db")}'
    
    # SQLALCHEMY_DATABASE_URI = (
    #      f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}"
    #      f"@/{os.environ.get('DB_NAME')}?unix_socket=/cloudsql/{os.environ.get('plantbuddy-426722:us-central1:plantbuddy-mysql-instance')}"
    # )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')  # Replace with a strong default or raise an error

    # Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'default-email@example.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '#private')  # Use environment variable

    # OAuth 2 client setup for login with google
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '#private')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '#private')
    GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

def init_app(app):
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']

s = URLSafeTimedSerializer(Config.SECRET_KEY)
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)
