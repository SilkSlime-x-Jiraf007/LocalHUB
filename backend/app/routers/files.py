from datetime import datetime
from typing import Dict, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Path as QueryPath, Query, BackgroundTasks
from pydantic import BaseModel
from app.database import get_db
from sqlalchemy.orm import Session, Query as SqlQuery
from sqlalchemy import func
import os
from app import models
from app.utils import response, md5, uniquify, Response, wrapper
from pathlib import Path
from app.auth import get_user, User
from PIL import Image
import enum
import imagehash
from pymediainfo import MediaInfo, Track
from bitstring import BitArray
import time
import random
# #############################################################################################


router = APIRouter()


# #############################################################################################


ROOT = Path("/data").resolve()

class OrderColumns(enum.Enum):
    upload_time = 'upload_time'
    size = 'size'
    filename = 'filename'
    type = 'type'

class OrderType(enum.Enum):
    asc = 'asc'
    desc = 'desc'


class File(BaseModel):
    id: int
    uri: str
    owner: str
    description: str
    upload_time: datetime
    size: str
    name: str
    type: str
    group: str | None
    state: str
    message: str | None


class FilePut(BaseModel):
    name: str | None = None
    description: str | None = None

class FileType(enum.Enum):
    IMAGE = 'Image'
    VIDEO = 'Video'
    TEXT = 'Text'
    MANGA = 'Manga'
    OTHER = 'Other'

class FileState(enum.Enum):
    PROCESSING = 'processing'
    ERROR = 'error'
    PRIVATE = 'private'
    PUBLIC = 'public'

class FileData(BaseModel):
    type: FileType
    size: str

class ImageData(FileData):
    width: int
    height: int
    phash: int
    colorhash: int

class VideoData(FileData):
    width: int
    height: int
    duration: int
    has_audio: bool

class TextData(FileData):
    pass

class MangaData(FileData):
    pass

def get_file_data(filepath: Path):
    tracks: Dict[str, Track] = {track.track_type:track for track in MediaInfo.parse(filepath).tracks}
    file_type = FileType.OTHER
    size = str(tracks['General'].file_size)
    if 'Image' in tracks:
        allowed_formats = ['GIF', 'JPEG', 'PNG', 'WebP']
        if tracks['Image'].format in allowed_formats:
            file_type = FileType.IMAGE
    elif 'Video' in tracks:
        if not tracks['General'].duration:
            file_type = FileType.IMAGE
        else:
            file_type = FileType.VIDEO
    elif len(tracks) == 1 and tracks['General'].file_extension.lower() == 'txt':
        file_type = FileType.TEXT
    elif len(tracks) == 1 and tracks['General'].file_extension.lower() == 'tar':
        file_type = FileType.MANGA

    if file_type == FileType.IMAGE:
        with Image.open(filepath) as img:
            return ImageData(
                type=file_type,
                size=size,
                width=img.width,
                height=img.height,
                phash=BitArray(hex=f"0x{str(imagehash.phash(img))}").int,
                colorhash=BitArray(hex=f"0x{str(imagehash.colorhash(img))}").int
            )
    elif file_type == FileType.VIDEO:
        return VideoData(
            type=file_type,
            size=size,
            width=tracks['Video'].width,
            height=tracks['Video'].height,
            duration=int(round(float(tracks['Video'].duration)))//1000,
            has_audio= 'Audio' in tracks
        )
    elif file_type == FileType.TEXT:
        return TextData(
            type=file_type,
            size=size,
        )
    elif file_type == FileType.MANGA:
        return MangaData(
            type=file_type,
            size=size,
        )
    else:
        return FileData(
            type=file_type,
            size=size,
        )

def get_human_size(bytes: int) -> str:
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    for i, size in enumerate(sizes):
        current_size = round(bytes/pow(1024, i), 2)
        if current_size < 1024:
            return f'{current_size} {size}'

# #############################################################################################


def file_get_dir_path_from_hash(hash: str, split: tuple = (1, 2)) -> Path:
    path = Path("public")
    i = 0
    for s in split:
        path = path / hash[i:i+s]
        i += s
    return path

def db_file_get_uri(db_file) -> Path:
    if db_file.state == "public":
        return file_get_dir_path_from_hash(db_file.hash) / db_file.filename
    else:
        return Path("user") / db_file.owner / db_file.filename

def convert(db_file: models.File) -> File:
    return File(
        id=db_file.id,
        owner=db_file.owner,
        description=db_file.description,
        upload_time=db_file.upload_time,
        size=get_human_size(int(db_file.size)),
        uri=str(Path('data') / db_file_get_uri(db_file)),
        name=str(Path(db_file.filename).stem),
        type=db_file.type,
        group=db_file.group_id,
        state=db_file.state,
        message=db_file.message
    )


def file_get_by_id(db: Session, id: int, username: str | None = None) -> models.File | None:
    db_file = db.query(models.File).filter(models.File.id == id)
    if username:
        db_file = db_file.filter(models.File.owner == username)
    return db_file.first()


def files_get_same_names(db: Session, filename: Path) -> List[str]:
    same_files = db.query(models.File).filter(models.File.filename.ilike(f"{filename.stem}%{filename.suffix}")).all()
    return [same_file.filename for same_file in same_files]


def files_get_all_private_query(
    db: Session,
    username: str | None = None,
    all: bool = False,
) -> SqlQuery:
    db_files = db.query(models.File).filter(models.File.state != "public")
    if username:
        db_files = db_files.filter(models.File.owner == username)
    db_files = db_files.order_by(models.File.state.asc(), models.File.upload_time.desc())
    return db_files


def files_get_all_public_query(
    db: Session,
    username: str | None = None,
    num: int = 10,
    page: int = 1,
    name: str | None = None,
    type: FileType | None = None,
    order_column: OrderColumns = OrderColumns.upload_time,
    order_type: OrderType = OrderType.desc,
    include: List[int] | None = None,
    ban: List[int] | None = None,
    strict: bool = True,
    all: bool = False,
    select_list: list = [models.File]
) -> SqlQuery:
    db_files = db.query(*select_list)
    db_files = db.query(models.File).filter(models.File.state == "public")
    if username:
        db_files = db_files.filter(models.File.owner == username)
    if name:
        db_files = db_files.filter(models.File.filename.ilike(f'%{name}%'))
    if type:
        db_files = db_files.filter(models.File.type == type.value)

    if include:
        sub_include = db.query(models.FilesTags.file_hash).filter(models.FilesTags.tag_id.in_(include)).group_by(models.FilesTags.file_hash)
        if strict:
            sub_include = sub_include.having(func.count(models.FilesTags.tag_id) == len(include))
        db_files = db_files.filter(models.File.hash.in_(sub_include))
    if ban:
        sub_ban = db.query(models.FilesTags.file_hash).filter(models.FilesTags.tag_id.in_(ban)).group_by(models.FilesTags.file_hash)
        db_files = db_files.filter(models.File.hash.notin_(sub_ban))
    column = getattr(models.File, order_column.value)
    order_rule = column.asc() if order_type == OrderType.asc else column.desc()
    if not all:
        return db_files.order_by(order_rule).offset((page-1)*num).limit(num)
    return db_files

def files_get_query(
    db: Session,
    username: str | None = None,

    state: FileState = FileState.PUBLIC,

    name: str | None = None,
    type: FileType | None = None,

    order_column: OrderColumns = OrderColumns.upload_time,
    order_type: OrderType = OrderType.desc,

    include: List[str] | None = None,
    ban: List[str] | None = None,
    strict: bool = True,

    select_list: list = [models.File]
) -> SqlQuery:
    db_files = db.query(*select_list)


    db_files = db.query(models.File).filter(models.File.state == state.value)


    if username:
        db_files = db_files.filter(models.File.owner == username)
    if name:
        db_files = db_files.filter(models.File.filename.ilike(f'%{name}%'))
    if type:
        db_files = db_files.filter(models.File.type == type.value)

    # if include:
    #     sub_include = db.query(models.FilesTags.file_hash).filter(models.FilesTags.tag_id.in_(include)).group_by(models.FilesTags.file_hash)
    #     if strict:
    #         sub_include = sub_include.having(func.count(models.FilesTags.tag_id) == len(include))
    #     db_files = db_files.filter(models.File.hash.in_(sub_include))
    # if ban:
    #     sub_ban = db.query(models.FilesTags.file_hash).filter(models.FilesTags.tag_id.in_(ban)).group_by(models.FilesTags.file_hash)
    #     db_files = db_files.filter(models.File.hash.notin_(sub_ban))
    column = getattr(models.File, order_column.value)
    order_rule = column.asc() if order_type == OrderType.asc else column.desc()
    db_files = db_files.order_by(order_rule)
    return db_files


def query_pages(query: SqlQuery, page=1, size=12) -> SqlQuery:
    return query.offset((page-1)*size).limit(size)


def file_calculate_params(db: Session, file):
    path = ROOT / db_file_get_uri(file)
    try:
        hash = md5(path)
        existed_private_file = db.query(models.File).filter(models.File.hash == hash).filter(models.File.owner == file.owner).filter(models.File.state != "public").first()
        existed_public_file = db.query(models.File).filter(models.File.hash == hash).filter(models.File.state == "public").first()
        if existed_private_file:
            file.message = f"Collision with your non-public {existed_private_file.filename}"
            file.state = "error"
            db.commit()
            os.remove(path)
            return
        if existed_public_file:
            file.message = f"Collision with your non-public {existed_public_file.filename}"
            file.state = "error"
            db.commit()
            os.remove(path)
            return
        
        file.hash = hash
        filedata = get_file_data(path)
        file.size = filedata.size
        file.type = filedata.type.value
        
        if filedata.type == FileType.IMAGE:
            db.add(models.Image(
                id=file.id,
                width=filedata.width,
                height=filedata.height,
                phash=filedata.phash,
                colorhash=filedata.colorhash
            ))
        elif filedata.type == FileType.VIDEO:
            db.add(models.Video(
                id=file.id,
                width=filedata.width,
                height=filedata.height,
                duration=filedata.duration,
                has_audio=filedata.has_audio
            ))
        elif filedata.type == FileType.TEXT:
            db.add(models.Story(
                id=file.id
            ))
        elif filedata.type == FileType.MANGA:
            db.add(models.Manga(
                id=file.id
            ))
        file.state = "private"
        db.commit()
    except Exception as e:
        db.rollback()
        file.state = "error"
        file.message = str(e)
        db.commit()
        os.remove(path)
    

def file_upload(
        db: Session,
        uploaded_file: UploadFile,
        bg_tasks: BackgroundTasks,
        user: User
    ):
    parent_path = ROOT / "user" / user.username
    if not parent_path.exists():
        parent_path.mkdir(exist_ok=True)
    filename = Path(uploaded_file.filename)
    filename = uniquify(filename, files_get_same_names(db, filename))
    path = parent_path / filename
    with open(path, "wb") as file:
        file.write(uploaded_file.file.read())
    try:
        file = models.File(
            filename=str(filename),
            owner=user.username,
            upload_time=datetime.now(),
            size=0,
        )
        db.add(file)
        db.flush()
        db.refresh(file)
        bg_tasks.add_task(file_calculate_params, db, file)
        db.commit()
    except:
        db.rollback()
        os.remove(path)
        raise


# def file_update(db: Session, hash: str, file_info: FilePut, username: str | None = None) -> None:
#     db_file = file_get_by_hash(db, hash, username)
#     if db_file is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "Файл не найден")
#     if file_info.description is not None:
#         db_file.description = file_info.description
#     old_filename = Path(db_file.filename)
#     if file_info.name != old_filename and file_info.name is not None:
#         new_filename = old_filename.with_stem(file_info.name)
#         db_file.filename = str(new_filename)
#         dir_path = file_get_dir_path(ROOT, db_file.hash)
#         old_path = dir_path / old_filename
#         new_path = dir_path / new_filename
#         if new_path.exists():
#             raise HTTPException(status.HTTP_400_BAD_REQUEST, "Указанное имя файла уже используется")
#         try:
#             old_path.rename(new_path)
#         except Exception:
#             db.rollback()
#             raise HTTPException(status.HTTP_400_BAD_REQUEST, "Не удалось изменить файл")


def file_delete(db: Session, id: int, username: str | None = None) -> None:
    db_file = file_get_by_id(db, id)
    if db_file is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    if username is not None and db_file.owner != username:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You are not the owner")
    path = ROOT / db_file_get_uri(db_file)
    if path.exists():
        os.remove(path)
    db.delete(db_file)

# #############################################################################################


@router.post("/", response_model=Response)
def upload_file(
        uploaded_file: UploadFile,
        bg_tasks: BackgroundTasks,
        user: User = Depends(get_user),
        db: Session = Depends(get_db),
    ):
    file_upload(db, uploaded_file, bg_tasks, user)
    return response(None, "File uploaded")


@router.get("/private", response_model=None)
def get_all_private_files(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=12, ge=1),
    all: bool = Query(default=False),
    user: User = Depends(get_user),
    db: Session = Depends(get_db)
):
    files_query = files_get_query(db=db, username=user.username, private=True)
    total: int = files_query.count()
    if not all:
        files_query = query_pages(files_query, page, size)
    files_list: List[models.File] = files_query.all()
    return response({
        "items": {db_file.id:convert(db_file) for db_file in files_list},
        "total": total
    })


@router.get("/", response_model=None)
def get_files(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=12, ge=1),
    all: bool = Query(default=False),

    owner: str | None = Query(default=None, max_length=100),
    name: str | None = Query(default=None, max_length=100),
    type: FileType | None = None,
    state: FileState = FileState.PUBLIC,

    order_column: OrderColumns = OrderColumns.upload_time,
    order_type: OrderType = OrderType.desc,

    iti: List[int] = Query(default=list()),
    bti: List[int] = Query(default=list()),
    strict: bool = Query(default=True),

    user: User = Depends(get_user),
    db: Session = Depends(get_db)
):
    if state == FileState.PUBLIC:
        if owner:
            _username = owner
        else:
            _username = None
    else:
        _username = user.username

    files_query: SqlQuery = files_get_query(
        db=db,
        username=_username,
        state=state,
        name=name,
        type=type,
        order_column=order_column,
        order_type=order_type,
        include=iti,
        ban=bti,
        strict=strict
    )
    total: int = files_query.count()
    if not all:
        files_query = query_pages(files_query, page, size)
    files_list: List[models.File] = files_query.all()
    return response({
        "items": [convert(db_file) for db_file in files_list],
        "total": total
    })
    # return response({
    #     "items": {db_file.id:convert(db_file) for db_file in files_list},
    #     "total": total
    # })


# @router.put("/{hash}", response_model=Response)
# def change_file(file_info: FilePut, hash: str = QueryPath(min_length=32, max_length=32), user: User = Depends(get_user), db: Session = Depends(get_db)):
#     file_update(db, hash, file_info, user.username)
#     db.commit()
#     return response(None, "Файл изменен")


@router.delete("/{id}", response_model=Response)
def delete_file(id: int, user: User = Depends(get_user), db: Session = Depends(get_db)):
    file_delete(db, id, user.username)
    db.commit()
    return response(None, "File deleted")