from persistence import repo


def print_employees_table():
    print('Employees')
    for employee in repo.employees.find_all():
        print(employee)


def print_activities_table():
    print('Activities')
    for activity in repo.activities.find_all():
        print(activity)


def print_suppliers_table():
    print('Suppliers')
    for supplier in repo.suppliers.find_all():
        print(supplier)


def print_products_table():
    print('Products')
    for product in repo.products.find_all():
        print(product)


def print_coffee_stands_table():
    print('Coffee stands')
    for coffee_stand in repo.coffee_stands.find_all():
        print(coffee_stand)


def print_employees_report():
    print('Employees report')
    for employee in repo.employees.find_all():
        name = employee.name
        salary = str(employee.salary)
        location = repo.coffee_stands.find(employee.coffee_stand)[0]
        total_sales = str(repo.get_total_sales(employee.id))
        print(name + ' ' + salary + ' ' + location + ' ' + total_sales)


def print_tables():
    print_activities_table()
    print_coffee_stands_table()
    print_employees_table()
    print_products_table()
    print_suppliers_table()
    print_employees_report()


def main():
    repo.connect()
    print_tables()


if __name__ == "__main__":
    main()
