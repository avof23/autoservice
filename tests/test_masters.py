import datetime

import pytest

from tests import db_session, create_test_data
from src import datecalc

id_hours = [(i, i+9, False) for i in range(1, 4)]
id_hours.extend([(i, i+12, True) for i in range(1, 4)])


@pytest.mark.parametrize("i, h, result", id_hours)
def test_free_master_in_date(db_session, i, h, result):
    datecalc.engine = db_session.bind
    cur_data = datetime.date.today()

    assert datecalc.check_free_master_in_date(i, datetime.datetime(
        cur_data.year,
        cur_data.month,
        cur_data.day,
        hour=h)
                                              ) == result


@pytest.mark.parametrize("qu", ['gen', 'el'])
def test_get_masters_db(db_session, qu):
    datecalc.engine = db_session.bind

    assert len(datecalc.get_masters_db(qu)) >= 1
    assert len(datecalc.get_statistic_masters_db(qu)) >= 1
