from gen.gen import *

def vending_machine(dict_of_items_to_cost, wanted_item):
        if has_item(dict_of_items_to_cost, wanted_item):
            announce_cost_of_wanted(dict_of_items_to_cost, wanted_item)
            confirmation = get_confirmation_from_user()
            update_vending_machine(confirmation, dict_of_items_to_cost, wanted_item)
        else:
            announce_shortage_to_user()


if __name__ == "__main__":
    element = input("what do you want?")
    vending_machine({'tomato': '1', 'chocolate': '2'}, element)