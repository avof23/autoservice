import datetime
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from faker.providers import DynamicProvider
from fastapi.testclient import TestClient

from src.db import Base, Masters, Clients, Statuses, Parts, Works, Orders
from app.routers import clients


def db_engine(file=False):
    DATABASE_URL = "sqlite:///:memory:"
    if file:
        DATABASE_URL = "sqlite:///test.db"
    loc_engine = create_engine(DATABASE_URL)
    return loc_engine


@pytest.fixture()
def db_session():
    engine = db_engine()
    Base.metadata.create_all(bind=engine)
    sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    yield sessionlocal()


@pytest.fixture()
def db_session_file():
    engine = db_engine(file=True)
    Base.metadata.create_all(bind=engine)
    sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    yield sessionlocal()
    engine.dispose()
    os.remove("test.db")


@pytest.fixture(autouse=True)
def create_test_data(db_session):
    fake = Faker()
    cur_data = datetime.date.today()

    masters_professions_provider = DynamicProvider(
        provider_name="masters_profession",
        elements=["gen", "el"],
    )
    fake.add_provider(masters_professions_provider)
    masters = [
            Masters(id=i,
                    master_name=fake.name(),
                    qualification=fake.masters_profession()
                    ) for i in range(1, 7)
    ]
    clients = [
            Clients(id=i,
                    name=fake.name(),
                    phone=fake.msisdn(),
                    email=fake.ascii_free_email(),
                    description='fake client for test'
                    ) for i in range(1, 11)
    ]
    statuses = [
        Statuses(id=1, status='create'),
        Statuses(id=2, status='create_push'),
        Statuses(id=3, status='inwork'),
        Statuses(id=4, status='ready')
    ]
    my_part_list = [
        'Filter', 'Oil', 'Brake',
        'gear', 'AirFilter', 'Clutch',
        'pumps', 'engine', 'cross member',
        'culinder', 'lamp', 'pipe', 'clips']

    my_work_list = [
        'replace', 'repair', 'restore',
        'change', 'diagnostic']

    parts = [
            Parts(id=i,
                  part_name=fake.sentence(ext_word_list=my_part_list, nb_words=2),
                  part_number=f'AS-{fake.pyint(min_value=0, max_value=9999, step=1)}',
                  price=fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=100, max_value=2500)
                  ) for i in range(1, 51)
        ]
    works = [
            Works(id=i,
                  work_name=fake.sentence(ext_word_list=my_work_list, nb_words=1),
                  price=fake.pyfloat(left_digits=4, right_digits=1, positive=True, min_value=100, max_value=1000),
                  norm_min=60,
                  for_selection=False,
                  requirements=fake.masters_profession()
                  ) for i in range(1, 11)
        ]
    orders = [
            Orders(id=i,
                   status_id=1,
                   start_date=datetime.datetime(cur_data.year, cur_data.month, cur_data.day, hour=i+9),
                   end_date=datetime.datetime(cur_data.year, cur_data.month, cur_data.day, hour=i+9+1),
                   credit_summ=fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=300, max_value=1500)*(-1),
                   order_summ=fake.pyfloat(left_digits=4, right_digits=2, positive=False, min_value=300, max_value=1500),
                   client_id=fake.pyint(min_value=1, max_value=10, step=1),
                   master_id=i
                   ) for i in range(1, 4)
    ]

    db_session.add_all(masters)
    db_session.add_all(clients)
    db_session.add_all(statuses)
    db_session.add_all(parts)
    db_session.add_all(works)
    db_session.add_all(orders)
    db_session.commit()


@pytest.fixture()
def app_test(db_session_file):
    from app.main import app
    clients.engine = db_session_file.bind
    yield TestClient(app)


def test_read_main(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API AutoService"}
