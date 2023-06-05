from typing import List, Union

from sqlalchemy.orm import Session

from .. import models, schemas


def get_user_follower(
    db: Session, user_follower: schemas.UserFollowerGet
) -> Union[schemas.UserFollower, None]:
    return (
        db.query(models.UserFollower)
        .filter(
            models.UserFollower.user_id == user_follower.user_id
            and models.UserFollower.follower_id == user_follower.follower_id
        )
        .first()
    )


def get_user_follower_list(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schemas.UserFollower]:
    return db.query(models.UserFollower).offset(skip).limit(limit).all()


def create_user_follower(
    db: Session, user_follower: schemas.UserFollowerCreate
) -> schemas.UserFollower:
    new_user_follower = models.UserFollower(**user_follower.dict())
    db.add(new_user_follower)
    db.commit()
    db.refresh(new_user_follower)
    return new_user_follower


def get_or_create_user_follower(
    db: Session,
    user_follower: Union[schemas.UserFollowerCreate, schemas.UserFollowerGet],
) -> schemas.UserFollower:
    db_user_follower = get_user_follower(db, user_follower=user_follower)
    if db_user_follower:
        return db_user_follower
    return create_user_follower(db=db, user_follower=user_follower)
