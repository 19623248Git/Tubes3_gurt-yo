import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection to the MariaDB database."""
    conn = None
    try:
        # --- IMPORTANT ---
        # Replace these values with your actual database credentials
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      # e.g., 'root'
            password="",
            database="tubes_3_stima"
        )
        print("Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
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
    # The project spec shows a one-to-many relationship, so we will
    # fetch the first matching application detail for simplicity.
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

# You will also need a function to get all CVs for the search logic later
def get_all_cv_data(conn):
    """Fetches the id, name, and CV path for all applicants."""
    if not conn or not conn.is_connected():
        print("Database is not connected.")
        return []

    results = []
    cursor = conn.cursor(dictionary=True)

    # MODIFIED: Select the applicant_id as well
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