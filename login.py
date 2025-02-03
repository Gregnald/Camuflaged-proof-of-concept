import os
import json
import requests
from database import *

import sqlite3
import requests

def delete_existing_user(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the email exists in the users table
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    # If the user exists, delete the record
    if existing_user:
        cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        conn.commit()

    conn.close()

def login_and_save_data(email: str, password: str):
    login_url = "https://student.bennetterp.camu.in/login/validate"
    payload = {
        "dtype": "M",
        "Email": email,
        "pwd": password
    }

    s = requests.Session()
    response = s.post(login_url, json=payload)

    try:
        resp_data = response.json()
        #print("Login Response:", resp_data)  # Debugging: Print the full response

    except ValueError:
        print("Failed to parse the response as JSON.")
        return False

    if resp_data and "output" in resp_data and "data" in resp_data["output"]:
        data = resp_data["output"]["data"]
        if "logindetails" in data:
            # Login successful
            delete_existing_user(email)
            email_prefix = email.split("@")[0].upper() # Extract the part before @ from the email
            email_end = email.split("@")[1]
            email = email_prefix + "@" + email_end
            delete_existing_user(email)
            new_user(name=data["logindetails"]["Name"],reg_no=email_prefix,email=email,password=password)
            store_js(resp_data,email)

            return True
        elif data.get("code") == "INVALID_CRED":
            print("Login failed: Invalid credentials.")
            return False

    print("Login failed: Unexpected response structure.")
    return False

def login_check(email: str, password: str):
    login_url = "https://student.bennetterp.camu.in/login/validate"
    payload = {
        "dtype": "M",
        "Email": email,
        "pwd": password
    }

    s = requests.Session()
    response = s.post(login_url, json=payload)

    try:
        resp_data = response.json()
    except ValueError:
        print("Failed to parse the response as JSON.")
        return False

    if resp_data and "output" in resp_data and "data" in resp_data["output"]:
        data = resp_data["output"]["data"]
        if "logindetails" in data:
            return True
        elif data.get("code") == "INVALID_CRED":
            print("Login failed: Invalid credentials.")
            return False

    # print("Login failed: Unexpected response structure.")
    return False
