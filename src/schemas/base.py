from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.core.settings import settings


class UserBase(BaseModel):
    name: str
    display_name: Optional[str]

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    id: int
    title: str
    done: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class FollowerBase(BaseModel):
    name: str
    domain: str
    ap_id: str
    inbox: str

    class Config:
        orm_mode = True


class UserFollowerBase(BaseModel):
    user_id: int
    follower_id: int

    class Config:
        orm_mode = True
