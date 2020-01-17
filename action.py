import sqlite3
import os
import atexit
import sys



dbcon = sqlite3.connect("moncafe.db")
cursor = dbcon.cursor()


def get_product_quantity(id):
    cursor.execute(
        "SELECT quantity FROM Products WHERE id=({})".format(id))
    return cursor.fetchone()[0]

def get_supplier(id):
    cursor.execute(
        "SELECT name FROM Suppliers WHERE id=({})".format(id))
    return cursor.fetchone()


def get_employee(id):
    cursor.execute(
        "SELECT name FROM Employees WHERE id=({})".format(id))
    return cursor.fetchone()


def update_products(id, amount):
    cursor.execute("""
                   UPDATE Products SET quantity=(?) WHERE id=(?)
               """, [amount, id])


def insert_activity(product_id, quantity, activator_id, date):
    cursor.execute("INSERT INTO Activities VALUES (?, ?, ?, ?)", (product_id, quantity, activator_id, date))


def perform_action(action):
    product_id = int(action[0])
    amount = int(action[1])
    activator = int(action[2])
    date = action[3].strip('\n')
    curr_quantity = int(get_product_quantity(product_id))
    if amount > 0:
        update_products(product_id, curr_quantity + amount)
        insert_activity(product_id, amount, activator, date)
    elif amount < 0 and curr_quantity >= amount:
        update_products(product_id, curr_quantity + amount)
        insert_activity(product_id, amount, activator, date)

    else:
        print("illegal argument")

def insert_data(actions):
    for line in actions:
        words = line.split(", ")
        perform_action(words)


def close_db():
    dbcon.commit()
    dbcon.close()



def main(argv):
    actions = open(argv[1], "r")  # TODO: Change file path to argument
    insert_data(actions)
    atexit.register(close_db)


if __name__ == "__main__":
   main(sys.argv)


