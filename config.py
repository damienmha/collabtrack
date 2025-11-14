import os
from dotenv import load_dotenv

# CRITICAL STEP: Load .env variables
# This looks for the .env file in the same directory and loads the keys/values 
# into the environment (os.environ).
load_dotenv() 

class Config:
    """Base configuration settings for the Flask application."""
    
    # Flask App Secrets 
    # Used for sessions and security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_insecure_default_key_dont_use_in_prod'
    
    # Database Configuration (PostgreSQL)
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    
    # SQLAlchemy format for the connection string
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:"
        f"{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Recommended to suppress warnings
    
    # WS S3 Configuration 
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_REGION = os.environ.get('AWS_REGION')

    # CRITICAL: Fix for session persistence on redirect in development environments
    SESSION_COOKIE_SAMESITE = 'Lax'