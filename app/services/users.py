from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.schemas import UserCreate, UserUpdate, UserResponse
from app.models.db_models import User
from app.crud.users import get_user_by_email, create_user as crud_create_user, update_user as crud_update_user
from app.auth.security import get_password_hash

def register_new_user(db: Session, user_in: UserCreate) -> UserResponse:
    db_user = get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system."
        )
    hashed_password = get_password_hash(user_in.password)
    user = crud_create_user(db, user_in, hashed_password)
    return user

def update_existing_user(db: Session, db_user: User, user_in: UserUpdate) -> UserResponse:
    if user_in.password:
        user_in.password = get_password_hash(user_in.password)
    updated_user = crud_update_user(db, db_user, user_in)
    return updated_user