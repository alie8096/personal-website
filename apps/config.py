import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Authentication Configuration
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_EMAIL= os.getenv("DATABASE_EMAIL")
    DATABASE_IS_ADMIN= os.getenv("DATABASE_IS_ADMIN")
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "site.db")

    # Template Configuration
    TEMPLATES_FOLDER = os.getenv("TEMPLATES_FOLDER", "templates")

    # Security Configuration
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Debug Configuration
    DEBUG = os.getenv("DEBUG", True)

    
