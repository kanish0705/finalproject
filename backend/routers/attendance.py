"""
Attendance Router - Student Attendance Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def check_attendance_warning(percentage: float) -> str:
    """Generate warning message if attendance is below 75%."""
    if percentage < 75:
        return f"Warning: Attendance is {percentage}% which is below 75%. You may face attendance shortage."
    return None


@router.get("/{register_number}", response_model=schemas.AttendanceSummary)
async def get_attendance(register_number: str, db: Session = Depends(get_db)):
    """
    Get attendance details for a student.
    Returns:
    - Subject-wise attendance
    - Overall attendance percentage
    - Warning if attendance < 75%
    """
    # Verify student exists
    student = db.query(models.Student).filter(
        models.Student.register_number == register_number
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Get attendance records
    attendance_records = db.query(models.Attendance).filter(
        models.Attendance.register_number == register_number
    ).all()
    
    if not attendance_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendance records found for this student"
        )
    
    # Process attendance with warnings
    subjects = []
    for record in attendance_records:
        warning = check_attendance_warning(record.attendance_percentage)
        subjects.append(schemas.AttendanceResponse(
            id=record.id,
            register_number=record.register_number,
            subject=record.subject,
            attendance_percentage=record.attendance_percentage,
            warning=warning
        ))
    
    # Calculate overall attendance
    total_percentage = sum(r.attendance_percentage for r in attendance_records)
    overall_attendance = round(total_percentage / len(attendance_records), 2)
    overall_warning = check_attendance_warning(overall_attendance)
    
    return schemas.AttendanceSummary(
        register_number=register_number,
        subjects=subjects,
        overall_attendance=overall_attendance,
        overall_warning=overall_warning
    )
