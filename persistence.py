import sqlite3
import atexit


class Employee:
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand

    def to_tuple(self):
        output = (self.id, self.name, self.salary, self.coffee_stand)
        return output


class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("INSERT INTO Employees VALUES (?, ?, ?, ?)",
                           (employee.id, employee.name, employee.salary, employee.coffee_stand))

    def find_all(self):
        c = self._conn.cursor()
        all_employees = c.execute("""
            SELECT id, name, salary, coffee_stand FROM Employees ORDER BY id
        """).fetchall()
        return [Employee(*row) for row in all_employees]

    def find_all_by_name(self):
        c = self._conn.cursor()
        all_employees = c.execute("""
                SELECT id, name, salary, coffee_stand FROM Employees ORDER BY name
            """).fetchall()
        return [Employee(*row) for row in all_employees]


class Supplier:
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def to_tuple(self):
        output = (self.id, self.name, self.contact_information)
        return output


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("INSERT INTO Suppliers VALUES (?, ?, ?)",
                           (supplier.id, supplier.name, supplier.contact_information))

    def find_all(self):
        c = self._conn.cursor()
        all_suppliers = c.execute("""
            SELECT id, name, contact_information FROM Suppliers ORDER BY id
        """).fetchall()
        return [Supplier(*row) for row in all_suppliers]


class Product:
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def to_tuple(self):
        output = (self.id, self.description, self.price, self.quantity)
        return output


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def find_description(self, product_id):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT description FROM Products WHERE id=({})".format(product_id))
        return cursor.fetchone()

    def insert(self, product):
        self._conn.execute("INSERT INTO Products VALUES (?, ?, ?, ?)",
                           (product.id, product.description, product.price, product.quantity))

    def update_products(self, product_id, amount):
        self._conn.execute("""
                       UPDATE Products SET quantity=(?) WHERE id=(?)
                   """, [amount, product_id])

    def get_product_quantity(self, product_id):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT quantity FROM Products WHERE id=({})".format(product_id))
        return cursor.fetchone()[0]

    def find_all(self):
        c = self._conn.cursor()
        all_products = c.execute("""
            SELECT id, description, price, quantity FROM Products ORDER BY id
        """).fetchall()
        return [Product(*row) for row in all_products]


class Coffee_stand:
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def to_tuple(self):
        output = (self.id, self.location, self.number_of_employees)
        return output


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("INSERT INTO Coffee_stands VALUES (?, ?, ?)",
                           (coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees))

    def find_all(self):
        c = self._conn.cursor()
        all_stands = c.execute("""
            SELECT id, location, number_of_employees FROM Coffee_stands ORDER BY id
        """).fetchall()
        return [Coffee_stand(*row) for row in all_stands]

    def find(self, id):
        c = self._conn.cursor()
        c.execute(
            "SELECT location FROM Coffee_stands WHERE id=({})".format(id))
        return c.fetchone()[0]


class Activity:
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def to_tuple(self):
        output = (self.product_id, self.quantity, self.activator_id, self.date)
        return output


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert_activity(self, activity):
        self._conn.execute("INSERT INTO Activities VALUES (?, ?, ?, ?)",
                           (activity.product_id, activity.quantity, activity.activator_id, activity.date))

    def find_all(self):
        c = self._conn.cursor()
        all_activities = c.execute("""
            SELECT product_id, quantity, activator_id, date FROM Activities ORDER BY date
        """).fetchall()
        return [Activity(*row) for row in all_activities]


class Employee_Report:
    def __init__(self, _id, name, salary, location):
        self.name = name
        self.salary = salary
        self.location = location
        self.total_sales = repo.get_total_sales(_id)

    def to_tuple(self):
        output = (self.name, self.salary, self.location, self.total_sales)
        return output


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
        cursor.execute(""" CREATE TABLE Activities(  product_id  INTEGER INTEGER REFERENCES Product(id),
                                                     quantity INTEGER NOT NULL,
                                                     activator_id INTEGER NOT NULL,
                                                     date DATE NOT NULL 
                                                     ) """)

    def get_total_sales(self, employee_id):
        c = self._conn.cursor()
        c.execute(
            "SELECT Activities.quantity, Products.price FROM Activities"
            " INNER JOIN Products ON Products.id = Activities.product_id"
            " WHERE activator_id=({})".format(employee_id))
        sales_record = c.fetchall()
        amount = 0
        for r in sales_record:
            _quantity = int(abs(r[0]))
            price = r[1]
            amount += _quantity * price
        return amount

    def get_activities_report(self):
        c = self._conn.cursor()
        report = c.execute("""
            SELECT date, Products.description, Activities.quantity, Employees.name, Suppliers.name FROM Activities
            LEFT JOIN Products on Activities.product_id = Products.id
            LEFT JOIN Employees on Activities.activator_id  = Employees.id
            LEFT JOIN Suppliers on Activities.activator_id  = Suppliers.id
            ORDER BY Activities.date
        """).fetchall()
        return report

    def get_employees_report(self):
        c = self._conn.cursor()
        reports = c.execute("""
                SELECT Employees.id, Employees.name, Employees.salary, Coffee_stands.location FROM Employees
                LEFT JOIN Coffee_stands on Coffee_stands.id = Employees.coffee_stand
                ORDER BY Employees.name""").fetchall()
        return [Employee_Report(*row) for row in reports]


repo = _Repository()
atexit.register(repo.close_db)
