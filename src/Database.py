import mysql.connector
from mysql.connector import Error
import json
import os

class Database:
    def __init__(self, config_path: str):
        """Initialize database connection with config file path."""
        try:
            with open(config_path, 'r') as f:
                self.credentials = json.load(f)
            print("Database credentials loaded successfully")
            self.conn = None

        except FileNotFoundError:
            print(f"Error: The credentials file was not found at {config_path}")
            raise
        except KeyError as e:
            print(f"Error: The key {e} is missing from the database.json file.")
            raise

    def create_connection(self):
        """Create a connection to the database."""
        try:
            self.conn = mysql.connector.connect(
                host=self.credentials['host'],
                user=self.credentials['user'],
                password=self.credentials['password'],
                database=self.credentials['database']
            )
            print("Database connection successful")
            return True
        except Error as e:
            print(f"Database Error: '{e}' occurred")
            return False
    
    def close_connection(self):
        """Close the database connection."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Database connection closed.")
        else:
            print("Connection is already closed.")

    def get_summary_details_by_id(self, detail_id):
        """
        Fetches all profile and application info for a specific detail_id
        using a single, efficient JOIN query.
        """
        if not self.conn or not self.conn.is_connected():
            return None

        details = {}
        cursor = self.conn.cursor(dictionary=True)

        # A single query to get all necessary information
        query = """
        SELECT 
            p.applicant_id, 
            p.first_name, 
            p.last_name,
            p.date_of_birth,
            p.address,
            p.phone_number,
            d.application_role,
            d.cv_path
        FROM 
            applicationdetail d
        JOIN 
            applicantprofile p ON d.applicant_id = p.applicant_id
        WHERE 
            d.detail_id = %s
        """
        try:
            cursor.execute(query, (detail_id,))
            details = cursor.fetchone()
            if details and details.get('date_of_birth'):
                details['date_of_birth'] = details['date_of_birth'].strftime('%Y-%m-%d')
                
        except Error as e:
            print(f"An error occurred while fetching summary details: {e}")
        finally:
            cursor.close()

        return details

    def get_all_cv_data(self):
        """
        Fetches all individual APPLICATIONS (not applicants) from the database.
        Each row represents a unique CV to be searched.
        """
        if not self.conn or not self.conn.is_connected():
            return []

        results = []
        cursor = self.conn.cursor(dictionary=True)

        # This query joins the tables to get all necessary info for each application
        query = """
        SELECT 
            d.detail_id, 
            p.applicant_id, 
            p.first_name, 
            p.last_name,
            d.application_role,
            d.cv_path 
        FROM 
            applicationdetail d
        JOIN 
            applicantprofile p ON d.applicant_id = p.applicant_id
        """
        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            cursor.close()

        return results