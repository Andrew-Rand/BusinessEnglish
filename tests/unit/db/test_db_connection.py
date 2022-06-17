import os
from urllib.parse import quote_plus

import unittest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from src.db.db_config import get_engine, get_session


class DBTestBase(unittest.TestCase):

    def setUp(self):
        self.db_user = os.environ.get("POSTGRES_USER")
        self.db_host = os.environ.get("POSTGRES_HOST")
        self.db_port = os.environ.get("POSTGRES_PORT")
        self.db_name = os.environ.get("POSTGRES_DB")
        self.db_password = os.environ.get("POSTGRES_PASSWORD")

        self.database_uri = f'postgresql://{self.db_user}:' \
                            f'%s@{self.db_host}:' \
                            f'{self.db_port}/' \
                            f'{self.db_name}'\
                            % quote_plus(self.db_password)
        self.engine = Engine(
            dialect="",
            url=f'postgresql://{self.db_user}:' \
                            f'%s@{self.db_host}:' \
                            f'{self.db_port}/' \
                            f'{self.db_name}'\
                            % quote_plus(self.db_password),
            pool=""
        )


class TestDBConnection(DBTestBase):

    def test_get_engine(self):

        engine = get_engine()

        self.assertEqual(str(engine.url), self.engine.url)

    def test_get_session(self):

        db_session = get_session()

        self.assertIsInstance(db_session, Session)
