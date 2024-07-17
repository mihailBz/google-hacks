import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    GOOGLE_CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
