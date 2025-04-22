from markit import *

async def get_time_table():
    import datetime, json, httpx
    from database import retrieve_js

    now = datetime.datetime.now()

    payload = json.loads(retrieve_js("S24CSEU0117@bennett.edu.in"))["output"]["data"]["progressionData"][0]
    payload.update({
        "PrName": "Undergraduate",
        "SemName": "Semester - 2",
        "AcYrNm": "2024-2025",
        "enableV2": True,
        "start": now.strftime("%Y-%m-%d"),
        "end": now.strftime("%Y-%m-%d"),
        "usrTime": now.strftime("%d-%m-%Y, %I:%M %p"),
        "schdlTyp": "slctdSchdl",
        "isShowCancelledPeriod": True,
        "isFromTt": True
    })

    sid = await get_sid("S24CSEU0117@bennett.edu.in","camu@1234")
    url = "https://student.bennetterp.camu.in/api/Timetable/get"
    headers = {
        "Cookie": f"connect.sid={sid}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://student.bennetterp.camu.in",
        "Referer": "https://student.bennetterp.camu.in/v2/timetable"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            data = response.json()
            print("GO")
    except Exception as e:
        print(f"[ERROR] While fetching timetable: {e}")

    return data

async def extract_pending_attendance_classes():
    result = {}
    response = await get_time_table()
    #print(type(response))
    try:
        periods = response["output"]["data"][0]["Periods"]
        for cls in periods:
            if "attendanceId" in cls and not cls.get("isAttendanceSaved"):
                result[cls["PeriodId"]] = [cls["attendanceId"], cls["isAttendanceSaved"]]
    except Exception as e:
        print(f"[ERROR] while extracting periods: {e}")
    print(result)
    return result

async def autc():
    while True:
        try:
            pending = await extract_pending_attendance_classes()
            #print(type(pending))
            for i in pending.values():
                print(i[0])
                await start_mark(i[0])
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] While fetching attendance: {e}")

if __name__ == "__main__":
    asyncio.run(autc())