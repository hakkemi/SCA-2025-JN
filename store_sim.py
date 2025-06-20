alerts = [] # for inventory
cd = None # current drink global var
# List stored with every existing order
every_order = []

''' 
** Boba Store Simulation **

User is the Barista
Drinks can be added to an order. 
Each order has a total ($) which will be calculated based on drink  adjustments
To the drink
Each time a drink is added to an order, it's subsequent ingredients will be subtracted from the current stock in the inventory.
If not enough ingredients are present in order to make the drink, the order will force complete and the current drink will be cancelled
The barista may adjust the inventory in order to take on more drink orders.
Alerts of ingredients falling below their threshold will be displayed on the main dashboard, and will be removed when inventory is adjusted
'''
# Nested dictionary containing ingredient names and relevant information
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
# WILL NOT BE INCLUDING (most) TOPPINGS IN RECIPES. I AM TOO LAZY. WE HAVE AN INFINITE SUPPLY OF BOBA FRUIT JELLY AND CF.
# Nested dictionaries containing recipes for large and medium sizes
recipes = {
    # ml, g, g
    "Signature Milk Tea": {
        "Medium": {
            "Milk": 150,
            "Black Tea": 20,
            "Sugar": 30,
        },
        "Large": {
            "Milk": 200,
            "Black Tea": 25,
            "Sugar": 40,
        },
    },
    "Thai Milk Tea": {
        "Medium": {
            "Milk": 150,
            "Thai Tea Mix": 25,
            "Sugar": 30,
        },
        "Large": {
            "Milk": 200,
            "Thai Tea Mix": 30,
            "Sugar": 40,
        },
    },
    "Oolong Milk Tea": {
        "Medium": {
            "Milk": 150,
            "Oolong Tea": 20,
            "Sugar": 30,
        },
        "Large": {
            "Milk": 200,
            "Oolong Tea": 25,
            "Sugar": 40,
        },
    },
    "Oreo Milk Tornado": {
        "Medium": {
            "Milk": 200,
            "Oreo Crumbs": 40,
            "Sugar": 40,
        },
        "Large": {
            "Milk": 250,
            "Oreo Crumbs": 50,
            "Sugar": 50,
        },
    },
    "Strawberry Milk Tornado": {
        "Medium": {
            "Milk": 200,
            "Strawberry Syrup": 50,
            "Sugar": 40,
        },
        "Large": {
            "Milk": 250,
            "Strawberry Syrup": 60,
            "Sugar": 50,
        },
    },
    "Taronado": {
        "Medium": {
            "Milk": 200,
            "Taro Powder": 30,
            "Sugar": 40,
        },
        "Large": {
                "Milk": 250,
                "Taro Powder": 40,
                "Sugar": 50,
        },
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
    {"name": "Signature Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Thai Milk Tea", "drink_type": "Tea Based","price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "drink_type": "Milk Based","price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]

class Drink:

    # Creates drink object with attributes
    def __init__(self, drink_id, name, drink_type, price, size="Medium", toppings=None):
        self.drink_id = drink_id
        self.name = name
        self.drink_type = drink_type
        self.price = price
        self.size = size
        self.toppings = toppings


# Class that stores drink objects and the total price of all drink objects
# Each time an order 'object' is created, the class will add +1 to the instance variable 'total_order_count'
class Order:
    total_order_count = 0 # total order counter
    def __init__(self, drink_list, drink_list_total):
        self.drink_list = drink_list
        self.drink_list_total = drink_list_total
        Order.total_order_count += 1

# Dashboard/"main menu" function to display options to user
def display_dashboard():
    print("\n--- Dashboard ---")
    print("1. Add Order")
    print("2. View Orders")
    print("3. View Inventory")
    print("4. Adjust Inventory")
    print("5. Quit program")
    print(f"Alerts: {alerts}")
    try: # checks to see if input is valid
        choice = int(input("Choice: "))
        print("-----------------")
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
            return None
        else:
            print("Invalid option! Please choose a number between 1 and 5.")
        return display_dashboard()
    except ValueError:
        print("Invalid input. Please enter an integer number between 1 and 5.")
        return display_dashboard()  # call dashboard again if input is invalid

# Prompts user for drink and drink adjustments, creates a drink object and stores it in a current order list
def add_drink_to_order(drink_list: list):

    # prints options
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

        current_topping = toppings_data["None"]
        for i, topping in enumerate(toppings_data):
            if toppings_choice == i + 1:
                current_topping = topping
                current_price += toppings_data[topping]
                break

        # creates the drink object
        cd = Drink(
            drink_id = drink.drink_id,
            name=drink.name,
            drink_type = drink.drink_type,
            price = current_price,
            size = current_size,
            toppings = current_topping # L: this is highlighted orange by IDE because if you don't have toppings data it's undefined
        ) # L: moved this parenthesis down to the next line

        # checks to see if there is enough ingredients associated with the drink to make it or not
        if cd.name in recipes and cd.size in recipes[cd.name]:
            for key in recipes[cd.name][cd.size]:
                if key in inventory:
                    if (inventory[key]["stock"] - recipes[cd.name][cd.size][key]) <= 0:
                        print(f"Not enough {key}. Please add to inventory. Completing and closing order now.")
                        return drink_list
                    elif (inventory[key]["stock"] - recipes[cd.name][cd.size][key]) <= (inventory[key]["threshold"]):
                        print(
                        f"*****\nWARNING: {key} stock will be {(inventory[key]["stock"] - recipes[cd.name][cd.size][key])} {inventory[key]["unit"]}.\n*****")
                        alert_message = f"Low: {key} ({(inventory[key]["stock"] - recipes[cd.name][cd.size][key])}) {inventory[key]["unit"]}, "
                        for sentence in alerts:
                            if key in sentence:  # removes any alerts associated with the ingredient name so alerts doesnt have duplicate ingredients
                                    alerts.remove(sentence)
                        alerts.append(alert_message)
                    inventory[key]["stock"] -= recipes[cd.name][cd.size][key]
        else:
            print(f"Recipe for {cd.name} (Size: {cd.size}) needs to be added. "
                  f"Order will be closed, no stock will be deducted")
            return drink_list
        drink_list.append(cd)
        print("--- Final ---")
        print("1. Complete order")
        print("2. Add another drink")
        print("3. Cancel Order")
        re_choice = int(input("Choice: "))
        while True:
            if re_choice == 1:
                print("-----------------")
                return drink_list
            elif re_choice == 2:
                print("-----------------")
                return add_drink_to_order(drink_list)
            elif re_choice == 3:
                print("-----------------")
                return None
            else:
                print("Drink added but invalid option, please enter an integer of 1 or 2")
                re_choice = int(input("Choice: "))
    else:
        print("Invalid option, please try again")
        return add_drink_to_order(drink_list)

# Creates a list of drink objects after calling add_drink_to_order, then adds the list to a global list
# which contains EVERY existing order
def add_new_order():
    order = []
    order_total = 0
    new_order_drink_list = add_drink_to_order(order)
    if not new_order_drink_list: # If the returned list is empty, no order is returned
        return None
    else:
        for drink in new_order_drink_list:
            order_total += drink.price
        new_order = Order(new_order_drink_list, order_total)
        every_order.append(new_order)
        return new_order

# Prints every existing order numerically
# Prints each drink object in the order numerically (prints the drink's # in the order, name, topping, size, and price attributes)
def view_orders():
    print("\n--- Orders Overview ---")
    if not every_order: # If the list is completely empty the barista is returned to the dashboard
        print("You have no completed orders!")
        print("-----------------")
        return display_dashboard()
    for i, order in enumerate(every_order):
        print(f"--- Order {i+1} ---")
        print(f"Order Total: ${order.drink_list_total:.2f}")
        for index, drink in enumerate(order.drink_list):
            print(f"{index+1}. {drink.name}, {drink.toppings}, {drink.size}, ${drink.price:.2f}")
    print("-----------------------")
    return display_dashboard()

# Prints the inventory, detailing current stock and unit of measurement
def view_inventory () :
    print(f"\n-- Inventory Overview ---")
    for ingredient, details in inventory.items():
        print(f"{ingredient}: {details["stock"]} {details["unit"]}")
    print("-----------------")

# Allows user to add stock to a certain ingredient
def adjust_inventory () :
    print("\n--- Inventory Adjustment ---")
    try:
        ingredient = input("Ingredient: ").lower().capitalize()
    except ValueError:
        print("Please enter a valid ingredient")
    for key in inventory.keys():
        if ingredient in key:
            print(f"{ingredient} current stock: {inventory[key]["stock"]}")
            try:
                adjustment = int(input("Add quantity: "))
                inventory[key]["stock"] += adjustment
                for sentence in alerts:
                    if ingredient in sentence: # removes any alerts associated with the ingredient name if threshold isnt met
                        if inventory[key]["stock"] > inventory[key]["threshold"]:
                            alerts.remove(sentence)
            except ValueError:
                print("Invalid input detected, please enter an integer.")
                print("-----------------")
                return adjust_inventory()
    print("-----------------")
    return None

def main ():
    display_dashboard()

# Creates a menu list with drink objects for each KEY from the menu_data dictionary
menu = [Drink(drink_id = i + 1, **item_data) for i, item_data in enumerate(menu_data)]

main()