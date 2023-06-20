SHELL = /bin/bash
.DEFAULT_GOAL = none

### help actions
help:
	@echo 'Basic usage:                                                                                       '
	@echo '    make install                Install python packages (with pip, from requirements.txt)          '
	@echo '    make install-dev            Install python packages (with pip, from requirements-dev.txt)      '
	@echo '    make clean                  Clean unused files generated from python executions                '
	@echo '    make test                   Run unit tests with pytest                                         '
	@echo '    make linter                 Run just linters checks like pyflakes and pytest                   '
	@echo '    make collect-static-files   Collect static files from Django like (./manage.py collectstatic)  '
	@echo '    make apply-db-migrations    Execute Django migrations on database like: (./manage.py runserver)'

### actions to clean project files
clean-cache-files:
	sudo rm -fr .cache;
	sudo find . -iname '*.pyc' -delete;
	sudo find . -iname '*.pyo' -delete;
	sudo find . -name '*,cover' -delete;
	sudo find . -iname __pycache__ -delete;

clean-pytest-files: clean-cache-files
	sudo rm -fr .coverage;
	sudo rm -fr .pytest_cache;
	sudo rm -fr db-unit-tests.sqlite3;

clean-coverage-files:
	sudo rm -fr htmlcov;
	sudo rm -fr junit.xml coverage.xml;

clean: clean-cache-files clean-pytest-files clean-coverage-files

### actions to install env
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

### alias for docker build
install-production: install

install-development: install-dev

### actions to build new envs
collect-static-files:
	mkdir -p /opt/django_files/{static,media} \
		&& ./manage.py collectstatic --no-input --clear

apply-db-migrations:
	./manage.py migrate --noinput

build-environment:
	make collect-static-files \
	    && make apply-db-migrations

### actions to test
lint: clean
	pylama .;
	make clean-pytest-files;

test: clean
	pytest --cov=apps --cov-config=.coveragerc --cov-report term:skip-covered --cov-report html:htmlcov --junit-xml=coverage.xml;
	make clean-pytest-files;
	sudo chmod 777 ./coverage.xml;
	sudo chmod -R 777 ./htmlcov;