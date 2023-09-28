from json import load as jsload
from pathlib import Path

LANG = 'en'
VALUT = 'UAH'
NEW_STATUS_ID = 1
WEEKEND_DAYS = [0, 6]
WORK_TIME = range(9, 18)  # with last hour

myself = Path(__file__).resolve()
with open(f'{myself.parents[1]}/data/text_templates.json', 'r') as file:
    template = jsload(file)
