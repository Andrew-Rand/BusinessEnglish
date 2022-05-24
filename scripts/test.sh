#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit # exit script when command fails
set -o pipefail # this setting prevents errors in a pipeline from being masked
set -o nounset # exit script when it tries to use undeclared variables

# INIT WORKING DIR
# ===================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
FILE_DIR=$(pwd)
cd ..
CWD="$(pwd)"

# RUN TESTS
#====================================================
echo ">>> START LOCAL TEST DB"

docker-compose -f docker-compose.${APP_ENV}.yml down  # force delete test db container if the last time has finished with an error
docker-compose -f docker-compose.${APP_ENV}.yml up --build -d  # run test db container

echo ">>> WAITING FOR POSTGRES START"

./scripts/waiting-for-postgres.sh

echo ">>> POSTGRES LAUNCHED SUCCESSFULLY"
echo ">>> MIGRATE"

alembic upgrade head
psql -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -d "${POSTGRES_DB}" -U "${POSTGRES_USER}" -f scripts/local/sql/initial_data.sql

echo ">>> RUN TESTS"

if coverage run --branch --source=src -m unittest discover -v
then
    RESULT=true
else
    RESULT=false
fi
coverage report
coverage html

echo ">>> REMOVE TEST DB"
docker-compose -f docker-compose.${APP_ENV}.yml down
# END
# ===================================================
echo ">>> $(basename ${BASH_SOURCE[0]}) DONE"

if [ "$RESULT" = false ] ; then
    exit 123
fi

echo $RESULT
