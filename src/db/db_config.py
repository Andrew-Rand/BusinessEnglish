from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.db.constants import user, passwd, host, port, db

engine = create_engine(f"postgresql://{user}:{passwd}@{host}:{port}/{db}")
db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()


Base = declarative_base()
