from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas


def get_tasks(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[schemas.Task]:
    return (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_task(
    db: Session, task: schemas.task.TaskCreate, user_id: int
) -> schemas.Task:
    new_task = models.Task(**task.dict(), user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
