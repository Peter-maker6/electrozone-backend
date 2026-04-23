import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class."""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-electronics-2024'
    
    # WhatsApp contact number (for customer support)
    WHATSAPP_NUMBER = os.environ.get('WHATSAPP_NUMBER', '254701565301')
    
    # PostgreSQL Database configuration (Render provides this)
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'electronics_ecommerce')
    
    # PostgreSQL URI
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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