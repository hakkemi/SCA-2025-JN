alerts = []  # for inventory
cd = None  # current drink global var
# List stored with every existing order
every_order = []

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
            "Black Tea": 35,
            "Sugar": 40,
        },
    },
    "Thai Milk Tea": {
        "Medium": {
            "Milk": 150,
            "Thai Tea Mix": 290,
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
    "None": 0.00,  # Keep 'None' as an option, but it won't be added to the list of toppings
    "Boba": 0.50,
    "Fruit Jelly": 0.75,
    "Cheese Foam": 0.85,
    "Oreo Crumbs": 0.85,
}
menu_data = [
    {"name": "Signature Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": []},
    # Default to empty list
    {"name": "Thai Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": []},
    {"name": "Oolong Milk Tea", "drink_type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": []},
    {"name": "Oreo Milk Tornado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": []},
    {"name": "Strawberry Milk Tornado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": []},
    {"name": "Taronado", "drink_type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": []},
]


class Drink:
    # Creates drink object with attributes
    def __init__(self, drink_id, name, drink_type, price, size="Medium", toppings=None):
        self.drink_id = drink_id
        self.name = name
        self.drink_type = drink_type
        self.price = price
        self.size = size
        # Ensure toppings is always a list
        self.toppings = toppings if toppings is not None else []


# Class that stores drink objects and the total price of all drink objects
# Each time an order 'object' is created, the class will add +1 to the instance variable 'total_order_count'
class Order:
    total_order_count = 0  # total order counter

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
    print(f"Alerts: {' '.join(alerts) if alerts else 'None'}")  # Improved alert display for multiple alerts

    try:  # checks to see if input is valid
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
        print("Invalid input. Enter an integer number.")
        return add_drink_to_order(drink_list)
    if drink_choice == 0:
        return drink_list  # Returns the current list, allowing to complete order without adding another drink

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
            print("Invalid size choice. Please enter 'M' or 'L'.")
            return add_drink_to_order(drink_list)  # Re-prompt if size is invalid

        selected_toppings = []
        topping_names = list(toppings_data.keys())  # Get topping names to display them

        while True:
            print("\n--- Toppings (select multiple, enter 0 to finish) ---")
            for i, topping in enumerate(topping_names):
                print(f"{i + 1}. {topping} (+${toppings_data[topping]:.2f})")
            print("0. Done adding toppings")

            try:
                toppings_choice = int(input("Choice: "))
            except ValueError:
                print("Invalid input, please enter an integer.")
                continue

            if toppings_choice == 0:
                break  # Exit topping selection loop

            if 1 <= toppings_choice <= len(topping_names):
                chosen_topping_name = topping_names[toppings_choice - 1]
                # Avoid adding 'None' as an actual topping if selected
                if chosen_topping_name != "None":
                    if chosen_topping_name not in selected_toppings:  # Prevent duplicate toppings
                        selected_toppings.append(chosen_topping_name)
                        current_price += toppings_data[chosen_topping_name]
                        print(f"Added {chosen_topping_name}. Current price: ${current_price:.2f}")
                    else:
                        print(f"{chosen_topping_name} already added.")
                else:
                    print("No toppings selected.")  # User chose 'None' but still allowed to add others
            else:
                print("Invalid topping choice. Please enter a number from the list or 0 to finish.")

        # creates the drink object
        cd = Drink(
            drink_id=drink.drink_id,
            name=drink.name,
            drink_type=drink.drink_type,
            price=current_price,
            size=current_size,
            toppings=selected_toppings  # Store the list of selected toppings
        )

        # checks to see if there is enough ingredients associated with the drink to make it or not
        if cd.name in recipes and cd.size in recipes[cd.name]:
            for key in recipes[cd.name][cd.size]:
                if key in inventory:
                    if (inventory[key]["stock"] - recipes[cd.name][cd.size][key]) <= 0:
                        print(f"Not enough {key}. Please add to inventory. Completing and closing order now.")
                        return drink_list  # Returns the current list of drinks, cancelling the last one
                    elif (inventory[key]["stock"] - recipes[cd.name][cd.size][key]) <= (inventory[key]["threshold"]):
                        print(
                            f"*****\nWARNING: {key} stock will be {(inventory[key]["stock"] - recipes[cd.name][cd.size][key])} {inventory[key]["unit"]}.\n*****")
                        alert_message = f"Low: {key} ({(inventory[key]["stock"] - recipes[cd.name][cd.size][key])}) {inventory[key]["unit"]},"

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
        print("3. Cancel Order")  # This option will discard the entire current order

        while True:
            try:
                re_choice = int(input("Choice: "))
                if re_choice == 1:
                    print("-----------------")
                    return drink_list  # Returns the list to add to a new order
                elif re_choice == 2:
                    print("-----------------")
                    return add_drink_to_order(drink_list)  # Recursively call to add another drink
                elif re_choice == 3:
                    print("-----------------")
                    # Revert inventory changes for the cancelled drink
                    if cd.name in recipes and cd.size in recipes[cd.name]:
                        for key in recipes[cd.name][cd.size]:
                            if key in inventory:
                                inventory[key]["stock"] += recipes[cd.name][cd.size][key]
                                # Re-check and update alerts if stock goes above threshold after revert
                                if inventory[key]["stock"] > inventory[key]["threshold"]:
                                    alerts[:] = [alert for alert in alerts if key not in alert]
                    print("Order cancelled.")
                    return None  # Indicates the order should be discarded
                else:
                    print("Invalid option, please enter an integer of 1, 2, or 3.")
            except ValueError:
                print("Invalid input, please enter an integer.")
    else:
        print("Invalid option, please try again")
        return add_drink_to_order(drink_list)


# Creates a list of drink objects after calling add_drink_to_order, then adds the list to a global list
# which contains EVERY existing order
def add_new_order():
    order = []
    order_total = 0
    new_order_drink_list = add_drink_to_order(order)
    if new_order_drink_list is None:  # If the returned list is None, the order was cancelled
        print("Order creation aborted.")
        return None
    elif not new_order_drink_list:  # If the returned list is empty, no drinks were added (e.g., cancelled at first choice)
        print("No drinks added to order.")
        return None
    else:
        for drink in new_order_drink_list:
            order_total += drink.price
        new_order = Order(new_order_drink_list, order_total)
        every_order.append(new_order)
        print(f"Order {Order.total_order_count} created with total: ${new_order.drink_list_total:.2f}")
        return new_order


# Prints every existing order numerically
# Prints each drink object in the order numerically (prints the drink's # in the order, name, topping, size, and price attributes)
def view_orders():
    print("\n--- Orders Overview ---")
    if not every_order:  # If the list is completely empty the barista is returned to the dashboard
        print("You have no completed orders!")
        print("-----------------")
        return display_dashboard()
    for i, order in enumerate(every_order):
        print(f"--- Order {i + 1} ---")
        print(f"Order Total: ${order.drink_list_total:.2f}")
        for index, drink in enumerate(order.drink_list):
            # Display toppings list nicely, or "None" if empty
            toppings_display = ", ".join(drink.toppings) if drink.toppings else "None"
            print(f"{index + 1}. {drink.name}, Toppings: [{toppings_display}], {drink.size}, ${drink.price:.2f}")
    print("-----------------------")
    return display_dashboard()


# Prints the inventory, detailing current stock and unit of measurement
def view_inventory():
    print(f"\n-- Inventory Overview ---")
    for ingredient, details in inventory.items():
        print(f"{ingredient}: {details["stock"]} {details["unit"]}")
    print("-----------------")


# Allows user to add stock to a certain ingredient
def adjust_inventory():
    print("\n--- Inventory Adjustment ---")
    # Display current inventory
    ingredients_list = list(
        inventory.keys())  # creates list with keys of inven dict to easily access the index with number
    for i, ingredient_name in enumerate(ingredients_list):
        print(f"{i + 1}. {ingredient_name}: {inventory[ingredient_name]['stock']} {inventory[ingredient_name]['unit']}")

    print("0. Back to Dashboard")

    while True:
        try:
            choice = int(input("Select ingredient to adjust (number): "))
            if choice == 0:
                print("-----------------")
                return

            if 1 <= choice <= len(ingredients_list):
                ingredient_name = ingredients_list[choice - 1]
                print(
                    f"{ingredient_name} current stock: {inventory[ingredient_name]['stock']} {inventory[ingredient_name]['unit']}")
                adjustment = int(input("Add quantity: "))
                if adjustment < 0:
                    print("Cannot add negative quantity. Enter a positive number.")
                    continue

                inventory[ingredient_name]["stock"] += adjustment
                print(
                    f"Updated {ingredient_name} stock: {inventory[ingredient_name]['stock']} {inventory[ingredient_name]['unit']}")

                # Updates and replaces each alert in the alerts list excluding any updated ingredients that are now above the threshold
                if inventory[ingredient_name]["stock"] > inventory[ingredient_name]["threshold"]:
                    alerts[:] = [alert for alert in alerts if ingredient_name not in alert]

                print("-----------------")
                return
            else:
                print("Invalid ingredient selection. Please choose a number from the list.")
        except ValueError:
            print("Invalid input. Please enter an integer number.")


def main():
    display_dashboard()


# Creates a menu list with drink objects for each KEY from the menu_data dictionary
menu = [Drink(drink_id=i + 1, **item_data) for i, item_data in enumerate(menu_data)]
main()
