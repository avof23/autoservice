
check:
		pylint src app --recursive=y --ignore-paths=./alembic/*,./tests/*
format:
		black .
		isort .
req:
		pip freeze > requirements.txt
prepare:
		pip install -r requirements.txt
test:
		coverage run -m pytest
run:
		python src/mainbot.py
api:
		uvicorn app.main:app --reload
