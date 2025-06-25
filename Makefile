.PHONY: test lint format clean install install-dev autofix

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=seek_core --cov-report=term-missing --cov-report=html

lint:
	@echo "Running flake8..."
	-flake8 seek_core tests || echo "⚠️  Flake8 issues found (non-blocking)"
	@echo "Running black..."
	-black --check seek_core tests || echo "⚠️  Black formatting issues found (non-blocking)"
	@echo "Running isort..."
	-isort --check seek_core tests || echo "⚠️  Import sorting issues found (non-blocking)"
	@echo "Running mypy..."
	-mypy seek_core || echo "⚠️  Type checking issues found (non-blocking)"
	@echo "Linting completed with warnings"

format:
	black seek_core tests
	isort seek_core tests

autofix:
	python scripts/autofix_lint.py

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
