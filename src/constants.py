from json import load as jsload

LANG = 'en'
VALUT = 'UAH'
NEW_STATUS_ID = 1
WEEKEND_DAYS = [0, 6]
WORK_TIME = range(9, 18)  # with last hour


with open('../data/text_templates.json', 'r') as file:
    template = jsload(file)
