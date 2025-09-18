.PHONY: up test lint help

up:
	docker compose up --build

test:
	docker compose run --rm app poetry run pytest --cov=app tests/

lint:
	docker compose exec app bash scripts/run_lint.sh

help:
	@echo "make up      # Dockerで開発環境を起動"
	@echo "make test    # テストを実行"
	@echo "make lint    # コードチェックを実行"