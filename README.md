Before working with database

make start - to run containers with app and database
exec container
python3 src/db/create_db.py




Migrate with alembic inside the app docker container

alembic upgrade head

To create new auto migration, use command

alembic revision --autogenerate -m "Added initial table"

If you have an error like database not up to date, run before

alembic stamp head




Load legacy tasks to db

docker ps

docker exec -it {container id} bash

export PYTHONPATH="${PYTHONPATH}:/usr/app/src/"
export PYTHONPATH="${PYTHONPATH}:/usr/app/task_legacy/"
python task_legacy/run_fixture_load.py 



