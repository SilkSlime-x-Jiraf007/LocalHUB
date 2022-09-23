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
    tag: str
    description: str
    category: str

class TagPost(BaseModel):
    tag: str
    description: str | None = None
    category: str | None = None

class TagPut(BaseModel):
    tag: str | None = None
    description: str | None = None
    category: str | None = None


# #############################################################################################

def tag_from_db(db_tag: models.Tag) -> Tag:
    return Tag(**db_tag.__dict__)


def tags_get(db: Session, category: str | None = None) -> List[models.Tag]:
    db_tags = db.query(models.Tag)
    if category is not None:
        db_tags = db_tags.filter(models.Tag.category == category)
    db_tags = db_tags.all()
    return db_tags


def tag_get(db: Session, tag: str) -> models.Tag:
    return db.query(models.Tag).filter(models.Tag.tag == tag).first()


def tag_create(db: Session, tag: TagPost) -> bool:
    if tag_get(db, tag.tag) is not None:
        return False
    db.add(models.Tag(**tag.dict()))
    return True


def tag_update(db: Session, tag_name: str, tag: TagPut) -> bool:
    db_tag = tag_get(db, tag_name)
    if db_tag is None:
        return False
    if db_tag.tag != tag.tag and tag.tag is not None:
        db_tag.tag = tag.tag
    if db_tag.description != tag.description and tag.description is not None:
        db_tag.description = tag.description
    if db_tag.category != tag.category and tag.category is not None:
        db_tag.category = tag.category
    return True


def tag_delete(db: Session, tag: str) -> bool:
    db_tag = tag_get(db, tag)
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
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Такой тэг уже существует")


@router.get("/", response_model=wrapper(List[Tag], "TagsGetResponse"))
def get_all_tags(category: str = None, user: User = Depends(get_user), db: Session = Depends(get_db)):
    return response([tag_from_db(tag) for tag in tags_get(db, category)])


@router.put("/", response_model=Response)
def edit_tag(tag: str, new_tag: TagPut, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if tag_update(db, tag, new_tag):
        db.commit()
        return response(None, "Тэг изменен")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Тэг не найден")


@router.delete("/", response_model=Response)
def remove_tag(tag: str, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if tag_delete(db, tag):
        db.commit()
        return response(None, "Тэг удален")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Тэг не найден")
