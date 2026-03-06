"""
Smart Campus Assistant - Simplified Demo
A clean working prototype for project evaluation
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
import os

# Initialize FastAPI app
app = FastAPI(
    title="Smart Campus Assistant",
    description="College Student Assistant - Timetable, Announcements & Resources",
    version="1.0.0",
    docs_url="/docs"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class TimetableEntry(BaseModel):
    day: str
    time: str
    subject: str
    room: str
    faculty: str

class Announcement(BaseModel):
    id: int
    title: str
    description: str
    date: str
    priority: str  # high, medium, low

class Resource(BaseModel):
    id: int
    title: str
    subject: str
    type: str  # pdf, link, notes
    url: str
    description: str

# ==================== MOCK DATA ====================

# Timetable data organized by department, semester, section
TIMETABLE_DATA = {
    "BCA": {
        3: {
            "A": [
                {"day": "Monday", "time": "09:00 - 10:00", "subject": "Data Structures", "room": "Lab 1", "faculty": "Dr. Sharma"},
                {"day": "Monday", "time": "10:00 - 11:00", "subject": "Database Systems", "room": "Room 201", "faculty": "Prof. Kumar"},
                {"day": "Monday", "time": "11:15 - 12:15", "subject": "Web Development", "room": "Lab 2", "faculty": "Ms. Singh"},
                {"day": "Monday", "time": "02:00 - 03:00", "subject": "Mathematics", "room": "Room 102", "faculty": "Dr. Patel"},
                {"day": "Tuesday", "time": "09:00 - 10:00", "subject": "Operating Systems", "room": "Room 203", "faculty": "Prof. Gupta"},
                {"day": "Tuesday", "time": "10:00 - 11:00", "subject": "Data Structures Lab", "room": "Lab 1", "faculty": "Dr. Sharma"},
                {"day": "Tuesday", "time": "11:15 - 12:15", "subject": "Data Structures Lab", "room": "Lab 1", "faculty": "Dr. Sharma"},
                {"day": "Tuesday", "time": "02:00 - 03:00", "subject": "English", "room": "Room 105", "faculty": "Ms. Verma"},
                {"day": "Wednesday", "time": "09:00 - 10:00", "subject": "Database Systems", "room": "Room 201", "faculty": "Prof. Kumar"},
                {"day": "Wednesday", "time": "10:00 - 11:00", "subject": "Web Development", "room": "Lab 2", "faculty": "Ms. Singh"},
                {"day": "Wednesday", "time": "11:15 - 12:15", "subject": "Mathematics", "room": "Room 102", "faculty": "Dr. Patel"},
                {"day": "Wednesday", "time": "02:00 - 03:00", "subject": "Operating Systems", "room": "Room 203", "faculty": "Prof. Gupta"},
                {"day": "Thursday", "time": "09:00 - 10:00", "subject": "Data Structures", "room": "Lab 1", "faculty": "Dr. Sharma"},
                {"day": "Thursday", "time": "10:00 - 11:00", "subject": "DBMS Lab", "room": "Lab 3", "faculty": "Prof. Kumar"},
                {"day": "Thursday", "time": "11:15 - 12:15", "subject": "DBMS Lab", "room": "Lab 3", "faculty": "Prof. Kumar"},
                {"day": "Thursday", "time": "02:00 - 03:00", "subject": "English", "room": "Room 105", "faculty": "Ms. Verma"},
                {"day": "Friday", "time": "09:00 - 10:00", "subject": "Web Development", "room": "Lab 2", "faculty": "Ms. Singh"},
                {"day": "Friday", "time": "10:00 - 11:00", "subject": "Operating Systems", "room": "Room 203", "faculty": "Prof. Gupta"},
                {"day": "Friday", "time": "11:15 - 12:15", "subject": "Mathematics", "room": "Room 102", "faculty": "Dr. Patel"},
                {"day": "Friday", "time": "02:00 - 03:00", "subject": "Soft Skills", "room": "Room 101", "faculty": "Mr. Joshi"},
            ],
            "B": [
                {"day": "Monday", "time": "09:00 - 10:00", "subject": "Database Systems", "room": "Room 202", "faculty": "Prof. Kumar"},
                {"day": "Monday", "time": "10:00 - 11:00", "subject": "Data Structures", "room": "Lab 2", "faculty": "Dr. Sharma"},
                {"day": "Monday", "time": "11:15 - 12:15", "subject": "Mathematics", "room": "Room 103", "faculty": "Dr. Patel"},
                {"day": "Monday", "time": "02:00 - 03:00", "subject": "Web Development", "room": "Lab 1", "faculty": "Ms. Singh"},
                {"day": "Tuesday", "time": "09:00 - 10:00", "subject": "English", "room": "Room 106", "faculty": "Ms. Verma"},
                {"day": "Tuesday", "time": "10:00 - 11:00", "subject": "Operating Systems", "room": "Room 204", "faculty": "Prof. Gupta"},
                {"day": "Tuesday", "time": "11:15 - 12:15", "subject": "Data Structures", "room": "Lab 2", "faculty": "Dr. Sharma"},
                {"day": "Tuesday", "time": "02:00 - 03:00", "subject": "Mathematics", "room": "Room 103", "faculty": "Dr. Patel"},
            ]
        }
    },
    "MCA": {
        1: {
            "A": [
                {"day": "Monday", "time": "09:00 - 10:00", "subject": "Programming in Python", "room": "Lab 4", "faculty": "Dr. Reddy"},
                {"day": "Monday", "time": "10:00 - 11:00", "subject": "Computer Networks", "room": "Room 301", "faculty": "Prof. Nair"},
                {"day": "Monday", "time": "11:15 - 12:15", "subject": "Software Engineering", "room": "Room 302", "faculty": "Ms. Iyer"},
                {"day": "Tuesday", "time": "09:00 - 10:00", "subject": "Database Management", "room": "Room 303", "faculty": "Prof. Das"},
                {"day": "Tuesday", "time": "10:00 - 11:00", "subject": "Python Lab", "room": "Lab 4", "faculty": "Dr. Reddy"},
                {"day": "Tuesday", "time": "11:15 - 12:15", "subject": "Python Lab", "room": "Lab 4", "faculty": "Dr. Reddy"},
            ]
        }
    }
}

# Announcements data
ANNOUNCEMENTS_DATA = [
    {
        "id": 1,
        "title": "Mid-Semester Examinations Schedule",
        "description": "Mid-semester examinations will be held from March 15-25, 2026. Students are advised to collect their hall tickets from the examination cell. Detailed timetable will be available on the notice board.",
        "date": "2026-03-05",
        "priority": "high"
    },
    {
        "id": 2,
        "title": "Tech Fest 2026 Registration Open",
        "description": "Annual Tech Fest 'TechnoVerse 2026' registrations are now open. Events include hackathon, coding competition, robotics, and project exhibition. Register before March 20th to avail early bird discount.",
        "date": "2026-03-04",
        "priority": "medium"
    },
    {
        "id": 3,
        "title": "Library Timings Extended",
        "description": "During examination period, library timings have been extended. New timings: 8:00 AM to 10:00 PM (Monday-Saturday). Students can access reading rooms and computer lab facilities.",
        "date": "2026-03-03",
        "priority": "low"
    },
    {
        "id": 4,
        "title": "Guest Lecture on AI & Machine Learning",
        "description": "A guest lecture on 'Future of AI in Industry' will be conducted by Dr. Ramesh from IIT Delhi on March 10th at 2:00 PM in the Main Auditorium. All students are encouraged to attend.",
        "date": "2026-03-02",
        "priority": "medium"
    },
    {
        "id": 5,
        "title": "Campus Placement Drive",
        "description": "Infosys and TCS will be conducting placement drives on March 18th and 20th respectively. Eligible students should register through the placement cell portal before March 12th.",
        "date": "2026-03-01",
        "priority": "high"
    }
]

# Resources data
RESOURCES_DATA = [
    {
        "id": 1,
        "title": "Data Structures Complete Notes",
        "subject": "Data Structures",
        "type": "pdf",
        "url": "https://example.com/ds-notes.pdf",
        "description": "Comprehensive notes covering arrays, linked lists, trees, graphs, and sorting algorithms."
    },
    {
        "id": 2,
        "title": "DBMS Tutorial - W3Schools",
        "subject": "Database Systems",
        "type": "link",
        "url": "https://www.w3schools.com/sql/",
        "description": "Interactive SQL tutorial with examples and practice exercises."
    },
    {
        "id": 3,
        "title": "Web Development Basics",
        "subject": "Web Development",
        "type": "pdf",
        "url": "https://example.com/webdev-basics.pdf",
        "description": "HTML, CSS, and JavaScript fundamentals with practical examples."
    },
    {
        "id": 4,
        "title": "Operating Systems Concepts",
        "subject": "Operating Systems",
        "type": "pdf",
        "url": "https://example.com/os-concepts.pdf",
        "description": "Notes on process management, memory management, and file systems."
    },
    {
        "id": 5,
        "title": "Python Official Documentation",
        "subject": "Programming",
        "type": "link",
        "url": "https://docs.python.org/3/",
        "description": "Official Python 3 documentation and tutorials."
    },
    {
        "id": 6,
        "title": "Computer Networks Notes",
        "subject": "Computer Networks",
        "type": "pdf",
        "url": "https://example.com/cn-notes.pdf",
        "description": "OSI model, TCP/IP, routing protocols, and network security concepts."
    },
    {
        "id": 7,
        "title": "Git & GitHub Tutorial",
        "subject": "Version Control",
        "type": "link",
        "url": "https://guides.github.com/",
        "description": "Learn Git version control and GitHub collaboration."
    },
    {
        "id": 8,
        "title": "Mathematics for Computer Science",
        "subject": "Mathematics",
        "type": "notes",
        "url": "https://example.com/math-cs.pdf",
        "description": "Discrete mathematics, probability, and linear algebra notes."
    }
]

# ==================== API ENDPOINTS ====================

@app.get("/", tags=["Root"])
async def root():
    """API health check and welcome message"""
    return {
        "message": "Welcome to Smart Campus Assistant API",
        "version": "1.0.0",
        "endpoints": ["/timetable", "/announcements", "/resources"],
        "docs": "/docs"
    }

class TimetableCreate(BaseModel):
    department: str
    semester: int
    section: str
    day: str
    time: str
    subject: str
    room: str
    faculty: str

@app.get("/timetable", response_model=List[TimetableEntry], tags=["Timetable"])
async def get_timetable(
    department: str = Query(..., description="Department code (e.g., BCA, MCA)"),
    semester: int = Query(..., description="Semester number (1-8)"),
    section: str = Query(..., description="Section (e.g., A, B)")
):
    """
    Get timetable based on Department, Semester, and Section.
    Returns weekly class schedule.
    """
    dept = department.upper()
    sec = section.upper()
    
    if dept in TIMETABLE_DATA:
        if semester in TIMETABLE_DATA[dept]:
            if sec in TIMETABLE_DATA[dept][semester]:
                return TIMETABLE_DATA[dept][semester][sec]
    
    # Return empty list if no timetable found
    return []

@app.post("/timetable", response_model=TimetableEntry, tags=["Timetable"])
async def add_timetable_entry(timetable: TimetableCreate):
    """
    Add a new timetable entry (Admin functionality).
    """
    dept = timetable.department.upper()
    semester = timetable.semester
    sec = timetable.section.upper()
    
    # Initialize nested dictionaries if they don't exist
    if dept not in TIMETABLE_DATA:
        TIMETABLE_DATA[dept] = {}
    if semester not in TIMETABLE_DATA[dept]:
        TIMETABLE_DATA[dept][semester] = {}
    if sec not in TIMETABLE_DATA[dept][semester]:
        TIMETABLE_DATA[dept][semester][sec] = []
    
    # Create the entry
    entry = {
        "day": timetable.day,
        "time": timetable.time,
        "subject": timetable.subject,
        "room": timetable.room,
        "faculty": timetable.faculty
    }
    
    TIMETABLE_DATA[dept][semester][sec].append(entry)
    
    return entry

@app.get("/announcements", response_model=List[Announcement], tags=["Announcements"])
async def get_announcements():
    """
    Get all announcements.
    Returns announcements sorted by date (newest first).
    """
    return ANNOUNCEMENTS_DATA

@app.post("/announcements", response_model=Announcement, tags=["Announcements"])
async def add_announcement(announcement: Announcement):
    """
    Add a new announcement (Admin functionality).
    """
    ANNOUNCEMENTS_DATA.insert(0, announcement.dict())
    return announcement

@app.get("/resources", response_model=List[Resource], tags=["Resources"])
async def get_resources(subject: Optional[str] = None):
    """
    Get study resources/materials.
    Optionally filter by subject.
    """
    if subject:
        return [r for r in RESOURCES_DATA if subject.lower() in r["subject"].lower()]
    return RESOURCES_DATA

@app.post("/resources", response_model=Resource, tags=["Resources"])
async def add_resource(resource: Resource):
    """
    Add a new resource (Admin functionality).
    """
    RESOURCES_DATA.insert(0, resource.dict())
    return resource

# Mount static files directory
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
