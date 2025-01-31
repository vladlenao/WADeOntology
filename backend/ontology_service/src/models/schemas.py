from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel

class Direction(str, Enum):
    FORWARD = "forward"  # entity → predicate → ?
    BACKWARD = "backward"  # ? → predicate → entity

class QueryResult(BaseModel):
    subject: str
    predicate: str
    object: str

class EntityRelation(BaseModel):
    predicate: str
    object: Optional[str] = None
    subject: Optional[str] = None

class EntityRelations(BaseModel):
    forward_relations: List[EntityRelation]
    backward_relations: List[EntityRelation]