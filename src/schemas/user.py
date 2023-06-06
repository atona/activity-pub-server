from datetime import datetime
from typing import List, Optional

from src.core.settings import settings

from .base import FollowerBase, UserBase
from .task import Task


class UserGet(UserBase):
    pass


class UserCreateRequest(UserBase):
    pass


class UserCreate(UserCreateRequest):
    private_key: str
    public_key: str
    pass


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tasks: List[Task] = []
    followers: Optional[List[FollowerBase]] = []


class UserSecret(User):
    private_key: str
    public_key: str
