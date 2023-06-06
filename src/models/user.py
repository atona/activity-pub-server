from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, index=True, nullable=False)
    private_key = Column(String, unique=True, index=True, nullable=False)
    public_key = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )

    tasks = relationship("Task", back_populates="user")

    followers = relationship(
        "Follower", secondary="user_follower", back_populates="users"
    )
