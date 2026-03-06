"""
JWT Authentication utilities for UniSphere
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

# JWT Configuration
SECRET_KEY = "unisphere-smart-student-assistant-secret-key-2024"  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Store for blacklisted tokens (simple in-memory store for prototype)
blacklisted_tokens = set()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_student(db: Session, register_number: str, password: str) -> Optional[models.Student]:
    """Authenticate a student with register number and password."""
    student = db.query(models.Student).filter(
        models.Student.register_number == register_number
    ).first()
    
    if not student:
        return None
    if not verify_password(password, student.password):
        return None
    return student


async def get_current_student(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.Student:
    """Get the current authenticated student from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if token is blacklisted
    if token in blacklisted_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        register_number: str = payload.get("sub")
        if register_number is None:
            raise credentials_exception
        token_data = schemas.TokenData(register_number=register_number)
    except JWTError:
        raise credentials_exception
    
    student = db.query(models.Student).filter(
        models.Student.register_number == token_data.register_number
    ).first()
    
    if student is None:
        raise credentials_exception
    return student


def blacklist_token(token: str):
    """Add token to blacklist for logout functionality."""
    blacklisted_tokens.add(token)
