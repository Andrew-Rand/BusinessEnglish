import os
import sys
from logging.config import fileConfig

from alembic import context

from src.db.constants import user, passwd, host, port, db


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", f"postgresql://{user}:{passwd}@{host}:{port}/{db}")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)


from src.user.models import BaseModel as user_base
from src.task.models import BaseModel as task_base
target_metadata = [user_base.metadata, task_base.metadata]
