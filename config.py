import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class."""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-electronics-2024'
    
    # WhatsApp contact number (for customer support)
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '254701565301')
    
    # Check if using PostgreSQL or SQLite
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Use PostgreSQL (for production/Render)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql+pg8000://')
    elif os.environ.get('DB_HOST'):
        # PostgreSQL with individual env vars
        DB_HOST = os.environ.get('DB_HOST', 'localhost')
        DB_PORT = int(os.environ.get('DB_PORT', 5432))
        DB_USER = os.environ.get('DB_USER', 'postgres')
        DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
        DB_NAME = os.environ.get('DB_NAME', 'electronics_ecommerce')
        SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        # Use SQLite for local development (no database server needed)
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'electronics_ecommerce.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # M-Pesa Daraja API Configuration (Sandbox)
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', 'your_consumer_key')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', 'your_consumer_secret')
    MPESA_BUSINESS_SHORTCODE = os.environ.get('MPESA_BUSINESS_SHORTCODE', '174379')
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', 'your_passkey')
    MPESA_CALLBACK_URL = os.environ.get('MPESA_CALLBACK_URL', 'https://example.com/api/payments/callback')
    MPESA_ENV = os.environ.get('MPESA_ENV', 'sandbox')  # sandbox or production
    
    # Email Configuration (Flask-Mail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5000/api/auth/google/callback')