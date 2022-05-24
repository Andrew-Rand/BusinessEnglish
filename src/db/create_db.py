from src.db.db_config import engine, db_session
from src.task.models import Task, Base


Base.metadata.create_all(bind=engine)
db_session.add(Task(type=1, question=['l'], answer=['o', 'h']))
db_session.commit()
