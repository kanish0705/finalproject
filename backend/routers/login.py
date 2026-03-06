"""
Login Router - Student Authentication
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from auth import (
    authenticate_student,
    create_access_token,
    get_current_student,
    blacklist_token,
    oauth2_scheme,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
async def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with register number and password.
    Returns JWT access token.
    """
    student = authenticate_student(db, login_data.register_number, login_data.password)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid register number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student.register_number},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Logout and invalidate the current token.
    """
    blacklist_token(token)
    return {"message": "Successfully logged out"}


@router.get("/student/profile", response_model=schemas.StudentProfile)
async def get_student_profile(
    current_student: models.Student = Depends(get_current_student)
):
    """
    Get the profile of the currently authenticated student.
    """
    return current_student
