#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"

set -o errexit # exit script when command fails
set -o pipefail # this setting prevents errors in a pipeline from being masked
set -o nounset # exit script when it tries to use undeclared variables



# INIT WORKING DIR
# ======================================================================================================
cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../..
CWD="$(pwd)"



# INSTALL PACKAGES
# ===================================================

if [ -x "$(command -v pip)" ]; then
  pip install -r requirements-dev.txt
elif [ -x "$(command -v pip3)" ]; then
  pip3 install -r requirements-dev.txt
else
  echo "No pip installed. Aborting"
  exit 1
fi



# INSTALL GIT-HOOKS
# ===================================================

echo ">>> copying git hooks"

# pre-commit
cd "${CWD}"
cp -f "${CWD}/scripts/hooks/pre-commit.sh" "${CWD}/.git/hooks/pre-commit"
chmod ug+x "${CWD}/.git/hooks/pre-commit"

# pre-push
cd "${CWD}"
cp -f "${CWD}/scripts/hooks/pre-push.sh" "${CWD}/.git/hooks/pre-push"
chmod ug+x "${CWD}/.git/hooks/pre-push"

echo ">>> git hooks installed"

echo ">>> $(basename ${BASH_SOURCE[0]}) DONE"
