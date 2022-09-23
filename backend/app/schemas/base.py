from typing import Any
from pydantic import BaseModel

class Response(BaseModel):
    message: str | None = None
    content: Any | None = None


class Tree(BaseModel):
    value: int
    label: str
    className: None | str = None
    children: None | list['Tree']    

class TreeExtended(BaseModel):
    tree: list[Tree]
    mapping: dict

class TreeResponce(Response):
    content: list[Tree]

class MappingResponse(Response):
    content: dict

class TreeExtendedResponce(Response):
    content: TreeExtended