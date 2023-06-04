from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from ..core.database import Base


class Follower(Base):
    __tablename__ = "follower"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    domain = Column(String, index=True, nullable=False)
    ap_id = Column(String, index=True, nullable=False)
    inbox = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    # nameとdomainの組み合わせで一意になる
    # __table_args__ = (UniqueConstraint("name", "domain", name="unique_name_domain"),)
    users = relationship("User", secondary="user_follower", back_populates="followers")
