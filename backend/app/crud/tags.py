from typing import List
from sqlalchemy.orm import Session
from app import models
from pydantic import BaseModel
from crud import categories


class Tag(BaseModel):
    id: int
    tag: str
    category_id: str


def convert(db_tag: models.Tag) -> Tag:
    return Tag(**db_tag.__dict__)


def get_all(db: Session, category_id: int | None = None) -> List[models.Tag]:
    db_tags = db.query(models.Tag)
    if category_id is not None:
        db_tags = db_tags.filter(models.Tag.category_id == category_id)
    db_tags = db_tags.order_by(models.Tag.tag.asc()).all()
    return db_tags


def get_one_by_id(db: Session, tag_id: int) -> models.Tag | None:
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def get_one_by_tag(db: Session, tag: str) -> models.Tag | None:
    return db.query(models.Tag).filter(models.Tag.tag == tag).first()


def create(db: Session, tag: str, category_id: int | None = None) -> bool:
    if get_one_by_tag(db, tag) is not None:
        return False
    if category_id:
        if categories.get_one_by_id(db, category_id) is not None:
            db.add(models.Tag(tag=tag, category_id=category_id))
        else:
            return False
    else:
        db.add(models.Tag(tag=tag))
    return True


def update(db: Session, tag_id: int, tag: str | None = None, category_id: int | None = None) -> bool:
    db_tag = get_one_by_id(db, tag_id)
    if db_tag is None:
        return False
    if db_tag.tag != tag and tag.tag is not None:
        db_tag.tag = tag
    if db_tag.category_id != category_id and category_id is not None:
        db_tag.category_id = category_id
    return True


def delete(db: Session, tag_id: int) -> bool:
    db_tag = get_one_by_id(db, tag_id)
    if db_tag is None:
        return False
    db.delete(db_tag)
    return True