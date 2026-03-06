# Smart Campus Assistant

A simplified college student assistant web application built with FastAPI and vanilla HTML/CSS/JavaScript.

## Features

1. **Timetable** - View class schedule by Department, Semester, and Section
2. **Announcements** - View and post campus announcements
3. **Resources** - Access study materials, PDFs, and useful links

## Project Structure

```
smart-campus-chatbot/
├── backend/
│   ├── main.py              # FastAPI application with all APIs
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # This file
└── static/
    └── index.html           # Frontend dashboard
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
cd backend
uvicorn main:app --reload
```

The server will start at: `http://127.0.0.1:8000`

### 3. Open the Application

Open your browser and navigate to: `http://127.0.0.1:8000/static/index.html`

## API Documentation

Access the interactive API docs at: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/timetable` | Get timetable (params: department, semester, section) |
| GET | `/announcements` | Get all announcements |
| POST | `/announcements` | Add new announcement |
| GET | `/resources` | Get study resources (optional: filter by subject) |

## Sample Data

The application includes sample data for:
- **BCA Semester 3 Section A & B** - Full weekly timetable
- **MCA Semester 1 Section A** - Sample timetable
- **5 Announcements** - Various priorities (high, medium, low)
- **8 Resources** - PDFs, links, and notes for different subjects

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data**: In-memory mock data (no database required)

### Announcements
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/announcements` | Get all announcements |

## Test Credentials

| Register Number | Password |
|----------------|----------|
| BCA2024001 | password123 |
| BCA2024002 | password123 |
| BCA2024003 | password123 |
| MCA2024001 | password123 |

## Example API Usage

### Login
```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"register_number": "BCA2024001", "password": "password123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```

### Get Profile (with token)
```bash
curl -X GET "http://127.0.0.1:8000/student/profile" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Attendance
```bash
curl -X GET "http://127.0.0.1:8000/attendance/BCA2024001"
```

### Get Marks
```bash
curl -X GET "http://127.0.0.1:8000/marks/BCA2024001"
```

### Get Fee Status
```bash
curl -X GET "http://127.0.0.1:8000/fees/BCA2024001"
```

### Create Complaint
```bash
curl -X POST "http://127.0.0.1:8000/complaint" \
  -H "Content-Type: application/json" \
  -d '{"register_number": "BCA2024001", "issue": "Library books not available"}'
```

### Get Timetable
```bash
curl -X GET "http://127.0.0.1:8000/timetable/Monday?department=BCA&semester=6&section=A"
```

### Get Announcements
```bash
curl -X GET "http://127.0.0.1:8000/announcements"
```

## Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **Attendance Warnings**: Automatic warnings for attendance < 75%
- **Fee Management**: Track payment status and overdue fines
- **Support Tickets**: Create and track complaints
- **Filtered Timetable**: Filter by department, semester, section

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with Bcrypt
- **Validation**: Pydantic

## License

This project is created for educational purposes as a BCA Final Year Project.
