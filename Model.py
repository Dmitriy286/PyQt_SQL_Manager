import json
from datetime import datetime

import sqlalchemy
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import select
from sqlalchemy.orm import Session
from mimesis import Person

ENGINE = create_engine("postgresql+psycopg2://root:pass@localhost/mydb", echo=True, future=True)
CONNECT_SESSION = Session(ENGINE)
MODEL = declarative_base(name='Model')

# Model.query = db_session.query_property() - ?????


# def init_db():
#     Model.metadata.create_all(bind=engine)


# query from a class
results = session.query(User).filter_by(name='ed').all()

# query with multiple classes, returns tuples
results = session.query(User, Address).join('addresses').filter_by(name='ed').all()

# query using orm-columns, also returns tuples
results = session.query(User.name, User.fullname).all()



def openDB(self):
    """
    Opens database connection
    :return:
    """


def create_employee():
    person = Person('ru')

    return {'name': person.first_name(),
            'surename': person.surname(),
            'login': '@' + person.username(mask='l_l'),
            'password': person.password(),
            'email': person.email(),
            'phone': person.telephone(),
            'register_time': datetime.now()}


def add_employee():
    employee = Employee(**create_employee())
    CONNECT_SESSION.begin()
    try:
        CONNECT_SESSION.add(employee)
    except:
        CONNECT_SESSION.rollback()
        raise
    else:
        CONNECT_SESSION.commit()

    return employee.to_dict()

# def delete(user_id):
#
#     session.delete(session.query(User).filter_by(id=user_id).all())
#     session.delete(obj2)
#
#     # commit (or flush)
#     session.commit()


def find_employee_by_name(self):

    stmt = select(Employee).where(Employee.name.in_(["spongebob"]))

    for emp in CONNECT_SESSION.scalars(stmt):
        print(emp)

def show_all_employees():
    return [x.to_dict() for x in User.query.all()]


class Employee(MODEL):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
        )

    id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String(200))
    surname = Column('surename', String(200))
    login = Column('login', String(200))
    password = Column('password', String(200))
    email = Column('email', String(200))
    phone = Column('phone', String(200))
    register_time = Column('register_time', DateTime())

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

    def __init__(self, **params):
        self.name = params.get("name")
        self.surname = params.get("surename")
        self.login = params.get("login")
        self.password = params.get("password")
        self.email = params.get("email")
        self.phone = params.get("phone")
        self.register_time = params.get("register_time")

    def to_dict(self):
        return dict(name=self.name, surname=self.surname, login=self.login,
                    password=self.password, email=self.email, phone=self.phone,
                    register_time=self.register_time)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True, default=str)


class Product(MODEL):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class ProductSubType(MODEL):
    __tablename__ = "productsubtype"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

init_db()
openDB()