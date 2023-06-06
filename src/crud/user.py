from typing import List, Union

from sqlalchemy.orm import Session

from .. import models, schemas


def get_user(db: Session, user_id: int) -> Union[schemas.User, None]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str) -> Union[schemas.User, None]:
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_secret_by_name(db: Session, name: str) -> Union[schemas.UserSecret, None]:
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
