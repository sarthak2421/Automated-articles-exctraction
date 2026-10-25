import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; set env vars manually

app = Flask(__name__)
# Adding configuration to app of database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketdb.db'
# SECRET_KEY should be set in environment variable (never hardcode in source)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-change-in-production')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # To route unsigned user to login page.
login_manager.login_message_category = 'info'
from Crop import models
from Crop import routes
