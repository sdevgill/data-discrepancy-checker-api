install:
	poetry install --no-root

dev:
	poetry run fastapi dev src/main.py

test:
	PYTHONPATH=src poetry run pytest src

.PHONY: install dev test
