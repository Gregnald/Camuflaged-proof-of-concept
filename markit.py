import httpx
import asyncio
import sqlite3
from sid import get_sid
from database import *
from qr import *
from getpass import getpass

async def mark_attendance(session_id: str, attendance_id: str, student_id: str):
    url = "https://student.bennetterp.camu.in/api/Attendance/record-online-attendance"
    headers = {
        "Cookie": f"connect.sid={session_id}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://student.bennetterp.camu.in",
        "Referer": "https://student.bennetterp.camu.in/v2/timetable",
    }
    payload = {
        "attendanceId": attendance_id,
        "isMeetingStarted": True,
        "StuID": student_id,
        "offQrCdEnbld": True
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            data = response.json()
            pass # print(data)
            if data["output"]["data"] is not None:
                code = data["output"]["data"]["code"]
                return code in ["SUCCESS", "ATTENDANCE_ALREADY_RECORDED"]
            else:
                pass # print(f"[FAIL] Invalid response for student: {student_id}")
                return False
    except Exception as e:
        pass # print(f"[ERROR] While marking for student {student_id}: {e}")
        return False


async def start_mark(qr_id: str):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT email FROM users')
    ems = c.fetchall()
    conn.close()

    tasks = []
    for em in ems:
        em = em[0]
        try:
            email_pass = get_pass(em)
            student_id = get_stu(em)

            task = asyncio.create_task(run_mark(em, email_pass, qr_id, student_id))
            tasks.append(task)
        except Exception as e:
            pass # print(f"[ERROR] While preparing student {em}: {e}")
            continue

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        em = ems[i][0]
        if isinstance(result, Exception):
            pass # print(f"[ERROR] {em}: {result}")
        elif result:
            pass # print(f"[OK] Marked attendance for {em}")
        else:
            pass # print(f"[FAIL] Couldn't mark attendance for {em}")
    return results

async def run_mark(email, password, qr_id, student_id):
    sid = await get_sid(email, password)
    if sid:
        return await mark_attendance(sid, qr_id, student_id)
    else:
        pass # print(f"[ERROR] No session for {email}")
        return False

# if __name__ == "__main__":
#     asyncio.run(autc())
#     qr_code = input("Enter QR Code: ")
#     asyncio.run(start_mark(qr_code))
