import requests
import json
from database import *
from sid import *
from datetime import datetime

def fetch_timetable_headerless(sid, json_payload):
    api_url = "https://student.bennetterp.camu.in/api/Timetable/get"
    cookies = {
        "connect.sid": sid
    }

        # Fetch today's date in the required format (YYYY-MM-DD)
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Add additional fields to the payload
    json_payload.update({
        "enableV2": True,
        "start": today_date,
        "end": today_date,
        "schdlTyp": "slctdSchdl",
        "isShowCancelledPeriod": True,
        "isFromTt": True
    })
    
    try:
        # Send the POST request without headers
        response = requests.post(api_url, cookies=cookies, json=json_payload)

        # Check if the response status code indicates success
        if response.status_code == 200:
            # Parse and return the JSON response
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

