import httpx

async def get_sid(email: str, password: str):
    login_url = "https://student.bennetterp.camu.in/login/validate"
    payload = {
        "dtype": "M",
        "Email": email,
        "pwd": password
    }

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(login_url, json=payload)
            data = response.json()["output"]["data"]
            session_id = response.cookies.get("connect.sid")

            if "logindetails" in data:
                print(f"[OK] Session found for {email}: {session_id}")
                return session_id
            else:
                print(f"[FAIL] Login failed for {email}")
                return None
    except Exception as e:
        print(f"[ERROR] get_sid failed for {email}: {e}")
        return None
