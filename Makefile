PYTHON_PROJECT := pycncnettunnel

lint:
	pylint -j 0 $(PYTHON_PROJECT)

all: lint

format:
	black $(PYTHON_PROJECT)

check:
	python -m unittest

devinstall:
	pip install -e .

.PHONY: format check lint
