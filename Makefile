include .env
export

# use .env.testing for the test target in MAKECMDGOALS (The targets given to make on the command line)
ifneq ($(filter test,$(MAKECMDGOALS)),)
include .env.testing
export $(shell sed 's/=.*//' .env.testing)
endif

# Targets
setup:
	./scripts/setup.sh

test:
	./scripts/test.sh

lint:
	./scripts/lint.sh

start:
	./scripts/start.sh