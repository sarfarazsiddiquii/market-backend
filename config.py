from pymongo import MongoClient
from dotenv import load_dotenv
import os
import atexit

load_dotenv()  # Load environment variables from a .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    MONGO_URI = os.getenv("DATABASE_URL")
    client = MongoClient(MONGO_URI)
    db = client['user_auth']
    users_collection = db['users']
    meetings_collection = db['meetings']

# Ensure MongoClient is closed on exit
atexit.register(Config.client.close)