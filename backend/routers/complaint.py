"""
Complaint Router - Support Ticket Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(tags=["Complaints"])


@router.post("/complaint", response_model=schemas.ComplaintResponse)
async def create_complaint(
    complaint: schemas.ComplaintCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new complaint / support ticket.
    """
    # Verify student exists
    student = db.query(models.Student).filter(
        models.Student.register_number == complaint.register_number
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Create complaint
    db_complaint = models.Complaint(
        register_number=complaint.register_number,
        issue=complaint.issue,
        status="Open"
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    return db_complaint


@router.get("/complaints/{register_number}", response_model=List[schemas.ComplaintResponse])
async def get_complaints(register_number: str, db: Session = Depends(get_db)):
    """
    Get all complaints for a student.
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
    
    # Get complaints
    complaints = db.query(models.Complaint).filter(
        models.Complaint.register_number == register_number
    ).order_by(models.Complaint.created_at.desc()).all()
    
    return complaints
