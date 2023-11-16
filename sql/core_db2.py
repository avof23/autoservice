import os
from datetime import datetime

from sqlalchemy import Table, Column, Integer, BigInteger, Numeric, \
    String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv('DB_HOSTNAME')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_passwd = os.getenv('DB_PASSWD')

engine = create_engine(
    f'postgresql+psycopg2://{db_user}:{db_passwd}@{db_host}/{db_name}'
)

metadata_obj = MetaData()

masters = Table(
    'masters',
    metadata_obj,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('master_name', String(30), nullable=False),
    Column('qualification', String(15), default='gen')
)

statuses = Table(
    'statuses',
    metadata_obj,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('status_name', String(15), nullable=False)
)

clients = Table(
    'clients',
    metadata_obj,
    Column('id', BigInteger, primary_key=True, autoincrement=True, comment='chat_id'),
    Column('name', String(30)),
    Column('phone', String(15)),
    Column('email', String(30)),
    Column('auto', String(30)),
    Column('number', String(10), nullable=True, unique=True),
    Column('description', Text),
    Index('idx_id_number', 'id', 'number'),
    comment='Stores clients data'
)

orders = Table(
    'orders',
    metadata_obj,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column("status_id", Integer, ForeignKey(statuses.c.id), nullable=False),
    Column('start_date', DateTime, default=datetime.now()),
    Column('end_date', DateTime),
    Column('credit_summ', Numeric(8, 2), default=0.0),
    Column('order_summ', Numeric(8, 2), default=0.0),
    Column('client_id', BigInteger, ForeignKey(clients.c.id)),
    Column('master_id', BigInteger, ForeignKey(masters.c.id)),
    Column('description', Text),
    comment='Stores orders data'
)

works = Table(
    'works',
    metadata_obj,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('work_name', String(200), nullable=False),
    Column('price', Numeric(8, 2), default=0.0),
    Column('norm_min', Integer, default=60),
    Column('for_selection', Boolean, default=False),
    Column('requirements', String(5), default='gen'),
    Column('description', Text),
    comment='Stores autoservice work data'
)

parts = Table(
    'parts',
    metadata_obj,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('part_name', String(200), nullable=False),
    Column('part_number', String(15)),
    Column('original_number', String(15)),
    Column('price', Numeric(8, 2), default=0.0),
    Column('compatibility', String(150)),
    Column('description', Text),
    comment='Stores auto parts data'
)

content_orders = Table(
    'content_orders',
    metadata_obj,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('order_id', BigInteger, ForeignKey(orders.c.id), nullable=False),
    Column('work_id', BigInteger, ForeignKey(works.c.id)),
    Column('part_id', BigInteger, ForeignKey(parts.c.id)),
    Column('quantity', Integer, default=1),
    comment='Stores item of orders'
)

metadata_obj.create_all(engine)
