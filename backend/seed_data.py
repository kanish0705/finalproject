"""
Seed Data Script for UniSphere
Run this script to populate the database with sample data for testing.

Usage: python seed_data.py
"""
from datetime import date, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from auth import get_password_hash


def seed_database():
    """Populate database with sample data."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(models.Student).delete()
        db.query(models.Attendance).delete()
        db.query(models.InternalMarks).delete()
        db.query(models.Fees).delete()
        db.query(models.Complaint).delete()
        db.query(models.Announcement).delete()
        db.query(models.Timetable).delete()
        db.commit()
        
        print("Seeding Students...")
        # ===================== STUDENTS =====================
        students = [
            models.Student(
                register_number="BCA2024001",
                name="Rahul Sharma",
                department="BCA",
                semester=6,
                section="A",
                password=get_password_hash("password123")
            ),
            models.Student(
                register_number="BCA2024002",
                name="Priya Singh",
                department="BCA",
                semester=6,
                section="A",
                password=get_password_hash("password123")
            ),
            models.Student(
                register_number="BCA2024003",
                name="Amit Kumar",
                department="BCA",
                semester=6,
                section="B",
                password=get_password_hash("password123")
            ),
            models.Student(
                register_number="MCA2024001",
                name="Sneha Patel",
                department="MCA",
                semester=4,
                section="A",
                password=get_password_hash("password123")
            ),
        ]
        db.add_all(students)
        db.commit()
        
        print("Seeding Attendance...")
        # ===================== ATTENDANCE =====================
        attendance_records = [
            # Rahul Sharma (BCA2024001)
            models.Attendance(register_number="BCA2024001", subject="Data Structures", attendance_percentage=85.5),
            models.Attendance(register_number="BCA2024001", subject="Web Development", attendance_percentage=92.0),
            models.Attendance(register_number="BCA2024001", subject="Database Management", attendance_percentage=78.0),
            models.Attendance(register_number="BCA2024001", subject="Python Programming", attendance_percentage=70.0),  # Warning
            models.Attendance(register_number="BCA2024001", subject="Software Engineering", attendance_percentage=88.5),
            
            # Priya Singh (BCA2024002)
            models.Attendance(register_number="BCA2024002", subject="Data Structures", attendance_percentage=95.0),
            models.Attendance(register_number="BCA2024002", subject="Web Development", attendance_percentage=98.0),
            models.Attendance(register_number="BCA2024002", subject="Database Management", attendance_percentage=92.5),
            models.Attendance(register_number="BCA2024002", subject="Python Programming", attendance_percentage=90.0),
            models.Attendance(register_number="BCA2024002", subject="Software Engineering", attendance_percentage=94.0),
            
            # Amit Kumar (BCA2024003)
            models.Attendance(register_number="BCA2024003", subject="Data Structures", attendance_percentage=65.0),  # Warning
            models.Attendance(register_number="BCA2024003", subject="Web Development", attendance_percentage=72.0),  # Warning
            models.Attendance(register_number="BCA2024003", subject="Database Management", attendance_percentage=68.0),  # Warning
            models.Attendance(register_number="BCA2024003", subject="Python Programming", attendance_percentage=74.5),  # Warning
            models.Attendance(register_number="BCA2024003", subject="Software Engineering", attendance_percentage=70.0),  # Warning
        ]
        db.add_all(attendance_records)
        db.commit()
        
        print("Seeding Internal Marks...")
        # ===================== INTERNAL MARKS =====================
        marks_records = [
            # Rahul Sharma (BCA2024001)
            models.InternalMarks(register_number="BCA2024001", subject="Data Structures", marks=42.0),
            models.InternalMarks(register_number="BCA2024001", subject="Web Development", marks=45.0),
            models.InternalMarks(register_number="BCA2024001", subject="Database Management", marks=38.0),
            models.InternalMarks(register_number="BCA2024001", subject="Python Programming", marks=40.0),
            models.InternalMarks(register_number="BCA2024001", subject="Software Engineering", marks=44.0),
            
            # Priya Singh (BCA2024002)
            models.InternalMarks(register_number="BCA2024002", subject="Data Structures", marks=48.0),
            models.InternalMarks(register_number="BCA2024002", subject="Web Development", marks=50.0),
            models.InternalMarks(register_number="BCA2024002", subject="Database Management", marks=47.0),
            models.InternalMarks(register_number="BCA2024002", subject="Python Programming", marks=49.0),
            models.InternalMarks(register_number="BCA2024002", subject="Software Engineering", marks=46.0),
            
            # Amit Kumar (BCA2024003)
            models.InternalMarks(register_number="BCA2024003", subject="Data Structures", marks=32.0),
            models.InternalMarks(register_number="BCA2024003", subject="Web Development", marks=35.0),
            models.InternalMarks(register_number="BCA2024003", subject="Database Management", marks=30.0),
            models.InternalMarks(register_number="BCA2024003", subject="Python Programming", marks=28.0),
            models.InternalMarks(register_number="BCA2024003", subject="Software Engineering", marks=33.0),
        ]
        db.add_all(marks_records)
        db.commit()
        
        print("Seeding Fee Records...")
        # ===================== FEES =====================
        fees_records = [
            models.Fees(
                register_number="BCA2024001",
                status="Paid",
                due_date=None,
                fine=0.0
            ),
            models.Fees(
                register_number="BCA2024002",
                status="Pending",
                due_date=date.today() + timedelta(days=15),
                fine=0.0
            ),
            models.Fees(
                register_number="BCA2024003",
                status="Pending",
                due_date=date.today() - timedelta(days=10),  # Overdue
                fine=500.0
            ),
            models.Fees(
                register_number="MCA2024001",
                status="Paid",
                due_date=None,
                fine=0.0
            ),
        ]
        db.add_all(fees_records)
        db.commit()
        
        print("Seeding Complaints...")
        # ===================== COMPLAINTS =====================
        complaints = [
            models.Complaint(
                register_number="BCA2024001",
                issue="WiFi connectivity issues in Block A",
                status="Open"
            ),
            models.Complaint(
                register_number="BCA2024001",
                issue="Library timing should be extended",
                status="In Progress"
            ),
            models.Complaint(
                register_number="BCA2024002",
                issue="AC not working in Lab 3",
                status="Resolved"
            ),
            models.Complaint(
                register_number="BCA2024003",
                issue="Canteen food quality needs improvement",
                status="Open"
            ),
        ]
        db.add_all(complaints)
        db.commit()
        
        print("Seeding Announcements...")
        # ===================== ANNOUNCEMENTS =====================
        announcements = [
            models.Announcement(
                title="Semester Exams Schedule Released",
                description="The semester examination schedule for the current academic year has been released. Please check the notice board for detailed timetable.",
                date=date.today()
            ),
            models.Announcement(
                title="Annual Sports Day",
                description="Annual Sports Day will be held on 15th March 2026. All students are encouraged to participate. Registration is open till 10th March.",
                date=date.today() - timedelta(days=2)
            ),
            models.Announcement(
                title="Guest Lecture on AI/ML",
                description="A guest lecture on 'Future of AI and Machine Learning' will be conducted by Dr. Rajesh Kumar from IIT Delhi on 20th March 2026 at 10:00 AM in Auditorium.",
                date=date.today() - timedelta(days=5)
            ),
            models.Announcement(
                title="Library Book Return Notice",
                description="All students are requested to return the library books before the semester end. Late fees will be applicable for overdue books.",
                date=date.today() - timedelta(days=7)
            ),
            models.Announcement(
                title="Holiday Notice - Holi Festival",
                description="The college will remain closed on 14th and 15th March 2026 on account of Holi festival. Classes will resume on 16th March.",
                date=date.today() - timedelta(days=10)
            ),
        ]
        db.add_all(announcements)
        db.commit()
        
        print("Seeding Timetable...")
        # ===================== TIMETABLE =====================
        # BCA 6th Semester Section A
        timetable_entries = [
            # Monday
            models.Timetable(day="Monday", subject="Data Structures", time="09:00 - 10:00", room="Room 101", department="BCA", semester=6, section="A"),
            models.Timetable(day="Monday", subject="Web Development", time="10:00 - 11:00", room="Lab 1", department="BCA", semester=6, section="A"),
            models.Timetable(day="Monday", subject="Database Management", time="11:15 - 12:15", room="Room 102", department="BCA", semester=6, section="A"),
            models.Timetable(day="Monday", subject="Python Programming", time="12:15 - 01:15", room="Lab 2", department="BCA", semester=6, section="A"),
            models.Timetable(day="Monday", subject="Software Engineering", time="02:00 - 03:00", room="Room 101", department="BCA", semester=6, section="A"),
            
            # Tuesday
            models.Timetable(day="Tuesday", subject="Python Programming", time="09:00 - 10:00", room="Lab 2", department="BCA", semester=6, section="A"),
            models.Timetable(day="Tuesday", subject="Data Structures", time="10:00 - 11:00", room="Room 101", department="BCA", semester=6, section="A"),
            models.Timetable(day="Tuesday", subject="Software Engineering", time="11:15 - 12:15", room="Room 102", department="BCA", semester=6, section="A"),
            models.Timetable(day="Tuesday", subject="Web Development", time="12:15 - 01:15", room="Lab 1", department="BCA", semester=6, section="A"),
            models.Timetable(day="Tuesday", subject="Database Management", time="02:00 - 03:00", room="Room 103", department="BCA", semester=6, section="A"),
            
            # Wednesday
            models.Timetable(day="Wednesday", subject="Web Development", time="09:00 - 10:00", room="Lab 1", department="BCA", semester=6, section="A"),
            models.Timetable(day="Wednesday", subject="Database Management", time="10:00 - 11:00", room="Room 102", department="BCA", semester=6, section="A"),
            models.Timetable(day="Wednesday", subject="Python Programming", time="11:15 - 12:15", room="Lab 2", department="BCA", semester=6, section="A"),
            models.Timetable(day="Wednesday", subject="Data Structures", time="12:15 - 01:15", room="Room 101", department="BCA", semester=6, section="A"),
            models.Timetable(day="Wednesday", subject="Project Work", time="02:00 - 04:00", room="Lab 3", department="BCA", semester=6, section="A"),
            
            # Thursday
            models.Timetable(day="Thursday", subject="Software Engineering", time="09:00 - 10:00", room="Room 101", department="BCA", semester=6, section="A"),
            models.Timetable(day="Thursday", subject="Python Programming", time="10:00 - 11:00", room="Lab 2", department="BCA", semester=6, section="A"),
            models.Timetable(day="Thursday", subject="Web Development", time="11:15 - 12:15", room="Lab 1", department="BCA", semester=6, section="A"),
            models.Timetable(day="Thursday", subject="Database Management", time="12:15 - 01:15", room="Room 102", department="BCA", semester=6, section="A"),
            models.Timetable(day="Thursday", subject="Data Structures", time="02:00 - 03:00", room="Room 103", department="BCA", semester=6, section="A"),
            
            # Friday
            models.Timetable(day="Friday", subject="Database Management", time="09:00 - 10:00", room="Room 102", department="BCA", semester=6, section="A"),
            models.Timetable(day="Friday", subject="Software Engineering", time="10:00 - 11:00", room="Room 101", department="BCA", semester=6, section="A"),
            models.Timetable(day="Friday", subject="Data Structures", time="11:15 - 12:15", room="Room 103", department="BCA", semester=6, section="A"),
            models.Timetable(day="Friday", subject="Python Programming", time="12:15 - 01:15", room="Lab 2", department="BCA", semester=6, section="A"),
            models.Timetable(day="Friday", subject="Web Development", time="02:00 - 03:00", room="Lab 1", department="BCA", semester=6, section="A"),
            
            # BCA 6th Semester Section B - Sample entries
            models.Timetable(day="Monday", subject="Data Structures", time="09:00 - 10:00", room="Room 201", department="BCA", semester=6, section="B"),
            models.Timetable(day="Monday", subject="Web Development", time="10:00 - 11:00", room="Lab 4", department="BCA", semester=6, section="B"),
            models.Timetable(day="Monday", subject="Database Management", time="11:15 - 12:15", room="Room 202", department="BCA", semester=6, section="B"),
        ]
        db.add_all(timetable_entries)
        db.commit()
        
        print("\n" + "="*50)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("="*50)
        print("\nTest Credentials:")
        print("-" * 30)
        print("Register Number: BCA2024001")
        print("Password: password123")
        print("-" * 30)
        print("Register Number: BCA2024002")
        print("Password: password123")
        print("-" * 30)
        print("Register Number: BCA2024003")
        print("Password: password123")
        print("-" * 30)
        print("Register Number: MCA2024001")
        print("Password: password123")
        print("="*50)
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
