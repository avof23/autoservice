from app.routers.orders import order_summ_calculate
from src import pushed
from tests import db_session, create_test_data


def test_calculation():
    assert order_summ_calculate(500, -500, 1000) == -1000
    assert order_summ_calculate(500, -200, 1000) == -700
    assert order_summ_calculate(1264, 0, 560) == 704
    assert order_summ_calculate(430, 0, 760.5) == -330.5
    assert order_summ_calculate(1340, -500, 1000) == -160
    assert order_summ_calculate(1500, -1500, 800) == -800
    assert order_summ_calculate(300, -100, 1050) == -850
    assert order_summ_calculate(300, -100, 300) == -100


def test_get_recipients(db_session):
    pushed.engine = db_session.bind
    for i in range(1, 5):
        if i == 1:
            assert pushed.get_recipients_db(i)[0]['status'] == 'create'
            pushed.set_pushed_db([2, 3])
            continue
        if i == 2:
            assert pushed.get_recipients_db(i)[0]['status'] == 'create_push'
            continue

        assert pushed.get_recipients_db(i) == list()
