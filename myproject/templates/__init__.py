import os
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv

# Create a login manager object
login_manager = LoginManager()

app = Flask(__name__)

# Load configuration
app.config['SECRET_KEY'] = 'mysecretkey'

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "login"

# MongoDB connection
load_dotenv()
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'diet_planner')
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

# Create collections for users
users_collection = mongo_db['users']
