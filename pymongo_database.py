from pymongo import MongoClient
import os
from dotenv import load_dotenv
# Retrieve MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Connection options
options = {
    "retryWrites": True,
    "w": "majority",
    "serverSelectionTimeoutMS": 5000,
    "connectTimeoutMS": 10000,
}

# Function to start MongoDB client
def start_client():
    try:
        client = MongoClient(MONGO_URI, **options)
        client.server_info()  # This line ensures that the client is connected
        return client
    except Exception as e:
        print(e)


