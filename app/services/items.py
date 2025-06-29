from typing import List
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.schemas import ItemCreate, ItemUpdate, ItemResponse
from app.models.db_models import Item, User
from app.crud.items import create_item as crud_create_item, get_item as crud_get_item, update_item as crud_update_item, delete_item as crud_delete_item, get_items_by_owner as crud_get_items_by_owner

def create_new_item_for_user(db: Session, item_in: ItemCreate, user_id: int) -> ItemResponse:
    item = crud_create_item(db, item_in, user_id)
    return item

def get_user_item_by_id(db: Session, item_id: int, current_user: User) -> ItemResponse:
    item = crud_get_item(db, item_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have access to it"
        )
    return item

def get_all_user_items(db: Session, current_user: User, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
    items = crud_get_items_by_owner(db, current_user.id, skip=skip, limit=limit)
    return items

def update_user_item(db: Session, item_id: int, item_in: ItemUpdate, current_user: User) -> ItemResponse:
    db_item = crud_get_item(db, item_id)
    if not db_item or db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission to update it"
        )
    updated_item = crud_update_item(db, db_item, item_in)
    return updated_item

def delete_user_item(db: Session, item_id: int, current_user: User) -> ItemResponse:
    db_item = crud_get_item(db, item_id)
    if not db_item or db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or you don't have permission to delete it"
        )
    deleted_item = crud_delete_item(db, item_id)
    if not deleted_item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )
    return deleted_item