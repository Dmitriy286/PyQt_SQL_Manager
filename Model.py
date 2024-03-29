import json
import psycopg2
import sqlalchemy_utils

from sqlalchemy import create_engine, MetaData, UniqueConstraint
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import select
from datetime import datetime
import sqlalchemy_utils

from ModelAbstractClass import MyModel
from PyQtMetaClass import DeclarativeABCMeta

metadata_obj = MetaData(schema="PyQt")
ENGINE = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/postgres", echo=True, future=True)
CONNECT_SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=ENGINE))
MODEL = declarative_base(metadata=metadata_obj, name='MODEL', metaclass=DeclarativeABCMeta)
MODEL.query = CONNECT_SESSION.query_property()


class Employee(MODEL, MyModel):
    """
    to_json method is not an abstract, is not implemented in current class
    """
    __tablename__ = "employees"
    # __table_args__ = {"schema": "PyQt"}
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

    def __init__(self, **params):
        super().__init__()
        self.id = params.get('id')
        self.name = params.get('name')
        self.password = params.get('password')
        self.username = params.get('username')
        self.orders = []

    def __repr__(self):
        return f"Employee(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    # def __dir__(self):
    #     return list(self.to_dict().keys())

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name, password=self.password,
                    username=self.username, orders=self.orders)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

    def get_fields(self):
        # entity_list = sqlalchemy_utils.functions.get_tables()
        return [i for i in self.to_dict().keys()]


        # entity_list = metadata_obj.tables
        # print(entity_list)
        #
        # entity = globals()["Employee"]
        # print(entity.__dict__['__module__'])
        # print(dir(entity))
        # variables = [i for i in entity.__dict__.keys() if not callable(i)]
        # print(variables)
        # variables_2 = entity.__dict__.keys()
        # print(variables_2)
        # field_list = sqlalchemy_utils.functions.get_columns(entity)
        # print(field_list)


class Customer(MODEL, MyModel):
    __tablename__ = "customers"
    # __table_args__ = {"schema": "PyQt"}

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
        super().__init__()
        self.id = params.get('id')
        self.email = params.get('email')
        self.name = params.get('name')
        self.username = params.get('username')
        self.password = params.get('password')
        self.phonenumber = params.get('phonenumber')
        self.orders = []
        # self.reg_date = params.get('reg_date')

    def __repr__(self):
        return f"Employee(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def to_dict(self):
        return dict(id=self.id, email=self.email, name=self.name, username=self.username,
                    password=self.password, phonenumber=self.phonenumber, orders = self.orders)
                    # reg_date=self.reg_date)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

    def get_fields(self):
        return [i for i in self.to_dict().keys()]


class Order(MODEL, MyModel):
    __tablename__ = 'orders'
    # __table_args__ = {"schema": "PyQt"}

    id = Column(Integer, primary_key=True)
    # date = Column(datetime, default=datetime.now)
    # register_time = Column('register_time', DateTime())
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee")

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer")

    # todo:
    # order_detail = relationship('OrderDetails', backref='order', uselist=False)

    def __init__(self, **params):
        super().__init__()
        self.id = params.get('id')
        # self.date = params.get('date')
        # self.employee_id = params.get('employee_id')
        # self.customer_id = params.get('customer_id')

        self.employee_id = 0
        self.customer_id = 0

    def set_employee_id(self, employee_id: int) -> None:
        self.employee_id = employee_id

    def set_customer_id(self, customer_id: int) -> None:
        self.customer_id = customer_id

    def __repr__(self):
        return f"Order(id={self.id!r}, " \
               # f"date={self.date!r}"

    def to_dict(self):
        return dict(id=self.id,
                    # date=self.date,
                    employee_id=self.employee_id,
                    customer_id=self.customer_id)
                    # reg_date=self.reg_date)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)

    def get_fields(self):
        return [i for i in self.to_dict().keys()]


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

def get_type(attribute_name):
    return get_type(attribute_name)


# def get_entities():
#     # entity_list = sqlalchemy_utils.functions.get_tables()
#     entity_list = metadata_obj.tables
#     print(entity_list)
#
#     entity = globals()["Employee"]
#     print(entity.__dict__['__module__'])
#     print(dir(entity))
#     variables = [i for i in entity.__dict__.keys() if not callable(i)]
#     print(variables)
#     variables_2 = entity.__dict__.keys()
#     print(variables_2)
#     field_list = sqlalchemy_utils.functions.get_columns(entity)
#     print(field_list)
