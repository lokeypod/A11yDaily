.PHONY: dev build down api-test web-lint api-lint format

dev:
	docker compose up --build

build:
	docker compose build

down:
	docker compose down

api-test:
	docker compose run --rm api pytest

web-lint:
	docker compose run --rm web npm run lint

api-lint:
	docker compose run --rm api ruff check .

format:
	docker compose run --rm api black .
	docker compose run --rm api ruff check . --fix
	docker compose run --rm web npm run lint
