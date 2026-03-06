"""
Timetable Router - Class Schedule Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import models
import schemas

router = APIRouter(prefix="/timetable", tags=["Timetable"])


@router.get("/{day}", response_model=List[schemas.TimetableResponse])
async def get_timetable(
    day: str,
    department: Optional[str] = None,
    semester: Optional[int] = None,
    section: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get timetable for a specific day.
    Optional filters: department, semester, section
    """
    # Build query
    query = db.query(models.Timetable).filter(
        models.Timetable.day.ilike(day)
    )
    
    # Apply optional filters
    if department:
        query = query.filter(models.Timetable.department.ilike(department))
    if semester:
        query = query.filter(models.Timetable.semester == semester)
    if section:
        query = query.filter(models.Timetable.section.ilike(section))
    
    timetable = query.order_by(models.Timetable.time).all()
    
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No timetable found for {day}"
        )
    
    return timetable
