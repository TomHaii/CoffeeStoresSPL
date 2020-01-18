import sqlite3
import atexit
import os


class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand


class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def find(self, employee):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM Employees WHERE id=({})".format(employee.id))
        return cursor.fetchone()

    def insert(self, employee):
        self._conn.execute("INSERT INTO Employees VALUES (?, ?, ?, ?)", (employee.id, employee.name, employee.salary, employee.coffee_stand))


class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("INSERT INTO Suppliers VALUES (?, ?, ?)", (supplier.id, supplier.name, supplier.contact_information))

    def find(self, supplier):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM Suppliers WHERE id=({})".format(supplier.id))
        return cursor.fetchone()


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def find(self, product_id):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT name FROM Products WHERE id=({})".format(product_id))
        return cursor.fetchone()

    def insert(self, product):
        self._conn.execute("INSERT INTO Products VALUES (?, ?, ?, ?)", (product.id, product.description, product.price, product.quantity))

    def update_products(self, product_id, amount):
        self._conn.execute("""
                       UPDATE Products SET quantity=(?) WHERE id=(?)
                   """, [amount, product_id])

    def get_product_quantity(self, product_id):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT quantity FROM Products WHERE id=({})".format(product_id))
        return cursor.fetchone()[0]


class Coffee_stand:
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("INSERT INTO Coffee_stands VALUES (?, ?, ?)", (coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees))


class Activity:
    def __init__(self, id, product_id, quantity, activator_id, date):
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert_activity(self, activity):
        self._conn.execute("INSERT INTO Activities VALUES (?, ?, ?, ?, ?)", (activity.id, activity.product_id, activity.quantity, activity.activator_id, activity.date))


class _Repository:
    def connect(self):
        self._conn = sqlite3.connect('moncafe.db')
        self.employees = _Employees(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.products = _Products(self._conn)
        self.coffee_stands = _Coffee_stands(self._conn)
        self.activities = _Activities(self._conn)

    def close_db(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        cursor = self._conn.cursor()
        cursor.execute(""" CREATE TABLE Employees(  id INTEGER PRIMARY KEY,
                                                     name TEXT NOT NULL,
                                                     salary REAL NOT NULL,
                                                     coffee_stand INTEGER REFERENCES Coffee_stand(id)
                                                     ) """)
        cursor.execute(""" CREATE TABLE Suppliers(  id INTEGER PRIMARY KEY,
                                                     name TEXT NOT NULL,
                                                     contact_information TEXT
                                                     ) """)
        cursor.execute(""" CREATE TABLE Products(   id INTEGER PRIMARY KEY,
                                                     description TEXT NOT NULL,
                                                     price REAL NOT NULL,
                                                     quantity INTEGER NOT NULL
                                                     ) """)
        cursor.execute(""" CREATE TABLE Coffee_stands(id  INTEGER PRIMARY KEY,
                                                     location TEXT NOT NULL,
                                                     number_of_employees INTEGER 
                                                     ) """)
        cursor.execute(""" CREATE TABLE Activities( id INTEGER PRIMARY KEY,
                                                    product_id  INTEGER INTEGER REFERENCES Product(id),
                                                     quantity INTEGER NOT NULL,
                                                     activator_id INTEGER NOT NULL,
                                                     date DATE NOT NULL 
                                                     ) """)





repo = _Repository()
atexit.register(repo.close_db)


