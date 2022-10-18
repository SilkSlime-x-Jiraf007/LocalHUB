from typing import List
from sqlalchemy.orm import Session
from app import models
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    category: str


def convert(category: models.Category) -> Category:
    return Category(**category.__dict__)


def get_all(db: Session) -> List[models.Category]:
    return db.query(models.Category).order_by(models.Category.category.asc()).all()


def get_one_by_category(db: Session, category: str) -> models.Category | None:
    return db.query(models.Category).filter(models.Category.category == category).first()


def get_one_by_id(db: Session, category_id: int) -> models.Category | None:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def create(db: Session, category: str) -> bool:
    if get_one_by_category(db, category) is not None:
        return False
    db.add(models.Category(category=category))
    return True


def update(db: Session, category_id: int, category: str) -> bool:
    db_category = get_one_by_id(db, category_id)
    if db_category is None:
        return False
    db_category.category = category
    return True


def delete(db: Session, category_id: int) -> bool:
    db_category = get_one_by_id(db, category_id)
    if db_category is None:
        return False
    db.delete(db_category)
    return True