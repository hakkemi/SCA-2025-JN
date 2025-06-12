alerts = []

class Drink:
    def __init__(self, price, size="Medium", toppings=None):
        self.price = price
        if not size == "Medium".lower():
            price += 1
        if not toppings == None:
            if toppings == "Boba".lower():
                price += 0.5
            elif toppings == "Fruit Jelly".lower():
                price += 0.75
            elif toppings == "Cheesefoam".lower():
                price += 0.85
#def main ():


def display_menu():
    print("--- Dashboard ---")
    print("1. Add Order")
    print("2. View Orders")
    print("3. View Inventory")
    print("4. Adjust Inventory")
    print("5. Quit program")
    print(f"Alerts: {alerts}")
    choice = int(input("Choice: "))
    validate_option(choice)

#def add_new_order():


#def view_orders():


#def view_inventory () :


#def adjust_inventory () :


def validate_option (choice):
    if 1 <= choice <= 5:
        if choice == 1:
            add_new_order()
        elif choice == 2:
            view_orders()
        elif choice == 3:
            view_inventory()
        elif choice == 4:
            adjust_inventory()
        elif choice == 5:
            print("Program quitted")
    else:
        print("Invalid option!")
        display_menu()

test = [signature_mt: Drink(5.00)]

