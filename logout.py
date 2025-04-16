import requests

def logout(session_cookie):
    url = "https://student.bennetterp.camu.in/api/logout"
    headers = {
        "Host": "student.bennetterp.camu.in",
        "Cookie": f"connect.sid={session_cookie}",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Clienttzofst": "330",
        "Origin": "https://student.bennetterp.camu.in",
        "Referer": "https://student.bennetterp.camu.in/v2/timetable",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Priority": "u=0",
        "Te": "trailers"
    }
    payload = {"isSessionDestroy": True}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200 and response.json().get("isLogOutStatus") == True:
            print("Logout successful!")
            return True
        else:
            print("Logout failed! Response:", response.json())
            return False
    except Exception as e:
        print("Error during logout:", str(e))
        return False