from fastapi import FastAPI, UploadFile, File
from datetime import datetime
from database import get_connection
import pandas as pd

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Smart Campus Academic Support Chatbot is running"}


@app.get("/timetable")
def get_timetable(department: str, semester: int, section: str):
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.strftime("%H:%M")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, department, semester, section, day, start_time, end_time, subject, faculty, room
        FROM timetable
        WHERE department = ? AND semester = ? AND section = ? AND day = ?
        ORDER BY start_time
    ''', (department, semester, section, current_day))
    rows = cursor.fetchall()
    conn.close()
    
    current_class = None
    upcoming_classes = []
    
    for row in rows:
        class_info = {
            "id": row[0],
            "department": row[1],
            "semester": row[2],
            "section": row[3],
            "day": row[4],
            "start_time": row[5],
            "end_time": row[6],
            "subject": row[7],
            "faculty": row[8],
            "room": row[9]
        }
        
        start_time = row[5]
        end_time = row[6]
        
        # Check if this is the current class
        if start_time <= current_time < end_time:
            current_class = class_info
        # Check if this is an upcoming class
        elif start_time > current_time:
            upcoming_classes.append(class_info)
    
    return {
        "day": current_day,
        "current_class": current_class,
        "upcoming_classes": upcoming_classes
    }


@app.get("/all-timetable")
def get_all_timetable(department: str, semester: int, section: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, department, semester, section, day, start_time, end_time, subject, faculty, room
        FROM timetable
        WHERE department = ? AND semester = ? AND section = ?
        ORDER BY 
            CASE day 
                WHEN 'Monday' THEN 1 
                WHEN 'Tuesday' THEN 2 
                WHEN 'Wednesday' THEN 3 
                WHEN 'Thursday' THEN 4 
                WHEN 'Friday' THEN 5 
            END, 
            start_time
    ''', (department, semester, section))
    rows = cursor.fetchall()
    conn.close()
    
    timetable = []
    for row in rows:
        timetable.append({
            "id": row[0],
            "department": row[1],
            "semester": row[2],
            "section": row[3],
            "day": row[4],
            "start_time": row[5],
            "end_time": row[6],
            "subject": row[7],
            "faculty": row[8],
            "room": row[9]
        })
    
    return {"timetable": timetable}


@app.post("/upload-timetable")
def upload_timetable(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)

        conn = get_connection()
        cursor = conn.cursor()

        # Clear existing timetable
        cursor.execute("DELETE FROM timetable")

        # Insert new data
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO timetable 
                (department, semester, section, day, start_time, end_time, subject, faculty, room)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["department"],
                int(row["semester"]),
                row["section"],
                row["day"],
                row["start_time"],
                row["end_time"],
                row["subject"],
                row["faculty"],
                row["room"]
            ))

        conn.commit()
        conn.close()

        return {"message": "Timetable uploaded successfully"}

    except Exception as e:
        return {"error": str(e)}


@app.post("/add-notice")
def add_notice(title: str, content: str, department: str):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO notices (title, content, department, created_at)
        VALUES (?, ?, ?, ?)
    ''', (title, content, department, created_at))
    conn.commit()
    conn.close()
    
    return {"message": "Notice added successfully"}


@app.get("/notices")
def get_notices(department: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, content, department, created_at
        FROM notices
        WHERE department = ?
        ORDER BY created_at DESC
    ''', (department,))
    rows = cursor.fetchall()
    conn.close()
    
    notices = []
    for row in rows:
        notices.append({
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "department": row[3],
            "created_at": row[4]
        })
    
    return {"notices": notices} 


from fastapi.responses import FileResponse

@app.get("/app")
def serve_app():
    return FileResponse("static/index.html")