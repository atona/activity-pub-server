from datetime import datetime
from typing import List, Optional

from .base import FollowerBase, UserBase
from .task import Task


class UserGet(UserBase):
    pass


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: List[Task] = []
    followers: Optional[List[FollowerBase]] = []
