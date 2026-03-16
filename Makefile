#!/usr/bin/env sh

COMPOSE_EXEC ?= docker-compose exec
EXEC_PYTHON ?= $(COMPOSE_EXEC) python
EXEC_NODE ?= $(COMPOSE_EXEC) node

bash/node:
	$(EXEC_NODE) sh

bash/python:
	$(EXEC_PYTHON) sh

pipenv/install:
	$(EXEC_PYTHON) sh -c "cd /application/function/documentProducer/ && pipenv install --sequential"
	$(EXEC_PYTHON) sh -c "cd /application/function/documentConsumer/ && pipenv install"
	#$(EXEC_PYTHON) sh -c "cd /application/function/parseSpreadsheet/ && pipenv install"

deploy/functions/python:
	$(EXEC_NODE) sh -c "sls deploy && sls s3deploy"

remove/functions/python:
	$(EXEC_NODE) sh -c "sls remove"
	$(EXEC_NODE) sh -c "sls s3eventremove"

init:
	$(MAKE) pipenv/install