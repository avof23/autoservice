from json import load as jsload
from pathlib import Path

LANG = 'en'
VALUT = 'UAH'
NEW_STATUS_ID = 1
READY_STATUS_ID = 5
WAIT_STATUS_ID = 4
WEEKEND_DAYS = [0, 6]
WORK_TIME = range(9, 18)  # with last hour
INTERVAL_PUSH_PLANNED = 3600
INTERVAL_PUSH_COMPLETE = 300

HOME_PROJECT = Path(__file__).resolve()
with open(f'{HOME_PROJECT.parents[1]}/data/text_templates.json', 'r') as file:
    template = jsload(file)
