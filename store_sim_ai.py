# Inventory alerts
alerts = []

# Toppings and their prices
toppings_data = {
    "Boba": 0.5,
    "Fruit Jelly": 0.75,
    "Cheese Foam": 0.85,
}

# Base menu data
menu_data = [
    {"name": "Signature Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Thai Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oolong Milk Tea", "type": "Tea Based", "price": 5.00, "size": "Medium", "toppings": None},
    {"name": "Oreo Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Strawberry Milk Tornado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
    {"name": "Taronado", "type": "Milk Based", "price": 7.00, "size": "Medium", "toppings": None},
]

# Drink class
class Drink:
    def __init__(self, drink_id, name, type, price, size="Medium", toppings=None):
        if size.lower() == "large":
            price += 1
        if toppings in toppings_data:
            price += toppings_data[toppings]
        self.drink_id = drink_id
        self.name = name
        self.type = type
        self.price = price
        self.size = size
        self.toppings = toppings

# Inherits from Drink
class Current_Drink(Drink):
    pass

# Order class to hold drinks
class Order:
    total_order_count = 0

    def __init__(self, drink_list):
        self.drink_list = drink_list
        Order.total_order_count += 1

# Show dashboard menu
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
        display_dashboard()

# Drink selection and topping logic
def add_drink_to_order(drink_list):
    print("\n--- Menu ---")
    print("0. View Total Drinks in Order")
    for i, drink in enumerate(menu):
        print(f"{i + 1}. {drink.name} (${drink.price:.2f})")

    try:
        drink_choice = int(input("Choice: "))
    except ValueError:
        print("Invalid input. Enter an integer.")
        return add_drink_to_order(drink_list)

    if drink_choice == 0:
        view_orders()
        return drink_list

    if 1 <= drink_choice <= len(menu):
        drink = menu[drink_choice - 1]

        # Size selection
        size_choice = input("Size (M/L): ").strip().lower()
        if size_choice not in ['m', 'l']:
            print("Invalid size. Try again.")
            return add_drink_to_order(drink_list)

        current_size = "Large" if size_choice == "l" else "Medium"
        current_price = drink.price + (1 if current_size == "Large" else 0)

        # Topping selection
        print("\n--- Toppings ---")
        for i, topping in enumerate(toppings_data):
            print(f"{i + 1}. {topping}")
        try:
            toppings_choice = int(input("Choice: "))
        except ValueError:
            print("Invalid topping choice.")
            return add_drink_to_order(drink_list)

        if 1 <= toppings_choice <= len(toppings_data):
            current_topping = list(toppings_data.keys())[toppings_choice - 1]
            current_price += toppings_data[current_topping]
        else:
            print("Invalid topping.")
            return add_drink_to_order(drink_list)

        # Create drink object
        current_drink = Current_Drink(
            drink_id=drink.drink_id,
            name=drink.name,
            type=drink.type,
            price=current_price,
            size=current_size,
            toppings=current_topping
        )

        drink_list.append(current_drink)

        print("\n--- Final ---")
        print("1. Complete order")
        print("2. Add another drink")

        try:
            re_choice = int(input("Choice: "))
        except ValueError:
            print("Invalid choice. Completing order.")
            return drink_list

        if re_choice == 1:
            return drink_list
        elif re_choice == 2:
            return add_drink_to_order(drink_list)
        else:
            print("Invalid choice. Completing order.")
            return drink_list

    else:
        print("Invalid menu choice. Try again.")
        return add_drink_to_order(drink_list)

# Add a new order
def add_new_order():
    order = []
    new_order_drink_list = add_drink_to_order(order)
    new_order = Order(new_order_drink_list)
    print(f"Order number: {new_order.total_order_count}")
    every_order.append(new_order)
    return new_order

# View all orders
def view_orders():
    if not every_order:
        print("You have no completed orders!")
        display_dashboard()
        return

    for i, order in enumerate(every_order):
        print(f"\n--- Order {i + 1} ---")
        for drink in order.drink_list:
            print(f"Drink ID: {drink.drink_id} | {drink.name} | Size: {drink.size} | Type: {drink.type} | Topping: {drink.toppings} | Price: ${drink.price:.2f}")

# Placeholder for inventory features
def view_inventory():
    print("Inventory feature not implemented yet.")
    display_dashboard()

def adjust_inventory():
    print("Inventory adjustment not implemented yet.")
    display_dashboard()

# Validate main dashboard choice
def validate_option_menu(choice):
    if choice == 1:
        add_new_order()
        display_dashboard()
    elif choice == 2:
        view_orders()
        display_dashboard()
    elif choice == 3:
        view_inventory()
    elif choice == 4:
        adjust_inventory()
    elif choice == 5:
        print("Program terminated")
    else:
        print("Invalid option. Please choose a number between 1 and 5.")
        display_dashboard()

# Start program
def main():
    display_dashboard()

# Build menu from data
menu = [Drink(drink_id=i + 1, **item_data) for i, item_data in enumerate(menu_data)]
every_order = []

main()
