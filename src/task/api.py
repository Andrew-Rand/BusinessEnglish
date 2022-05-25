from sqlalchemy.orm import Session, Query

from src.task.models import Task


def get_task_list(db_session: Session, skip: int = 0, limit: int = 100) -> Query:
    return db_session.query(Task).offset(skip).limit(limit).all()
