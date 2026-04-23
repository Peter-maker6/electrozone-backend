"""
Drop and recreate the entire database fresh.
"""
import pymysql
from config import Config

# First, connect WITHOUT database to drop and recreate it
connection = pymysql.connect(
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD
)

try:
    with connection.cursor() as cursor:
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Drop database if exists
        cursor.execute(f"DROP DATABASE IF EXISTS {Config.DB_NAME}")
        print(f"🗑️ Dropped database '{Config.DB_NAME}'")
        
        # Create fresh database
        cursor.execute(f"CREATE DATABASE {Config.DB_NAME}")
        print(f"✓ Created new database '{Config.DB_NAME}'")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
    connection.commit()
    print("\n✅ Database completely reset!")
    print("Now run: python run.py")

finally:
    connection.close()