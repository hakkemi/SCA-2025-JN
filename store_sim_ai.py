alerts = []  # for inventory
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
    {"name": "Thai Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]


class Drink:
    # creates drink object with attributes
    def __init__(self, drink_id, name, type, price, size="Medium", toppings=None):
        self.drink_id = drink_id
        self.name = name
        self.type = type
        self.price = price
        self.size = size
        self.toppings = toppings


# child class to not make myself confused bc im stupid doesnt actualyl do anything cool :C
class Current_Drink(Drink):
    pass


# class that stores drink objects and the total price of all drink objects
class Order():
    total_order_count = 0  # total order counter

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
    try:  # checks to see if input is valid
        choice = int(input("Choice: "))
        validate_option_menu(choice)
    except ValueError:
        print("Invalid input. Please enter an integer number between 1 and 5.")
        display_dashboard()  # call dashboard again if input is invalid


# NEW FUNCTION: Checks if there's enough inventory for a specific drink
def check_inventory_for_drink(drink_name, drink_size, selected_topping):
    if drink_name not in recipes:
        print(f"Error: Recipe for '{drink_name}' not found.")
        return False, f"Recipe for '{drink_name}' not found."

    # Check main drink ingredients
    for ingredient, quantity_needed in recipes[drink_name].items():
        if ingredient not in inventory:
            print(f"Error: Ingredient '{ingredient}' for '{drink_name}' not in inventory.")
            return False, f"Ingredient '{ingredient}' for '{drink_name}' not in inventory."
        if inventory[ingredient]["stock"] < quantity_needed:
            return False, f"Not enough {ingredient} in stock for {drink_name}. Current: {inventory[ingredient]['stock']} {inventory[ingredient]['unit']}, Needed: {quantity_needed} {inventory[ingredient]['unit']}."

    # Check topping inventory if applicable
    if selected_topping and selected_topping != "None":
        if selected_topping not in inventory:  # Assuming toppings are also in inventory for simplicity
            print(f"Error: Topping '{selected_topping}' not in inventory.")
            return False, f"Topping '{selected_topping}' not in inventory."

        # You'll need to define how much of a topping is consumed per serving.
        # For now, let's assume 1 serving of topping for each drink.
        # You mentioned "will add serving quant for toppings laterrrrrrrrrrrrrrrrrr"
        # If you have specific quantities for toppings, use them here.
        topping_quantity_needed = 1  # Placeholder: Adjust this based on your topping consumption
        if inventory[selected_topping]["stock"] < topping_quantity_needed:
            return False, f"Not enough {selected_topping} in stock. Current: {inventory[selected_topping]['stock']} {inventory[selected_topping]['unit']}, Needed: {topping_quantity_needed} {inventory[selected_topping]['unit']}."

    return True, "Inventory sufficient."


# prompts user for drink and drink adjustments, creates a drink object and stores it in a current order list
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
            print("Invalid size choice. Please enter 'M' or 'L'.")
            return add_drink_to_order(drink_list)

        print("--- Toppings ---")
        current_topping = "None"  # Initialize to None
        topping_price_addition = 0.00
        for i, topping in enumerate(toppings_data):
            print(f"{i + 1}. {topping} (${toppings_data[topping]:.2f})")
        print(f"{len(toppings_data) + 1}. None")  # Option for no topping

        try:
            toppings_choice = int(input("Choice: "))
        except ValueError:
            print("Invalid option, please enter an integer")
            return add_drink_to_order(drink_list)

        if 1 <= toppings_choice <= len(toppings_data):
            # Get the topping name based on the user's choice
            topping_names = list(toppings_data.keys())
            current_topping = topping_names[toppings_choice - 1]
            topping_price_addition = toppings_data[current_topping]
        elif toppings_choice == len(toppings_data) + 1:
            current_topping = "None"
            topping_price_addition = 0.00
        else:
            print("Invalid topping choice.")
            return add_drink_to_order(drink_list)

        # --- IMPORTANT: Check inventory BEFORE creating the drink object ---
        # Note: We pass the drink.name for the recipe lookup, current_size (though not used in current recipes),
        # and current_topping for topping-specific checks.
        inventory_sufficient, message = check_inventory_for_drink(drink.name, current_size, current_topping)

        if not inventory_sufficient:
            print(f"\nCannot add '{drink.name}' with '{current_topping}' ({current_size}). {message}")
            print("Please choose a different drink or topping.")
            return add_drink_to_order(drink_list)  # Prompt again

        current_price += topping_price_addition

        current_drink = Current_Drink(
            drink_id=drink.drink_id,
            name=drink.name,
            type=drink.type,
            price=current_price,
            size=current_size,
            toppings=current_topping)
        drink_list.append(current_drink)
        print(f"'{current_drink.name}' with '{current_drink.toppings}' added to order.")

        print("--- Final ---")
        print("1. Complete order")
        print("2. Add another drink")
        try:
            re_choice = int(input("Choice: "))
        except ValueError:
            print("Invalid option, please enter an integer of 1 or 2")
            return add_drink_to_order(drink_list)

        if re_choice == 1:
            # subtract_inventory is called only when the order is complete,
            # and we've already confirmed stock for each drink added
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


# creates a list of drink objects after calling add_drink_to_order, then adds the list to a global list
# which contains EVERY existing order
def add_new_order():
    order = []
    order_total = 0
    new_order_drink_list = add_drink_to_order(order)
    if not new_order_drink_list:  # If add_drink_to_order returns an empty list or None (due to cancellation)
        print("Order cancelled or empty.")
        return None
    else:
        for drink in new_order_drink_list:
            order_total += drink.price
        new_order = Order(new_order_drink_list, order_total)
        # debug print(f"Order Number: {new_order.total_order_count}")
        every_order.append(new_order)
        print(f"\nOrder #{new_order.total_order_count} completed! Total: ${new_order.drink_list_total:.2f}")
        return new_order


# prints each drink object in an order (prints the drink's name, topping, size, and price attributes)
def view_orders():
    if not every_order:
        print("You have no completed orders!")
        display_dashboard()
    for i, order in enumerate(every_order):
        print(f"--- Order {i + 1} ---")
        print(f"Order Total: ${order.drink_list_total:.2f}")
        for i, drink in enumerate(order.drink_list):
            print(f"{i + 1}. {drink.name}, {drink.toppings}, {drink.size}, ${drink.price:.2f}")


# literally just prints the inventory, function probably not needed?
def view_inventory():
    print(f"\n-- Inventory Overview ---")
    for ingredient, details in inventory.items():
        print(f"{ingredient}: {details["stock"]} {details["unit"]}")


# takes the stock from an individual order and subtracts it from existing stock
# This function is now called AFTER check_inventory_for_drink has passed
def subtract_inventory(drink_list):
    for drink in drink_list:
        if drink.name in recipes:
            drink_name = drink.name
            for key, quantity_needed in recipes[drink_name].items():
                if key in inventory:
                    inventory[key]["stock"] -= quantity_needed
                    # Check for low stock after subtraction and add alert
                    if inventory[key]["stock"] <= inventory[key]["threshold"]:
                        # Only add if not already in alerts to avoid duplicates
                        alert_message = f"Low stock: {key} stock is {inventory[key]['stock']} {inventory[key]['unit']}."
                        if alert_message not in alerts:
                            alerts.append(alert_message)
                else:
                    print(f"Warning: Ingredient '{key}' for '{drink_name}' not found in inventory during subtraction.")
        # Topping subtraction: Assuming 1 unit per serving, adjust as needed
        if drink.toppings and drink.toppings != "None" and drink.toppings in inventory:
            topping_quantity_consumed = 1  # Adjust this based on your actual topping consumption
            if inventory[drink.toppings][
                "stock"] >= topping_quantity_consumed:  # Should always be true if check_inventory passed
                inventory[drink.toppings]["stock"] -= topping_quantity_consumed
                if inventory[drink.toppings]["stock"] <= inventory[drink.toppings]["threshold"]:
                    alert_message = f"Low stock: {drink.toppings} stock is {inventory[drink.toppings]['stock']} {inventory[drink.toppings]['unit']}."
                    if alert_message not in alerts:
                        alerts.append(alert_message)
            else:
                print(f"Warning: Not enough {drink.toppings} to subtract, despite prior check.")


# allows user to add stock to a certain ingredient
def adjust_inventory():
    ingredient = input("Ingredient: ").lower()
    ingredient = ingredient.capitalize()  # Capitalize to match dictionary keys

    found = False
    for key in inventory.keys():
        if ingredient == key:  # Exact match for better control
            found = True
            print(f"\n{ingredient} current stock: {inventory[key]["stock"]} {inventory[key]["unit"]}")
            try:
                adjustment = int(input(f"Add quantity (in {inventory[key]["unit"]}): "))
                if adjustment < 0:
                    print("Please enter a positive number to add stock.")
                else:
                    inventory[key]["stock"] += adjustment
                    print(f"{ingredient} new stock: {inventory[key]["stock"]} {inventory[key]["unit"]}")
                    # Remove any existing low stock alerts for this ingredient if stock is now above threshold
                    alert_to_remove = f"Low stock: {key} stock is {inventory[key]['stock']} {inventory[key]['unit']}."
                    for alert in alerts:
                        if key in alert and inventory[key]['stock'] > inventory[key]['threshold']:
                            alerts.remove(alert)
                            break  # Assume only one alert per ingredient for simplicity
            except ValueError:
                print("Invalid input. Please enter an integer number for quantity.")
            break
    if not found:
        print(f"Ingredient '{ingredient}' not found in inventory.")


# checks to see if the user inputted a valid choice
# again i dont think i need to make a seperate function for this, i should prob just do recursion in the display
# dashboard
def validate_option_menu(choice):
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
        exit()  # Use exit() to terminate the program
    else:
        print("Invalid option! Please choose a number between 1 and 5.")
    display_dashboard()  # Always return to dashboard unless program is terminated


def main():
    display_dashboard()


# creates a menu list with drink objects for each key from the menu_data dictionary
menu = [Drink(drink_id=i + 1, **item_data) for i, item_data in enumerate(menu_data)]
# list stored with every existing order
every_order = []

main()