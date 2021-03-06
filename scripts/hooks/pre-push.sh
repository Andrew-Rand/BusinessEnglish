#!/bin/bash
# COPY TO .git/hooks/pre-push

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit # exit script when command fails
set -o pipefail # this setting prevents errors in a pipeline from being masked
set -o nounset # exit script when it tries to use undeclared variables




# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")"
FILE_DIR=$(pwd)
cd ../../
CWD="$(pwd)"




# RUN CHECK
# ======================================================================================================
make test


echo ">>> $(basename ${BASH_SOURCE[0]}) DONE"
