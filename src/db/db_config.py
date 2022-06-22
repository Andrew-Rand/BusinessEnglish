from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.constants import user, passwd, host, port, db


def get_engine():
    engine = create_engine(f"postgresql://{user}:{passwd}@{host}:{port}/{db}")

    def get_session():
        return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)()

    return get_session


get_session = get_engine()
