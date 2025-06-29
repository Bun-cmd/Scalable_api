from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.models.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.auth.dependencies import get_current_active_user
from app.models.db_models import User
from app.services.items import create_new_item_for_user, get_all_user_items, get_user_item_by_id, update_user_item, delete_user_item

router = APIRouter()

@router.post("/items/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item_route(
    item_in: ItemCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_new_item_for_user(db, item_in, current_user.id)

@router.get("/items/", response_model=List[ItemResponse])
async def read_items_for_user(
    skip: int = 0, limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_all_user_items(db, current_user, skip=skip, limit=limit)

@router.get("/items/{item_id}", response_model=ItemResponse)
async def read_item_by_id(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_user_item_by_id(db, item_id, current_user)

@router.patch("/items/{item_id}", response_model=ItemResponse)
async def update_item_route(
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_user_item(db, item_id, item_in, current_user)

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_route(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    delete_user_item(db, item_id, current_user)
    return