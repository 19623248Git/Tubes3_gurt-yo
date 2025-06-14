import mysql.connector
from mysql.connector import Error
import json
import os

def create_connection():
    conn = None
    try:
        file_path = '../config/database.json'

        with open(file_path, 'r') as f:
            credentials = json.load(f)

        conn = mysql.connector.connect(
            host=credentials['host'],
            user=credentials['user'],
            password=credentials['password'],
            database=credentials['database']
        )
        print("Database connection successful")

    except FileNotFoundError:
        print(f"Error: The credentials file was not found at {file_path}")
    except KeyError as e:
        print(f"Error: The key {e} is missing from the database.json file.")
    except Error as e:
        print(f"Database Error: '{e}' occurred")
    
    return conn

def close_connection(conn):
    """Close the database connection."""
    if conn.is_connected():
        conn.close()
        print("Database connection closed.")
    else:
        print("Connection is already closed.")

def get_summary_details_by_id(conn, detail_id):
    """
    Fetches all profile and application info for a specific detail_id
    using a single, efficient JOIN query.
    """
    if not conn or not conn.is_connected():
        return None

    details = {}
    cursor = conn.cursor(dictionary=True)

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

def get_all_cv_data(conn):
    """
    Fetches all individual APPLICATIONS (not applicants) from the database.
    Each row represents a unique CV to be searched.
    """
    if not conn or not conn.is_connected():
        return []

    results = []
    cursor = conn.cursor(dictionary=True)

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