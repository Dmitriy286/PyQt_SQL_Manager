import sqlalchemy
import psycopg2

from mimesis import Person
from sqlalchemy import select

from .Model import Employee, CONNECT_SESSION


def create_employee():
    person = Person('ru')

    return {
            'name': person.name(),
            'username': '@' + person.username(mask='l_l'),
            'active': True,
            'password': person.password(),
            'email': person.email(),
            'phonenumber': person.telephone(),
            'photo': person.political_views(),
            'filename': ""
            }

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

def find_employee_by_name(employee_name: str) -> ...:

    stmt = select(Employee).where(Employee.name.in_([employee_name]))

    for emp in CONNECT_SESSION.scalars(stmt):
        print(emp)
    return stmt

def query_find_employee_by_name(search_name: str) -> ...: #todo какое должно быть возвращаемое значение
    # query from a class
    results = CONNECT_SESSION.query(Employee).filter_by(name='ed').all()
    return results

def show_all_employees():
    return [x.to_dict() for x in Employee.query.all()]



# query with multiple classes, returns tuples
results = CONNECT_SESSION.query(Employee, Role).join('addresses').filter_by(name='ed').all()

# query using orm-columns, also returns tuples
results = CONNECT_SESSION.query(User.name, User.fullname).all()
