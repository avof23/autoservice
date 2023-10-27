
check:
		pylint src --recursive=y --ignore qtest.py,core_db2.py
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
