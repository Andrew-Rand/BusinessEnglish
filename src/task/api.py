from random import choice
from typing import List, Union
from uuid import UUID

from sqlalchemy.orm import Session, Query

from src.basecore.error_handler import NotFoundError, NOT_FOUND_ERROR_MESSAGE
from src.task.models import Task
from src.task.serializers import TaskSchema


def get_task_list(db_session: Session, skip: int = 0, limit: int = 100) -> List[Task]:

    return db_session.query(Task).offset(skip).limit(limit).all()


def get_task_by_id(db_session: Session, task_id: UUID) -> Query:

    task_obj = db_session.query(Task).filter(Task.id == task_id).first()

    if not task_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    return task_obj


def create_task(db_session: Session, task: TaskSchema) -> Task:

    task_obj = Task(type=task.type, question=task.question, answer=task.answer)
    db_session.add(task_obj)
    db_session.commit()
    db_session.refresh(task_obj)

    return task_obj


def remove_task(db_session: Session, task_id: UUID):

    task_obj = get_task_by_id(db_session=db_session, task_id=task_id)

    if not task_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    db_session.delete(task_obj)
    db_session.commit()


def update_task(db_session: Session, task_id: UUID, question: List[str], answer: List[str]) -> Task:
    task_obj = get_task_by_id(db_session=db_session, task_id=task_id)

    if not task_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    task_obj.question = question
    task_obj.answer = answer
    db_session.commit()
    db_session.refresh(task_obj)
    return task_obj


def get_random_task(db_session: Session) -> Union[Query, None]:

    task_qs = db_session.query(Task).all()
    if task_qs:
        return choice(task_qs)
    return None


def check_task(db_session: Session, task_id: UUID, answer: str) -> bool:

    task_obj = get_task_by_id(db_session=db_session, task_id=task_id)

    if not task_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    if answer.lower() in [answer.lower() for answer in task_obj.answer]:
        return True
    else:
        return False
