from random import choice
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session, Query

from src.task.models import Task
from src.task.serializers import TaskSchema


def get_task_list(db_session: Session, skip: int = 0, limit: int = 100) -> Query:
    return db_session.query(Task).offset(skip).limit(limit).all()


def get_task_by_id(db_session: Session, task_id: UUID) -> Query:
    return db_session.query(Task).filter(Task.id == task_id).first()


def create_task(db_session: Session, task: TaskSchema) -> Task:
    task = Task(type=task.type, question=task.question, answer=task.answer)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def remove_task(db_session: Session, task_id: UUID):
    task = get_task_by_id(db_session=db_session, task_id=task_id)
    db_session.delete(task)
    db_session.commit()


def update_task(db_session: Session, task_id: UUID, question: List[str], answer: List[str]) -> Task:
    task = get_task_by_id(db_session=db_session, task_id=task_id)
    task.question = question
    task.answer = answer
    db_session.commit()
    db_session.refresh(task)
    return task


def get_random_task(db_session: Session) -> Query:
    task_qs = db_session.query(Task).all()
    return choice(task_qs)
