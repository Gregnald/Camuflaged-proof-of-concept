import sqlite3
import os
import json
from login import *

# Global variable for the database name
db_name = "database.db"

# Function to create the database and specified table
# By default, creates 'users' table with two columns
def create_db(table='users', db_name="database.db", **columns):
    if not columns:
        columns = {"email": "TEXT UNIQUE NOT NULL", "password": "TEXT NOT NULL"}
    columns_str = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, {columns_str})")
        print(f"Database and table '{table}' created successfully in '{db_name}'!")

# Insert a new user into the database, optionally storing a JSON file
def new_user(db_name="database.db", table="users",**user_data):
    columns = ", ".join(user_data.keys())
    placeholders = ", ".join("?" for _ in user_data)
    values = tuple(user_data.values())
    try:
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            c.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
            conn.commit()
            print("New user added successfully.",values)
            return True
    except sqlite3.IntegrityError:
        print("Error: Duplicate entry or constraint violation.")

# Clear all entries in a table
def clear_db(table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table}")
        conn.commit()
        print(f"All entries in '{table}' table cleared.")

# Delete the entire database file
def del_db(db_name="database.db"):
    try:
        os.remove(db_name)
        print(f"Database '{db_name}' deleted successfully.")
    except FileNotFoundError:
        print("No database found to delete.")

# Delete specific users by unique keys
def del_user(table="users", db_name="database.db", **conditions):
    condition_str = " AND ".join([f"{col} = ?" for col in conditions])
    values = tuple(conditions.values())
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table} WHERE {condition_str}", values)
        conn.commit()
        print("User(s) deleted successfully.")

# Read user details by conditions (supports multiple filters)
def read_user(table="users", db_name="database.db", **conditions):
    condition_str = " AND ".join([f"{col} = ?" for col in conditions])
    values = tuple(conditions.values())
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        query = f"SELECT * FROM {table} WHERE {condition_str}"
        c.execute(query, values)
        results = c.fetchall()
        for result in results:
            print(result)
        return results

# Modify specific entries of a user
def modify_user(table="users", db_name="database.db", conditions=None, **updates):
    if not conditions:
        print("No conditions provided for update.")
        return
    update_str = ", ".join([f"{col} = ?" for col in updates])
    condition_str = " AND ".join([f"{col} = ?" for col in conditions])
    values = tuple(updates.values()) + tuple(conditions.values())
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"UPDATE {table} SET {update_str} WHERE {condition_str}", values)
        conn.commit()
        print("User modified successfully.")

# Read all entries in a table
def read_all(table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table}")
        results = c.fetchall()
        for row in results:
            print(row)
        return results

# Read a specific table
def read_table(table, db_name="database.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table}")
            return c.fetchall()
    except sqlite3.OperationalError:
        print(f"Table '{table}' not found.")
        return None

# Add a column to a specific table
def add_column(table="users", db_name="database.db", **columns):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        try:
            for column_name, column_type in columns.items():
                c.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
                print(f"Column '{column_name}' added to table '{table}'.")
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")

# Delete a column from a specific table (SQLite 3.35+)
def del_column(column, table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        try:
            c.execute(f"ALTER TABLE {table} DROP COLUMN {column}")
            print(f"Column '{column}' deleted from table '{table}'.")
        except sqlite3.OperationalError as e:
            print(f"Error: {e}")

# Add a new table
def add_table(table="users", db_name="database.db", **columns):
    columns_str = ", ".join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table} ({columns_str})")
        print(f"Table '{table}' created successfully.")

# Delete a specific table
def del_table(table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        try:
            c.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Table '{table}' deleted successfully.")
        except sqlite3.OperationalError:
            print(f"Table '{table}' not found.")

# Store a JSON file in the database linked to a specific email
def store_js(file_data, email, column="bahikhata", table="users", db_name="database.db"):
    # Ensure the data is a JSON string and then encode it to binary
    json_data = json.dumps(file_data)  # Convert to JSON string
    binary_data = json_data.encode('utf-8')  # Convert JSON string to binary
    
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        
        # Check if the email exists in the table
        c.execute(f"SELECT 1 FROM {table} WHERE email = ?", (email,))
        exists = c.fetchone()
        
        if exists:
            # Update the existing entry
            c.execute(f"UPDATE {table} SET {column} = ? WHERE email = ?", (binary_data, email))
            print(f"Updated data for email '{email}' in the database.")
        else:
            # Insert a new entry
            c.execute(f"INSERT INTO {table} (email, {column}) VALUES (?, ?)", (email, binary_data))
            print(f"File stored successfully as a new entry linked to email '{email}'.")
        
        # Commit changes
        conn.commit()

# Retrieve a JSON file from the database linked to a specific email
def retrieve_js(email, column="bahikhata", table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        
        # Retrieve the binary data
        c.execute(f"SELECT {column} FROM {table} WHERE email = ?", (email,))
        result = c.fetchone()
        
        if result:
            binary_data = result[0]  # The binary data stored in the database
            
            try:
                # Decode binary to JSON string and then parse to dictionary
                json_data = json.loads(binary_data.decode('utf-8'))  # Decode and parse JSON
                
                # Convert to indented JSON string for readability
                indented_json = json.dumps(json_data, indent=None)
                return indented_json
            except (UnicodeDecodeError, json.JSONDecodeError):
                print("Error: Failed to decode or parse JSON data.")
                return None
        else:
            print(f"No data found for email '{email}'.")
            return None
        
def get_pass(email, column="password", table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        c.execute(f"SELECT {column} FROM {table} WHERE email = ?", (email,))
        result=c.fetchone()
        if result:
            return result[0]
        else:
            print("No password found for",email)
            return None
        
def get_stu(email, column="password", table="users", db_name="database.db"):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        json_data = retrieve_js(email)
        try:
            indented_json = json.loads(json_data)
            StuID = indented_json["output"]["data"]["logindetails"]["Student"][0]["StuID"]
            if StuID:
                return StuID
            else:
                return None
        except Exception as e:
            print("Failed to fetch JSON file")
            return None
        
def db_login(email:str,password:str, table="users", db_name="database.db"):
    from login import login_check
    if login_check(email,password):
        with sqlite3.connect(db_name) as conn:
            c = conn.cursor()
            c.execute(f"SELECT password FROM {table} WHERE email = ?", (email,))
            result=c.fetchone()
            if result and result[0]==password:
                return True
            else:
                return False
    return False