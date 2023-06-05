from sqlalchemy import Column, ForeignKey, Integer

from ..core.database import Base


class UserFollower(Base):
    __tablename__ = "user_follower"
    # foreign key
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    # foreign key
    follower_id = Column(Integer, ForeignKey("follower.id"), primary_key=True)
