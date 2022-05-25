Before working with database

make start - to run containers with app and database
exec container
run python3
from src.db.utils import Base, get_session
Base.metadata.create_all(get_session().bind)


Base.metadata.create_all(engine)
