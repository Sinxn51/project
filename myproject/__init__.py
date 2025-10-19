import os
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv


# Create a login manager object
login_manager = LoginManager()

load_dotenv()

# Often people will also separate these into a separate config.py file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='templates', static_url_path='')

# Load configuration
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')

app.config.from_object(Config)

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"

# MongoDB (Compass/local) connection
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'diet_planner')
mongo_client: MongoClient = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

# Create collections for users
users_collection = mongo_db['users']