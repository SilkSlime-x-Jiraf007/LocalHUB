from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.utils import response, wrapper, Response, BaseModel
from app.auth import get_user, get_admin_user, User

# #############################################################################################


router = APIRouter()


# #############################################################################################

class Tag(BaseModel):
    id: int
    tag: str
    category_id: str

class TagPost(BaseModel):
    tag: str
    category_id: int | None = None

class TagPut(BaseModel):
    tag: str | None = None
    category: str | None = None


# #############################################################################################


def tag_from_db(db_tag: models.Tag) -> Tag:
    return Tag(**db_tag.__dict__)


def tag_get_by_id(db: Session, tag_id: int) -> models.Tag | None:
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def tag_get_by_tag(db: Session, tag: str) -> models.Tag | None:
    return db.query(models.Tag).filter(models.Tag.tag == tag).first()


def tags_get(db: Session, category_id: int | None = None) -> List[models.Tag]:
    db_tags = db.query(models.Tag)
    if category_id is not None:
        db_tags = db_tags.filter(models.Tag.category_id == category_id)
    db_tags = db_tags.order_by(models.Tag.tag.asc()).all()
    return db_tags


def tag_create(db: Session, tag: TagPost) -> bool:
    if tag_get_by_tag(db, tag.tag) is not None:
        return False
    db.add(models.Tag(**tag.dict()))
    return True


def tag_update(db: Session, tag_id: int, tag: TagPut) -> bool:
    db_tag = tag_get_by_id(db, tag_id)
    if db_tag is None:
        return False
    if db_tag.tag != tag.tag and tag.tag is not None:
        db_tag.tag = tag.tag
    if db_tag.category != tag.category and tag.category is not None:
        db_tag.category = tag.category
    return True


def tag_delete(db: Session, tag_id: int) -> bool:
    db_tag = tag_get_by_id(db, tag_id)
    if db_tag is None:
        return False
    db.delete(db_tag)
    return True


# #############################################################################################


@router.post("/", response_model=Response)
def add_new_tag(tag: TagPost, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if tag_create(db, tag):
        db.commit()
        return response(None, "Тэг создан")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Такой тэг уже существует")


@router.get("/", response_model=wrapper(List[Tag], "TagsGetResponse"))
def get_all_tags(category: str = None, user: User = Depends(get_user), db: Session = Depends(get_db)):
    return response([tag_from_db(tag) for tag in tags_get(db, category)])


@router.put("/{tag_id}", response_model=Response)
def edit_tag(tag_id: int, tag: TagPut, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if tag_update(db, tag_id, tag):
        db.commit()
        return response(None, "Тэг изменен")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Тэг не найден")


@router.delete("/{tag_id}", response_model=Response)
def remove_tag(tag_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if tag_delete(db, tag_id):
        db.commit()
        return response(None, "Тэг удален")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Тэг не найден")
