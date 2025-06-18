alerts = [] # for inventory

'''
# L: Overall, it might be helpful to add drink_type-hints to your code to make it easier to understand the types of particular objects
# 
# L: Nice inventory representation! You can also use this thing called a dataclass that might make the code a little bit easier
# L: I use dataclasses because I'm afraid that I would mistype "threshold" or things like that and lead to extra bugs
# L: using dataclasses makes it so that the IDE can detect typos
# 
# L: For now, I would keep the representation you have, since it works and uses what we've learned in class
# L: but in case you're curious, here's how I'd write your same inventory
* from dataclasses import dataclass
* from enum import Enum


# Enums are nice when you have a few potential options for strings
# String Enums pretty much act just like strings, but avoid typos
# List out all potential units to avoid typos
* class UnitType(str, Enum):
    ml = "ml"
    g = "g"
    servings = "servings"

# List out all potential shop item names to avoid typos
* class ShopItemName(str, Enum):
    milk = "Milk"
    black_tea = "Black Tea"
    sugar = "Sugar"
    boba = "Boba"
    fruit_jelly = "Fruit Jelly"
    cheese_foam = "Cheese Foam"
    oolong_tea = "Oolong Tea"
    strawberry_syrup = "Strawberry Syrup"
    taro_powder = "Taro Powder"
    oreo_crumbs = "Oreo Crumbs"
    thai_tea_mix = "Thai Tea Mix"


# L: a dataclass is what you use when you have a class without any methods
* @dataclass
class ShopItem:
    name: ShopItemName
    stock: int
    unit: UnitType
    threshold: int

# L: create a dictionary of shop items that goes from the shop item name to the shop item
# L: again, DONT USE THIS - just want you to see that it's possible
# L: I like how you have it set up currently
* london_inventory = {
    ShopItemName.milk: ShopItem(ShopItemName.milk, 1000, UnitType.ml, 200),
    ShopItemName.black_tea: ShopItem(ShopItemName.black_tea, 500, UnitType.g, 100),
    # etc.
}
'''


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
# also maybe add diff recipes for large/small sizes !
recipes = {
    # ml, g, g
    "Signature Milk Tea": {
        "Milk": 900,
        "Black Tea": 20,
        "Sugar": 600,
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
    {"name": "Signature Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Thai Milk Tea", "drink_type": "Tea Based","price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "drink_type": "Milk Based","price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]
cd = None
class Drink:

    # creates drink object with attributes
    def __init__(self, drink_id, name, drink_type, price, size="Medium", toppings=None):
        self.drink_id = drink_id
        self.name = name
        self.drink_type = drink_type
        self.price = price
        self.size = size
        self.toppings = toppings

# child class of drink
# L: There are two alternative ways of doing this
# L: 1. Add a property to the `Drink` class that's just a boolean `.current`
# L: 2. Create a global variable called `current_drink` that just stores the current drink
# L: I lean towards (2) because it ensures that you always only have one current drink

# class that stores drink objects and the total price of all drink objects
# L: cool use of the mixture between class properties and instance properties!
# L: As your IDE suggests, you can remove the parentheses in `class Order():` since they're empty
# done (used to java classes lolol)
class Order:
    total_order_count = 0 # total order counter
    def __init__(self, drink_list, drink_list_total):
        self.drink_list = drink_list
        self.drink_list_total = drink_list_total
        Order.total_order_count += 1

# dashboard/"main menu" function to display options to user
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
        return display_dashboard()
    except ValueError:
        print("Invalid input. Please enter an integer number between 1 and 5.")
        return display_dashboard()  # call dashboard again if input is invalid

# prompts user for drink and drink adjustments, creates a drink object and stores it in a current order list
def add_drink_to_order(drink_list):

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

        # creates the drink object
        cd = Drink(
            drink_id = drink.drink_id,
            name=drink.name,
            drink_type = drink.drink_type,
            price = current_price,
            size = current_size,
            toppings = current_topping # L: this is highlighted orange by IDE because if you don't have toppings data it's undefined
        ) # L: moved this parenthesis down to the next line

        if cd.name in recipes:
            for key in recipes[cd.name]:
                if key in inventory:
                    if (inventory[key]["stock"] - recipes[cd.name][key]) <= 0:
                        print(f"Not enough {key}. Please add to inventory. Completing and closing order now.")
                        return drink_list
                    elif (inventory[key]["stock"] - recipes[cd.name][key]) <= (inventory[key]["threshold"] + 100):
                        print(
                        f"*****\nWARNING: {key} stock will be {(inventory[key]["stock"] - recipes[cd.name][key])} {inventory[key]["unit"]}.\n*****")
                        alert_message = f"Low: {key} ({(inventory[key]["stock"] - recipes[cd.name][key])}) {inventory[key]["unit"]}, "
                        for sentence in alerts:
                            if key in sentence:  # removes any alerts associated with the ingredient name so alerts doesnt have duplicate ingredients
                                    alerts.remove(sentence)
                        alerts.append(alert_message)
                    inventory[key]["stock"] -= recipes[cd.name][key]
        else:
            print("Recipe needs to be added")
        drink_list.append(cd)
        print("--- Final ---")
        print("1. Complete order")
        print("2. Add another drink")
        print("3. Cancel Order")
        re_choice = int(input("Choice: "))
        # L: turning this into a while loop (until they answer something valid) can make it so that the user doesn't have to re-answer all of the previous questions
        # added
        while True:
            if re_choice == 1:
                return drink_list
            elif re_choice == 2:
                return add_drink_to_order(drink_list)
            elif re_choice == 3:
                return None
            else:
                print("Drink added but invalid option, please enter an integer of 1 or 2")
                re_choice = int(input("Choice: "))
    else:
        print("Invalid option, please try again")
        return add_drink_to_order(drink_list)

# creates a list of drink objects after calling add_drink_to_order, then adds the list to a global list
# which contains EVERY existing order
def add_new_order():
    order = []
    order_total = 0
    new_order_drink_list = add_drink_to_order(order)
    if not new_order_drink_list: # L: solid Python syntax! I like this
        return None
    else:
        for drink in new_order_drink_list:
            order_total += drink.price
        new_order = Order(new_order_drink_list, order_total)
        # debug print(f"Order Number: {new_order.total_order_count}")
        every_order.append(new_order)
        return new_order

# prints each drink object in an order (prints the drink's name, topping, size, and price attributes)
def view_orders():
    print("\n--- Orders Overview ---")
    if not every_order: # if the list is completely empty blud gets returned to display dashboard
        print("You have no completed orders!")
        return display_dashboard()
    for i, order in enumerate(every_order):
        print(f"--- Order {i+1} ---")
        print(f"Order Total: ${order.drink_list_total:.2f}")
        for index, drink in enumerate(order.drink_list):
            print(f"{index+1}. {drink.name}, {drink.toppings}, {drink.size}, ${drink.price:.2f}")
    return display_dashboard()

# literally just prints the inventory, function probably not needed?
def view_inventory () :
    print(f"\n-- Inventory Overview ---")
    for ingredient, details in inventory.items():
        print(f"{ingredient}: {details["stock"]} {details["unit"]}")

# allows user to add stock to a certain ingredient
def adjust_inventory () :
    print("\n--- Inventory Adjustment ---")
    ingredient = input("Ingredient: ").lower().capitalize()
    for key in inventory.keys():
        if ingredient in key:
            print(f"{ingredient} current stock: {inventory[key]["stock"]}")
            adjustment = int(input("Add quantity: "))
            inventory[key]["stock"] += adjustment
            for sentence in alerts:
                if ingredient in sentence: # removes any alerts associated with the ingredient name if threshold isnt met
                    if inventory[key]["stock"] > inventory[key]["threshold"]:
                        alerts.remove(sentence)

def main ():
    display_dashboard()
    # i dont actually know if i need this but i love me some main action

# creates a menu list with drink objects for each key from the menu_data dictionary
menu = [Drink(drink_id = i + 1, **item_data) for i, item_data in enumerate(menu_data)]
    # literally the same thing menu = []
    # for i, item_data in enumerate(menu_data):
    #     drink = Drink(drink_id = i + 1, **item_data)
    #     menu.append(drink)
# list stored with every existing order
every_order = []

main()