.PHONY: test lint format clean install install-dev

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=seek_core --cov-report=term-missing --cov-report=html

lint:
	flake8 seek_core tests
	black --check seek_core tests
	isort --check seek_core tests
	mypy seek_core

format:
	black seek_core tests
	isort seek_core tests

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .coverage

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
