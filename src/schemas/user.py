from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .task import Task


class UserBase(BaseModel):
    name: str
    display_name: Optional[str]


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: List[Task] = []

    class Config:
        orm_mode = True
