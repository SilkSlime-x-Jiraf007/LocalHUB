import enum
import hashlib
from fastapi import Request
from sqlalchemy.engine import Row
import os
from app.models import *
from typing import Any, BinaryIO
from app.schemas import Tree
from user_agents import parse

def get_user_agent(request: Request) -> str:
    return str(parse(request.headers.get("User-Agent")))

def get_children(result, parent_id = 0) -> list[Tree] | None:
    children = []
    for row in result:
        if row.parent == parent_id:
            children.append(Tree(**{
                'value' : row.id,
                'label' : row.name,
                'className' : ('new' if row.new else '') if hasattr(row, 'new') else '',
                'children' : get_children(result, row.id)
            }))
    return children if len(children) else None



def response(content = None, message = None):
    return {
        'content': content,
        'message': message
    }

class WorkState(enum.IntEnum):
    CREATED = 0
    QUEUED = 1
    PROCESSING = 2
    COMPLETE = 3
    ERROR = -1



def model_to_dict(model) -> dict:
    row_dict = {}
    model_dict = {f"{column.name}": getattr(
        model, column.name) for column in model.__table__.columns}
    for key in model_dict:
        if key not in row_dict:
            row_dict[key] = model_dict[key]
    return row_dict
    

def models_to_dict(models: list[Any]) -> list[dict]:
    return [model_to_dict(model) for model in models]

def row_to_dict(row: Row) -> dict:
    row_dict = {}
    for prefix, model in row._asdict().items():
        model_dict = {f"{prefix}__{column.name}": getattr(
            model, column.name) for column in model.__table__.columns}
        for key in model_dict:
            if key not in row_dict:
                row_dict[key] = model_dict[key]
    return row_dict


def rows_to_dict(rows: list[Row]) -> list[dict]:
    return [row_to_dict(row) for row in rows]


def dict_to_row(dict: dict) -> tuple:
    def factory(classname: str):
        return globals()[classname.capitalize()]
    models_dict = {}
    for key, value in dict.dict().items():
        table, column = key.split('__')
        if table not in models_dict:
            models_dict[table] = {}
        models_dict[table][column] = value
    objects = tuple(factory(class_name)(**model_dict)
                    for class_name, model_dict in models_dict.items())
    return objects
