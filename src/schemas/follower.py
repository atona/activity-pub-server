from datetime import datetime
from typing import List, Optional

from .base import FollowerBase, UserBase


class FollowerCreate(FollowerBase):
    pass


class Follower(FollowerBase):
    created_at: datetime
    updated_at: datetime
    users: Optional[List[UserBase]] = []
