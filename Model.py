import json
import psycopg2

from sqlalchemy import create_engine, MetaData, UniqueConstraint
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import select
from datetime import datetime

ENGINE = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/postgres", echo=True, future=True)
CONNECT_SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=ENGINE))
MODEL = declarative_base(name='Model')
MODEL.query = CONNECT_SESSION.query_property()


class Employee(MODEL):
    __tablename__ = "PyQt.employees"
# postgres.public.employees
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(200))
    password = Column('password', String(200))
    username = Column('username', String(200))
    orders = relationship("Order")
    # orders = relationship("Order", backref="employee")

    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('password')
    )

    # addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    # register_time = Column('register_time', DateTime())

    def __init__(self, **params):
        self.id = params.get('id')
        self.name = params.get('name')
        self.password = params.get('password')
        self.username = params.get('username')
        self.orders = params.get('orders')

    def __repr__(self):
        return f"Employee(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name, password=self.password,
                    username=self.username, orders=self.orders)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)


class Customer(MODEL):
    __tablename__ = "PyQt.customers"

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(200))
    name = Column('name', String(200))
    username = Column('username', String(200))
    password = Column('password', String(200))
    phonenumber = Column('phonenumber', String(200))
    # reg_date = Column('reg_date', datetime)
    orders = relationship("Order")
    # orders = relationship("Order", backref="employee")

    __table_args__ = (
        UniqueConstraint('username'),
        UniqueConstraint('password'),
        UniqueConstraint('email'),
    )

    def __init__(self, **params):
        self.id = params.get('id')
        self.email = params.get('email')
        self.name = params.get('name')
        self.username = params.get('username')
        self.password = params.get('password')
        self.phonenumber = params.get('phonenumber')
        # self.reg_date = params.get('reg_date')

    def __repr__(self):
        return f"Employee(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def to_dict(self):
        return dict(id=self.id, email=self.email, name=self.name, username=self.username,
                    password=self.password, phonenumber=self.phonenumber)
                    # reg_date=self.reg_date)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)


class Order(MODEL):
    __tablename__ = 'PyQt.orders'
    id = Column(Integer(), primary_key=True)
    # date = Column(datetime, default=datetime.now)

    employee_id = Column(Integer, ForeignKey('PyQt.employees.id'))
    employee = relationship("Employee")

    customer_id = Column(Integer(), ForeignKey('PyQt.customers.id'))
    customer = relationship("Customer")

    # todo:
    # order_detail = relationship('OrderDetails', backref='order', uselist=False)

def init_db():
    MODEL.metadata.create_all(bind=ENGINE)

def del_db():
    MODEL.metadata.drop_all(bind=ENGINE)

def openDB():
    """
    Opens database connection
    :return:
    """
    ...

def commit_session():
    CONNECT_SESSION.commit()