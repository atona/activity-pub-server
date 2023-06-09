from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas, service
from .core.database import Base, SessionLocal, engine
from .core.utils import create_key_pair

Base.metadata.create_all(bind=engine)

app = FastAPI()


# DBに接続
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return "THIS IS FAST API INDEX PAGE."


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreateRequest, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"User name: {user.name} already exists."
        )

    new_user = schemas.UserCreate(
        name=user.name, display_name=user.display_name, private_key="", public_key=""
    )
    new_user.private_key, new_user.public_key = create_key_pair()
    return crud.create_user(db=db, user=new_user)


@app.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/{name}/followers/", response_model=schemas.Follower)
def create_follower(
    name: str, follower: schemas.FollowerCreate, db: Session = Depends(get_db)
):
    user = service.get_user_service(schemas.UserGet(name=name), db)
    return service.follow_service(user, follower, db)


@app.get("/users/{name}/followers/", response_model=List[schemas.Follower])
def get_users(
    name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    user = service.get_user_service(schemas.UserGet(name=name), db)
    return user.followers[skip : limit - 1]


# @app.get("/users/{user_id}", response_model=schemas.User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = crud.get_user(db, user_id=user_id)
#     if user:
#         raise HTTPException(status_code=404, detail=f"User ID: {user_id} not found")
#     return user


# @app.post("/users/{user_id}/tasks/", response_model=schemas.Task)
# def create_task_for_user(
#     user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
# ):
#     task = crud.create_user_task(db=db, task=task, user_id=user_id)
#     return task


# @app.get("/users/{user_id}/tasks/", response_model=List[schemas.Task])
# def get_tasks_for_user(
#     user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
# ):
#     tasks = crud.get_tasks(db=db, user_id=user_id, skip=skip, limit=limit)
#     return tasks


import src.api
import src.webfinger
