from random import choice
from typing import List, Union, Any, Dict
from uuid import UUID

from sqlalchemy.orm import Session, Query

from src.basecore.error_handler import NotFoundError, NOT_FOUND_ERROR_MESSAGE
from src.task.models import Task
from src.user.api import get_user_by_id


def get_task_list(db_session: Session, skip: int = 0, limit: int = 100) -> List[Task]:

    return db_session.query(Task).offset(skip).limit(limit).all()


def get_task_by_id(db_session: Session, task_id: UUID) -> Query:

    task_obj = db_session.query(Task).filter(Task.id == task_id).first()

    if not task_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    return task_obj


def create_task(db_session: Session, data: Dict[str, Any]) -> Task:

    task_obj = Task(type=data['type'], question=data['question'], answer=data['answer'])
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


def update_task(db_session: Session, task_id: UUID, data: Dict[str, Any]) -> Task:
    task_obj = get_task_by_id(db_session=db_session, task_id=task_id)

    if not task_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    task_obj.question = data['question']
    task_obj.answer = data['answer']
    db_session.commit()
    db_session.refresh(task_obj)
    return task_obj


def get_random_task(db_session: Session) -> Union[Query, None]:

    task_qs = db_session.query(Task).all()
    if task_qs:
        return choice(task_qs)
    return None


def check_task(db_session: Session, task_id: UUID, answer: str, user_id: str = None) -> bool:

    task_obj = get_task_by_id(db_session=db_session, task_id=task_id)
    user_obj = get_user_by_id(db_session=db_session, user_id=user_id)

    if not task_obj or not user_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    if answer.lower() in [answer.lower() for answer in task_obj.answer]:
        user_obj.successed_tasks += 1
        user_obj.streak += 1
        result = True
    else:
        # TODO: Add field with user warnings, if user has 3 warnings per day, zero out a streak. Give them a chance)
        user_obj.streak = 0
        result = False

    db_session.commit()
    db_session.refresh(user_obj)

    return result
