from typing import List, Union

from sqlalchemy.orm import Session

from .. import models, schemas


def get_follower(db: Session, follower_id: int) -> Union[schemas.Follower, None]:
    return db.query(models.Follower).filter(models.Follower.id == follower_id).first()


def get_follower_by_name(db: Session, name: str) -> Union[schemas.Follower, None]:
    return db.query(models.Follower).filter(models.Follower.name == name).first()


def get_followers(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schemas.Follower]:
    return db.query(models.Follower).offset(skip).limit(limit).all()


def create_follower(db: Session, follower: schemas.FollowerCreate) -> schemas.Follower:
    new_follower = models.Follower(**follower.dict())
    db.add(new_follower)
    db.commit()
    db.refresh(new_follower)
    return new_follower


def get_or_create_follower(
    db: Session, follower: schemas.FollowerCreate
) -> schemas.Follower:
    db_follower = get_follower_by_name(db, name=follower.name)
    if db_follower:
        return db_follower
    return create_follower(db=db, follower=follower)
