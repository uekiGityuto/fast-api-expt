.PHONY: dev pipfreeze history revision upgrade downgrade

dev:
	@echo "Starting development server..."
	@uvicorn app.main:app --reload --log-config app/logging_config.json --no-access-log --no-use-colors
pipfreeze:
	@echo "Freezing pip dependencies..."
	@pip freeze > requirements.txt

history:
	@alembic history

revision:
	@echo "Creating migration file..."
	@alembic revision --autogenerate -m "$(m)"

upgrade:
	@if [ -n "$(v)" ]; then \
		alembic upgrade $(v); \
	else \
		alembic upgrade head; \
	fi

# 初期状態に戻すためは、`make downgrade v=base` とする
# 一つ前のバージョンに戻したい場合には、`make downgrade v=-1` とする
downgrade:
	@alembic downgrade $(v)

help:
	@echo "Available targets:"
	@echo "  dev            : Start the development server."
	@echo "  pipfreeze      : Freeze pip dependencies."
	@echo "  history        : Show the migration history."
	@echo "  revision m=<message>  : Create a new migration file with the specified message."
	@echo "  upgrade v=<version>   : Upgrade the database to the specified version (default: head)."
	@echo "  downgrade v=<version> : Downgrade the database to the specified version."
