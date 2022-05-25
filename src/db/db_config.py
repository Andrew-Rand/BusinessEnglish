from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.db.constants import user, passwd, host, port, db


def get_engine():
    return create_engine(f"postgresql://{user}:{passwd}@{host}:{port}/{db}")


def get_session():
    engine = get_engine()
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)()


Base = declarative_base()
