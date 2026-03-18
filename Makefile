VENV = .venv
PYTHON = $(VENV)/bin/python
RUFF = $(VENV)/bin/ruff
MYPY = $(VENV)/bin/mypy
PYTEST = $(VENV)/bin/pytest

.PHONY: lint fix lint-file format typecheck test check up down

lint:
	$(RUFF) check .

fix:
	$(RUFF) check --fix .

lint-file:
	$(RUFF) check $(FILE)

format:
	$(RUFF) format .

typecheck:
	$(MYPY) src/ app/

test:
	$(PYTEST) tests/ -v

check: lint typecheck test

up:
	docker-compose up --build

down:
	docker-compose down
