"""
SQLAlchemy Models for UniSphere - Smart Student Assistant
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Student(Base):
    """Student table for authentication and profile"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    register_number = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String(5), nullable=False)
    password = Column(String(255), nullable=False)  # Hashed password


class Attendance(Base):
    """Attendance records for students"""
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    register_number = Column(String(20), index=True, nullable=False)
    subject = Column(String(100), nullable=False)
    attendance_percentage = Column(Float, nullable=False)


class InternalMarks(Base):
    """Internal marks for students"""
    __tablename__ = "internal_marks"

    id = Column(Integer, primary_key=True, index=True)
    register_number = Column(String(20), index=True, nullable=False)
    subject = Column(String(100), nullable=False)
    marks = Column(Float, nullable=False)


class Fees(Base):
    """Fee status for students"""
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    register_number = Column(String(20), index=True, nullable=False)
    status = Column(String(20), nullable=False)  # Paid / Pending
    due_date = Column(Date, nullable=True)
    fine = Column(Float, default=0.0)


class Complaint(Base):
    """Complaints / Support tickets"""
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    register_number = Column(String(20), index=True, nullable=False)
    issue = Column(Text, nullable=False)
    status = Column(String(20), default="Open")  # Open / In Progress / Resolved
    created_at = Column(DateTime, server_default=func.now())


class Announcement(Base):
    """Announcements for students"""
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, server_default=func.current_date())


class Timetable(Base):
    """Class timetable"""
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    subject = Column(String(100), nullable=False)
    time = Column(String(20), nullable=False)  # e.g., "09:00 - 10:00"
    room = Column(String(20), nullable=False)
    department = Column(String(50), nullable=False)
    semester = Column(Integer, nullable=False)
    section = Column(String(5), nullable=False)
