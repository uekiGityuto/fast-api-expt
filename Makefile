.PHONY: dev pipfreeze

dev:
	@echo "Starting development server..."
	@uvicorn app.main:app --reload
pipfreeze:
	@echo "Freezing pip dependencies..."
	@pip freeze > requirements.txt
