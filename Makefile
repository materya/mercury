#!make

export DOCKER_BUILDKIT = 1
export COMPOSE_DOCKER_CLI_BUILD = 1

# Command Variables
D = docker
DC = docker-compose
DCFLAGS = --rm dev
PYTHON = python

build_dir = build
dist_dir = dist
name = `$(PYTHON) setup.py --name`

artifacts = \
	.coverage \
	.mypy_cache \
	.pytest_cache \
	src/*.egg-info

all: install
.PHONY: all

clean: distclean
	@rm -rf $(artifacts)
	@find . -depth -name '__pycache__' -exec rm -rv {} \;
	@$(PYTHON) setup.py clean
.PHONY: clean

container:
	@$(DC) build
.PHONY: container

dist:
	@$(PYTHON) setup.py sdist bdist_wheel

distclean:
	@rm -rf $(build_dir) $(dist_dir)
.PHONY: distclean

install: dist
	@$(PYTHON) setup.py install
.PHONY: install

install-dev:
	@$(PYTHON) -m pip install -e .[dev,doc,extras,test]
.PHONY: install-dev

lint:
	@$(PYTHON) -m flake8 src
.PHONY: lint

test:
	@$(PYTHON) -m pytest
.PHONY: test

test-clean:
	@$(PYTHON) -m pytest --cache-clear
.PHONY: test-clean

typecheck:
	@echo "type checking is broken atm, skipping."
	@#$(PYTHON) -m mypy src
.PHONY: typecheck

upload: upload-check
	@$(PYTHON) -m twine upload $(dist_dir)/*
.PHONY: upload

upload-check: dist
	@$(PYTHON) -m twine check $(dist_dir)/*
.PHONY: upload-check

upload-test: upload-check
	@$(PYTHON) -m twine upload --repository testpypi $(dist_dir)/*
.PHONY: upload-test

uninstall:
	@$(PYTHON) -m pip uninstall -y $(name)
.PHONY: uninstall

uninstall-dev:
	@$(PYTHON) setup.py develop -u
.PHONY: uninstall-dev
