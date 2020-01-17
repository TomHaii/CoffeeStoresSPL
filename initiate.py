import sqlite3
import os
import sys


def create_tables(cursor):
    cursor.execute(""" CREATE TABLE Employees(id  INT PRIMARY KEY,
                                                 name TEXT NOT NULL,
                                                 salary REAL NOT NULL,
                                                 coffee_stand INTEGER REFERENCES Coffee_stand(id)
                                                 ) """)
    cursor.execute(""" CREATE TABLE Suppliers(id  INT PRIMARY KEY,
                                                 name TEXT NOT NULL,
                                                 contact_information TEXT
                                                 ) """)
    cursor.execute(""" CREATE TABLE Products(id  INT PRIMARY KEY,
                                                 description TEXT NOT NULL,
                                                 price REAL NOT NULL,
                                                 quantity INTEGER NOT NULL
                                                 ) """)
    cursor.execute(""" CREATE TABLE Coffee_stands(id  INT PRIMARY KEY,
                                                 location TEXT NOT NULL,
                                                 number_of_employees INTEGER 
                                                 ) """)
    cursor.execute(""" CREATE TABLE Activities(product_id  INTEGER INTEGER REFERENCES Product(id),
                                                 quantity INTEGER NOT NULL,
                                                 activator_id INTEGER NOT NULL,
                                                 date DATE NOT NULL 
                                                 ) """)


def insert_data(cursor, config):
    for line in config:
        words = line.split(", ")
        print(words)
        if words[0] == 'C':
            insert_coffee_stand(cursor, words[1], words[2], words[3].strip('\n'))
        elif words[0] == 'S':
            insert_supplier(cursor, words[1], words[2], words[3].strip('\n'))
        elif words[0] == 'E':
            insert_employee(cursor, words[1], words[2], words[3], words[4].strip('\n'))
        elif words[0] == 'P':
            insert_product(cursor, words[1], words[2], words[3].strip('\n'), 0)



def insert_employee(cursor, id, name, salary, coffee_stand):
    cursor.execute("INSERT INTO Employees VALUES (?, ?, ?, ?)", (id, name, salary, coffee_stand))


def insert_supplier(cursor, id, name, contact_information):
    cursor.execute("INSERT INTO Suppliers VALUES (?, ?, ?)", (id, name, contact_information))


def insert_product(cursor, id, description, price, quantity):
    cursor.execute("INSERT INTO Products VALUES (?, ?, ?, ?)", (id, description, price, quantity))


def insert_coffee_stand(cursor, id, location, number_of_employees):
    cursor.execute("INSERT INTO Coffee_stands VALUES (?, ?, ?)", (id, location, number_of_employees))



def close_db(dbcon):
    dbcon.commit()
    dbcon.close()


def main(argv):
    DBExist = os.path.isfile("moncafe.db")
    if DBExist:
        os.remove("moncafe.db")
    config = open(argv[0], "r")  # TODO: Change file path to argument
    dbcon = sqlite3.connect("moncafe.db")
    cursor = dbcon.cursor()
    create_tables(cursor)
    insert_data(cursor, config)
    close_db(dbcon)


if __name__ == "__main__":
   main(sys.argv[1:])


