from typing import List, Optional
from sqlmodel import Session, select
from app.models.db_models import Item
from app.models.schemas import ItemCreate, ItemUpdate

def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.get(Item, item_id)

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    statement = select(Item).offset(skip).limit(limit)
    return db.exec(statement).all()

def get_items_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Item]:
    statement = select(Item).where(Item.owner_id == owner_id).offset(skip).limit(limit)
    return db.exec(statement).all()

def create_item(db: Session, item_in: ItemCreate, owner_id: int) -> Item:
    db_item = Item(**item_in.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, db_item: Item, item_in: ItemUpdate) -> Item:
    for field, value in item_in.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int) -> Optional[Item]:
    item = db.get(Item, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item