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


class Category(BaseModel):
    id: int
    category: str


class CategoryPost(BaseModel):
    category: str

# #############################################################################################


def category_from_db(category: models.Category):
    return Category(**category.__dict__)


def categories_get(db: Session) -> List[models.Category]:
    return db.query(models.Category).order_by(models.Category.category.asc()).all()


def category_get_by_category(db: Session, category: str) -> models.Category:
    return db.query(models.Category).filter(models.Category.category == category).first()


def category_get_by_id(db: Session, category_id: int) -> models.Category:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def category_create(db: Session, category: CategoryPost) -> bool:
    if category_get_by_category(db, category.category) is not None:
        return False
    db.add(models.Category(category=category.category))
    return True


def category_update(db: Session, category_id: str, category: CategoryPost) -> bool:
    db_category = category_get_by_id(db, category_id)
    if db_category is None:
        return False
    db_category.category = category.category
    return True


def category_delete(db: Session, category_id: int) -> bool:
    db_category = category_get_by_id(db, category_id)
    if db_category is None:
        return False
    db.delete(db_category)
    return True


# #############################################################################################


@router.post("/", response_model=Response)
def add_new_category(category: CategoryPost, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if category_create(db, category):
        db.commit()
        return response(None, "Категория создана")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Такая категория уже существует")


@router.get("/", response_model=wrapper(List[Category], "CategoriesGetResponse"))
def get_all_categories(user: User = Depends(get_user), db: Session = Depends(get_db)):
    return response([category_from_db(category) for category in categories_get(db)])


@router.put("/{category_id}", response_model=Response)
def rename_category(category_id: int, category: CategoryPost, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if category_update(db, category_id, category):
        db.commit()
        return response(None, "Категория изменена")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")


@router.delete("/{category_id}", response_model=Response)
def remove_category(category_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if category_delete(db, category_id):
        db.commit()
        return response(None, "Категория удалена")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")
