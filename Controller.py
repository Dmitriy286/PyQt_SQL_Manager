import sqlalchemy
import psycopg2

from mimesis import Person
from sqlalchemy import select

from Model import Employee, CONNECT_SESSION, commit_session


def create_employee():
    person = Person('ru')

    return {
            'name': person.name(),
            'username': '@' + person.username(mask='l_l'),
            'password': person.password(),
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

def query_find_employee_by_id(employee_id) -> ...: #todo какое должно быть возвращаемое значение
    employee = CONNECT_SESSION.query(Employee).get(employee_id)
    return employee

def show_all_employees():
    return [x.to_dict() for x in Employee.query.all()]

def changeEmployee(self):
    user = query_find_employee_by_id()
    user.login = "@tur"
    commit_session()

def delete_employee(employee_id):
    # CONNECT_SESSION.delete(CONNECT_SESSION.query(Employee).filter_by(id=employee_id).all())
    employee_to_delete = CONNECT_SESSION.query(Employee).get(employee_id)
    CONNECT_SESSION.delete(employee_to_delete)
    # commit (or flush)
    CONNECT_SESSION.commit()

# # query with multiple classes, returns tuples
# results = CONNECT_SESSION.query(Employee, Role).join('addresses').filter_by(name='ed').all()
#
# # query using orm-columns, also returns tuples
# results = CONNECT_SESSION.query(User.name, User.fullname).all()
