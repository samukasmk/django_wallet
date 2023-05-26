SHELL = /bin/bash
.DEFAULT_GOAL = none

### help actions
help:
	@echo 'Usage:                                                                                              '
	@echo '                                                                                                    '
	@echo '    make install           Install python packages (with pip, from requirements.txt)                '
	@echo '    make install-dev       Install python packages (with pip, from requirements-dev.txt)            '
	@echo '    make test              Run unit tests with pytest                                               '
	@echo '    make coverage          Run unit tests with coverage statistics with pytest                      '


### actions to clean project files
clean: clean-cache

clean-cache:
	sudo rm -fr db-unit-tests.sqlite3;
	sudo rm -fr htmlcov;
	sudo rm -fr .cache;
	sudo rm -fr .coverage;
	sudo rm -fr .pytest_cache;
	sudo rm -fr junit.xml coverage.xml;
	sudo find . -iname '*.pyc' -delete;
	sudo find . -iname '*.pyo' -delete;
	sudo find . -name '*,cover' -delete;
	sudo find . -iname __pycache__ -delete;


### actions to install env
install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements-dev.txt


### actions to build new envs
collect-static-files:
	mkdir -p /opt/belvo_files/{static,media} \
		&& ./manage.py collectstatic --no-input --clear

apply-db-migrations:
	./manage.py migrate --noinput

build-environment:
	make collect-static-files && make apply-db-migrations

### actions to test
lint:
	pylama .

test: clean-cache
	pytest .

coverage-xml: clean-cache
	pytest --junit-xml=junit.xml .



