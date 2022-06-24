## Business english API 
This is an API for english education application in a business domain.
You can get all information about allowed endpoints, using url (if u start the API locally)

    http://127.0.0.1:3000/docs

### Running application

First you need to install Docker and Docker compose on your computer

https://docs.docker.com/compose/install/

Then open your terminal in project dir and use command

    make start

or

    pipenv run start

### Before working with database

Before working with database u need to add all required values into the .env file. 
Then run application with docker (look at the Running application section)
Find container with the application with command 
    docker ps

And go inside

    docker exec -it container_id bash

Inside the container run next command to initial your db:

    export PYTHONPATH="${PYTHONPATH}:/usr/app/src/"
    python3 src/db/create_db.py

#### Another way to initial db

Migrate with alembic inside the app docker container

    alembic upgrade head

To create new auto migration, use command

    alembic revision --autogenerate -m "Added initial table"

If you have an error like database not up to date, run before

    alembic stamp head


### Upload tasks into the db

There is json file with all task for the application. 
To upload it to the db, run command inside the app container

    export PYTHONPATH="${PYTHONPATH}:/usr/app/src/"
    export PYTHONPATH="${PYTHONPATH}:/usr/app/task_legacy/"
    python task_legacy/run_fixture_load.py 



