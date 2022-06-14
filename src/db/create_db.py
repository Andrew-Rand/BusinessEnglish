from src.db.db_config import get_engine, get_session
from src.basecore.models import Base
from src.task.models import Task


Base.metadata.create_all(bind=get_engine())
db_session = get_session()
db_session.add(Task(type=1, question=['l'], answer=['o', 'h']))
db_session.commit()
