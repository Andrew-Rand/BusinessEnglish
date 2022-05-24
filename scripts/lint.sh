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




# INIT COLOR HIGHLIGHTING
# ===================================================

RED='\033[0;31m'
RED_BG='\e[41m'
BLACK='\e[1;30m'
CYAN='\e[36m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'


process_counter=0
function start_section() {
    process_counter=$((process_counter+1))
    echo -e "${BLUE}[STEP ${process_counter} : ${1}]${NC}"
}
function end_section() {
    COUNT_OF_ERRORS=$1
    if (( ${COUNT_OF_ERRORS} > 0))
    then
        echo -e "\n${RED_BG}${BLACK}  FAILED  ${NC}   ${1} errors found\n"
        exit 1
    fi
    echo -e "${GREEN}>> DONE without errors${NC}\n"
}

function lint() {
  echo "$1"
    start_section "LINTING FLAKE"
    flake8 $1
    end_section 0

    start_section "LINTING PYLINT"
    pylint --errors-only -j 4 $1 --disable=import-error
    end_section 0

    start_section "LINTING BLACK"
    black --check $1
    end_section 0

    start_section "LINTING BANDIT"
    bandit $1
    end_section 0
}


# SEARCH ALL PY FILES
# ===================================================

DIFF_FILES=$(git diff --name-only --diff-filter=d --staged | grep -E '\.py$' | grep -wv 'alembic' | tr '\n' ' ' || true)

# RUN LINTING
# ===================================================
if [[ -z $DIFF_FILES ]]
then
  echo "No files to check"
else
  lint "$DIFF_FILES"
fi

# END
# ===================================================
echo ">>> $(basename ${BASH_SOURCE[0]}) DONE"
