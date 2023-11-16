from tests import db_session, db_session_file, create_test_data, app_test
from src.db import Clients


def test_get_clients(db_session):
    assert db_session.get(Clients, 1).id == 1
    assert db_session.get(Clients, 2).id == 2
    assert db_session.get(Clients, 3).id == 3


def test_api_get_clients(app_test):
    response = app_test.get("/clients/")
    assert response.status_code == 200
