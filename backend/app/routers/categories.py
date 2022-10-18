from typing import List, Type
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from app.utils import response, wrapper, Response, BaseModel
from app.auth import get_user, get_admin_user, User
from crud import categories


router = APIRouter()


class CategoryName(BaseModel):
    category: str


@router.post("/", response_model=Response)
def add_new_category(category: str = Body(), user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if categories.create(db, category):
        db.commit()
        return response(None, "Категория создана")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Такая категория уже существует")


@router.get("/", response_model=wrapper(List[categories.Category], "CategoriesGetResponse"))
def get_all_categories(user: User = Depends(get_user), db: Session = Depends(get_db)):
    return response([categories.convert(category) for category in categories.get_all(db)])


@router.put("/{category_id}", response_model=Response)
def rename_category(category_id: int, category: str = Body(), user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if categories.update(db, category_id, category):
        db.commit()
        return response(None, "Категория изменена")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")


@router.delete("/{category_id}", response_model=Response)
def remove_category(category_id: int, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    if categories.delete(db, category_id):
        db.commit()
        return response(None, "Категория удалена")
    else:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Категория не найдена")
