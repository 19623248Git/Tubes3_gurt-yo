import mysql.connector
from mysql.connector import Error
import json
import os

def create_connection():
    conn = None
    try:
        file_path = 'config/database.json'

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

def get_applicant_details(conn, name):
    """
    Query the database for applicant details by their first name.
    This function joins the applicantprofile and applicationdetail tables.
    """
    if not conn or not conn.is_connected():
        print("Database is not connected.")
        return None

    # The result will be a dictionary to hold the fetched data
    applicant_data = {}
    
    # Use a dictionary cursor to get results as {column_name: value}
    cursor = conn.cursor(dictionary=True) 

    # SQL Query to join the tables and get all required info
    query = """
    SELECT 
        p.first_name,
        p.last_name,
        p.date_of_birth,
        p.address,
        p.phone_number,
        d.application_role,
        d.cv_path
    FROM 
        applicantprofile p
    JOIN 
        applicationdetail d ON p.applicant_id = d.applicant_id
    WHERE 
        p.applicant_id = %s
    LIMIT 1
    """

    try:
        # The (name,) is a tuple containing the parameter for the query
        cursor.execute(query, (name,))
        result = cursor.fetchone() # Fetch the first matching record
        if result:
            applicant_data = result
            # Convert date object to a string for display
            if applicant_data.get('date_of_birth'):
                applicant_data['date_of_birth'] = applicant_data['date_of_birth'].strftime('%d-%m-%Y')

    except Error as e:
        print(f"The error '{e}' occurred")
    return applicant_data

def get_all_cv_data(conn):
    """Fetches the id, name, and CV path for all applicants."""
    if not conn or not conn.is_connected():
        print("Database is not connected.")
        return []

    results = []
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.applicant_id, p.first_name, d.cv_path 
    FROM applicantprofile p
    JOIN applicationdetail d ON p.applicant_id = d.applicant_id
    """
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

    return results