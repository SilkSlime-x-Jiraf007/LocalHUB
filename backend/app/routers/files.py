from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Path as queryPath
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session
import os
from app import models
from app.utils import response, md5, uniquify, Response, wrapper
from pathlib import Path
from app.auth import get_user, User


# #############################################################################################


router = APIRouter()


# #############################################################################################


ROOT = Path("/data").resolve()


class FileGet(BaseModel):
    hash: str
    uri: str
    owner: str
    description: str
    upload_time: datetime
    size: float
    name: str


class FilePut(BaseModel):
    name: str | None = None
    description: str | None = None

# #############################################################################################


def files_get_same(db: Session, filename: Path) -> list:
    same_files = db.query(models.File).filter(models.File.filename.ilike(f"{filename.stem}%{filename.suffix}")).all()
    return [same_file.filename for same_file in same_files]


def file_get_path(root: Path, hash: str, filename: Path, split: tuple = (1, 2)) -> Path:
    path = root
    i = 0
    for s in split:
        path = path / hash[i:i+s]
        i += s
    return path / filename


def file_upload(db: Session, uploaded_file: UploadFile, user: User):
    hash = md5(uploaded_file.file)
    existed_file = db.query(models.File).filter(
        models.File.hash == hash).first()
    if existed_file:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            f"Такой файл уже был загружен под именем {existed_file.filename} ({hash})")
    filename = Path(uploaded_file.filename)
    filename = uniquify(filename, files_get_same(db, filename))
    path = file_get_path(ROOT, hash, filename)
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        file.write(uploaded_file.file.read())
    try:
        db.add(models.File(
            hash=hash,
            filename=str(filename),
            owner=user.username,
            description="",
            upload_time=datetime.now(),
            size=round(path.stat().st_size / 1024, 2)
        ))
        db.commit()
    except:
        db.rollback()
        os.remove(path)
        raise


def file_from_db(db_file: models.File) -> list[FileGet]:
    return FileGet(
        hash=db_file.hash,
        uri=str(file_get_path(Path(), db_file.hash, db_file.filename)),
        owner=db_file.owner,
        description=db_file.description,
        upload_time=db_file.upload_time,
        size=db_file.size,
        name=str(Path(db_file.filename).stem),
    )


def files_get(db: Session, username: str | None = None) -> List[models.File]:
    db_files = db.query(models.File)
    if username:
        db_files = db_files.filter(models.File.owner == username)
    db_files = db_files.order_by(models.File.upload_time.desc()).all()
    return db_files


def file_get(db: Session, hash: str, username: str | None = None) -> models.File:
    db_file = db.query(models.File).filter(models.File.hash == hash)
    if username:
        db_file = db_file.filter(models.File.owner == username)
    db_file = db_file.order_by(models.File.upload_time.desc()).first()
    return db_file

# #############################################################################################


@router.post("/", response_model=Response)
def upload_file(uploaded_file: UploadFile, user: User = Depends(get_user), db: Session = Depends(get_db)):
    file_upload(db, uploaded_file, user)
    return response(None, "Файл загружен")


@router.get("/", response_model=wrapper(List[FileGet]))
def get_all_files(user: User = Depends(get_user), db: Session = Depends(get_db)):
    return response([file_from_db(db_file) for db_file in files_get(db, user.username)])


@router.put("/{hash}", response_model=Response)
def change_file(file_info: FilePut, hash: str = queryPath(min_length=32, max_length=32), user: User = Depends(get_user), db: Session = Depends(get_db)):
    db_file = file_get(db, hash, user.username)
    if file_info.description:
        if file_info.description != db_file.description:
            db_file.description = file_info.description
    if file_info.name:
        old_filename = Path(db_file.filename)
        if file_info.name != old_filename.stem:
            new_filename = old_filename.with_stem(file_info.name)
            db_file.filename = str(new_filename)

            old_path = file_get_path(ROOT, db_file.hash, old_filename)
            new_path = file_get_path(ROOT, db_file.hash, new_filename)
            if new_path.exists():
                raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                    "Данное имя файла уже используется")
            try:
                old_path.rename(new_path)
            except Exception:
                db.rollback()
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Не удалось изменить файл")
    db.commit()
    return response(None, "Файл изменен")


@router.delete("/{hash}", response_model=Response)
def delete_file(hash: str = queryPath(min_length=32, max_length=32), user: User = Depends(get_user), db: Session = Depends(get_db)):
    db_file = file_get(db, hash, user.username)
    if db_file is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Файл не найден")
    
    db.delete(db_file)
    try:
        os.remove(file_get_path(ROOT, db_file.hash, db_file.filename))
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Не удалось удалить файл")
    db.commit()
    return response(None, "Файл удален")