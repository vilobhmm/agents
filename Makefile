.PHONY: install test format lint clean help

help:
	@echo "OpenClaw Makefile Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make format     - Format code with black"
	@echo "  make lint       - Run linters"
	@echo "  make clean      - Clean build artifacts"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest --cov=openclaw --cov-report=html tests/

format:
	black openclaw/ projects/ examples/
	isort openclaw/ projects/ examples/

lint:
	flake8 openclaw/ projects/ examples/
	mypy openclaw/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run-example-simple:
	python examples/simple_agent.py

run-example-multi:
	python examples/multi_agent.py

run-example-proactive:
	python examples/proactive_agent.py
