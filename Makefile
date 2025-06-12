.PHONY: up test lint format help

up:
	docker-compose up --build

test:
	poetry run pytest --cov=app tests/

lint:
	poetry run flake8 app tests

format:
	poetry run black app tests

help:
	@echo "make up      # Dockerで開発環境を起動"
	@echo "make test    # テストを実行"
	@echo "make lint    # コードの静的チェック"
	@echo "make format  # コード整形"