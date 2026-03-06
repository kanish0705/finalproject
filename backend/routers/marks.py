"""
Marks Router - Internal Marks Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/marks", tags=["Internal Marks"])


@router.get("/{register_number}", response_model=schemas.MarksSummary)
async def get_marks(register_number: str, db: Session = Depends(get_db)):
    """
    Get internal marks for a student.
    Returns:
    - Subject-wise marks
    - Total marks
    - Average marks
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
    
    # Get marks records
    marks_records = db.query(models.InternalMarks).filter(
        models.InternalMarks.register_number == register_number
    ).all()
    
    if not marks_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No marks records found for this student"
        )
    
    # Process marks
    subjects = [
        schemas.MarksResponse(
            id=record.id,
            register_number=record.register_number,
            subject=record.subject,
            marks=record.marks
        )
        for record in marks_records
    ]
    
    # Calculate totals
    total_marks = sum(r.marks for r in marks_records)
    average_marks = round(total_marks / len(marks_records), 2)
    
    return schemas.MarksSummary(
        register_number=register_number,
        subjects=subjects,
        total_marks=total_marks,
        average_marks=average_marks
    )
