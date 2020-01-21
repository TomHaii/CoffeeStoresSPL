from persistence import repo


def print_employees_table():
    print('Employees')
    for employee in repo.employees.find_all():
        print(employee.to_tuple())


def print_activities_table():
    print('Activities')
    for activity in repo.activities.find_all():
        print(activity.to_tuple())


def print_suppliers_table():
    print('Suppliers')
    for supplier in repo.suppliers.find_all():
        print(supplier.to_tuple())


def print_products_table():
    print('Products')
    for product in repo.products.find_all():
        print(product.to_tuple())


def print_coffee_stands_table():
    print('Coffee stands')
    for coffee_stand in repo.coffee_stands.find_all():
        print(coffee_stand.to_tuple())


def print_employees_report():
    print('Employees report')
    for report in repo.get_employees_report():
        print(*(report.to_tuple()))


def print_activities_report():
    if len(repo.get_activities_report()) > 0:
        print('Activities')
        for activity in repo.get_activities_report():
            print(activity)


def print_tables():
    print_activities_table()
    print_coffee_stands_table()
    print_employees_table()
    print_products_table()
    print_suppliers_table()
    print("")
    print_employees_report()
    print("")
    print_activities_report()


def main():
    repo.connect()
    print_tables()


if __name__ == "__main__":
    main()
