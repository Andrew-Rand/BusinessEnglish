#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit # exit script when command fails
set -o pipefail # this setting prevents errors in a pipeline from being masked
set -o nounset # exit script when it tries to use undeclared variables

echo ">>> START THE PROJECT"

docker-compose -f docker-compose.${APP_ENV}.yml down  # force delete test db container if the last time has finished with an error
docker-compose -f docker-compose.${APP_ENV}.yml up --build -d  # run test db container