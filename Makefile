
check:
		pylint src app --recursive=y --ignore-paths=./alembic/*,./tests/*,./sql/*
format:
		black .
		isort .
req:
		pip freeze > requirements.txt
prepare:
		pip install -r requirements.txt
test:
		export PYTHONPATH=~/PycharmProjects/AutoService/src:/home/runner/work/autoservice/autoservice/src && coverage run -m pytest
run:
		python src/mainbot.py
api:
		uvicorn app.main:app --reload
