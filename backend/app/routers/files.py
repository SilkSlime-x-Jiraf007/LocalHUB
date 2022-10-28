from datetime import datetime
from typing import Dict, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Path as QueryPath, Query
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
    hash: str
    uri: str
    owner: str
    description: str
    upload_time: datetime
    size: str
    name: str
    type: str
    group: str | None


class FilePut(BaseModel):
    name: str | None = None
    description: str | None = None

class FileType(enum.Enum):
    IMAGE = 'Image'
    VIDEO = 'Video'
    TEXT = 'Text'
    MANGA = 'Manga'
    OTHER = 'Other'

def get_file_data(filepath: Path):
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


def file_get_dir_path(root: Path, hash: str, split: tuple = (1, 2)) -> Path:
    path = root
    i = 0
    for s in split:
        path = path / hash[i:i+s]
        i += s
    return path


def file_get_name(filename: Path) -> str:
    return str(Path(filename).stem)


def convert(db_file: models.File) -> File:
    return File(
        hash=db_file.hash,
        owner=db_file.owner,
        description=db_file.description,
        upload_time=db_file.upload_time,
        size=get_human_size(int(db_file.size)),
        uri=str(file_get_dir_path(Path(), db_file.hash) / db_file.filename),
        name=file_get_name(db_file.filename),
        type=db_file.type,
        group=db_file.group_id
    )


def file_get_by_hash(db: Session, hash: str, username: str | None = None) -> models.File | None:
    db_file = db.query(models.File).filter(models.File.hash == hash)
    if username:
        db_file = db_file.filter(models.File.owner == username)
    db_file = db_file.order_by(models.File.upload_time.desc()).first()
    return db_file


def files_get_same_names(db: Session, filename: Path) -> List[str]:
    same_files = db.query(models.File).filter(models.File.filename.ilike(f"{filename.stem}%{filename.suffix}")).all()
    return [same_file.filename for same_file in same_files]


def files_get_all_query(
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


def file_upload(db: Session, uploaded_file: UploadFile, group: UUID, user: User) -> bool:
    hash = md5(uploaded_file.file)
    existed_file = file_get_by_hash(db, hash)
    if existed_file:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Такой файл уже был загружен под именем '{existed_file.filename}' ({hash}) пользователем '{existed_file.owner}'")
    filename = Path(uploaded_file.filename)
    filename = uniquify(filename, files_get_same_names(db, filename))
    path = file_get_dir_path(ROOT, hash) / filename
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        file.write(uploaded_file.file.read())
    filedata = get_file_data(path)
    try:
        db.add(models.File(
            hash=hash,
            filename=str(filename),
            owner=user.username,
            description="",
            upload_time=datetime.now(),
            size=filedata.size,
            type=filedata.type.value,
            group_id=str(group) if group else None
        ))
        if filedata.type == FileType.IMAGE:
            db.add(models.Image(
                hash=hash,
                width=filedata.width,
                height=filedata.height,
                phash=filedata.phash,
                colorhash=filedata.colorhash
            ))
        elif filedata.type == FileType.VIDEO:
            db.add(models.Video(
                hash=hash,
                width=filedata.width,
                height=filedata.height,
                duration=filedata.duration,
                has_audio=filedata.has_audio
            ))
        elif filedata.type == FileType.TEXT:
            db.add(models.Story(
                hash=hash,
            ))
        elif filedata.type == FileType.MANGA:
            db.add(models.Manga(
                hash=hash,
            ))

        db.commit()
        return True
    except:
        db.rollback()
        os.remove(path)
        raise


def file_update(db: Session, hash: str, file_info: FilePut, username: str | None = None) -> None:
    db_file = file_get_by_hash(db, hash, username)
    if db_file is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Файл не найден")
    if file_info.description is not None:
        db_file.description = file_info.description
    old_filename = Path(db_file.filename)
    if file_info.name != old_filename and file_info.name is not None:
        new_filename = old_filename.with_stem(file_info.name)
        db_file.filename = str(new_filename)
        dir_path = file_get_dir_path(ROOT, db_file.hash)
        old_path = dir_path / old_filename
        new_path = dir_path / new_filename
        if new_path.exists():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Указанное имя файла уже используется")
        try:
            old_path.rename(new_path)
        except Exception:
            db.rollback()
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Не удалось изменить файл")


def file_delete(db: Session, hash: str, username: str | None = None):
    db_file = file_get_by_hash(db, hash, username)
    if db_file is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Файл не найден")
    db.delete(db_file)
    try:
        os.remove(file_get_dir_path(ROOT, db_file.hash) / db_file.filename)
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Не удалось удалить файл")


# #############################################################################################


@router.post("/", response_model=Response)
def upload_file(uploaded_file: UploadFile, group: UUID | None = None, user: User = Depends(get_user), db: Session = Depends(get_db)):
    file_upload(db, uploaded_file, group, user)
    return response(None, "Файл загружен")



@router.get("/", response_model=wrapper(List[File]))
def get_all_files(
    num: int = Query(default=10, ge=1, le=100),
    page: int = Query(default=1, ge=1),
    name: str | None = Query(default=None, max_length=100),
    type: FileType | None = None,
    order_column: OrderColumns = OrderColumns.upload_time,
    order_type: OrderType = OrderType.desc,
    iti: List[int] = Query(default=list()),
    bti: List[int] = Query(default=list()),
    strict: bool = Query(default=True),
    all: bool = Query(default=False),
    user: User = Depends(get_user),
    db: Session = Depends(get_db)
):
    files: List[models.File] = files_get_all_query(
        db,
        user.username,
        num=num,
        page=page,
        name=name,
        type=type,
        order_column=order_column,
        order_type=order_type,
        include=iti,
        ban=bti,
        strict=strict,
        all=all
    ).all()
    return response([convert(db_file) for db_file in files])


@router.put("/{hash}", response_model=Response)
def change_file(file_info: FilePut, hash: str = QueryPath(min_length=32, max_length=32), user: User = Depends(get_user), db: Session = Depends(get_db)):
    file_update(db, hash, file_info, user.username)
    db.commit()
    return response(None, "Файл изменен")


@router.delete("/{hash}", response_model=Response)
def delete_file(hash: str = QueryPath(min_length=32, max_length=32), user: User = Depends(get_user), db: Session = Depends(get_db)):
    file_delete(db, hash, user.username)
    db.commit()
    return response(None, "Файл удален")