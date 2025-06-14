import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.Seeder import Seeder
from mysql.connector import Error

def test_database_connection():
    base_dir = '../data'
    config_path = '../config/database.json'
    seeder = None
    
    try:
        # Initialize seeder
        seeder = Seeder(base_dir, config_path)
        print("\nTesting database connection...")
        
        # Test connection by attempting to connect
        seeder._connect_db()
        if seeder.conn and seeder.conn.is_connected():
            server_info = seeder.conn.get_server_info()
            print(f"✓ Successfully connected to MySQL Server version {server_info}")
            
            # Get database info
            seeder.cursor.execute("SELECT DATABASE()")
            database_name = seeder.cursor.fetchone()[0]
            print(f"✓ Connected to database: {database_name}")
            return True
        else:
            print("✗ Failed to establish database connection")
            return False
            
    except Error as e:
        print(f"✗ Database connection failed: {str(e)}")
        return False
    finally:
        if seeder and hasattr(seeder, 'conn') and seeder.conn and seeder.conn.is_connected():
            seeder._close_db()
            print("✓ Database connection closed successfully")

def test_seeder():
    if not test_database_connection():
        print("✗ Database connection test failed. Skipping seeder test.")
        return False

    # Test initialization and database connection
    base_dir = '../data'
    config_path = '../config/database.json'
    
    try:
        # Initialize seeder
        seeder = Seeder(base_dir, config_path)
        print("✓ Seeder initialization successful")
        
        # Test table creation
        seeder.create_tables()
        print("✓ Table creation successful")
        
        # Test data seeding
        seeder.seed_data()
        print("✓ Data seeding successful")
        
        # Verify seeded data
        seeder.verify_data()
        print("✓ Data verification successful")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Seeder tests...")
    success = test_seeder()  # This will run database connection test first
    sys.exit(0 if success else 1)