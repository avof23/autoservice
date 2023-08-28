
check:
		pylint src --recursive=y
format:
		black .
		isort .
req:
		pip freeze > requirements.txt
test:
		coverage run -m pytest