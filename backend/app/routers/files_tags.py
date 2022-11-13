# from typing import List
# from fastapi import APIRouter, Depends, HTTPException, status, Body, Path as QueryPath, Query
# from app.database import get_db
# from sqlalchemy.orm import Session
# from app import models
# from app.utils import response, wrapper, Response, BaseModel
# from app.auth import get_user, get_admin_user, User
# from .tags import Tag, tag_from_db
# # #############################################################################################


# router = APIRouter()


# # #############################################################################################



# # #############################################################################################




# # #############################################################################################


# # @router.post("/", response_model=Response)
# # def add_new_tag(tag: TagPost, user: User = Depends(get_admin_user), db: Session = Depends(get_db)):
# #     if tag_create(db, tag):
# #         db.commit()
# #         return response(None, "Тэг создан")
# #     else:
# #         db.rollback()
# #         raise HTTPException(status.HTTP_400_BAD_REQUEST, "Такой тэг уже существует")

# def get_file_tags_all(db: Session, hash: str) -> List[models.Tag]:
#     return db.query(models.Tag).join(models.FilesTags, models.FilesTags.tag_id == models.Tag.id).filter(models.FilesTags.file_hash == hash).all()

# @router.get("/{hash}/tags", response_model=wrapper(List[Tag], "FileTagsGetResponse"))
# def get_all_file_tags(hash: str = QueryPath(min_length=32, max_length=32), user: User = Depends(get_user), db: Session = Depends(get_db)):
#     return response([tag_from_db(tag) for tag in get_file_tags_all(db, hash)])


# # @router.put("/{tag_id}", response_model=Response)
# # def edit_tag(tag_id: int, tag: TagPut, user: User = Depends(get_user), db: Session = Depends(get_db)):
# #     if tag_update(db, tag_id, tag):
# #         db.commit()
# #         return response(None, "Тэг изменен")
# #     else:
# #         db.rollback()
# #         raise HTTPException(status.HTTP_404_NOT_FOUND, "Тэг не найден")


# # @router.delete("/{tag_id}", response_model=Response)
# # def remove_tag(tag_id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
# #     if tag_delete(db, tag_id):
# #         db.commit()
# #         return response(None, "Тэг удален")
# #     else:
# #         db.rollback()
# #         raise HTTPException(status.HTTP_404_NOT_FOUND, "Тэг не найден")
