from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.utils import response, wrapper, Response
from app.auth import get_user, get_admin_user, User


# #############################################################################################


router = APIRouter()


# #############################################################################################


# #############################################################################################


def categories_get(db: Session) -> List[models.Category]:
    return db.query(models.Category).all()


def category_get(db: Session, category: str) -> models.Category:
    return db.query(models.Category).filter(models.Category.category == category).first()


def category_create(db: Session, category: str) -> bool:
    if category_get(db, category) is not None:
        return False
    db.add(models.Category(category=category))
    return True


def category_update(db: Session, old_category: str, new_category: str) -> bool:
    db_category = category_get(db, old_category)
    if db_category is None:
        return False
    db_category.category = new_category
    return True


def category_delete(db: Session, category: str) -> bool:
    db_category = category_get(db, category)
    if db_category is None:
        return False
    db.delete(db_category)
    return True


# #############################################################################################


@router.post("/", response_model=Response)
def add_new_category(category: str = Body(), user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if category_create(db, category):
        db.commit()
        return response(None, "Категория создана")
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Такая категория уже существует")


@router.get("/", response_model=wrapper(List[str], "CategoriesGetResponse"))
def get_all_categories(user: User = Depends(get_user), db: Session = Depends(get_db)):
    return response([category.category for category in categories_get(db)])


@router.put("/", response_model=Response)
def rename_category(category: str, new_category: str = Body(), user: User = Depends(get_user), db: Session = Depends(get_db)):
    if category_update(db, category, new_category):
        db.commit()
        return response(None, "Категория изменена")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")


@router.delete("/", response_model=Response)
def remove_category(category: str, user: User = Depends(get_user), db: Session = Depends(get_db)):
    if category_delete(db, category):
        db.commit()
        return response(None, "Категория удалена")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")
