import hashlib
from typing import Any, BinaryIO, Dict
from pathlib import Path
from pydantic import BaseModel, create_model
import random
import string

class Response(BaseModel):
    message: str | None = None
    content: Any | None = None

def get_random_string(k=20):
    return ''.join(random.choices(string.ascii_uppercase, k=k))

def wrapper(type, name: str | None = None) -> BaseModel:
    if name is None:
        name = get_random_string()
    return create_model(name, content=(type, ...), __base__=Response)

def wrapper_paged(type, name: str | None = None) -> BaseModel:
    if name is None:
        name = get_random_string()
    return create_model(name, content=(type, ...), __base__=Response)

def response(content: Any | None = None, message: str | None = None) -> Response:
    return {
        'content': content,
        'message': message
    }

def md5(fname: Path):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def uniquify(filename: Path, same_files: list[str]) -> Path:
    counter = 1
    temp_path = filename
    while str(temp_path) in same_files:
        temp_path = filename.with_stem(f"{filename.stem} ({counter})")
        counter+=1
    return temp_path