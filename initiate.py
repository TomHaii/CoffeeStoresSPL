import sys
import persistence

from persistence import repo
import os

def insert_data(config):
    for line in config:
        words = line.split(", ")
        print(words)
        if words[0] == 'C':
            coffee_stand = persistence.Coffee_stand(words[1], words[2], words[3].strip('\n'))
            repo.coffee_stands.insert(coffee_stand)
        elif words[0] == 'S':
            supplier = persistence.Supplier(words[1], words[2], words[3].strip('\n'))
            repo.suppliers.insert(supplier)
        elif words[0] == 'E':
            employee = persistence.Employee(words[1], words[2], words[3], words[4].strip('\n'))
            repo.employees.insert(employee)
        elif words[0] == 'P':
            product = persistence.Product(words[1], words[2], words[3].strip('\n'), 0)
            repo.products.insert(product)


def main(argv):
    DBExist = os.path.isfile("moncafe.db")
    if DBExist:
        os.remove("moncafe.db")
    config = open(argv[0], "r")  # TODO: Change file path to argument
    repo.connect()
    repo.create_tables()
    insert_data(config)



if __name__ == "__main__":
   main(sys.argv[1:])


