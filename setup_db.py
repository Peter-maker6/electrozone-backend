import pymysql
from config import Config

def create_database():
    """Create the database if it doesn't exist."""
    try:
        # Connect without database first
        connection = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
            print(f"✓ Database '{Config.DB_NAME}' created or already exists")
        
        connection.close()
        print("✓ MySQL database setup complete!")
        return True
        
    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        print("\nPlease make sure:")
        print("1. MySQL is running")
        print("2. The credentials in config.py are correct")
        print("3. MySQL server allows remote connections (if applicable)")
        return False

if __name__ == '__main__':
    create_database()