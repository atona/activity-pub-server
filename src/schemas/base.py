from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int = Field(alias="user_id")
    name: str
    display_name: Optional[str]
    created_at: datetime
    updated_at: datetime

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
    id: int = Field(alias="follower_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
