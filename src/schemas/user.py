from typing import List, Optional

from .base import FollowerBase, UserBase
from .task import Task


class UserCreate(UserBase):
    pass


class User(UserBase):
    tasks: List[Task] = []
    followers: Optional[List[FollowerBase]] = []
