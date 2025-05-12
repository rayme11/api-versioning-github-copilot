import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/?replicaSet=rs0")  # Removed extra "/"
DATABASE_NAME = os.getenv("MONGO_APP_DB_NAME", "bookhub")