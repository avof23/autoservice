
check:
		pylint src --recursive=y --ignore qtest.py,core_db2.py
format:
		black .
		isort .
req:
		pip freeze > requirements.txt
test:
		coverage run -m pytest
run:
        python mainbot.py