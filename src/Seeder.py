import mysql.connector
from mysql.connector import Error
import os
import json
from src.DirectoryScanner import DirectoryScanner

class Seeder:
        """
        Seeds a MariaDB/MySQL database from a directory structure using DirectoryScanner.
        """
        def __init__(self, base_dir: str, config_path: str):
                """
                Initializes the Seeder.
                @param base_dir (str): The path to the root directory to scan.
                @param config_path (str): Path to the JSON config file containing database connection parameters.
                """
                print(f"\nInitializing Seeder for directory: '{base_dir}'")
                self.scanner = DirectoryScanner(base_dir)
                try:
                        with open(config_path, 'r') as config_file:
                                self.db_config = json.load(config_file)
                        print(f"Successfully loaded database config from '{config_path}'")
                except Exception as e:
                        print(f"Error loading database config from '{config_path}': {e}")
                        raise
                self.conn = None
                self.cursor = None

        def _connect_db(self):
                """Establishes a connection to the MariaDB/MySQL database."""
                try:
                        self.conn = mysql.connector.connect(**self.db_config)
                        self.cursor = self.conn.cursor()
                        print(f"Successfully connected to database '{self.db_config.get('database')}'")
                except Error as e:
                        print(f"Error connecting to MariaDB/MySQL database: {e}")
                        raise

        def _close_db(self):
                """Closes the database connection."""
                if self.conn and self.conn.is_connected():
                        self.conn.commit()
                        self.cursor.close()
                        self.conn.close()
                        print(f"Database connection closed.")

        def create_tables(self):
                """
                Creates the database tables based on the ERD.
                """
                self._connect_db()
                try:
                        db_name = self.db_config.get('database')
                        # Use IF EXISTS for safer dropping
                        self.cursor.execute(f"DROP TABLE IF EXISTS {db_name}.ApplicationDetail")
                        self.cursor.execute(f"DROP TABLE IF EXISTS {db_name}.ApplicantProfile")
                        print("Dropped existing tables (if any).")

                        self.cursor.execute('''
                                CREATE TABLE ApplicantProfile (
                                applicant_id INT AUTO_INCREMENT PRIMARY KEY,
                                first_name VARCHAR(50) DEFAULT NULL,
                                last_name VARCHAR(50) DEFAULT NULL,
                                date_of_birth DATE DEFAULT NULL,
                                address VARCHAR(255) DEFAULT NULL,
                                phone_number VARCHAR(20) DEFAULT NULL
                                )
                        ''')
                        print("Table 'ApplicantProfile' created successfully.")

                        self.cursor.execute('''
                                CREATE TABLE ApplicationDetail (
                                detail_id INT AUTO_INCREMENT PRIMARY KEY,
                                applicant_id INT NOT NULL,
                                application_role VARCHAR(100) DEFAULT NULL,
                                cv_path TEXT,
                                FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id) ON DELETE CASCADE
                                )
                        ''')
                        print("Table 'ApplicationDetail' created successfully.")
                except Error as e:
                        print(f"Error creating tables: {e}")
                finally:
                        self._close_db()

        def seed_data(self):
                """
                Scans the directory and populates the database tables.
                Creates groups of applicants with different numbers of applications:
                - 5 applicants with 1 role each
                - 5 applicants with 2 roles each
                - 5 applicants with 3 roles each
                And so on...
                """
                import random
                from datetime import datetime, timedelta

                def generate_random_date(start_year=1970, end_year=2000):
                    start_date = datetime(start_year, 1, 1)
                    end_date = datetime(end_year, 12, 31)
                    days_between = (end_date - start_date).days
                    random_days = random.randint(0, days_between)
                    return start_date + timedelta(days=random_days)

                def generate_random_phone():
                    prefix = random.choice(['0812', '0813', '0814', '0815', '0816', '0855', '0856', '0857', '0858'])
                    suffix = ''.join(random.choices('0123456789', k=8))
                    return f"{prefix}{suffix}"

                def generate_random_address():
                    streets = ['Jalan Sudirman', 'Jalan Thamrin', 'Jalan Gatot Subroto', 'Jalan Asia Afrika', 
                              'Jalan Diponegoro', 'Jalan Ahmad Yani', 'Jalan Pahlawan']
                    cities = ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta', 'Semarang', 'Medan', 'Palembang']
                    numbers = random.randint(1, 200)
                    street = random.choice(streets)
                    city = random.choice(cities)
                    return f"{street} No. {numbers}, {city}"

                file_map = self.scanner.getMap()
                if not file_map:
                    print("No data to seed. The scanned directory is empty or unreadable.")
                    return

                # Convert file_map into a list of roles for easier access
                roles = [(role, paths) for role, paths in file_map.items()]
                total_roles = len(roles)

                self._connect_db()
                try:
                    # Create groups of applicants with different numbers of role applications
                    current_applicant_id = 1
                    
                    # For each group (1 role, 2 roles, 3 roles, etc.)
                    for num_roles in range(1, total_roles + 1):
                        print(f"\nCreating applicants who will apply for {num_roles} role(s)...")
                        
                        # Create 5 applicants for this group
                        for i in range(5):
                            # Create applicant profile
                            first_name = f"Group{num_roles}"
                            last_name = f"Applicant{current_applicant_id}"
                            date_of_birth = generate_random_date().strftime('%Y-%m-%d')
                            address = generate_random_address()
                            phone_number = generate_random_phone()

                            self.cursor.execute('''
                                INSERT INTO ApplicantProfile 
                                (first_name, last_name, date_of_birth, address, phone_number) 
                                VALUES (%s, %s, %s, %s, %s)
                            ''', (first_name, last_name, date_of_birth, address, phone_number))
                            
                            applicant_id = self.cursor.lastrowid
                            print(f"  - Created profile for {first_name} {last_name} (ID: {applicant_id})")

                            # Select random roles for this applicant
                            selected_roles = random.sample(roles, num_roles)
                            
                            # Create applications for each selected role
                            for role, paths in selected_roles:
                                # Pick a random CV path from this role's available paths
                                cv_path = random.choice(paths)
                                application_role = role.replace('-', ' ').replace('_', ' ').title()
                                
                                self.cursor.execute('''
                                    INSERT INTO ApplicationDetail 
                                    (applicant_id, application_role, cv_path) 
                                    VALUES (%s, %s, %s)
                                ''', (applicant_id, application_role, cv_path))
                                
                                detail_id = self.cursor.lastrowid
                                print(f"    - Created application (ID: {detail_id}) for role '{application_role}'")
                            
                            current_applicant_id += 1

                except Error as e:
                    print(f"Error seeding data: {e}")
                finally:
                    self._close_db()
                    print("\nData seeding process complete.")

        def verify_data(self):
                """
                Connects to the database and prints its contents to verify seeding.
                Shows how different groups of applicants have different numbers of applications.
                """
                print("\n--- Verifying Seeded Data ---")
                self._connect_db()
                try:
                        print("\n--- ApplicantProfile Table ---")
                        query = """
                            SELECT p.*, COUNT(d.detail_id) as total_applications
                            FROM ApplicantProfile p
                            LEFT JOIN ApplicationDetail d ON p.applicant_id = d.applicant_id
                            GROUP BY p.applicant_id
                            ORDER BY p.applicant_id
                            LIMIT 15;
                        """
                        self.cursor.execute(query)
                        print("(applicant_id, first_name, last_name, dob, address, phone, total_applications)")
                        for row in self.cursor.fetchall():
                                print(row)

                        print("\n--- ApplicationDetail Table (showing multiple roles per applicant) ---")
                        query = """
                            SELECT d.detail_id, d.applicant_id, p.first_name, p.last_name, d.application_role
                            FROM ApplicationDetail d
                            JOIN ApplicantProfile p ON d.applicant_id = p.applicant_id
                            ORDER BY d.applicant_id, d.detail_id
                            LIMIT 30;
                        """
                        self.cursor.execute(query)
                        print("(detail_id, applicant_id, first_name, last_name, role)")
                        for row in self.cursor.fetchall():
                                print(row)
                        
                        print("\n--- Application Count Summary ---")
                        query = """
                            SELECT 
                                SUBSTRING_INDEX(p.first_name, 'Group', -1) as group_number,
                                COUNT(DISTINCT p.applicant_id) as applicants_in_group,
                                COUNT(d.detail_id) / COUNT(DISTINCT p.applicant_id) as applications_per_applicant
                            FROM ApplicantProfile p
                            LEFT JOIN ApplicationDetail d ON p.applicant_id = d.applicant_id
                            GROUP BY SUBSTRING_INDEX(p.first_name, 'Group', -1)
                            ORDER BY CAST(SUBSTRING_INDEX(p.first_name, 'Group', -1) AS SIGNED);
                        """
                        self.cursor.execute(query)
                        print("(group_number, applicants_in_group, applications_per_applicant)")
                        for row in self.cursor.fetchall():
                                print(row)
                except Error as e:
                        print(f"Error verifying data: {e}")
                finally:
                        self._close_db()