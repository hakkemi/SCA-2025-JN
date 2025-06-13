alerts = []
# i am nawt handling any exceptions or errors rn
class Drink:

    def __init__(self, drink_id, name, type, price, size="Medium", toppings=None):
        if size.lower() == "Large".lower():
            price += 1
        if not toppings == None:
            if toppings == "Boba".lower():
                price += 0.5
            elif toppings == "Fruit Jelly".lower():
                price += 0.75
            elif toppings == "Cheesefoam".lower():
                price += 0.85
        self.drink_id = drink_id
        self.name = name
        self.type = type
        self.price = price
        self.size = size
        self.toppings = toppings
class Order:
    current = []
print("hi")

def display_dashboard():
    print("--- Dashboard ---")
    print("1. Add Order")
    print("2. View Orders")
    print("3. View Inventory")
    print("4. Adjust Inventory")
    print("5. Quit program")
    print(f"Alerts: {alerts}")
    choice = int(input("Choice: "))
    validate_option_menu(choice)

def add_new_order():
    display_add_menu()
    drink_choice = int(input("Choice: "))
    if 0 <= drink_choice <= len(menu):
        for index, drink in enumerate(menu):
            if drink_choice == drink.drink_id:
                size_choice = input("Size (M/L): ")
                if size_choice.lower() == "L".lower():
                    drink.size = "Large"
                    drink.price += 1
                print("--- Toppings ---")
                print("1. Boba")
                print("2. Fruit Jelly")
                print("3. Cheesefoam")
                print("4. None")
                toppings_choice = int(input("Choice: "))
                if toppings_choice == 1:
                    drink.price += 0.5
                elif toppings_choice == 2:
                    drink.price += 0.75
                elif toppings_choice == 3:
                    drink.price += 0.85
                print("1. Return to dashboard (completes current order)")
                print("2. Add another drink")
                re_choice = int(input("Choice: "))
                if re_choice == 1:
                    display_dashboard()
                elif re_choice == 2:
                    add_new_order()

def display_add_menu ():
    print("--- Menu ---")
    print("0. View Total Drinks in Order")
    for i, drink in enumerate(menu):
        print(f"{i + 1}. {drink.name} {drink.drink_id}")

# def view_orders():


#def view_inventory () :


#def adjust_inventory () :


def validate_option_menu (choice):
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
            print("Program terminated")
    else:
        print("Invalid option!")
        display_dashboard()

def main ():
    display_dashboard()


menu_data = [
    {"name": "Signature Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Thai Milk Tea", "type": "Tea Based","price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "type": "Milk Based","price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]
menu = [Drink(drink_id = i + 1, **item_data) for i, item_data in enumerate(menu_data)]
# literally the same thing menu = []
# for i, item_data in enumerate(menu_data):
#     drink = Drink(drink_id = i + 1, **item_data)
#     menu.append(drink)

main()
