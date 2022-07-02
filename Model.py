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

def openDB(self):
    """
    Opens database connection
    :return:
    """

# def delete(user_id):
#
#     session.delete(session.query(User).filter_by(id=user_id).all())
#     session.delete(obj2)
#
#     # commit (or flush)
#     session.commit()

class Employee(MODEL):
    __tablename__ = "employee"

    id = Column('id', Integer, primary_key=True)
    active = Column('active', bool)
    email = Column('email', String(200))
    name = Column('name', String(200))
    password = Column('password', String(200))
    phonenumber = Column('phonenumber', String(200))
    photo = Column('phone', String(200))
    username = Column('username', String(200))
    filename = Column('filename', String(200))

    # addresses = relationship(
    #     "Address", back_populates="user", cascade="all, delete-orphan"
    #     )

    # register_time = Column('register_time', DateTime())

    def __repr__(self):
        return f"Employee(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def __init__(self, **params):
        self.id = params.get('id')
        self.active = params.get('active')
        self.email = params.get('email')
        self.name = params.get('name')
        self.password = params.get('password')
        self.phonenumber = params.get('phonenumber')
        self.photo = params.get('photo')
        self.username = params.get('username')
        self.filename = params.get('filename')

    def to_dict(self):
        return dict(id=self.id, active=self.active, email=self.email,
                    name=self.name, password=self.password, phonenumber=self.phonenumber,
                    photo=self.photo, username=self.username, filename=self.filename)

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




# init_db()
# openDB()