import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5433/db_chatbot')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Activer les connexions sécurisées
    PREFERRED_URL_SCHEME = 'https'
