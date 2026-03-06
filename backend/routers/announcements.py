"""
Announcements Router - Campus Announcements
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/announcements", tags=["Announcements"])


@router.get("", response_model=List[schemas.AnnouncementResponse])
async def get_announcements(db: Session = Depends(get_db)):
    """
    Get all announcements.
    Returns announcements sorted by date (newest first).
    """
    announcements = db.query(models.Announcement).order_by(
        models.Announcement.date.desc()
    ).all()
    
    return announcements
