from .base import TaskBase


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    user_id: int
