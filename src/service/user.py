from fastapi import Depends, HTTPException
from requests import Session

from src import crud, schemas


def get_user_service(user: schemas.UserCreate, db: Session) -> schemas.User:
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail=f"User name: {user.name} is not found.")
