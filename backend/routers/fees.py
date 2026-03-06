"""
Fees Router - Fee Status Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/fees", tags=["Fees"])


@router.get("/{register_number}", response_model=schemas.FeesResponse)
async def get_fee_status(register_number: str, db: Session = Depends(get_db)):
    """
    Get fee status for a student.
    Returns:
    - Payment status (Paid / Pending)
    - Due date (if pending)
    - Fine amount
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
    
    # Get fee record
    fee_record = db.query(models.Fees).filter(
        models.Fees.register_number == register_number
    ).first()
    
    if not fee_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fee record found for this student"
        )
    
    return fee_record
