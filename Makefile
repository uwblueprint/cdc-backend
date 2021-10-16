SHELL:=/bin/bash

CONFIG_FILE=secrets/dev-ec2-config.yaml
DOCKER_CONFIG_FILE=secrets/dev-ec2-config.yaml
PYTHON_PATH=.

.PHONY: install
install:
	@echo "Python version: " `python --version`
	@echo " ---- Make sure above version is atleast 3.7.1 or the installation process may fail ----"
	@echo ""
	@echo " ---- Installing requirements... ----"
	@pip install -r requirements.txt
	@pre-commit install
	@echo ""
	@echo " ---- Setting up Postgres (make sure Postgres is running) ----"
	@PYTHONPATH=$(PYTHON_PATH) CONFIG_PATH=$(CONFIG_FILE) python scripts/create-tables.py
	@PYTHONPATH=$(PYTHON_PATH) CONFIG_PATH=$(CONFIG_FILE) python scripts/insert_data.py


.PHONY: docker_install
docker_install:
	@echo "Python version: " `python --version`
	@echo " ---- Make sure above version is atleast 3.7.1 or the installation process may fail ----"
	@echo ""
	@echo " ---- Installing requirements... ----"
	@pip install -r requirements.txt
	@echo ""
	@echo " ---- Setting up Postgres (make sure Postgres is running) ----"
	@PYTHONPATH=$(PYTHON_PATH) CONFIG_PATH=$(DOCKER_CONFIG_FILE) python scripts/create-tables.py
	@PYTHONPATH=$(PYTHON_PATH) CONFIG_PATH=$(DOCKER_CONFIG_FILE) python scripts/insert_data.py
