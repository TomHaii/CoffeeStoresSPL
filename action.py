import sys
import persistence
from persistence import repo



def perform_action(action_id, action):
    product_id = int(action[0])
    amount = int(action[1])
    activator = int(action[2])
    date = action[3].strip('\n')
    curr_quantity = int(repo.products.get_product_quantity(product_id))
    if (amount > 0) or (amount < 0 and curr_quantity >= amount):
        repo.products.update_products(product_id, curr_quantity + amount)
        activity = persistence.Activity(action_id, product_id, amount, activator, date)
        repo.activities.insert_activity(activity)
        action_id += 1
        return True
    else:
        print("illegal argument")



def main(argv):
    action_id = 1
    actions = open(argv[1], "r")  # TODO: Change file path to argument
    for line in actions:
        words = line.split(", ")
        if perform_action(action_id, words):
            action_id += 1


if __name__ == "__main__":
   main(sys.argv)


