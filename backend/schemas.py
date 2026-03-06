"""
Pydantic Schemas for UniSphere - Smart Student Assistant
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# ===================== Authentication Schemas =====================

class LoginRequest(BaseModel):
    register_number: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    register_number: Optional[str] = None


# ===================== Student Schemas =====================

class StudentBase(BaseModel):
    register_number: str
    name: str
    department: str
    semester: int
    section: str


class StudentProfile(StudentBase):
    id: int

    class Config:
        from_attributes = True


# ===================== Attendance Schemas =====================

class AttendanceBase(BaseModel):
    subject: str
    attendance_percentage: float


class AttendanceResponse(AttendanceBase):
    id: int
    register_number: str
    warning: Optional[str] = None

    class Config:
        from_attributes = True


class AttendanceSummary(BaseModel):
    register_number: str
    subjects: List[AttendanceResponse]
    overall_attendance: float
    overall_warning: Optional[str] = None


# ===================== Internal Marks Schemas =====================

class MarksBase(BaseModel):
    subject: str
    marks: float


class MarksResponse(MarksBase):
    id: int
    register_number: str

    class Config:
        from_attributes = True


class MarksSummary(BaseModel):
    register_number: str
    subjects: List[MarksResponse]
    total_marks: float
    average_marks: float


# ===================== Fees Schemas =====================

class FeesBase(BaseModel):
    status: str
    due_date: Optional[date] = None
    fine: float = 0.0


class FeesResponse(FeesBase):
    id: int
    register_number: str

    class Config:
        from_attributes = True


# ===================== Complaint Schemas =====================

class ComplaintCreate(BaseModel):
    register_number: str
    issue: str


class ComplaintResponse(BaseModel):
    id: int
    register_number: str
    issue: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ===================== Announcement Schemas =====================

class AnnouncementBase(BaseModel):
    title: str
    description: str


class AnnouncementResponse(AnnouncementBase):
    id: int
    date: date

    class Config:
        from_attributes = True


# ===================== Timetable Schemas =====================

class TimetableBase(BaseModel):
    day: str
    subject: str
    time: str
    room: str
    department: str
    semester: int
    section: str


class TimetableResponse(TimetableBase):
    id: int

    class Config:
        from_attributes = True
