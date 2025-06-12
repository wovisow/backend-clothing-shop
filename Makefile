MODULE=src.main:app
APP_HOST=127.0.0.1
APP_PORT=8000
ALEMBIC = alembic -c src/external/database/alembic.ini

linter:
	ruff format . && ruff check . --fix

app:
	uvicorn $(MODULE) --reload --host $(APP_HOST) --port $(APP_PORT)

local:
	docker compose up -d

migrate:
	$(ALEMBIC) upgrade head

revision:
	$(ALEMBIC) revision --autogenerate

downgrade:
	$(ALEMBIC) downgrade -1