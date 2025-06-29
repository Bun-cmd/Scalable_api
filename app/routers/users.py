from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database import get_db, create_db_and_tables
from app.models.schemas import UserCreate, UserResponse, Token, UserUpdate
from app.auth.security import verify_password, create_access_token
from app.auth.dependencies import get_current_active_user, get_current_active_superuser
from app.services.users import register_new_user, update_existing_user
from app.crud.users import get_user, get_users, delete_user, get_user_by_email
from app.models.db_models import User

router = APIRouter()

@router.on_event("startup")
def on_startup():
    create_db_and_tables()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(
    user_in: UserCreate, db: Session = Depends(get_db)
):
    return register_new_user(db, user_in)

@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.patch("/users/me/", response_model=UserResponse)
async def update_users_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_existing_user(db, current_user, user_in)

@router.get("/users/", response_model=List[UserResponse])
async def read_users_all(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser) # Only superusers can list all users
):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user_by_id(
    user_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser) # Only superusers can get user by ID
):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    deleted_user = delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return