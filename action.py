import sys
import persistence
from persistence import repo


def perform_action(action):
    id = 1
    product_id = int(action[0])
    amount = int(action[1])
    activator = int(action[2])
    date = action[3].strip('\n')
    curr_quantity = int(repo.products.get_product_quantity(product_id))
    if amount > 0:
        repo.products.update_products(product_id, curr_quantity + amount)
        activity = persistence.Activity
        insert_activity(product_id, amount, activator, date)
    elif amount < 0 and curr_quantity >= amount:
        update_products(product_id, curr_quantity + amount)
        insert_activity(product_id, amount, activator, date)

    else:
        print("illegal argument")



def main(argv):
    actions = open(argv[1], "r")  # TODO: Change file path to argument
    for line in actions:
        words = line.split(", ")
        perform_action(words)

if __name__ == "__main__":
   main(sys.argv)


