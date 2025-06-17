alerts = [] # for inventory
inventory = {
    "Milk": {"stock": 1000, "unit": "ml", "threshold": 200},
    "Black Tea": {"stock": 500, "unit": "g", "threshold": 100},
    "Sugar": {"stock": 700, "unit": "g", "threshold": 150},
    "Boba": {"stock": 300, "unit": "servings", "threshold": 50},
    "Fruit Jelly": {"stock": 250, "unit": "servings", "threshold": 40},
    "Cheese Foam": {"stock": 200, "unit": "servings", "threshold": 30},
    "Oolong Tea": {"stock": 400, "unit": "g", "threshold": 80},
    "Strawberry Syrup": {"stock": 300, "unit": "ml", "threshold": 60},
    "Taro Powder": {"stock": 200, "unit": "g", "threshold": 40},
    "Oreo Crumbs": {"stock": 150, "unit": "g", "threshold": 30},
    "Thai Tea Mix": {"stock": 350, "unit": "g", "threshold": 70},
}
# will add serving quant for toppings laterrrrrrrrrrrrrrrrrr
recipes = {
    # ml, g, g
    "Signature Milk Tea": {
        "Milk": 150,
        "Black Tea": 20,
        "Sugar": 30,
    },
    "Thai Milk Tea": {
        "Milk": 150,
        "Thai Tea Mix": 25,
        "Sugar": 30,
    },
    "Oolong Milk Tea": {
        "Milk": 150,
        "Oolong Tea": 20,
        "Sugar": 30,
    },
    "Oreo Milk Tornado": {
        "Milk": 200,
        "Oreo Crumbs": 40,
        "Sugar": 40,
    },
    "Strawberry Milk Tornado": {
        "Milk": 200,
        "Strawberry Syrup": 50,
        "Sugar": 40,
    },
    "Taronado": {
        "Milk": 200,
        "Taro Powder": 30,
        "Sugar": 40,
    },
}
toppings_data = {
    "None": 0.00,
    "Boba": 0.50,
    "Fruit Jelly": 0.75,
    "Cheese Foam": 0.85,
    "Oreo Crumbs": 0.85,
}
menu_data = [
    {"name": "Signature Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Thai Milk Tea", "type": "Tea Based","price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "type": "Milk Based","price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]

class Drink:

    def __init__(self, drink_id, name, type, price, size="Medium", toppings=None):

        self.drink_id = drink_id
        self.name = name
        self.type = type
        self.price = price
        self.size = size
        self.toppings = toppings
class Current_Drink (Drink):
    pass
class Order():
    total_order_count = 0
    def __init__(self, drink_list):
        self.drink_list = drink_list
        Order.total_order_count += 1
def display_dashboard():
    print("\n--- Dashboard ---")
    print("1. Add Order")
    print("2. View Orders")
    print("3. View Inventory")
    print("4. Adjust Inventory")
    print("5. Quit program")
    print(f"Alerts: {alerts}")
    try:
        choice = int(input("Choice: "))
        validate_option_menu(choice)
    except ValueError:
        print("Invalid input. Please enter an integer number between 1 and 5.")
        display_dashboard()  # Call dashboard again if input is invalid

def add_drink_to_order(drink_list):
    print("\n--- Menu ---")
    print("0. Cancel Order")
    for i, drink in enumerate(menu):
        print(f"{i + 1}. {drink.name} (${drink.price:.2f})")

    try:
        drink_choice = int(input("Choice: "))
    except ValueError:
        print("Invalid input. Enter an int #")
        return add_drink_to_order(drink_list)
    if drink_choice == 0:
        return drink_list

    if 1 <= drink_choice <= len(menu):
        drink = menu[drink_choice - 1]
        print("--- Size ---")
        size_choice = input("Size (M/L): ").strip().lower()
        if size_choice.lower() == "l":
            current_size = "Large"
            current_price = (drink.price + 1)
        elif size_choice.lower() == "m":
            current_size = "Medium"
            current_price = drink.price
        else:
            return add_drink_to_order(drink_list)

        print("--- Toppings ---")
        for i, topping in enumerate(toppings_data):
            print(f"{i + 1}. {topping}")

        try:
            toppings_choice = int(input("Choice: "))
        except ValueError:
            print("Invalid option, please enter an integer")
            return add_drink_to_order(drink_list)
        if toppings_choice == 0:
            print("Invalid option")
            return add_drink_to_order(drink_list)

        for i, topping in enumerate(toppings_data):
            if toppings_choice == (i + 1):
                current_topping = topping
                current_price += toppings_data[topping]

        current_drink = Current_Drink(
            drink_id = drink.drink_id,
            name=drink.name,
            type = drink.type,
            price = current_price,
            size = current_size,
            toppings = current_topping)
        drink_list.append(current_drink)
        print("--- Final ---")
        print("1. Complete order")
        print("2. Add another drink")
        re_choice = int(input("Choice: "))
        if re_choice == 1:
            subtract_inventory(drink_list)
            return drink_list
        elif re_choice == 2:
            return add_drink_to_order(drink_list)
        else:
            print("Invalid option, please enter an integer of 1 or 2")
            return add_drink_to_order(drink_list)
    else:
        print("Invalid option, please try again")
        return add_drink_to_order(drink_list)

def add_new_order():
    order = []
    new_order_drink_list = add_drink_to_order(order)
    if not new_order_drink_list:
        return None
    else:
        new_order = Order(new_order_drink_list)
        print(f"Order Number: {new_order.total_order_count}")
        every_order.append(new_order)
        return new_order

def view_orders():
    if not every_order:
        print("You have no completed orders!")
        display_dashboard()
    for i, order in enumerate(every_order):
        print(f"--- Order {i+1} ---")
        for drink in order.drink_list:
            print(f"{drink.name}, {drink.toppings}, {drink.size}, ${drink.price:.2f}")

def view_inventory () :
    print(f"\n-- Inventory Overview ---")
    for ingredient, details in inventory.items():
        print(f"{ingredient}: {details["stock"]} {details["unit"]}")

# takes from individual order, will be implemented later
def subtract_inventory (drink_list):
    for drink in drink_list:
        if drink.name in recipes:
            drink_name = drink.name
            for key in recipes[drink_name]:
                if key in inventory:
                    # print(f"og stock: {inventory[key]["stock"]}")
                    # print(f"new stock: {inventory[key]["stock"]}")
                    if (inventory[key]["stock"]) <= inventory[key]["threshold"]:
                        print(f"Low on {inventory[key]}")
                        alerts.append(f"Low stock: {key} stock is {inventory[key]['stock']}.")
                    else:
                        inventory[key]["stock"] -= recipes[drink_name][key]

        else:
            print("Recipe needs to be added")
def adjust_inventory () :
    ingredient = input("Ingredient: ").lower()
    ingredient = ingredient.capitalize()
    for key in inventory.keys():
        if ingredient in key:
            print(f"\n{ingredient} current stock: {inventory[key]["stock"]}")
            adjustment = int(input("Add quantity: "))
            inventory[key]["stock"] += adjustment

def validate_option_menu (choice):
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
        print("Invalid option! Please choose a number between 1 and 5.")
        display_dashboard()
    display_dashboard()

def main ():
    display_dashboard()

menu = [Drink(drink_id = i + 1, **item_data) for i, item_data in enumerate(menu_data)]
# literally the same thing menu = []
# for i, item_data in enumerate(menu_data):
#     drink = Drink(drink_id = i + 1, **item_data)
#     menu.append(drink)
every_order = []

main()