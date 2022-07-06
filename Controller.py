import sqlalchemy
import psycopg2

from mimesis import Person
from sqlalchemy import select

from Model import Employee, Customer, Order, CONNECT_SESSION, commit_session


def create_obj(entity: str):
    # person = Person('ru')
    temp_obj = globals()[entity]()
    dict_ = {}
    for field in temp_obj.get_fields()[1:]:
        if isinstance(getattr(temp_obj, field), list):
            dict_[field] = []
        else:
            dict_[field] = ""

    return dict_

def add_obj(entity):
    obj = globals()[entity](**create_obj(entity))
    # CONNECT_SESSION.begin()
    try:
        CONNECT_SESSION.add(obj)
    except:
        CONNECT_SESSION.rollback()
        raise
    else:
        CONNECT_SESSION.commit()

    return obj

def find_employee_by_name(employee_name: str) -> ...:

    stmt = select(Employee).where(Employee.name.in_([employee_name]))

    for emp in CONNECT_SESSION.scalars(stmt):
        print(emp)
    return stmt

def query_find_employee_by_name(search_name: str) -> ...: #todo какое должно быть возвращаемое значение
    results = CONNECT_SESSION.query(Employee).filter_by(name='ed').all()
    return results

def query_find_by_id(entity, id) -> ...: #todo какое должно быть возвращаемое значение
    obj = CONNECT_SESSION.query(entity).get(id)
    return obj

def show_all(entity):
    return [x.to_dict() for x in entity.query.all()]

def delete_obj(entity, id):
    obj_to_delete = CONNECT_SESSION.query(entity).get(id)
    CONNECT_SESSION.delete(obj_to_delete)
    CONNECT_SESSION.commit()

# # query with multiple classes, returns tuples
# results = CONNECT_SESSION.query(Employee, Role).join('addresses').filter_by(name='ed').all()
#
# # query using orm-columns, also returns tuples
# results = CONNECT_SESSION.query(User.name, User.fullname).all()
