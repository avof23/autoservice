"""This module describes the database structure using sqlalchemy ORM. Classes are used"""
import os

from sqlalchemy import Column, Integer, BigInteger, Numeric, \
    String, Text, DateTime, Boolean, ForeignKey, Index, func, text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv('DB_HOSTNAME')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_passwd = os.getenv('DB_PASSWD')


engine = create_engine(
    f'postgresql+psycopg2://{db_user}:{db_passwd}@{db_host}/{db_name}'
)
Base = declarative_base()


class BaseModel(Base):
    """Parent class on Base class"""
    __abstract__ = True


class Masters(BaseModel):
    """The class describes the database table and relationship"""
    __tablename__ = 'masters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    master_name = Column(String(30), nullable=False)
    qualification = Column(String(15), server_default=text("'gen'"))

    order = relationship('Orders', back_populates='master', lazy='joined')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.id} {self.master_name}'


class Statuses(BaseModel):
    """The class describes the database table and relationship"""
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(15), nullable=False)

    order = relationship('Orders', back_populates='status', lazy='joined')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.id} {self.status}'


class Orders(BaseModel):
    """The class describes the database table and relationship"""
    __tablename__ = 'orders'
    __tableargs__ = {'comment': 'Stores orders data'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False)
    start_date = Column(DateTime, server_default=func.CURRENT_TIMESTAMP())
    end_date = Column(DateTime)
    credit_summ = Column(Numeric(8, 2), server_default=text('0'))
    order_summ = Column(Numeric(8, 2), server_default=text('0'))
    client_id = Column(BigInteger, ForeignKey('clients.id'))
    master_id = Column(BigInteger, ForeignKey('masters.id'))
    description = Column(Text)

    master = relationship('Masters', back_populates='order', lazy='joined')
    status = relationship('Statuses', back_populates='order', lazy='joined')
    client = relationship('Clients', back_populates='order', lazy='joined')
    content_orders = relationship('ContentOrders', back_populates='order', lazy='joined')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.id} {self.start_date} {self.order_summ} {self.description}'


class Clients(BaseModel):
    """The class describes the database table and relationship, indexes"""
    __tablename__ = 'clients'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='chat_id')
    name = Column(String(30))
    phone = Column(String(15))
    email = Column(String(30))
    auto = Column(String(30))
    number = Column(String(10), nullable=True, unique=True)
    description = Column(Text)

    __table_args__ = (Index('idx_id_number', 'id', 'number'), {'comment': 'Stores clients data'})
    order = relationship('Orders', back_populates='client', lazy='joined')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.id} {self.name} {self.phone} Auto: {self.auto} {self.number}'


class Works(BaseModel):
    """The class describes the database table and relationship"""
    __tablename__ = 'works'
    __tableargs__ = {'comment': 'Stores autoservice work data'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    work_name = Column(String(200), nullable=False)
    price = Column(Numeric(8, 2), server_default=text('0'))
    norm_min = Column(Integer, server_default=text('60'))
    for_selection = Column(Boolean, server_default='f')
    requirements = Column(String(5), server_default=text("'gen'"))
    description = Column(Text)

    order = relationship('ContentOrders', back_populates='work')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.id} {self.work_name} {self.price} NM:{self.norm_min}'


class Parts(BaseModel):
    """The class describes the database table and relationship"""
    __tablename__ = 'parts'
    __tableargs__ = {'comment': 'Stores auto parts data'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    part_name = Column(String(200), nullable=False)
    part_number = Column(String(15))
    original_number = Column(String(15))
    price = Column(Numeric(8, 2), server_default=text('0'))
    compatibility = Column(String(150))
    description = Column(Text)

    order = relationship('ContentOrders', back_populates='part')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.id} {self.part_name} {self.part_number} {self.price}'


class ContentOrders(BaseModel):
    """The class describes the database table and relationship"""
    __tablename__ = 'content_orders'
    __tableargs__ = {'comment': 'Stores item of orders'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    work_id = Column(BigInteger, ForeignKey('works.id'))
    part_id = Column(BigInteger, ForeignKey('parts.id'))
    quantity = Column(Integer, server_default=text('1'))

    work = relationship('Works', back_populates='order', lazy='joined')
    part = relationship('Parts', back_populates='order', lazy='joined')
    order = relationship('Orders', back_populates='content_orders', lazy='joined')

    def __repr__(self):
        """The method returns a information string of object"""
        return f'{self.order_id} {self.work_id}/{self.part_id} {self.quantity}'


def init_db():
    Base.metadata.create_all(engine)
