GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}

.PHONY: help clean test clean-build isort run

.DEFAULT: help

help:
	@echo "make clean:"
	@echo "       Removes all pyc, pyo and __pycache__"
	@echo ""
	@echo "make setup"
	@echo "       Install prod dependencies"
	@echo "       Needs virtualenv activated and git initalized"
	@echo ""
	@echo "make isort:"
	@echo "       Run isort command cli in development features"
	@echo ""
	@echo "make lint:"
	@echo "       Run lint"
	@echo ""
	@echo "make test:"
	@echo "       Run tests with coverage, lint, and clean commands"
	@echo ""
	@echo "make release:"
	@echo "       Creates a new tag and set the version in this package"
	@echo "       Ex: make release v=1.0.0"
	@echo ""

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . | grep -E "__pycache__|.pytest_cache|.DS_Store$$" | xargs rm -rf

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean: clean-build clean-pyc clean-test

clone-dotenv:
	@echo "---- Clone dotenv ----"
	@cp .env-example .env
	@echo "---- Finish clone ----"

setup:
	@echo "---- Installing Python dependencies ----"
	@pip install -r requirements/base.txt --upgrade

setup_dev: clone-dotenv
	@echo "---- Installing Python dev dependencies ----"
	@pip install -r requirements/dev.txt --upgrade
	@flake8 --install-hook git
	@git config --bool flake8.strict true

coverage:
	@echo "---- Create coverage ----"
	@pytest --verbose --cov=hub_cep	--color=yes --cov-report html --cov-report xml:cov.xml tests/
	@coverage html -d htmlcov
	@coverage-badge > static/coverage.svg

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint: clean
	flake8

test:
	@pytest --verbose --cov=hub_cep	--color=yes  tests/

test-all:
	tox

release:
	@echo "creating a new release ${v}"
	@echo "version = '${v}'" > `pwd`/__version__.py
	@git add `pwd`/__version__.py
	@git add `pwd`/static/coverage.svg
	@git commit -m '${v}'
	@git tag ${v}
	@git push origin ${v}
	@git push --set-upstream origin "${GIT_CURRENT_BRANCH}"
	@git push origin

deploy: clean
	@python setup.py sdist bdist_wheel
	@twine upload dist/*

